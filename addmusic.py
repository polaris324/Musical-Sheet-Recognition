import mido
import numpy as np
from os import listdir
import tensorflow
from mido import Message, MidiFile, MidiTrack
import cv2

beat = 960 #四分音符長度
key = 'C' # key of staff
def _changeKey(Chord):
    if Chord != '':
        global key
        key = Chord

def whichkey(note):
    if(key == 'C' or key== 'a'):
        return note
    elif(key == 'G' or key== 'e'):     #G大調
        if(note == 65 or note == 77):
            note = note + 1
    elif(key == 'D' or key== 'b'):   #D大調
        if(note == 65 or note == 77 or note == 60 or note == 72 or note == 84):
            note = note + 1
    elif(key == 'A' or key== '#f'):   #A大調
        if(note == 65 or note == 77 or note == 60 or note == 72 or note == 84 or note == 55 or note == 67 or note == 79):
            note = note + 1
    elif(key == 'E' or key== '#c'):   #E大調
        if (note == 65 or note == 77 or note == 60 or note == 72 or note == 84 or note == 55 or note == 67 or note == 79 or note == 62 or note == 74 or note == 86):
            note = note + 1
    elif(key == 'B' or key== '#g'):   #B大調
        if (note == 65 or note == 77 or note == 60 or note == 72 or note == 84 or note == 55 or note == 67 or note == 79 or note == 62 or note == 74 or note == 86 or note == 57 or note == 69 or note == 81):
            note = note + 1
    elif(key == '#F' or key== 'd'):   #F大調
        if (note == 65 or note == 77 or note == 60 or note == 72 or note == 84 or note == 55 or note == 67 or note == 79 or note == 62 or note == 74 or note == 86 or note == 57 or note == 69 or note == 81 or note == 64 or note == 76):
            note = note + 1
    elif(key == '#C' or key== '#a'):   #升C大調
        if(note < 100):
            note = note + 1
    elif(key == 'F'):
        if(note == 59 or note == 71 or note == 83):
            note = note - 1
    """
    elif(key == 'B'):
        if(note == 59 or note == 71 or note == 83 or note == 64 or note == 76):
            note = note - 1
    elif(key == ''):
        if(note == 59 or note == 71 or note == 83 or note == 64 or note == 76):
            note = note - 1
    """

    return note
def _changeBeat(beatNum):
    if beatNum != '':
        global beat
        beat = int(beatNum)

def howLong(Long): #設定音長值
    global beat
    
    if(Long == 4):
        return beat
    elif(Long == 8):
        return int(beat / 2)
    elif(Long == 16):
        return int(beat / 4)
    elif(Long == 2):
        return beat * 2
    elif(Long == 1):
        return beat * 4
    else:
        return 0
        

def addmusic(timeL, noteArr):
    mid = MidiFile()

    # Track
    track = MidiTrack()
    mid.tracks.append(track)

    #num = note%126     測試用
    for loop in range(len(noteArr)):
        if(noteArr[loop]<100): #有音符
            time = howLong(timeL[loop])
            whichkey(noteArr[loop])
            track.append(mido.Message("note_on", note=noteArr[loop], velocity=100, time=0, channel=1))
            track.append(mido.Message("note_off", note=noteArr[loop], velocity=100, time=time, channel=1))
    
        elif(noteArr[loop] == 121): #4分休止符
            time = beat
            track.append(mido.Message("note_on", note=60, velocity=0, time=0, channel=1))
            track.append(mido.Message("note_off", note=60, velocity=0, time=time, channel=1))
        elif (noteArr[loop] == 122): #8分休止符
            time = int(beat/2)
            track.append(mido.Message("note_on", note=60, velocity=0, time=0, channel=1))
            track.append(mido.Message("note_off", note=60, velocity=0, time=time, channel=1))
        elif (noteArr[loop] == 123): #全休止符
            time = beat*4
            track.append(mido.Message("note_on", note=60, velocity=0, time=0, channel=1))
            track.append(mido.Message("note_off", note=60, velocity=0, time=time, channel=1))
        elif (noteArr[loop] == 124): #16分休止符
            time = int(beat/4)
            track.append(mido.Message("note_on", note=60, velocity=0, time=0, channel=1))
            track.append(mido.Message("note_off", note=60, velocity=0, time=time, channel=1))
        elif (noteArr[loop] == 125): #2分休止符
            time = beat*2
            track.append(mido.Message("note_on", note=60, velocity=0, time=0, channel=1))
            track.append(mido.Message("note_off", note=60, velocity=0, time=time, channel=1))

    mid.save("datamusic.mid")

def add(track, timeL, noteArr):

    mid = MidiFile()

    #Track
    track = MidiTrack()
    mid.tracks.append(track)

    # Array input here
    notelist_H = [60, 62, 64, 65, 67, 120]
    notelist_L = [16, 8, 4, 0, 4, 0]

    addmusic(track, notelist_L, notelist_H)

    mid.save("datamusic.mid")