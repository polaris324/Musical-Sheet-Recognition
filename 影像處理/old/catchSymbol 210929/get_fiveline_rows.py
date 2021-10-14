def get_fiveline_rows(img1, lastx):
    
    row = img1.shape[0]  # Image Height
    staffRow = []
    lineRow = []
    line_count = 0
    
    for i in range(row):   #in height
        if (img1[i, lastx-1] == 255):  #is black
            lineRow.append(i)
            line_count += 1
        if (line_count == 5): # one set
            staffRow.append(lineRow)
            lineRow = []
            line_count = 0
    return staffRow
            
            
    