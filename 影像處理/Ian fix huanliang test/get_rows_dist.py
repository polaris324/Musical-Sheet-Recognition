
import numpy as np

def get_rows_dist(staffRow):
    row = len(staffRow) # num of staff row
    staffRow_spacing = []   # mean of each line spacing
    
    for i in range(row):    # loop each row
        row_spacing = []
        for j in range(4):  # search each row spacing
            row_spacing.append(staffRow[i][j+1] - staffRow[i][j] -1)
        counts = np.bincount(row_spacing)
        staffRow_spacing.append(np.argmax(counts))
    counts = np.bincount(staffRow_spacing)
    line_spacing = np.argmax(counts)
    
    return staffRow_spacing, line_spacing