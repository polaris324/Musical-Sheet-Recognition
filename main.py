from pre_processing import preprocessing
from findline import findline
from five import five
from get_fiveline_rows import get_fiveline_rows
from get_rows_dist import get_rows_dist
from getSymbol import getSymbol
from noteheight import noteheight
from NotationByNN import noteLength
from addmusic import addmusic
import cv2
import os
import time

# In[Read Image]
filename = input() # maybe use .argparse to avoid error input
img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
h, w = img.shape  # Image Length & Width

# In[Image Preprocessing]
thresh, h, w = preprocessing(img, h, w)

# In[Staff Detection]
imgmark = findline(thresh, h, w)
fiveline, lastx = five(imgmark)

# In[Reference line distance & thickness]
staffRow = get_fiveline_rows(fiveline, lastx)
staffRow_spacing, line_spacing = get_rows_dist(staffRow)

# In[GET NODE]
mapSymbol = getSymbol(fiveline, thresh, staffRow, staffRow_spacing, lastx)

# In[Get Note High & Note Long]
# noteH = noteheight(mapSymbol)
# noteL = noteLength(mapSymbol)

# In[Create Music]
# addmusic(noteL, noteH)