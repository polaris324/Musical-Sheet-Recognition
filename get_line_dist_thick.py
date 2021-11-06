import cv2
import os
import numpy as np
from collections import Counter

def get_line_dist_thick(img1, lastx):
    row = img1.shape[0]  # Image Height

    col = []        
    white_con_list = []
    black_con_list = []
    run_count = 0  # (相同值的连续累積數)
    run_type = img1[0, lastx-1]  # 255/0
    for j in range(row):   #in height
        if (img1[j, lastx-1] == run_type):  
            run_count += 1
        else:                               #連續中斷
            col.append(run_count)
            if (run_type == 0):
                white_con_list.append(run_count)
            else:
                black_con_list.append(run_count)

            # 累積值切換 0/255
            run_type = img1[j, lastx-1]
            run_count = 1
    
    # 把最後累積加回來
    col.append(run_count)
    if (run_type == 0):
        white_con_list.append(run_count)
    else:
        black_con_list.append(run_count)
    # 容器資料型態
    white_collect = Counter(white_con_list)
    black_collect = Counter(black_con_list)

    line_spacing = white_collect.most_common(1)[0][0]
    line_width = black_collect.most_common(1)[0][0]
    print("line spacing ", line_spacing)
    print("line width ", line_width)
    
    return line_width, line_spacing