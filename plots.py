import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import sympy
from turtle import textinput

time = []
top = []
bottom = []

framerate = int(textinput("Framrate", "Please enter Framerate:"))
heightmax = int(textinput("2m", "What is the pixel at 2m"))
heightmin = int(textinput("0m", "What is the pixel at 0m"))


def FrameToS(x):
    return x / framerate


def PixeltoHeight(x):
    m = 2 / (heightmax - heightmin)
    return m * x - m * heightmin


with open("data.txt", "r") as f:
    for i in f.readlines():
        x, y, z = list(map(int, i.split()))
        time.append(x)
        top.append(y)
        bottom.append(z)

QuickCheck = plt.figure(0)
plt.scatter(time, top, c="blue")
plt.scatter(time, bottom, c="red")
QuickCheck.show()

time = list(map(FrameToS, time))
top = list(map(PixeltoHeight, top))
bottom = list(map(PixeltoHeight, bottom))

tot_time = sympy.ceiling(time[-1] * 100)
timeLine = list(map(lambda x: x / 100, range(tot_time)))


def lineFunc(x, a, b, c):
    return (a * (x**2)) + (b * x) + c


t = sympy.symbols("t")


start = int(textinput("Start Bottom", "What Frame does the bottom start moving"))
bottomTime = list(filter(lambda x: x >= FrameToS(start), timeLine))

Sta, Stb, Stc = curve_fit(lineFunc, time, top)[0]
Sba, Sbb, Sbc = curve_fit(lineFunc, time[start:], bottom[start:])[0]

st_eq = (Sta * t**2) + (Stb * t) + Stc
vt_eq = sympy.diff(st_eq)
at_eq = sympy.diff(vt_eq)

sb_eq = (Sba * t**2) + (Sbb * t) + Sbc
vb_eq = sympy.diff(sb_eq)
ab_eq = sympy.diff(vb_eq)

st_est = list(map(lambda x: (Sta * x**2) + (Stb * x) + Stc, timeLine))
vt_est = [vt_eq.subs(t, i) for i in timeLine]
at_est = [at_eq.subs(t, i) for i in timeLine]

sb_est = list(map(lambda x: (Sba * x**2) + (Sbb * x) + Sbc, bottomTime))
vb_est = [vb_eq.subs(t, i) for i in bottomTime]
ab_est = [ab_eq.subs(t, i) for i in bottomTime]

data = plt.figure(1)
plt.title("$Displacement (Scatter)$")
plt.xlabel("$Time (s)$")
plt.ylabel("$Distance (m)$")
plt.scatter(time, top, c="blue")
plt.scatter(time, bottom, c="red")
data.savefig("data.png")
data.show()

s = plt.figure(2)
plt.title("$Displacement$")
plt.xlabel("$Time (s)$")
plt.ylabel("$Distance (m)$")
plt.plot(timeLine, st_est, c="blue")
plt.plot(bottomTime, sb_est, c="red")
s.savefig("Displacement.png")
s.show()

v = plt.figure(3)
plt.title("$Velocity$")
plt.xlabel("$Time (s)$")
plt.ylabel("$Velocity (m/s)$")
plt.plot(timeLine, vt_est, c="blue")
plt.plot(bottomTime, vb_est, c="red")
v.savefig("Velocity.png")
v.show()

a = plt.figure(4)
plt.title("$Acceleration$")
plt.xlabel("$Time (s)$")
plt.ylabel("$Acceleration (m/s^{2})$")
plt.plot(timeLine, at_est, c="blue")
plt.plot(bottomTime, ab_est, c="red")
a.savefig("Acceleration.png")
a.show()

print(st_eq)
print(vt_eq)
print(at_eq)
print(sb_eq)
print(vb_eq)
print(ab_eq)
input()
