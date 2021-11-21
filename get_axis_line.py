# -*- coding: utf-8 -*-
"""
"""
import cv2
import numpy as np
from scipy import stats
from getSymbol import getSymbol
import time

"""test header
from pre_processing import preprocessing
img = cv2.imread('3.png', cv2.IMREAD_GRAYSCALE)
h, w = img.shape  # Image Length & Width

thresh, h, w = preprocessing(img, h, w)
"""

def findstaff_spacing(thresh, h, w):
    
    lineAxis = [] # Catch all related line axis
    threshOfLine = np.multiply(w, 0.6).astype(int) # set thresh line of staffline
    
    numAryOfBlack = np.count_nonzero(thresh==0, axis=1) # get Hist of each row
    
    distCnt = 0 # counter for each spacing
    
    for row in range(h):    # if match staffline, get axis
        if numAryOfBlack[row] > threshOfLine:
            lineAxis.append([row, distCnt])
            distCnt = 0
        else:
            distCnt += 1
    spacing = stats.mode(lineAxis)[0][0][1]
    
    lineCnt = 0
    flag_findfive = 0
    lineRow = []
    staffRow = []
    
    for row in range(len(lineAxis)):
        if(flag_findfive):
            if((lineAxis[row][1] - spacing) >= 0):
                lineRow.append(lineAxis[row][0])
                lineCnt += 1
            else:
                lineRow.pop(lineCnt)
                lineRow.append(lineAxis[row][0])
    
            if(lineCnt == 4):
                staffRow.append(lineRow)
                lineRow = []
                lineCnt = 0
                flag_findfive = 0
        else:
            flag_findfive = 1
            lineRow.append(lineAxis[row][0])
            
          
    
    imgmask = np.zeros([h, w], dtype="uint8")
    lastX = 0
    
    for each in range(len(staffRow)):
        for row in range(5):
            for col in range(w-1,0,-1):
                if thresh[staffRow[each][row]][col] == 0:
                    imgmask[staffRow[each][row]][col] = 255
                    if(col > lastX):
                        lastX = col
                    
    # getSymbol(imgmask, thresh, staff_row2, staffRow_spacing, lastX)
    
    cv2.imwrite("imgmask.jpg", imgmask) # if output test img
    
    return imgmask, staffRow, spacing, lastX

# "exec_time set"
# exec_time = []
# "exec_time scan"
# a = time.time()
# "exec_time stop"
# b = time.time()
# exec_time.append( b - a )
# print('Method', exec_time[0])