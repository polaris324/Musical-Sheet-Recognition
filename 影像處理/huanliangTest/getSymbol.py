import cv2
import os
import numpy as np

def saveImg(fiveline, th, yfirst, ylast, xfirst, xlast): #add Symbol to fiveline
    for yaxis in range(yfirst, ylast):
        for xaxis in range(xfirst, xlast):
            fiveline[yaxis][xaxis] = th[yaxis][xaxis]
    return fiveline

def getSymbol(fiveline, thresh, staffRow, staffRow_spacing, lastx):
    print(len(staffRow))
    
    for i in range(len(staffRow)):  #each row
        for j in range(lastx):          #search first line xaxis loc
            if(thresh[staffRow[i][0]][j] == 0 
               and thresh[staffRow[i][0] + staffRow_spacing[i] + 1][j] == 0
               and thresh[staffRow[i][0] + 2*staffRow_spacing[i] + 2][j] == 0
               and thresh[staffRow[i][0] + 3*staffRow_spacing[i] + 3][j] == 0
               and thresh[staffRow[i][0] + 4*staffRow_spacing[i] + 4][j] == 0):
                print(j)
                break;
        
        ##pre find symbol
        #save searchCmp(default 5 line look like)
        l = 0
        searchCmp = []
        top_y = staffRow[i][0] - 5 * staffRow_spacing[i] - 1      #first line
        bottom_y = staffRow[i][4] + 5 * staffRow_spacing[i] + 1      #last line
        for k in range(top_y, bottom_y):
            searchCmp.append(thresh[k][j])
            l += 1
        
        #start find and comp
        flag=0
        for k in range(j,lastx):    #left to right
            tmp=[]
            
            #save a thresh tmp
            for l in range(top_y,bottom_y):
                tmp.append(thresh[l][k])
            
            #comp
            if(flag == 0):  #find first xaxis change(each Symbol)
                
                if(searchCmp != tmp):
                    set_topx = k-5
                    flag = 1
            else:
                if(searchCmp == tmp):   #find last xaxis change(each Symbol)
                    set_endx = k+5
                    flag = 0
                    print(set_topx,set_endx)
                    fiveline = saveImg(fiveline, thresh, top_y, bottom_y, set_topx, set_endx)
        
    cv2.imshow("show", fiveline)
    cv2.waitKey(0)
                
            