import cv2
import numpy as np

"""
img = cv2.imread("1.png", cv2.IMREAD_GRAYSCALE)
binary = cv2.adaptiveThreshold(~img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, -10)
w, h = img.shape
cv2.imshow("cell", binary)
cv2.waitKey(0)

rows,cols=binary.shape
scale = 20
#识别横线
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (cols//scale, 1))
eroded = cv2.erode(binary, kernel, iterations=1)
#cv2.imshow("Eroded Image",eroded)
dilatedcol = cv2.dilate(eroded, kernel, iterations=1)
cv2.imshow("Dilated Image", dilatedcol)
cv2.waitKey(0)
"""