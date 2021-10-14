import cv2
import os
import numpy as np

def findline(path):

    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    h, w = img.shape

    #  Noise Removal
    img = cv2.fastNlMeansDenoising(img, None, 10, 7, 21)
    
    # Deskewing
    # = None =
    
    h, w = img.shape
    imgmack = np.zeros([h, w], dtype="uint8")
    imgmack2 = np.zeros([h, w], dtype="uint8")
    #imgmack2 = np.zeros([h, w, 3], dtype="uint8") # if need output test img
    
    #  Binarization
    ret, thresh1 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # print(ret)
    # ret, thresh1 = cv2.threshold(img, 160, 255, cv2.THRESH_BINARY)
    # cv2.imshow("show", thresh1)
    # cv2.waitKey(0)
    
    # if y,-5x~+5x (h.line) same set to white else black
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
                
    #cv2.imshow("thresh", thresh1)
    #cv2.imshow("imgmack", imgmack)
    #cv2.waitKey(0)
    
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
    
    
    #cv2.imshow("imgmack2", imgmack2)
    #cv2.waitKey(0)
    #cv2.imwrite("imgmack2.jpg", imgmack2) # if output test img
    return thresh1, imgmack2
    #return imgmack, imgmack2