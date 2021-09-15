# -*- coding: utf-8 -*-
"""
Created on Tue May 11 00:23:01 2021

@author: 易昶辰
"""
import cv2
import numpy as np
import tensorflow
from tensorflow.keras import utils
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense#, Flatten
#from tensorflow.keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D

# In[Read Folder]
from os import listdir

path = r'data/cuts_auto'
folder_list = listdir(path)

x_img = [0] * len(folder_list)
y_label = [0] * len(folder_list)


# In[NN with cuts_auto]

from sklearn.model_selection import train_test_split

for label in range(len(folder_list)):    #Read Label
    y_label[label] = folder_list[label][0]
    if(folder_list[label][1] != '_'):
        y_label[label] += folder_list[label][1]

for i in range(len(folder_list)):       #Read Image in and resize
    img_in = cv2.imread(path + '/' + folder_list[i],cv2.IMREAD_GRAYSCALE)
    x_img[i] = cv2.resize(img_in, (64, 32))


x_img = np.array(x_img)

x_img = x_img.reshape(len(folder_list), 2048).astype('float32')

x_img = x_img.astype('float32') / 255.0
random_state=15
test_size=0.75
x_train_img, x_test_img = train_test_split(x_img,random_state=random_state,test_size=test_size)

y_train_label, y_test_label = train_test_split(y_label,random_state=random_state,test_size=test_size)

y_train_label =  utils.to_categorical(y_train_label)
y_test_label =  utils.to_categorical(y_test_label)

tensorflow.keras.backend.clear_session()

model = Sequential()
model.add(Dense(units=256,
                input_dim=64*32,
                kernel_initializer='normal',
                activation='relu'))

model.add(Dense(units=int(y_label[0]) + 1,
                kernel_initializer='normal',
                activation='softmax'))
print(model.summary())

model.compile(loss='categorical_crossentropy',
              optimizer='adam', metrics=['accuracy'])

train_history = model.fit(x=x_train_img,y=y_train_label,
                         epochs=150, batch_size=8,verbose=1)#epochs=10, batch_size=200#10

model = tensorflow.keras.models.load_model('Save_Model_NN') #remove this when train

scores = model.evaluate(x_test_img, y_test_label)

print('accuracy=',scores[1])


# In[Import Model]

#model.save('Save_Model_NN')

model = tensorflow.keras.models.load_model('Save_Model_NN')

