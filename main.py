from findline import findline
from five import five
from get_fiveline_rows import get_fiveline_rows
from get_rows_dist import get_rows_dist
from getSymbol import getSymbol
from noteheight import noteheight
import cv2
import os

# In[Read Image]
filename = input()
img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

# In[Image Preprocessing + Staff Detection]
thresh, imgmark = findline(filename)
fiveline, lastx = five(imgmark)

# In[Reference line distance & thickness]
staffRow = get_fiveline_rows(fiveline, lastx)
staffRow_spacing, line_spacing = get_rows_dist(staffRow)
#print(staffRow)
#print(" ")
#print(staffRow_spacing, line_spacing, lastx)
#os.remove("final.jpg")

# In[GET NODE]
mapSymbol = getSymbol(fiveline, thresh, staffRow, staffRow_spacing, lastx)

# In[Get Note High & Note Long]
noteheight(mapSymbol)
# midi_inputList = getPredict(thresh, mapSymbol)

# In[Create Music]
# addMusic(midi_inputList)