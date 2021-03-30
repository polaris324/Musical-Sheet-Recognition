import cv2
import os
import numpy as np

img = cv2.imread("final.jpg", cv2.IMREAD_GRAYSCALE)

cv2.imshow("show", img)
cv2.waitKey(0)

print(img[0, 0])
h, w = img.shape

f = open("whereline.txt", "w")

line = [0]*h

for y in range(h-1):
    for x in range(w-1):
        if(img[y, x] == 255):
            line[y] = line[y] + 1
for y in range(h-1):
    f.write(str(line[y]))
    f.write("\n")


f.close()
