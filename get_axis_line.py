# -*- coding: utf-8 -*-
"""
"""
import cv2
import numpy as np
from scipy import stats
# from getSymbol import getSymbol
# import time

"""test header"""
# from pre_processing import preprocessing
# img = cv2.imread('21-1.jpg', cv2.IMREAD_GRAYSCALE)
# h, w = img.shape  # Image Length & Width

# thresh, h, w = preprocessing(img, h, w)


def findstaff_spacing(thresh, h, w):
    
    lineAxis = [] # Catch all related line axis
    threshOfLine = np.multiply(w, 0.6).astype(int) # set thresh line of staffline
    
    numAryOfBlack = np.count_nonzero(thresh==0, axis=1) # get Hist of each row
    
    distCnt = 0 # counter for each spacing
    
    for row in range(h):    # if match staffline, get axis
        if numAryOfBlack[row] > threshOfLine and distCnt != 0:
            lineAxis.append([row, distCnt])
            distCnt = 0
        else:
            distCnt += 1
    spacing = stats.mode(lineAxis)[0][0][1]
    
    lineCnt = 0
    flag_findfive = 0
    # Exception_staffLine = 0
    lineRow = []
    staffRow = []
    
    for row in range(len(lineAxis)):
        if(flag_findfive):
            if(    (lineAxis[row][1] - spacing) >= -1 
               and (lineAxis[row][1] - spacing) <=  2): # is staffline, spacing is +-1
                lineRow.append(lineAxis[row][0])
                lineCnt += 1
                # print("found staff line", lineRow)
            elif(lineAxis[row][1] == 0):                # is overlapping, pop last & add new staffline
                lineRow.pop(lineCnt)
                lineRow.append(lineAxis[row][0])
                # print("found overlapping", lineRow)
            # elif(lineCnt != 0):
                # Exception_staffLine = 1
    
            if(lineCnt == 4):                           # if found five staffline, then add to one group
                staffRow.append(lineRow)
                lineRow = []
                lineCnt = 0
                flag_findfive = 0
        else:                                           # catch flag if first staffline for each group
            flag_findfive = 1
            lineRow.append(lineAxis[row][0])
            
    imgmask = np.zeros([h, w], dtype="uint8")   # comfirm staffline generate
    lastX = w
    
    # if raise exception, need to return a callout value
    
    # output gen comfirm staffline
    
    for each in range(len(staffRow)):
        for row in range(5):
            lastCheck_flag = 1
            for col in range(w-1,0,-1):
                if thresh[staffRow[each][row]][col] == 0:
                    imgmask[staffRow[each][row]][col] = 255
                    
                    if(row == 4 and lastCheck_flag and col <= lastX and
                       thresh[staffRow[each][row]-1][col-1] == 255):
                        # print(staffRow[each][row], col)
                        lastX = col
                        lastCheck_flag = 0
                    
    # check monophony or not
    monophony = 0
    for row in range(staffRow[0][4], staffRow[1][0] + spacing, 1):
        if(thresh[row][lastX+1] == 0):
            monophony = 1
        else:
            monophony = 0
            break
    
    cv2.imwrite("imgmask.jpg", imgmask) # if output test img
    
    # if raise exception, need to return a callout value
    return imgmask, staffRow, spacing, lastX, monophony , #lineAxis

"""test main"""
# imgmask, staffRow, spacing, lastX, mono, Arr = findstaff_spacing(thresh, h, w)

# "exec_time set"
# exec_time = []
# "exec_time scan"
# a = time.time()
# "exec_time stop"
# b = time.time()
# exec_time.append( b - a )
# print('Method', exec_time[0])