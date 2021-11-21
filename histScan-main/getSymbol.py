import cv2
import os
import pickle
import numpy as np

mapNote = [] # 存放音符坐標Array
catchSymbolIndex = 0 #圖片編號定位
thresh = []

# In[保存此x-axis的列&取出連續計數]

def saveThreshTmp(top, bottom, y):
    global thresh
    tmp = []
    tail = 0  #tmp pixer 的計數器
    tailCnt = 0
    
    for x in range(top,bottom): # 上+5綫到下+5綫
        tmp.append(thresh[x][y])    # 目前x-asix上+5綫到下+5綫pixer存入tmp
        
        if(thresh[x][y] == 0 and thresh[x+1][y] == 0):  #count node tail
            tail+=1

        else:
            if(tail > tailCnt):     # 最大連續計數
                tailCnt = tail
                # 'check'
                # if(y == 453):
                #     print("[checkTail]", tail, tailCnt, x)
            tail=0                  # 重置連續計數
    if(tail > tailCnt):     # 最大連續計數
        tailCnt = tail
    return tmp, tailCnt

# In[add Symbol to fiveline]

def saveImg(imgmask, th, yfirst, ylast, xfirst, xlast, i):
    
    for yaxis in range(yfirst, ylast):
        for xaxis in range(xfirst, xlast):
            imgmask[yaxis][xaxis] = th[yaxis][xaxis]

    crop_img = th[yfirst:ylast, xfirst:xlast]
    if not os.path.exists("notedata"):
        os.mkdir("notedata")
    
    num = str(i)
    # cv2.imwrite("notedata/" + num.zfill(5) + ".jpg", crop_img)
    cv2.imwrite("notedata/" + num + ".jpg", crop_img)
    
    return imgmask

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
            'check'
            # print(loop + top)
        else:
            if(cnt > maxcnt):
                maxcnt = cnt
            cnt = 0
            
    return maxcnt

# In[crop Symbol]

