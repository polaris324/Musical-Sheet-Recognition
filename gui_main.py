import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import pygame
import tkinterdnd2 as tkd # https://pythonguides.com/python-tkinter-drag-and-drop/ pip install tkinterdnd2

import findline
from five import five
from get_fiveline_rows import get_fiveline_rows
from get_rows_dist import get_rows_dist
from getSymbol import getSymbol
import noteheight
from NotationByNN import noteLength
import addmusic

def drop(event):
    var.set(event.data)

def openByFilePath():
    print("Upload")# test
    file_location = e_box.get()
    # print(file_loc)# test
    
    showImage(file_location)
    # img = Image.open(file_loc)
    # canvas = tk.Canvas(ws, width=img.width // 5, height=img.height // 5, bg='gray')
    # img = img.resize( (img.width // 5, img.height // 5) )
    # image_file =  ImageTk.PhotoImage(img)
        
    # label = tk.Label(image = image_file)
    # label.grid(column=1, row=1 , padx=10, pady=10)
    #https://stackoverflow.com/questions/66159973/display-image-when-button-is-clicked-python-gui
    
    # return

def Upload():
    path = filedialog.askopenfilename()
    global testText
    testText = path
    print(path)
    showImage(path)

def main():
    global filelocation,keys,tempo
    statusText.set('Status : Running')
    filename = testText
    
    findline._changeThersholdType(threshold.get(), thValue)
    thresh, imgmark = findline.findline(filename)
    fiveline, lastx = five(imgmark)
    
    staffRow = get_fiveline_rows(fiveline, lastx)
    staffRow_spacing, line_spacing = get_rows_dist(staffRow)
    
    mapSymbol = getSymbol(fiveline, thresh, staffRow, staffRow_spacing, lastx)
    try:
        noteheight._changeKey(keysValue.get()[0].upper())
    except IndexError:
        noteheight._changeKey('C')
    noteH = noteheight.noteheight(mapSymbol)
    noteL = noteLength(mapSymbol)
    
    addmusic._changeBeat(tempo.get())
    addmusic.addmusic(noteL, noteH)
    statusText.set('Status : Done')
    

def showImage(file_location):    
    image_width = Image.open(file_location).width
    image_height = Image.open(file_location).height
    if ( max(image_height, image_width) == image_height ):# vertical image
        resize_height = 600
        resize_width = 600/image_height*image_width
    else:# horizon image
        resize_height = 450/image_width*image_height
        resize_width = 450
    image_file = ImageTk.PhotoImage(Image.open(file_location).resize((int(resize_width), int(resize_height))))
    
    canvas.image = image_file
    canvas.create_image(225,300,anchor='center',image = image_file)
    global haveImage
    haveImage = True
    statusText.set('Status : Ready')

def showTempoValueBySelect(event):
     #print("New Element Selected")# test
     print(tempo.get())# test
     tempoText.set('Tempo of the sheet : ' + tempo.get())
     
def getTempoValue():
     #print("New Element Entered")# test
     print(tempo.get())# test
     tempoText.set('Tempo of the sheet : ' + tempo.get())
     global haveImage
     if haveImage:
         statusText.set('Status : Ready')
     #play_music(music_file)

def showThresholdValueBySelect(event):
     #print("New Element Selected")# test
     print(threshold.get())# test
     thresholdTypeText.set('Threshold type :' + threshold.get())
     if threshold.get() == " Customize":
         thresholdValue.grid()
     else:
         thresholdValue.grid_remove()
     global haveImage
     if haveImage:
         statusText.set('Status : Ready')
    

def getScaleValue(event):
    w = event.widget
     #print("New Element Selected")# test
    if isinstance(w, tk.Scale):
        print (w.get())
        global thValue
        thValue = w.get()
    global haveImage
    if haveImage:
        statusText.set('Status : Ready')
     
def getKeysValue(event):
    w = event.widget
    if isinstance(w, tk.Entry):
        print (w.get())
        keysText.set('Keys : ' + keysValue.get()[0].upper())
    global haveImage
    if haveImage:
        print(haveImage)
        statusText.set('Status : Ready')
#-----------------------------------------------------------------------------------------------


# Initial window setting
ws = tkd.Tk()
ws.title("ProjectGUI")
ws.geometry("1115x750")
#ws.iconbitmap("Downloads\icon.ico")
ws.config(bg="lightgray")

# Create Frame for Canvas
frame = tk.Frame(ws)
canvas = tk.Canvas(frame, width=450, height=600)
canvas.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

frame.grid(column=1, row=1, columnspan=3, rowspan=16)

# Drag and drop setting
var = tk.StringVar()
tk.Label(ws, text='Path of the Folder :',bg="lightgray").grid(column=0, row=0, padx=10, pady=10, sticky=tk.N)
# EnterBox
e_box = tk.Entry(ws, textvar=var, width=45)
e_box.grid(column=1, row=0 , padx=10, pady=10, sticky=tk.N)
e_box.drop_target_register(tkd.DND_FILES)
e_box.dnd_bind('<<Drop>>', drop)

# SendFilePath Button
btn_upload = tk.Button(ws, text='Send', command=openByFilePath)#https://stackoverflow.com/questions/13099908/python-tkinter-return-value-from-function-used-in-command
btn_upload.grid(column=2, row=0, padx=10, pady=5)

