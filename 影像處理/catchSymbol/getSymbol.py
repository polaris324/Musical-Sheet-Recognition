import cv2
import os
import pickle
import numpy as np

def saveImg(fiveline, th, yfirst, ylast, xfirst, xlast, i): #add Symbol to fiveline
    for yaxis in range(yfirst, ylast):
        for xaxis in range(xfirst, xlast):
            fiveline[yaxis][xaxis] = th[yaxis][xaxis]

    crop_img = th[yfirst:ylast, xfirst:xlast]
    if not os.path.exists("notedata"):
        os.mkdir("notedata")

    cv2.imwrite("notedata/" + str(i) + ".jpg", crop_img)
    '''
    with open("notedata/" + str(i) + ".jpg", "wb") as filepath:
        pickle.dump(crop_img, filepath)
    '''
    return fiveline

def getSymbol(fiveline, thresh, staffRow, staffRow_spacing, lastx):
    print(len(staffRow))
    index = 0
    
    for i in range(len(staffRow)):  #each row
        for j in range(lastx):          #search first line xaxis loc
            if(thresh[staffRow[i][0]][j] == 0 
               and thresh[staffRow[i][0] + 1][j] == 255
               and thresh[staffRow[i][1]][j] == 0
               and thresh[staffRow[i][2]][j] == 0
               and thresh[staffRow[i][3]][j] == 0
               and thresh[staffRow[i][4]][j] == 0):
                j=j+1   #get from next x-axis
                #print(j)
                #print("")
                break;
        
        '''
        if(thresh[staffRow[i][0]][j] == 0 
               and thresh[staffRow[i][0] + 1][j] == 255
               and thresh[staffRow[i][0] + staffRow_spacing[i] + 1][j] == 0
               and thresh[staffRow[i][0] + 2*staffRow_spacing[i] + 2][j] == 0
               and thresh[staffRow[i][0] + 3*staffRow_spacing[i] + 3][j] == 0
               and thresh[staffRow[i][0] + 4*staffRow_spacing[i] + 4][j] == 0):
                print(j)
                print("")
                break;
        '''
        
        ##pre find symbol
        #save searchCmp(default 5 line look like)
        l = 0
        searchCmp = []
        top_y = staffRow[i][0] - 5 * staffRow_spacing[i] - 1      #first line
        bottom_y = staffRow[i][4] + 5 * staffRow_spacing[i] + 1   #last line
        for k in range(top_y, bottom_y):
            searchCmp.append(thresh[k][j])
            l += 1
        
        #start find and comp
        flag=0
        #loop
        k = j
        while k < lastx:    #left to right
            tmp=[]
            tailCnt=0
            tail=0
            tailStart=0
            
            #save a thresh tmp
            for l in range(top_y,bottom_y):
                tmp.append(thresh[l][k])
                
                if(thresh[l][k] == 0 and thresh[l+1][k] == 0):  #count node tail
                    tail+=1
                    if(tail == 1):
                        tailStart = l
                    if(tail > tailCnt):
                        tailCnt = tail
                else:
                    tail=0
            
            #if(k == 406):
                #print("node406", tailCnt, tailStart)
            
            #comp
            if(flag == 0):  #find first xaxis change(each Symbol)
                
                if(searchCmp != tmp):
                    #print("flag")
                    set_topx = k-5
                    flag = 1
                
            if(flag):
                if(searchCmp == tmp):   #find last xaxis change(end of symbol)
                    set_endx = k+5
                    flag = 0
                elif(tailCnt > (3 * staffRow_spacing[i])):
                    if( tailCnt  != (4 * staffRow_spacing[i] + 4)):
                        set_topx = k - round(1.5 * staffRow_spacing[i])
                        k = k + 2 * staffRow_spacing[i]
                        set_endx = k
                        flag = 0
                        #print("node", tailCnt)
                #(tailCnt  == (4 * staffRow_spacing[i] + 4) and tailStart != staffRow[i][0])
                if(flag == 0):
                    #if(i==3):
                        #print(k, set_topx, set_endx, top_y, bottom_y)
                    fiveline = saveImg(fiveline, thresh, top_y, bottom_y, set_topx, set_endx, index)
                    index = index + 1
            k += 1
        
    cv2.imshow("show", fiveline)
    cv2.waitKey(0)

    cv2.imwrite("test.jpg", fiveline)
                
            