# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 15:32:54 2021

@author: 易昶辰

"""
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import pygame
import tkinterdnd2 as tkd # https://pythonguides.com/python-tkinter-drag-and-drop/ pip install tkinterdnd2

# from findline import findline
from pre_processing import preprocessing, _changeThersholdType
from get_axis_line import findstaff_spacing
from getSymbol import getSymbol
import noteheight
from NotationByNN import noteLength
import addmusic
mapSymbol = 0
def drop(event):
    var.set(event.data)

def openByFilePath():
    print("Upload")# test
    file_location = e_box.get()
    # print(file_loc)# test
    
    showImage(file_location)
    #https://stackoverflow.com/questions/66159973/display-image-when-button-is-clicked-python-gui
    
def Upload():
    path = filedialog.askopenfilename()
    global testText
    testText = path
    print(path)
    showImage(path)

def showImage(file_location):    
    image_width = Image.open(file_location).width
    image_height = Image.open(file_location).height
    if ( max(image_height, image_width) == image_height ):# vertical image
        resize_height = 600
        resize_width = 600/image_height*image_width
    else:# horizon image
        resize_height = 450/image_width*image_height
        resize_width = 450
    image_file = ImageTk.PhotoImage(Image.open(file_location).resize((int(resize_width), int(resize_height))))
    
    canvas.image = image_file
    canvas.create_image(225,300,anchor='center',image = image_file)
    global haveImage
    haveImage = True
    statusText.set("狀態 : 圖片已載入")

def mainA():
    statusText.set("狀態 : 執行中...")
    filename = testText
    img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    h, w = img.shape  # Image Length & Width
    
    # statusText.set('Status : Running - preprocessing')
    reload()
    _changeThersholdType(threshold.get(), thValue)
    thresh, h, w = preprocessing(img, h, w)
    
    reload()
    imgmask, staffRow, spacing, lastX, mono = findstaff_spacing(thresh, h, w)
    # imgmark = findline(thresh, h, w)
    # fiveline, lastx = five(imgmark)
    
    statusText.set("狀態 : 符號擷取中...")
    reload()
    # staffRow = get_fiveline_rows(fiveline, lastx)
    # staffRow_spacing, line_spacing = get_rows_dist(staffRow)
    
    global mapSymbol
    mapSymbol = getSymbol(imgmask, thresh, staffRow, spacing, lastX, mono)
    showThImage("test.jpg")
    try:
        noteheight._changeKey(keysValue.get()[0].upper())
    except IndexError:
        noteheight._changeKey('C')
    # showImage(testText)
    statusText.set("狀態 : 符號擷取完成")
    
    # statusText.set('Status : Running - CNN')
    # reload()
    # noteH = noteheight.noteheight(mapSymbol)
    # noteL = noteLength(mapSymbol)
    
    # statusText.set('Status : Running - creating Music')
    # reload()
    # addmusic._changeBeat(tempo.get())
    # addmusic.addmusic(noteL, noteH)
    # statusText.set('Status : Done')
    
def mainB():
    global mapSymbol
    
    statusText.set("狀態 : 符號辨識中...")
    reload()
    noteH = noteheight.noteheight(mapSymbol)
    noteL = noteLength(mapSymbol)
    
    statusText.set("狀態 : 音樂生成中...")
    reload()
    addmusic._changeBeat(tempo.get())
    addmusic.addmusic(noteL, noteH)
    statusText.set("狀態 : 音樂生成完畢")
        
def reload():
    ws.update()
    
def showThImage(which_file):
    image_width = Image.open(which_file).width
    image_height = Image.open(which_file).height
    if ( max(image_height, image_width) == image_height ):# vertical image
        resize_height = 600
        resize_width = 600/image_height*image_width
    else:# horizon image
        resize_height = 450/image_width*image_height
        resize_width = 450
    image_file = ImageTk.PhotoImage(Image.open(which_file).resize((int(resize_width)+20, int(resize_height)+20)))
    
    canvas_2.image = image_file
    canvas_2.create_image(225,300,anchor='center',image = image_file)

# def showImage(file_location):    
#     image_width = Image.open(file_location).width
#     image_height = Image.open(file_location).height
#     if ( max(image_height, image_width) == image_height ):# vertical image
#         resize_height = 600
#         resize_width = 600/image_height*image_width
#     else:# horizon image
#         resize_height = 450/image_width*image_height
#         resize_width = 450
#     image_file = ImageTk.PhotoImage(Image.open(file_location).resize((int(resize_width), int(resize_height))))
    
#     canvas.image = image_file
#     canvas.create_image(225,300,anchor='center',image = image_file)
#     global haveImage
#     haveImage = True
#     statusText.set('Status : Ready')

def showTempoValueBySelect(event):
     #print("New Element Selected")# test
     print(tempo.get())# test
     tempoText.set("MIDI節拍單位 :" + tempo.get())
     
def getTempoValue():
     #print("New Element Entered")# test
     print(tempo.get())# test
     tempoText.set("MIDI節拍單位 :" + tempo.get())
     global haveImage
     if haveImage:
         statusText.set("狀態 : 參數已變更(MIDI節拍單位 : "+ tempo.get() + " )")
     else:
         statusText.set("狀態 : 參數已變更[請輸入圖片]")
     #play_music(music_file)

def showThresholdValueBySelect(event):
     #print("New Element Selected")# test
     print(threshold.get())# test
     thresholdTypeText.set("二值化方法 :" + threshold.get())
     if threshold.get() == " 自定義閥值":
         thresholdValue.grid()
     else:
         thresholdValue.grid_remove()
     global haveImage
     if haveImage:
         statusText.set("狀態 : 參數已變更(二值化方法 : "+ threshold.get() + " )")
     else:
        statusText.set("狀態 : 參數已變更[請輸入圖片]")
     import time
     reload()
     time.sleep(1.5)
     statusText.set("狀態 : 二值化執行中...")
     filename = testText
    
     reload()
     img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
     h, w = img.shape  # Image Length & Width
     _changeThersholdType(threshold.get(), thValue)
     thresh, h, w = preprocessing(img, h, w)
    
     reload()
     imgmask, staffRow, spacing, lastX, mono = findstaff_spacing(thresh, h, w)
    #  fiveline, lastx = five(imgmark)
     
     showThImage("imgmask.jpg")
     statusText.set("狀態 : 二值化完成")
    

def getScaleValue(event):
    w = event.widget
     #print("New Element Selected")# test
    if isinstance(w, tk.Scale):
        print (w.get())
        global thValue
        thValue = w.get()
    global haveImage
    if haveImage:
        statusText.set("狀態 : 參數已變更\n(二值化-自定義方法之參數 : "+ (str(thValue)) + " )")
    else:
        statusText.set("狀態 : 參數已變更[請輸入圖片]")
    import time
    reload()
    time.sleep(1.5)
    statusText.set("狀態 : 二值化執行中...")
    filename = testText
    
    reload()
    img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    h, w = img.shape  # Image Length & Width
    _changeThersholdType(threshold.get(), thValue)
    thresh, h, w = preprocessing(img, h, w)
    
    reload()
    imgmask, staffRow, spacing, lastX, mono = findstaff_spacing(thresh, h, w)
     
    showThImage("imgmask.jpg")
    statusText.set("狀態 : 二值化完成")
     
def getKeysValue(event):
    w = event.widget
    KEYS = "ABCDEFG"
    if isinstance(w, tk.Entry):
        if(KEYS.find(keysValue.get()[0].upper()) != -1):
            print (w.get())
            keysText.set("調性 : " + keysValue.get()[0].upper())
        else:
            keysText.set("調性 : 輸入不正確\n[請輸入正確調性(介於A~G不分大小寫)]")
    global haveImage
    if haveImage:
        statusText.set("狀態 : 參數已變更(調性 : "+ keysValue.get()[0].upper() + " )")
    else:
        statusText.set("狀態 : 參數已變更[請輸入圖片]")
#-----------------------------------------------------------------------------------------------


# Initial window setting
ws = tkd.Tk()
ws.title("Musical-Sheet-Recognition")
ws.geometry("1450x750")
ws.iconbitmap("Logo_256.ico")
ws.config(bg="lightgray")

# Create Frame for Canvas
frame = tk.Frame(ws)
canvas = tk.Canvas(frame, width=450, height=600)
canvas.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

frame.grid(column=1, row=1, columnspan=3, rowspan=16)
tk.Label(ws, text="輸入圖像", bg="lightgray").grid(column=1, row=17, columnspan=3)

# Drag and drop setting
var = tk.StringVar()
var.set("請拖拉文件至此")
tk.Label(ws, text="文件位置 :",bg="lightgray").grid(column=0, row=0, padx=10, pady=10, sticky=tk.N)
# EnterBox
e_box = tk.Entry(ws, textvar=var, width=45)
e_box.grid(column=1, row=0 , padx=10, pady=10, sticky=tk.N)
e_box.drop_target_register(tkd.DND_FILES)
e_box.dnd_bind('<<Drop>>', drop)

# SendFilePath Button
btn_upload = tk.Button(ws, text="開啟", command=openByFilePath)#https://stackoverflow.com/questions/13099908/python-tkinter-return-value-from-function-used-in-command
btn_upload.grid(column=2, row=0, padx=10, pady=5)

# Upload Button
btn_upload = tk.Button(ws, text="選擇文件", command=Upload)
btn_upload.grid(column=3, row=0, padx=10, pady=5)
haveImage = False

#DirectEnter/SelectBox for Speed Selection
tempoText = tk.StringVar()
tempoText.set("MIDI節拍單位 :")     
tk.Label(ws, textvariable=tempoText,bg="lightgray", anchor=tk.W, width=32).grid(column=4, row=0, columnspan=3)
'''
values=["Larghissimo -20",
        "Grave 20-40",
        "Langsam 40-45",
        "Largo 40-60",
        "Larghetto 60-66",
        "Adagio 66-76",
        "Andante 76-108",
        "Mäßig 108-120",
        "Allegro 120-168",
        "Vivace 138-168",
        "Presto 168-200",
        "Prestissimo 200-"]
'''
# combo = ttk.Combobox(ws,values = values)
#combo = ttk.Combobox(ws)
tempo = tk.StringVar()
tk.Entry(ws, textvariable = tempo).grid(column=4, row=1, pady=10, columnspan=3,sticky='NWE')
# combo.bind("<<ComboboxSelected>>", showTempoValueBySelect)
#combo.grid(column=4, row=1, pady=10, columnspan=3,sticky='NWE')
tk.Button(ws, text="設定", command=getTempoValue).grid(column=7, row=1, padx=10, pady=10, sticky=tk.N)

# Bar for threshold
thresholdTypeText = tk.StringVar()
thresholdTypeText.set("二值化方法 :")
tk.Label(ws, textvariable=thresholdTypeText, bg="lightgray").grid(column=4, row=2, columnspan=3, sticky=tk.W)
values=[" OTSU",
        " 自定義閥值",
        " YEN"]
threshold = tk.StringVar()
thresholdTypeCombo = ttk.Combobox(ws, value = values, textvariable=threshold)
thresholdTypeCombo.bind("<<ComboboxSelected>>", showThresholdValueBySelect)
thresholdTypeCombo.grid(column=4, row=3, columnspan=3, sticky='WES')
thValue = tk.StringVar()
thresholdValue = tk.Scale(ws, from_=1, to=254,orient='horizonta' ,tickinterval=50,length=200)
thresholdValue.grid(column=4, row=4, rowspan=4, columnspan=3, padx=10, pady=5)
thresholdValue.bind("<ButtonRelease>", getScaleValue)
thresholdValue.grid_remove()

# Keys
keysText = tk.StringVar()
keysText.set("調性 :")
tk.Label(ws, textvariable=keysText, bg="lightgray").grid(column=4, row=8, columnspan=3, sticky=tk.W)
keysValue = tk.StringVar()
keysEntry = tk.Entry(ws, textvariable = keysValue)
keysEntry.bind("<KeyRelease>", getKeysValue)
keysEntry.grid(column=4, row=9, pady=10, columnspan=3,sticky='NWE')

# Submit
statusText = tk.StringVar()
statusText.set("狀態 :")
tk.Label(ws, textvariable=statusText, bg="lightgray").grid(column=4, row=10, columnspan=3, sticky=tk.W)
Confirm = tk.Button(ws, text="進行音符擷取", command=mainA)
Confirm.grid(column=4, row=11, columnspan=3, padx=10, pady=5,sticky = 'we')
Run = tk.Button(ws, text="執行樂譜辨識", command=mainB)
Run.grid(column=4, row=12, columnspan=3, padx=10, pady=5,sticky = 'we')

# Music player
pygame.mixer.init()
def play():
    pygame.mixer.music.load("datamusic.mid")
    pygame.mixer.music.play()

def pause():
    pygame.mixer.music.pause()

def stop():
    pygame.mixer.music.stop()

def ex():
    pygame.mixer.music.stop()
    ws.destroy()

tk.Label(ws, text="播放控制 :", bg="lightgray").grid(column=4, row=15, columnspan=3, sticky=tk.W)
Play = tk.Button(ws, text = "播放", command = play).grid(column=4, row=16, padx=10, pady=5, sticky='swe')
# Pause = tk.Button(ws,text = 'Pause', command = pause).grid(column=5, row=16, padx=10, pady=5, sticky='swe')
Stop = tk.Button(ws, text="停止", command=stop).grid(column=6, row=16, padx=10, pady=5, sticky='swe')

#Threshold Image
thImg = tk.Frame(ws)
canvas_2 = tk.Canvas(thImg, width=450, height=600)
canvas_2.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

thImg.grid(column=8, row=1, columnspan=3, rowspan=16)
tk.Label(ws, text="預處理結果", bg="lightgray").grid(column=8, row=17, columnspan=3)


#Exit Button
quit_buttom = tk.Button(ws, text="離開程式", command=ex)
quit_buttom.grid(column=11, row=17, padx=10, pady=5)

#-----------------------------------------------------------------------------------------------
# Progress bar widget
'''
progress = ttk.Progressbar(ws, orient = tk.HORIZONTAL,
              length = 100, mode = 'determinate')
  
# Function responsible for the updation
# of the progress bar value

cmd = False


def start():
    import time
    progress.start(1000)
    for per in range(100):
        progress['value'] = per
        ws.update_idletasks()
        ws.update()
        time.sleep(0.1)

def pause():
    progress.pause()

def stop():
    progress.stop()
    
    
progress.grid(column=4, row=1, columnspan=3, padx=10, pady=5,sticky='ews')

# This button will initialize
# the progress bar
tk.Button(ws, text = 'Start', command = start).grid(column=4, row=2, padx=10, pady=5, sticky='nwe')
tk.Button(ws, text = 'Pause', command = pause).grid(column=5, row=2, padx=10, pady=5, sticky='nwe')
tk.Button(ws, text = 'Stop', command = stop).grid(column=6, row=2, padx=10, pady=5, sticky='nwe')
'''
#-----------------------------------------------------------------------------------------------

ws.mainloop()