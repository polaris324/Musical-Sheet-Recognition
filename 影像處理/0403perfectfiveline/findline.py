import cv2
import os
import numpy as np

def findline(path):

    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    h, w = img.shape


    #print(img[0, 0])

    imgmack = np.zeros([h, w, 3], dtype="uint8")
    imgmack2 = np.zeros([h, w, 3], dtype="uint8")

    ret, thresh1 = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)
    #cv2.imshow("show", thresh1)
    #cv2.waitKey(0)

    for y in range(h-1):
        for x in range(w-1):
            if(thresh1[y, x] == 0 and
               thresh1[y, x - 1] == 0 and
               thresh1[y, x - 2] == 0 and
               thresh1[y, x - 3] == 0 and
               thresh1[y, x - 4] == 0 and
               thresh1[y, x - 5] == 0 and
               thresh1[y, x + 1] == 0 and
               thresh1[y, x + 2] == 0 and
               thresh1[y, x + 3] == 0 and
               thresh1[y, x + 4] == 0 and
               thresh1[y, x + 5] == 0):
                imgmack[y, x] = 255

    #cv2.imshow("show", imgmack)
    #cv2.waitKey(0)

    cv2.imwrite("final.jpg", imgmack)
    img2 = cv2.imread("final.jpg", cv2.IMREAD_GRAYSCALE)
    ret2, thresh2 = cv2.threshold(img2, 200, 255, cv2.THRESH_BINARY)
    #print(thresh2[0, 0])

    for y in range(h-1): #檢查是不是一線段
        for x in range(w-1):
            if(thresh2[y, x] == 255):
                if(
                        thresh2[y, x - 1] == 255 and
                        thresh2[y, x - 2] == 255 and
                        thresh2[y, x - 3] == 255 and
                        thresh2[y, x - 4] == 255 and
                        thresh2[y, x - 5] == 255 and
                        thresh2[y, x + 1] == 255 and
                        thresh2[y, x + 2] == 255 and
                        thresh2[y, x + 3] == 255 and
                        thresh2[y, x + 4] == 255 and
                        thresh2[y, x + 5] == 255
                ):
                    #畫線並且上下去掉
                    imgmack2[y, x] = 255
                    imgmack2[y + 1, x] = 0
                    imgmack2[y + 2, x] = 0
                    imgmack2[y - 1, x] = 0
                    imgmack2[y - 2, x] = 0


    #cv2.imshow("show", imgmack2)
    #cv2.waitKey(0)
    cv2.imwrite("final.jpg", imgmack2)
