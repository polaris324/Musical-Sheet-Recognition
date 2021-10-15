import cv2
import tensorflow
import numpy as np

def whichnote(num):
    note = 60
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
            note = 100 #高音譜記號
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
        #note = whichnote(num)
        notelist.append(int(num))
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
