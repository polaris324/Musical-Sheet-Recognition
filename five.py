import cv2
import os
import numpy as np
from regulatex import regulatex

def five(img):
    #img = cv2.imread("imgmack2.jpg", cv2.IMREAD_GRAYSCALE) # if test img
    h, w = img.shape
    
    current_xtail = w-1
    lastx = 0
    lasty = 0

    # found the last of x axis
    while(current_xtail > 0):
        for current_yhead in range(h-1):
            if(img[current_yhead][current_xtail] == 255):   # record & break if found xtail
                lastx = current_xtail
                lasty = current_yhead
                break
        if(lastx != 0): #if xtail not empty
            break
        current_xtail -= 1

    testx = lastx
    #print(lastx)
    listy = []
    # found all line(y axis) position
    for y in range(h-1):
        if(img[y][testx] == 255 or
            img[y][testx-1] == 255 or
            img[y][testx-2] == 255 or
            img[y][testx-3] == 255 or
            img[y][testx+1] == 255 or
            img[y][testx+2] == 255 or
            img[y][testx+3] == 255):
            listy.append(y)

    #cv2.imshow("show", img)
    #cv2.waitKey(0)

    #print(listy)

    listx = []
    # found all line(x-left axis) position
    for y in listy:
        for x in range(w-1):
            if (img[y][x] == 255):
                listx.append(x)
                break
    #print(listx)
    five = np.zeros([h, w, 1], dtype="uint8")
    
    listx = regulatex(listx)

    #print(listx)
    i = 0
    # build only fiveline pic
    while(i<len(listy)):
        intx = listx[i]
        while (intx < lastx):
            five[listy[i]][intx] = 255
            intx = intx + 1
        i += 1

    cv2.imwrite("Binarizated Img.jpg", five) # if output test img
    return five, lastx