def getSymbol(imgmask, threshMap, staffRow, staffRow_spacing, lastx):
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
        top_y    = staffRow[i][0] - (5 * staffRow_spacing) - 1   # top-first line scan
        bottom_y = staffRow[i][4] + (5 * staffRow_spacing) + 1   # botton-last line scan
        
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
        'temp of check'
        tmpIndex = 163


        while k < lastx:    # five-line, left to right
            tmp=[]              # current up-down Array
            
            tailCnt2 = tailCnt #前一個
            
            # save a thresh tmp
            tmp, tailCnt = saveThreshTmp(top_y, bottom_y, k) #tailCnt=0可以不用

            'check'
            # if( index == tmpIndex -1):
            #     print("[node]", k, tailCnt, tailCnt2, firstCut, maxCnt2, bottom_y-top_y, index)
            
            
            # comp
            # 未抓捕狀態 find first xaxis change(each Symbol)
            if(flag == 0):
                if(not np.array_equal(searchCmp, tmp)):   # 比較測資不同發生時，開始記錄
                    
                    maxCnt = tailCnt    # store current 最大 連續pixers 計數
                    set_topx = k - staffRow_spacing  # 設定索取x坐標起點
                    set_endx = k #210928
                    
                    # get first impact info 211007
                    firstImpact_Locx = k # 保存第一個觸發x-axis位置
                    # 'check '
                    # if(index == tmpIndex -1):
                    #         print("[檢查firstImpact_Col]", k, top_y)

                    flag = 1    # Jump 抓捕狀態
                    
            # 抓捕狀態
            if(flag):
                
                
                if(tailCnt > maxCnt):   # 更新symbol 最大 連續pixers 計數
                    maxCnt = tailCnt
                    maxChangeFlag = 1

                'check each x-aixs by a index'
                if(index == tmpIndex -1):
                        print("[檢查竪綫]", i, k, tailCnt, set_topx, '~', getListDiffCnt(firstImpact_Locx - 1, maxlocX, staffRow[i], top_y, bottom_y), index+1)
                
                if(tailCnt >= (3 * staffRow_spacing)):  # 連續竪綫大於3閒
                    'check'
                    if(index == tmpIndex -1):
                        print("[upTo3jian]", k, tailCnt, tailCnt2, index+1)
                    if( tailCnt2 <= 1 and 
                       (tailCnt == (staffRow[i][4] - staffRow[i][0]) or
                        tailCnt == (staffRow[i][4] - staffRow[i][0] + 1) or
                        tailCnt >= (bottom_y - staffRow[i][0]))): # 連續竪綫長度為閒
                            
                        'check'
                        if(index == tmpIndex -1):
                            print("[長度為閒]", k, tailCnt, index)

                        tailCnt_tmp = tailCnt          # loop 比較用 # 追查 211020
                        hold = k                    # loop 更新x-axis 截取位置
                        while(tailCnt_tmp == tailCnt): # loop 跳過相同竪綫長度
                            hold += 1
                            tmp, tailCnt_tmp = saveThreshTmp(top_y, bottom_y, hold)
                        
                        # 小節綫處理
                        if(tailCnt_tmp < (0.2 * staffRow_spacing)): # 下一個 x-aixs 沒符號特徵
                            set_endx = k + staffRow_spacing  # 設定索取x坐標終點
                            k = set_endx    # x-aixs 設定為 right-last 定下次搜尋目標位置
                            flag = 0        # Jump 輸出狀態
                        
                    if(firstCut == 0 and flag == 1): # 連續竪綫長度不為閒 # 211007 不是x軸第一個符號（不是譜號）
                        
                        'check'
                        if(index == tmpIndex -1):
                            print("[upTo3jian & 不為閒]", k, tailCnt, tailCnt2, maxCnt2, maxlocX, getListDiffCnt(firstImpact_Locx - 1, maxlocX, staffRow[i], top_y, bottom_y), index+1)
                        
                        #分成左杠右杠
                        if( (tailCnt2 != 0 and maxCnt2 != 0) and
                            (getListDiffCnt(firstImpact_Locx - 1, maxlocX, staffRow[i], top_y, bottom_y) >= round(0.78 * staffRow_spacing)) ):  #符杆前面有連續pixel
                            #只有不超過閒的連續pixel（單音符）
                            print(".\ ", k, i, maxCnt2, tailCnt2, printFlag, index+1) 
                            set_topx = k - round(1.8 * staffRow_spacing)
                            if(set_topx < firstImpact_Locx):
                                set_topx = firstImpact_Locx - round(0.5 * staffRow_spacing)
                            
                            k = k + round(0.8 * staffRow_spacing)
                        
                        else: #/.
                            print("\. ", k, i, maxCnt2, tailCnt2, printFlag, index+1)
                            set_topx = k - round(0.8 * staffRow_spacing) #[0.8]
                            k = k + round(1.8 * staffRow_spacing)
                            
                        set_endx = k

                        'check'
                        # if(index == tmpIndex -1):
                        #     print(set_topx, '~', set_endx, printFlag)

                        maxCnt=0
                        maxCnt2 = 0
                        flag = 0        # Jump 輸出狀態
                        # if(index+1==7):
                        #     print(k, set_topx, set_endx, top_y, bottom_y)

                
                elif(searchCmp == tmp): #find last xaxis change(end of symbol)
                    'check'
                    if(index == tmpIndex-1):
                        print("[一般變化結束]", k, firstCut, maxCnt)
                    flag = 0
                    
                    if(firstCut==1 and maxCnt <= staffRow_spacing+1):
                        print("[FristCut]", k, maxCnt, tailCnt, index)
                        # firstCut=0
                        flag=0
                        k += 1
                        continue
                
                    if(maxCnt > staffRow_spacing or (k - firstImpact_Locx) > staffRow_spacing):   #一般情況
                        set_endx = k + staffRow_spacing # 應該改成 k + staffRow_spacing[i]
                        'check'
                        if(index == tmpIndex-1):
                            print("[一般變化結束]", k, set_topx, '~', set_endx, maxCnt, index+1)
                        
                        firstCut=0 #211007 重置
                        maxCnt2=0  #211011 重置

                    else: #遇到附點音符
                        
                        imgmask = saveImg(imgmask, thresh, y1, y2, x1, k+5, index)
                        'save Array[]'
                        # saveArray(y1, y2, x1, k+5, index)
                        
                        maxCnt2 = 0 #211008 重值
                        index = index + 1
                        printFlag = 0
                        k += 6
                        continue
                


                if(flag == 0):
                    
                    # if(i==2):
                    #         print(k, x1, x2, y1, y2, printFlag)
                    if(printFlag):  #輸出上一個symbol
                        # if(index == tmpIndex):
                        #     print("print", k, x1, x2, y1, y2, printFlag, index)
                        imgmask = saveImg(imgmask, thresh, y1, y2, x1, x2, index) # 符號進行輸出（上單元）
                        'save Array[]'
                        # saveArray(y1, y2, x1, x2, index)
                        
                        index = index + 1   # 符號計數+1
                    x1,x2,y1,y2 = set_topx, set_endx, top_y, bottom_y   # 覆蓋單元符號坐標記錄（新單元）
                    if(index == tmpIndex):
                        print("saveArray", k, x1, x2, y1, y2, printFlag, index)
                    printFlag=1
                elif(maxChangeFlag):
                    maxCnt2 = maxCnt # 如果不符合上面的，找下一個
                    maxlocX = k #最大連續計數的x-axis 211013
                    maxChangeFlag = 0
                    
            k += 1
        print("list_lastone:", y1, y2, x1, x2, index)
        imgmask = saveImg(imgmask, thresh, y1, y2, x1, x2, index)
        
        'save Array[]'
        # saveArray(y1, y2, x1, x2, index)
        index = index + 1 
        

    # In[Output Test Img]
        
    # cv2.imshow("show", fiveline)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    cv2.imwrite("test.jpg", imgmask)
    
    # return mapNote