# -*- coding: utf-8 -*-
"""
Image Preprocessing in:
    Resize Maximum image width limit 1024px
    Noise Removal
    Deskewing(None)
    Binarization
"""
import cv2
import numpy as np
from skimage.filters import threshold_yen

"""Global variable"""
thresholdSelect = ' Otsu'   # 預設二值化為 (Otsu自適應 \ Customize \ Ken)
thresholdRet    = 200      # 固定阈值變數

def _changeThersholdType(thresholdType, retNum):
    global thresholdSelect
    global thresholdRet
    thresholdSelect = thresholdType
    thresholdRet = retNum

def resizeW1024(img, h, w):
    scale_percent = 1 - (w - 1024) / w
    width = int(w * scale_percent)
    height = int(h * scale_percent)
    dim = (width, height)
    
    return cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

def preprocessing(img, h, w):

    # Image Resize
    if(w > 1024): # if image is too big, resize to regular size
        img = resizeW1024(img, h, w)
        h, w = img.shape  # new Image Length & Width
    
    #  Noise Removal
    imgNR = cv2.fastNlMeansDenoising(img, None, 10, 7, 21)
    
    # Deskewing = None =
    
    #  Binarization
    if (thresholdSelect   == ' Customize'): # Using Global binarization with T
        ret, thresh = cv2.threshold(imgNR, thresholdRet, 255, cv2.THRESH_BINARY)
    elif (thresholdSelect == ' YEN'      ): # Using Global binarization with YEN
        binary = threshold_yen(imgNR)
        binary_niblack = imgNR >= binary
        thresh = binary_niblack * np.uint8(255)
    else:                                   # Using Global binarization with OTSU
        ret, thresh = cv2.threshold(imgNR, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        print(ret)
    
    # thresh = result of the preprocessing
    cv2.imwrite("Preprocessing_Img.jpg", thresh) # output binarizated result
    return thresh, h, w
