import cv2 as cv
import numpy as np
from turtle import textinput

vid = textinput("Video", "What is the name of the video")

cap = cv.VideoCapture(vid)

size = (int(cap.get(3)), int(cap.get(4)))
result = cv.VideoWriter("tracers.avi", cv.VideoWriter_fourcc(*"MJPG"), 60, size)

print(size)
currframe = 0
output = ""
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        new = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        bw = cv.threshold(new, 128, 255, cv.THRESH_BINARY)[1]
        arr = np.array(bw)
        loc = np.where(arr == 0)
        top = loc[0][0], loc[1][0]
        bottom = loc[0][len(loc[0]) - 1], loc[1][len(loc[1]) - 1]
        frame = cv.line(
            frame,
            (0, loc[0][0]),
            (size[0] - 1, loc[0][0]),
            color=[0, 0, 255],
            thickness=2,
        )
        frame = cv.line(
            frame,
            (0, loc[0][len(loc[0]) - 1]),
            (size[0] - 1, loc[0][len(loc[0]) - 1]),
            color=[0, 0, 255],
            thickness=2,
        )
        cv.putText(
            frame, f"top {top},bottom = {bottom}", (50, 50), cv.FONT_HERSHEY_PLAIN, 2, 0
        )
        frame = cv.resize(frame, size)
        result.write(frame)
        cv.imshow("Black And White", bw)
        cv.imshow("Tracers", frame)
        cv.waitKey(100)
        print(f"{currframe}: Top = {size[1] - top[0]} Bottom = {size[1]  - bottom[0]}")
        output += f"{currframe} {size[1] - top[0]} {size[1]  - bottom[0]} \n"
        currframe += 1

    else:
        break

with open("data.txt", "w") as f:
    f.write(output)

cap.release()
result.release()

cv.destroyAllWindows()
