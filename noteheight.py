import cv2
import tensorflow
import numpy as np
"""
key = 'D' # key of staff

def _changeKey(Chord):
    if Chord != '':
        global key
        key = Chord
"""
def whichnote(num, key):
    note = 100
    if(num<19):
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
    else:
        if (num ==19):
            note = 100 #垃圾
        elif (num == 20):
            note = 120 #高音譜記號
        elif (num == 21):
            note = 121 #4分休止符
        elif (num == 22):
            note = 122 #8分休止符
        elif (num == 23):
            note = 123 #全休止符
        elif (num == 26):
            note = 124 #16分止符
        elif (num == 27):
            note = 125 #2分止符

    # KEY selection
    """
    if(key == 'C'):
        return note

    if(key == 'G'):     #G大調
        if(note == 65 or note == 77):
            note = note + 1
    elif(key == 'D'):   #D大調
        if(note == 65 or note == 77 or note == 60 or note == 72 or note == 84):
            note = note + 1
    elif(key == 'D'):   #A大調
        if(note == 65 or note == 77 or note == 60 or note == 72 or note == 84 or note == 55 or note == 67 or note == 79):
            note = note + 1
    elif(key == 'E'):   #E大調
        if (note == 65 or note == 77 or note == 60 or note == 72 or note == 84 or note == 55 or note == 67 or note == 79 or note == 62 or note == 74 or note == 86):
            note = note + 1
    elif(key == 'B'):   #B大調
        if (note == 65 or note == 77 or note == 60 or note == 72 or note == 84 or note == 55 or note == 67 or note == 79 or note == 62 or note == 74 or note == 86 or note == 57 or note == 69 or note == 81):
            note = note + 1
    elif(key == 'F'):   #F大調
        if (note == 65 or note == 77 or note == 60 or note == 72 or note == 84 or note == 55 or note == 67 or note == 79 or note == 62 or note == 74 or note == 86 or note == 57 or note == 69 or note == 81 or note == 64 or note == 76):
            note = note + 1
    elif(key == 'D'):   #升C大調
        if(note < 100):
            note = note + 1
    """
    return note

def noteheight(mapsymbol):
    resize_x = 64
    resize_y = 32
    x_test = [0]
    notelist = []
    model = tensorflow.keras.models.load_model("Save_Model_note")
    img = cv2.imread("test.jpg")
    
    for num in range(len(mapsymbol)):

        y1, y2, x1, x2 = mapsymbol[num]
        #print(y1, y2, x1, x2)
        crop_img = img[y1:y2, x1:x2]
        #cv2.imwrite("what/" + str(num).zfill(5) + ".jpg", crop_img)
        x_test[0] = cv2.resize(crop_img, (resize_x, resize_y))
        x_test = np.array(x_test)
        x_Test = x_test.astype("float32") / 255.0
        num = np.argmax(model.predict(x_Test), axis=-1)# 音高模型
        #print(num)
        note = whichnote(num)
        notelist.append(int(note))
        """
        if(note<=86):
            notelist.append(note)
        """
        #for x in range(len(mapsymbol[num])):
        #    print(mapsymbol[num][x], end='')
        #    print(" ", end='')
        #print("\n")
    #print(notelist)
    return notelist
