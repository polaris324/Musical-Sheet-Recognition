import mido
import numpy as np
from os import listdir
import tensorflow
from mido import Message, MidiFile, MidiTrack
import cv2

beat = 960 #四分音符長度

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