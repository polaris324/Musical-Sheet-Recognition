import cv2
import os
import numpy as np


img = cv2.imread("final.jpg", cv2.IMREAD_GRAYSCALE)

h, w = img.shape

x = w-1

lastx = 0
lasty = 0

while(x > 0):
    for y in range(h-1):
        if(img[y][x] == 255):
            lastx = x
            lasty = y
            break
    if(lastx!=0):
        break
    x = x - 1


testx = lastx-10

listy = []
for y in range(h-1):
    if(img[y][testx] == 255):
        listy.append(y)

#print(listy)

listx = []
for y in listy:
    for x in range(w-1):
        if (img[y][x] == 255):
            listx.append(x)
            break
print(listx)

five = np.zeros([h, w, 1], dtype="uint8")

for y in listy:
    for x in listx:
        intx = x
        while(intx < lastx):

            five[y][intx] = 255
            intx = intx + 1

cv2.imwrite("five.jpg", five)