# Upload Button
btn_upload = tk.Button(ws, text='Upload', command=Upload)
btn_upload.grid(column=3, row=0, padx=10, pady=5)
haveImage = False

#DirectEnter/SelectBox for Speed Selection
tempoText = tk.StringVar()
tempoText.set('Tempo of the sheet :')   
tk.Label(ws, textvariable=tempoText,bg="lightgray", anchor=tk.W, width=32).grid(column=4, row=0, columnspan=3)
'''
values=["Larghissimo -20",
        "Grave 20-40",
        "Langsam 40-45",
        "Largo 40-60",
        "Larghetto 60-66",
        "Adagio 66-76",
        "Andante 76-108",
        "Mäßig 108-120",
        "Allegro 120-168",
        "Vivace 138-168",
        "Presto 168-200",
        "Prestissimo 200-"]
'''
# combo = ttk.Combobox(ws,values = values)
#combo = ttk.Combobox(ws)
tempo = tk.StringVar()
tk.Entry(ws, textvariable = tempo).grid(column=4, row=1, pady=10, columnspan=3,sticky='NWE')
# combo.bind("<<ComboboxSelected>>", showTempoValueBySelect)
#combo.grid(column=4, row=1, pady=10, columnspan=3,sticky='NWE')
tk.Button(ws, text='Set Tempo', command=getTempoValue).grid(column=7, row=1, padx=10, pady=10, sticky=tk.N)

# Bar for threshold
thresholdTypeText = tk.StringVar()
thresholdTypeText.set('Threshold type :')
tk.Label(ws, textvariable=thresholdTypeText, bg="lightgray").grid(column=4, row=2, columnspan=3, sticky=tk.W)
values=[" OTSU",
        " Customize",
        " YEN"]
threshold = tk.StringVar()
thresholdTypeCombo = ttk.Combobox(ws, value = values, textvariable=threshold)
thresholdTypeCombo.bind("<<ComboboxSelected>>", showThresholdValueBySelect)
thresholdTypeCombo.grid(column=4, row=3, columnspan=3, sticky='WES')
thValue = tk.StringVar()
thresholdValue = tk.Scale(ws, from_=0, to=255,orient='horizonta' ,tickinterval=50,length=200)
thresholdValue.grid(column=4, row=5, rowspan=3, columnspan=3, padx=10, pady=5)
thresholdValue.bind("<ButtonRelease>", getScaleValue)
thresholdValue.grid_remove()

# Keys
keysText = tk.StringVar()
keysText.set('Keys :')
tk.Label(ws, textvariable=keysText, bg="lightgray").grid(column=4, row=8, columnspan=3, sticky=tk.W)
keysValue = tk.StringVar()
keysEntry = tk.Entry(ws, textvariable = keysValue)
keysEntry.bind("<KeyRelease>", getKeysValue)
keysEntry.grid(column=4, row=9, pady=10, columnspan=3,sticky='NWE')

# Submit
statusText = tk.StringVar()
statusText.set('Status :')
tk.Label(ws, textvariable=statusText, bg="lightgray").grid(column=4, row=14, columnspan=3, sticky=tk.W)
filelocation = tk.StringVar()
Run = tk.Button(ws, text='RUN', command=main)
Run.grid(column=4, row=15, columnspan=3, padx=10, pady=5,sticky = 'we')

# Music player
pygame.mixer.init()
def play():
    pygame.mixer.music.load("datamusic.mid")
    pygame.mixer.music.play()
        
def pause():
    pygame.mixer.music.pause()

def stop():
    pygame.mixer.music.stop()
    #ws.destroy()

Play = tk.Button(ws, text = 'Play', command = play).grid(column=4, row=16, padx=10, pady=5, sticky='swe')
Pause = tk.Button(ws,text = 'Pause', command = pause).grid(column=5, row=16, padx=10, pady=5, sticky='swe')
Stop = tk.Button(ws, text="Stop", command=stop).grid(column=6, row=16, padx=10, pady=5, sticky='swe')

#Exit Button
quit_buttom = tk.Button(ws, text="Exit Program", command=ws.destroy)
quit_buttom.grid(column=7, row=17, padx=10, pady=5)

#-----------------------------------------------------------------------------------------------
# Progress bar widget
'''
progress = ttk.Progressbar(ws, orient = tk.HORIZONTAL,
              length = 100, mode = 'determinate')
  
# Function responsible for the updation
# of the progress bar value

cmd = False


def start():
    import time
    progress.start(1000)
    for per in range(100):
        progress['value'] = per
        ws.update_idletasks()
        ws.update()
        time.sleep(0.1)

def pause():
    progress.pause()

def stop():
    progress.stop()
    
    
progress.grid(column=4, row=1, columnspan=3, padx=10, pady=5,sticky='ews')

# This button will initialize
# the progress bar
tk.Button(ws, text = 'Start', command = start).grid(column=4, row=2, padx=10, pady=5, sticky='nwe')
tk.Button(ws, text = 'Pause', command = pause).grid(column=5, row=2, padx=10, pady=5, sticky='nwe')
tk.Button(ws, text = 'Stop', command = stop).grid(column=6, row=2, padx=10, pady=5, sticky='nwe')
'''
#-----------------------------------------------------------------------------------------------

ws.mainloop()