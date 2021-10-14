import cv2
import os
import pickle
import numpy as np

mapNote = [] # 存放音符坐標Array
catchSymbolIndex = 0 #圖片編號定位
thresh = []

# In[保存此x-axis的列&取出連續計數]

def saveThreshTmp(top, bottom, k):
    global thresh
    tmp = []
    tail = 0  #tmp pixer 的計數器
    tailCnt = 0
    
    for l in range(top,bottom): # 上+5綫到下+5綫
        tmp.append(thresh[l][k])    # 目前x-asix上+5綫到下+5綫pixer存入tmp
        
        if(thresh[l][k] == 0 and thresh[l+1][k] == 0):  #count node tail
            tail+=1
        else:
            if(tail > tailCnt):     # 最大連續計數
                tailCnt = tail
            tail=0                  # 重置連續計數
    return tmp, tailCnt

# In[add Symbol to fiveline]

def saveImg(fiveline, th, yfirst, ylast, xfirst, xlast, i):
    
    for yaxis in range(yfirst, ylast):
        for xaxis in range(xfirst, xlast):
            fiveline[yaxis][xaxis] = th[yaxis][xaxis]

    crop_img = th[yfirst:ylast, xfirst:xlast]
    if not os.path.exists("notedata"):
        os.mkdir("notedata")
    
    num = str(i)
    cv2.imwrite("notedata/" + num.zfill(5) + ".jpg", crop_img)
    # cv2.imwrite("notedata/" + num + ".jpg", crop_img)
    
    return fiveline

# In[add Symbol to list[]]

def saveArray(yfirst, ylast, xfirst, xlast, i):
    global catchSymbolIndex
    axis = [yfirst, ylast, xfirst, xlast]
    
    if(catchSymbolIndex == i):
        mapNote.pop(catchSymbolIndex - 1)
    mapNote.append(axis)
    catchSymbolIndex = i
    return

# In[comp 2 list & return unmatch cnt at listB have the weight]
def getListDiffCnt(k, maxX, staffRow, top, bottom):
    cnt=0;maxcnt=0
    listA, tmp = saveThreshTmp(top, bottom, k)
    listB, tmp = saveThreshTmp(top, bottom, maxX)
    
    for loop in range(5):
        listA[staffRow[loop] - top] = 255
    
    for loop in range(len(listA)):
        if(listA[loop] == 255 and listB[loop] == 0):
            cnt += 1
        else:
            if(cnt > maxcnt):
                maxcnt = cnt
            cnt = 0
            
    return maxcnt

# In[crop Symbol]

