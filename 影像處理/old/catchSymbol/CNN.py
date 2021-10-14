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
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D

# In[Read Folder]
from os import listdir

path = r'data/cuts'
folder_list = listdir(path)

x_train_img = [0] * len(folder_list)
y_train_label = [0] * len(folder_list)
#print(folder_list)

# In[Resize Setting]

resize_x = 64
resize_y = 32
dim = resize_x * resize_y

# In[CNN_Read Data]

for label in range(len(folder_list)):    #Read Label
    if(folder_list[label][1] == '_'):
        y_train_label[label] = folder_list[label][0]
    elif(folder_list[label][1] != '_'):
        y_train_label[label] = folder_list[label][0] + folder_list[label][1]
    #print(y_train_label[label])

print(y_train_label[20])

for i in range(len(folder_list)):       #Read Image in and resize
    img_in = cv2.imread(path + '/' + folder_list[i])
    x_train_img[i] = cv2.resize(img_in, (resize_x, resize_y))


x_train_img = np.array(x_train_img)

x_Train = x_train_img.astype('float32') / 255.0

y_Train_OneHot = utils.to_categorical(y_train_label)


path = r'data/tests'
folder_list = listdir(path)

x_test_img = [0] * len(folder_list)
y_test_label = [0] * len(folder_list)

for label in range(len(folder_list)):    #Read Label
    if (folder_list[label][1] == '_'):
        y_test_label[label] = folder_list[label][0]
    elif (folder_list[label][1] != '_'):
        y_test_label[label] = folder_list[label][0] + folder_list[label][1]


for i in range(len(folder_list)):       #Read Image in and resize
    img_in = cv2.imread(path + '/' + folder_list[i])
    x_test_img[i] = cv2.resize(img_in, (resize_x, resize_y))
    
x_test_img = np.array(x_test_img)

x_Test = x_test_img.astype("float32") / 255.0

y_Test_OneHot =  utils.to_categorical(y_test_label)

# In[CNN_ModelBuild & Train]
tensorflow.keras.backend.clear_session()

model = Sequential()

model.add(Conv2D(filters=32,kernel_size=(3, 3),
                 input_shape=(32, 64, 3),
                 activation='relu', 
                 padding='same'))
model.add(MaxPooling2D(pool_size=(3, 3)))

model.add(Conv2D(filters=64, kernel_size=(3, 3),
                 activation='relu',
                 padding='same'))
model.add(MaxPooling2D(pool_size=(3, 3)))

model.add(Flatten())

model.add(Dense(units=256,
                input_dim=dim,
                kernel_initializer='normal', 
                activation='relu'))

model.add(Flatten())
"""
print("////////////////////")
print(y_train_label)
print(y_train_label[7])
"""
model.add(Dense(units=19,
                kernel_initializer='normal',
                activation='softmax'))

print(model.summary())

model.compile(loss='categorical_crossentropy', 
              optimizer='adam', metrics=['accuracy'])


train_history = model.fit(x=x_Train,y=y_Train_OneHot,
                         epochs=300, batch_size=15,verbose=1)#epochs=10, batch_size=200


# In[Import Model]

model.save('Save_Model')

model = tensorflow.keras.models.load_model('Save_Model')


# In[CNN_Test]

scores = model.evaluate(x_Test, y_Test_OneHot)

print('accuracy=',scores[1])

prediction = np.argmax(model.predict(x_Test), axis=-1)
print('prediction=', prediction)
print('actuallyvalue=', y_test_label)
# In[]

