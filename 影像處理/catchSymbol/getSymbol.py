import cv2
import os
import pickle
import numpy as np

def saveThreshTmp(top, bottom, k, thresh, tmp, tailCnt):    #保存此x-axis的列&取出連續計數
    tail=0  #tmp pixer 的計數器
    tailStart=0 #尾巴連續的起點
    
    for l in range(top,bottom): #上+5綫到下+5綫
        tmp.append(thresh[l][k]) #目前x-asix上+5綫到下+5綫pixer存入tmp
        
        if(thresh[l][k] == 0 and thresh[l+1][k] == 0):  #count node tail
            tail+=1
            if(tail == 1): #是尾巴頭
                tailStart = l
            if(tail > tailCnt): #尾巴連續
                tailCnt = tail
        else:
            tail=0
    return tmp, tailCnt

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
        for k in range(top_y, bottom_y):
            searchCmp.append(thresh[k][j])
            l += 1
        
        #start find and comp
        flag=0
        #loop
        k = j
        
        printFlag = 0   #上一個symbol輸出flag
        x1=0;x2=0;y1=0;y2=0 #crop for next symbol
        
        while k < lastx:    #left to right
            tmp=[]
            tailCnt=0
            
            
            
            #save a thresh tmp
            tmp, tailCnt = saveThreshTmp(top_y, bottom_y, k, thresh, tmp, tailCnt)
            #if(k == 406):
                #print("node406", tailCnt, tailStart)
            
            #comp
            if(flag == 0):  #find first xaxis change(each Symbol)
                
                if(searchCmp != tmp):   #比較測資不同發生時，開始記錄
                    print("flag, start:", k, tailCnt)
                    maxCnt = tailCnt
                    set_topx = k-5     #設定索取x坐標起點
                    flag = 1
                
            if(flag):
                
                if(tailCnt > maxCnt):   #此symbol内最大連續pixer數
                    maxCnt = tailCnt
                
                if(tailCnt > (3 * staffRow_spacing[i])):  #連續竪綫大於3閒
                    print(staffRow[i][4] - staffRow[i][0])
                    if( tailCnt  == (staffRow[i][4] - staffRow[i][0]) or
                        tailCnt  == (staffRow[i][4] - staffRow[i][0] + 1)): #連續竪綫為閒
                    #if( tailCnt  == (4 * staffRow_spacing[i] + 4)):
                        tailCnt2 = tailCnt
                        hold = k
                        
                        while(tailCnt2 == tailCnt):
                            hold += 1
                            tmp, tailCnt2 = saveThreshTmp(top_y, bottom_y, hold, thresh, tmp, tailCnt=0)
                        #print("tc:", tailCnt2)
                        if(tailCnt2 >= 0 and tailCnt2 <= 1):
                            set_endx = k+5  #設定索取x坐標終點
                            k = k+5
                            flag = 0
                        else:
                            set_topx = k - round(1.5 * staffRow_spacing[i])
                            k = k + 2 * staffRow_spacing[i]
                            set_endx = k
                            flag = 0
                            #print("node long:", tailCnt)
                    else:
                        set_topx = k - round(1.5 * staffRow_spacing[i])
                        k = k + 2 * staffRow_spacing[i]
                        set_endx = k
                        flag = 0        
                
                elif(searchCmp == tmp): #find last xaxis change(end of symbol)
                    
                    flag = 0
                    if(maxCnt > staffRow_spacing[i]):   #一般情況
                        set_endx = k+5
                    else:                               #遇到附點音符
                        #print("fn", k, x1, k+5, y1, y2)
                        fiveline = saveImg(fiveline, thresh, y1, y2, x1, k+5, index)
                        printFlag = 0
                        index = index + 1
                        k += 6
                        continue
                        
                if(flag == 0):
                    #if(i==9):
                            #print(k, x1, x2, y1, y2, printFlag)
                    
                    if(printFlag):  #輸出上一個symbol
                        fiveline = saveImg(fiveline, thresh, y1, y2, x1, x2, index)
                    x1,x2,y1,y2 = set_topx, set_endx, top_y, bottom_y   #覆蓋
                    printFlag=1
                    index = index + 1
            k += 1
        fiveline = saveImg(fiveline, thresh, y1, y2, x1, x2, index)
        
    cv2.imshow("show", fiveline)
    cv2.waitKey(0)

    cv2.imwrite("test.jpg", fiveline)
                
'''
if(searchCmp == tmp):   #find last xaxis change(end of symbol)
    set_endx = k+5
    flag = 0
elif(tailCnt > (3 * staffRow_spacing[i])):
    if( tailCnt  == (4 * staffRow_spacing[i] + 4)):
        tmp, tailCnt2 = saveThreshTmp(top_y, bottom_y, k+1, thresh, tmp, tailCnt=0)
        if(searchCmp == tmp):
            set_endx = k+5
            flag = 0
    if(flag):
        
        #if( tailCnt  != (4 * staffRow_spacing[i] + 4)):
        if(i==2):
            print("node found:", k)
        set_topx = k - round(1.5 * staffRow_spacing[i])
        k = k + 2 * staffRow_spacing[i]
        set_endx = k
        flag = 0
        print("node long:", tailCnt)
'''