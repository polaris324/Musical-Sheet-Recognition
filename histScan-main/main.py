from pre_processing import preprocessing
from get_axis_line import findstaff_spacing
from getSymbol import getSymbol
# from noteheight import noteheight
# from NotationByNN import noteLength
# from addmusic import addmusic
import cv2
import os
import time

# In[Read Image]
filename = input() # maybe use .argparse to avoid error input
img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
h, w = img.shape  # Image Length & Width

# In[Image Preprocessing]
thresh, h, w = preprocessing(img, h, w)

# In[Staff Detection, Reference line distance & thickness]
imgmask, staffRow, spacing, lastX = findstaff_spacing(thresh, h, w)

# In[GET NODE]
mapSymbol = getSymbol(imgmask, thresh, staffRow, spacing, lastX)

# In[Get Note High & Note Long]
# noteH = noteheight(mapSymbol)
# noteL = noteLength(mapSymbol)

# In[Create Music]
# addmusic(noteL, noteH)