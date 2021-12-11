import cv2
import numpy as np
import tensorflow
# In[NN]
'''
def GetSingleNotePrediction(x_img):
    
    model = tensorflow.keras.models.load_model('Save_Model')
    
    x_img = np.array(x_img)
    
    x_img = x_img.reshape(1,2048).astype('float32')
    
    x_img = x_img.astype('float32') / 255.0
    
    prediction = np.argmax(model.predict(x_img))
    
    return prediction
'''
def noteLength(mapSymbol):
    resize_x = 64
    resize_y = 32
    
    temp = [0]
    notelist = []
    
    model = tensorflow.keras.models.load_model('Save_Model_NN')
    
    img = cv2.imread("test.jpg")
    
    for each in range (len(mapSymbol)):
        y1, y2, x1, x2 = mapSymbol[each]
        crop_img = img[y1:y2, x1:x2]
        temp[0] = cv2.resize(crop_img, (resize_x, resize_y))
        temp = np.array(temp)
        temp = temp.astype("float32") / 255.0
        length = np.argmax(model.predict(temp), axis=-1)
        notelist.append(int(length))
    # print(notelist)
    return notelist
