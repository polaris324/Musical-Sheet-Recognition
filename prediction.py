# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 15:48:51 2021

@author: huanl
"""
import cv2
import numpy as np
import tensorflow

def whichnote(num):
    note = 100
    if(num<19):
        if (num==0):
            note = 55 #G
        elif (num == 1):
            note = 57 #A
        elif (num == 2):
            note = 59 #B
        elif (num == 3):
            note = 60 #C
        elif (num == 4):
            note = 62 #D
        elif (num == 5):
            note = 64 #E
        elif (num == 6):
            note = 65 #F
        elif (num == 7):
            note = 67 #G
        elif (num == 8):
            note = 69 #A
        elif (num == 9):
            note = 71 #B
        elif (num == 10):
            note = 72 #C
        elif (num == 11):
            note = 74 #D
        elif (num == 12):
            note = 76 #E
        elif (num == 13):
            note = 77 #F
        elif (num == 14):
            note = 79 #G
        elif (num == 15):
            note = 81 #A
        elif (num == 16):
            note = 83 #B
        elif (num == 17):
            note = 84 #C
        elif (num == 18):
            note = 86 #D
    else:
        if (num ==19):
            note = 100 #垃圾
        elif (num == 20):
            note = 120 #高音譜記號
        elif (num == 21):
            note = 121 #4分休止符
        elif (num == 22):
            note = 122 #8分休止符
        elif (num == 23):
            note = 123 #全休止符
        elif (num == 26):
            note = 124 #16分止符
        elif (num == 27):
            note = 125 #2分止符
    return note

def cnnPrediction(modelH, modelL, mapSymbol):
    resize_x = 64
    resize_y = 32
    temp = [0]
    
    notelistH = []
    notelistL = []
    
    img = cv2.imread("test.jpg")
    
    for num in range(len(mapSymbol)):
        y1, y2, x1, x2 = mapSymbol[num]
        crop_img = img[y1:y2, x1:x2]
        temp[0] = cv2.resize(crop_img, (resize_x, resize_y))
        temp = np.array(temp)
        temp = temp.astype("float32") / 255.0
        numH = np.argmax(modelH.predict(temp), axis=-1)# 音高模型
        length = np.argmax(modelL.predict(temp), axis=-1)# 音長模型
        
        note = whichnote(numH)
        notelistH.append(int(note))
        notelistL.append(int(length))
    
    return notelistH, notelistL