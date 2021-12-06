from pre_processing import preprocessing
from get_axis_line import findstaff_spacing
from getSymbol import getSymbol
from noteheight import noteheight
from NotationByNN import noteLength
from addmusic import addmusic
from cv2 import imread, IMREAD_GRAYSCALE
# import os
# import time

# In[Read Image]
filename = input() # maybe use .argparse to avoid error input
img = imread(filename, IMREAD_GRAYSCALE)
h, w = img.shape  # Image Length & Width

# In[Image Preprocessing]
thresh, h, w = preprocessing(img, h, w)

# In[Staff Detection, Reference line distance & thickness]
imgmask, staffRow, spacing, lastX, mono = findstaff_spacing(thresh, h, w)

# In[GET NODE]
mapSymbol = getSymbol(imgmask, thresh, staffRow, spacing, lastX, mono)

# In[Get Note High & Note Long]

noteH = noteheight(mapSymbol)
noteL = noteLength(mapSymbol)

# In[Create Music]
addmusic(noteL, noteH)