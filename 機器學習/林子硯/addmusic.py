import mido
from os import listdir
from mido import Message

def addmusic(track, timeL, note):
    num = whichnote(note)
    #num = note%126     測試用
    track.append(mido.Message("note_on", note=num, velocity=100, time=0, channel=1))
    track.append(mido.Message("note_off", note=num, velocity=100, time=timeL, channel=1))

def whichnote(num):
    note = 60
    if (num==0):
        note = 55 #G
    elif (num == 1):
        note = 57 #A
    elif (num == 2):
        note = 59 #B
    elif (num == 3):
        note = 60 #C
    elif (num == 4):
        note = 62 #D
    elif (num == 5):
        note = 64 #E
    elif (num == 6):
        note = 65 #F
    elif (num == 7):
        note = 67 #G
    elif (num == 8):
        note = 69 #A
    elif (num == 9):
        note = 71 #B
    elif (num == 10):
        note = 72 #C
    elif (num == 11):
        note = 74 #D
    elif (num == 12):
        note = 76 #E
    elif (num == 13):
        note = 77 #F
    elif (num == 14):
        note = 79 #G
    elif (num == 15):
        note = 81 #A
    elif (num == 16):
        note = 83 #B
    elif (num == 17):
        note = 84 #C
    elif (num == 18):
        note = 86 #D

    return note

path = r'notedata'
folder_list = listdir(path)

mid = mido.MidiFile()
track = mido.MidiTrack()
mid.tracks.append(track)
note = 60
for imglist in range(len(folder_list)):
    x = folder_list[imglist]
    note = 0#音高模型
    timeL = 0#音長模型
    #note = whichnote(num)  測試用
    #note = note + 2        測試用
    #timeL = 400            測試用
    addmusic(track, timeL, note)
    print(x)

mid.save("datamusic.mid")
