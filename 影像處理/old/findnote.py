import cv2
import numpy as np


img = cv2.imread("1.png", cv2.IMREAD_GRAYSCALE)
binary = cv2.adaptiveThreshold(~img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, -10)
h, w = binary.shape
imgaft = np.zeros([h, w, 3], dtype="uint8")

cv2.imwrite("outputbin.jpg", binary)

print(w, h)
print(binary[0, 0])
for y in range(h-1):
    for x in range(w-1):
        #print(binary[x, y])
        if(binary[y, x] == 255):
            if (binary[y-1, x]==255 and binary[y-2, x]==255):
                imgaft[y, x] = 255
            if(binary[y-2, x] == 0 and
               binary[y+2, x] == 0 and
               binary[y, x-2] == 0 and
               binary[y, x+2] == 0):
                imgaft[y, x] = 255

cv2.imwrite("outputfin.jpg", imgaft)
