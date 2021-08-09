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
        
        ##pre find symbol
        #save searchCmp(default 5 line look like)
        l = 0
        searchCmp = []
        top_y = staffRow[i][0] - 5 * staffRow_spacing[i] - 1      #first line
        bottom_y = staffRow[i][4] + 5 * staffRow_spacing[i] + 1   #last line
        for k in range(top_y, bottom_y):    #把起點copy成一個default測資
            searchCmp.append(thresh[k][j])
            l += 1
        
        #start find and comp
        flag=0
        #loop
        k = j
        while k < lastx:    #left to right
            tmp=[]      #目前x-asis的比較測資
            tailCnt=0   #記錄音符尾巴連續
            tail=0      #tmp pixer 的計數器
            tailStart=0 #尾巴連續的起點
            
            #save a thresh tmp
            for l in range(top_y,bottom_y): #上+5綫到下+5綫
                tmp.append(thresh[l][k])    #目前x-asix上+5綫到下+5綫pixer存入tmp
                
                if(thresh[l][k] == 0 and thresh[l+1][k] == 0):  #count node tail
                    tail+=1
                    if(tail == 1):  #是尾巴頭
                        tailStart = l
                    if(tail > tailCnt): #尾巴連續
                        tailCnt = tail
                else:
                    tail=0        
            
            #comp
            if(flag == 0):  #find first xaxis change(each Symbol)
                
                if(searchCmp != tmp):   #比較測資不同發生時，開始記錄
                    #print("flag")
                    set_topx = k-5      #設定索取x坐標起點
                    flag = 1            #開始抓圖
                
            if(flag):
                if(searchCmp == tmp):   #find last xaxis change(end of symbol)
                    set_endx = k+5      #設定索取x坐標終點
                    flag = 0
                elif(tailCnt > (3 * staffRow_spacing[i])):  #連續竪綫大於3閒
                    if( tailCnt  != (4 * staffRow_spacing[i] + 4)): #連續竪綫非閒
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
                
            