def getSymbol(fiveline, threshMap, staffRow, staffRow_spacing, lastx):
    global thresh
    thresh = threshMap
    print(len(staffRow)) # 每個五綫 y-axis 位置
    index = 1
    
    for i in range(len(staffRow)):  # loop each five-line row
        for j in range(lastx):          # loop for search first x-axis loc of five-line
            if(thresh[staffRow[i][0]][j] == 0 
               and thresh[staffRow[i][0] + 1][j] == 255
               and thresh[staffRow[i][1]][j] == 0
               and thresh[staffRow[i][2]][j] == 0
               and thresh[staffRow[i][3]][j] == 0
               and thresh[staffRow[i][4]][j] == 0):
                j=j+1   #get from next x-axis
                break;
        
        # In[Store Default five-line Array]
        
        # save searchCmp(default five-line look like)
        searchCmp = [] #default five-line store array
        top_y    = staffRow[i][0] - (5 * staffRow_spacing[i]) - 1   # top-first line scan
        bottom_y = staffRow[i][4] + (5 * staffRow_spacing[i]) + 1   # botton-last line scan
        
        l = 0 # tmp
        for k in range(top_y, bottom_y): # loop for store default five-line
            searchCmp.append(thresh[k][j])
            l += 1
        
        # In[Find & Comp]
        flag = 0
        # loop
        k = j
        
        printFlag = 0           # 上一個symbol輸出flag (0:不輸出，1:輸出)
        x1=0;x2=0;y1=0;y2=0     # loc crop for next symbol
        firstCut = 1            # 是否為five-line第一個被剪的
        firstImpact_Locx = 0
        tailCnt=0           # 單次y-axis 連續pixers 計數
        tailCnt2 = 0
        maxChangeFlag = 0
        maxCnt2 = 0
        maxlocX = 0
        
        while k < lastx:    # five-line, left to right
            tmp=[]              # current up-down Array
            
            tailCnt2 = tailCnt #前一個
            
            # save a thresh tmp
            tmp, tailCnt = saveThreshTmp(top_y, bottom_y, k) #tailCnt=0可以不用
            
            
            # comp
            # 未抓捕狀態 find first xaxis change(each Symbol)
            if(flag == 0):
                if(not np.array_equal(searchCmp, tmp)):   # 比較測資不同發生時，開始記錄
                    
                    maxCnt = tailCnt    # store current 最大 連續pixers 計數
                    set_topx = k - staffRow_spacing[i]  # 設定索取x坐標起點
                    set_endx = k #210928
                    
                    # get first impact info 211007
                    firstImpact_Locx = k # 保存第一個觸發x-axis位置 
                    flag = 1    # Jump 抓捕狀態
                    
            # 抓捕狀態
            if(flag):
                
                
                if(tailCnt > maxCnt):   # 更新symbol 最大 連續pixers 計數
                    maxCnt = tailCnt
                    maxChangeFlag = 1
                
                if(tailCnt >= (3 * staffRow_spacing[i])):  # 連續竪綫大於3閒
                    if( tailCnt2 <= 1 and 
                       (tailCnt == (staffRow[i][4] - staffRow[i][0]) or
                        tailCnt == (staffRow[i][4] - staffRow[i][0] + 1) or
                        tailCnt >= (bottom_y - staffRow[i][0]))): # 連續竪綫長度為閒
                            
                        tailCnt_tmp = tailCnt          # loop 比較用 # 追查 211020
                        hold = k                    # loop 更新x-axis 截取位置
                        while(tailCnt_tmp == tailCnt): # loop 跳過相同竪綫長度
                            hold += 1
                            tmp, tailCnt_tmp = saveThreshTmp(top_y, bottom_y, hold)
                        
                        # 小節綫處理
                        if(tailCnt_tmp < (0.2 * staffRow_spacing[i])): # 下一個 x-aixs 沒符號特徵
                            set_endx = k + staffRow_spacing[i]  # 設定索取x坐標終點
                            k = set_endx    # x-aixs 設定為 right-last 定下次搜尋目標位置
                            flag = 0        # Jump 輸出狀態
                        
                    if(firstCut == 0 and flag == 1): # 連續竪綫長度不為閒 # 211007 不是x軸第一個符號（不是譜號）
                    
                        #分成左杠右杠
                        if( (tailCnt2 != 0 and maxCnt2 != 0) and
                            (getListDiffCnt(firstImpact_Locx - 1, maxlocX, staffRow[i], top_y, bottom_y) >= round(0.78 * staffRow_spacing[i])) ):  #符杆前面有連續pixel
                            #只有不超過閒的連續pixel（單音符）

                            set_topx = k - round(1.8 * staffRow_spacing[i])
                            if(set_topx < firstImpact_Locx):
                                set_topx = firstImpact_Locx - round(0.5 * staffRow_spacing[i])
                            
                            k = k + staffRow_spacing[i]
                        
                        else: #/.
                            set_topx = k - staffRow_spacing[i] #[0.8]
                            k = k + round(1.8 * staffRow_spacing[i])
                            
                        set_endx = k

                        maxCnt=0
                        maxCnt2 = 0
                        flag = 0        # Jump 輸出狀態
                
                elif(searchCmp == tmp): #find last xaxis change(end of symbol)
                    flag = 0
                    
                    if(firstCut==1 and maxCnt <= staffRow_spacing[i]+1):
                        flag=0
                        k += 1
                        continue
                
                    if(maxCnt > staffRow_spacing[i] or (k - firstImpact_Locx) > staffRow_spacing[i]):   #一般情況
                        set_endx = k + staffRow_spacing[i] # 應該改成 k + staffRow_spacing[i]
                        
                        firstCut=0 #211007 重置
                        maxCnt2=0  #211011 重置

                    else:                               #遇到附點音符
                        
                        fiveline = saveImg(fiveline, thresh, y1, y2, x1, k+5, index)
                        'save Array[]'
                        saveArray(y1, y2, x1, k+5, index)
                        
                        maxCnt2 = 0 #211008 重值
                        index = index + 1
                        printFlag = 0
                        k += 6
                        continue
                
                if(flag == 0):
                    
                    if(printFlag):  #輸出上一個symbol

                        fiveline = saveImg(fiveline, thresh, y1, y2, x1, x2, index)
                        'save Array[]'
                        saveArray(y1, y2, x1, x2, index)
                        
                        index = index + 1
                    x1,x2,y1,y2 = set_topx, set_endx, top_y, bottom_y   #覆蓋
                    printFlag=1
                elif(maxChangeFlag):
                    maxCnt2 = maxCnt # 如果不符合上面的，找下一個
                    maxlocX = k #最大連續計數的x-axis 211013
                    maxChangeFlag = 0
                    
            k += 1
        fiveline = saveImg(fiveline, thresh, y1, y2, x1, x2, index)
        
        'save Array[]'
        saveArray(y1, y2, x1, x2, index)
        index = index + 1 
        

    # In[Output Test Img]
        
    cv2.imshow("show", fiveline)
    cv2.waitKey(0)
    cv2.imwrite("test.jpg", fiveline)
    
    return mapNote