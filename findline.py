import cv2
import os
import numpy as np
import time

def findline(thresh, h, w):
    
    imgmack = np.zeros([h, w], dtype="uint8")
    imgmack2 = np.zeros([h, w], dtype="uint8")
    
    # if y,-5x~+5x (h.line) same set to white else black
    for y in range(h-1):
        for x in range(w-1):
            if(thresh[y, x] == 0 and
               thresh[y, x - 1] == 0 and
               thresh[y, x - 2] == 0 and
               thresh[y, x - 3] == 0 and
               thresh[y, x - 4] == 0 and
               thresh[y, x - 5] == 0 and
               thresh[y, x + 1] == 0 and
               thresh[y, x + 2] == 0 and
               thresh[y, x + 3] == 0 and
               thresh[y, x + 4] == 0 and
               thresh[y, x + 5] == 0):
                imgmack[y, x] = 255
    
    for y in range(h-1): #檢查是不是一線段
        for x in range(w-1):
            if(imgmack[y, x] == 255):
                if(
                        imgmack[y, x - 1] == 255 and
                        imgmack[y, x - 2] == 255 and
                        imgmack[y, x - 3] == 255 and
                        imgmack[y, x - 4] == 255 and
                        imgmack[y, x - 5] == 255 and
                        imgmack[y, x + 1] == 255 and
                        imgmack[y, x + 2] == 255 and
                        imgmack[y, x + 3] == 255 and
                        imgmack[y, x + 4] == 255 and
                        imgmack[y, x + 5] == 255
                ):
                    #畫線並且上下去掉
                    imgmack2[y, x] = 255
                    imgmack2[y + 1, x] = 0
                    imgmack2[y + 2, x] = 0
                    imgmack2[y - 1, x] = 0
                    imgmack2[y - 2, x] = 0
                    imgmack2[y + 1, x+1] = 0
                    imgmack2[y + 2, x+1] = 0
                    imgmack2[y - 1, x+1] = 0
                    imgmack2[y - 2, x+1] = 0
    
    return imgmack2