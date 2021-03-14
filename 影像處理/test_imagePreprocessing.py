# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 10:28:08 2021

@author: huanl
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

def get_ref_lengths(img):
    num_rows = img.shape[0]  # Image Height (number of rows)
    num_cols = img.shape[1]  # Image Width (number of columns)
    rle_image_white_runs = []  # Cumulative white run list
    rle_image_black_runs = []  # Cumulative black run list
    sum_all_consec_runs = []  # Cumulative consecutive black white runs

    for i in range(num_cols):
        col = img[:, i]
        rle_col = []
        rle_white_runs = []
        rle_black_runs = []
        run_val = 0  # (The number of consecutive pixels of same value)
        run_type = col[0]  # Should be 255 (white) initially
        for j in range(num_rows):
            if (col[j] == run_type):
                # increment run length
                run_val += 1
            else:
                # add previous run length to rle encoding
                rle_col.append(run_val)
                if (run_type == 0):
                    rle_black_runs.append(run_val)
                else:
                    rle_white_runs.append(run_val)

                # alternate run type
                run_type = col[j]
                # increment run_val for new value
                run_val = 1

        # add final run length to encoding
        rle_col.append(run_val)
        if (run_type == 0):
            rle_black_runs.append(run_val)
        else:
            rle_white_runs.append(run_val)

        # Calculate sum of consecutive vertical runs
        sum_rle_col = [sum(rle_col[i: i + 2]) for i in range(len(rle_col))]

        # Add to column accumulation list
        rle_image_white_runs.extend(rle_white_runs)
        rle_image_black_runs.extend(rle_black_runs)
        sum_all_consec_runs.extend(sum_rle_col)

    white_runs = Counter(rle_image_white_runs)
    black_runs = Counter(rle_image_black_runs)
    black_white_sum = Counter(sum_all_consec_runs)

    line_spacing = white_runs.most_common(1)[0][0]
    line_width = black_runs.most_common(1)[0][0]
    width_spacing_sum = black_white_sum.most_common(1)[0][0]

    assert (line_spacing + line_width == width_spacing_sum), "Estimated Line Thickness + Spacing doesn't correspond with Most Common Sum "

    return line_width, line_spacing

#  Read Image
img2 = cv2.imread('1.png', 0)

#  Noise Removal
img = cv2.fastNlMeansDenoising(img2, None, 10, 7, 21)

cv2.imshow('test', img)
cv2.waitKey()

#  Binarization
## Global Thresholding(需要手動調)
#ret1, imgB = cv2.threshold(img,161,255,cv2.THRESH_BINARY)
## Otsu's Thresholding
ret, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

cv2.imwrite('binarized.jpg', img)
cv2.imshow('binarized.jpg', img)
plt.hist(img.ravel(),256) #檢查
cv2.waitKey()

#  Deskewing 偏斜校正

#  Reference Lengths
line_width, line_spacing = get_ref_lengths(img)