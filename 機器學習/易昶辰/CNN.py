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
from tensorflow.keras.layers import Conv2D, MaxPooling2D#, ZeroPadding2D

# In[Read Folder]
from os import listdir

path = r'data/cuts'
folder_list = listdir(path)

x_train_img = [0] * len(folder_list)
y_train_label = [0] * len(folder_list)


# In[Resize Setting]

resize_x = 64
resize_y = 32
dim = resize_x * resize_y

# In[CNN_Read Data]

for label in range(len(folder_list)):    #Read Label
    y_train_label[label] = folder_list[label][0]

for i in range(len(folder_list)):       #Read Image in and resize
    img_in = cv2.imread(path + '/' + folder_list[i])
    x_train_img[i] = cv2.resize(img_in, (resize_x, resize_y))


x_train_img = np.array(x_train_img)

x_Train = x_train_img.astype('float32') / 255.0

y_Train_OneHot =  utils.to_categorical(y_train_label)



path = r'data/tests'
folder_list = listdir(path)

x_test_img = [0] * len(folder_list)
y_test_label = [0] * len(folder_list)

for label in range(len(folder_list)):    #Read Label
    y_test_label[label] = folder_list[label][0]

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

model.add(Dense(units=int(max(y_train_label)) + 1, 
                kernel_initializer='normal', 
                activation='softmax'))

print(model.summary())

model.compile(loss='categorical_crossentropy', 
              optimizer='adam', metrics=['accuracy'])

train_history = model.fit(x=x_Train,y=y_Train_OneHot,
                         epochs=200, batch_size=10,verbose=1)#epochs=10, batch_size=200


# In[Import Model]

model.save('Save_Model')

model = tensorflow.keras.models.load_model('Save_Model')
'''
print(model.summary())

model.compile(loss='categorical_crossentropy', 
              optimizer='adam', metrics=['accuracy'])

train_history = model.fit(x=x_Train,y=y_Train_OneHot,
                         epochs=200, batch_size=10,verbose=1)#epochs=10, batch_size=200
'''

# In[CNN_Test]

scores = model.evaluate(x_Test, y_Test_OneHot)

print('accuracy=',scores[1])

prediction = np.argmax(model.predict(x_Test), axis=-1)
print('prediction=', prediction)

#print('actuallyvalue=', y_test_label)
# In[NN with cuts_auto]

from sklearn.model_selection import train_test_split

path = r'data/cuts_auto'
folder_list = listdir(path)

x_img = [0] * len(folder_list)
y_label = [0] * len(folder_list)

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
x_train_img, x_test_img = train_test_split(x_img,random_state=random_state,test_size=0.25)

y_train_label, y_test_label = train_test_split(y_label,random_state=random_state,test_size=0.25)

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
                         epochs=50, batch_size=4,verbose=0)#epochs=10, batch_size=200#100 20

scores = model.evaluate(x_test_img, y_test_label)

print('accuracy=',scores[1])

# In[HeatMap]

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

np.random.seed(0)

uniform_data = np.random.rand(2,3)

epochsTimes = [10,25,50,100,200,250,500,1000]
batchSizes = [1,2,4,8,16]

for epochs in epochsTimes:
    for batch_size in batchSizes:
        print(epochs*batch_size)




#https://cs231n.github.io/classification/

# In[KNN_Read Data]

path = r'data/cuts'
folder_list = listdir(path)

x_train_img = [0] * len(folder_list)
y_train_label = [0] * len(folder_list)

for label in range(len(folder_list)):    #Read Label
    y_train_label[label] = folder_list[label][0]
    
for i in range(len(folder_list)):        #Read Image in and resize
    img_in = cv2.imread(path + '/' + folder_list[i])
    x_train_img[i] = cv2.resize(img_in, (resize_x, resize_y))


path = r'data/tests'
folder_list = listdir(path)

x_test_img = [0] * len(folder_list)
y_test_label = [0] * len(folder_list)

for label in range(len(folder_list)):    #Read Label
    y_test_label[label] = folder_list[label][0]

for i in range(len(folder_list)):        #Read Image in and resize
    img_in = cv2.imread(path + '/' + folder_list[i])
    x_test_img[i] = cv2.resize(img_in, (resize_x, resize_y))
    
x_train_img = np.array(x_train_img)
x_test_img = np.array(x_test_img)
ytr = np.array(y_train_label)


xtr_row = x_train_img.reshape(x_train_img.shape[0], resize_x * resize_y * 3)

xte_row = x_test_img.reshape(x_test_img.shape[0], resize_x * resize_y * 3)
    
# In[KNN_FunctionsBuild]

class NearestNeighbor(object):
  def __init__(self):
    pass

  def train(self, X, y):
    """ X is N x D where each row is an example. Y is 1-dimension of size N """
    # the nearest neighbor classifier simply remembers all the training data
    self.Xtr = X
    self.ytr = y

  def predict(self, X):
    """ X is N x D where each row is an example we wish to predict label for """
    num_test = X.shape[0]
    # lets make sure that the output type matches the input type
    Ypred = np.zeros(num_test, dtype = self.ytr.dtype)

    # loop over all test rows
    for i in range(num_test):
      # find the nearest training image to the i'th test image
      # using the L1 distance (sum of absolute value differences)
      #distances = np.sum(np.abs(self.Xtr - X[i,:]), axis = 1)
      distances = np.sqrt(np.sum(np.square(self.Xtr - X[i,:]), axis = 1))
      min_index = np.argmin(distances) # get the index with smallest distance
      Ypred[i] = self.ytr[min_index] # predict the label of the nearest example

    return Ypred


# In[KNN_ModelBuild & Train]

nn = NearestNeighbor() # create a Nearest Neighbor classifier class
nn.train(xtr_row, ytr) # train the classifier on the training images and labels
Y_predict = nn.predict(xte_row) # predict labels on the test images

# and now print the classification accuracy, which is the average number
# of examples that are correctly predicted (i.e. label matches)

print('accuracy: %f' % ( np.mean(Y_predict == y_test_label) ))

# In[Useless]
'''
x_test_img_gray = [0] * 4

x_test_img_gray[0] = cv2.imread('2_test_2.png' , cv2.IMREAD_GRAYSCALE)
x_test_img_gray[0] = cv2.resize(x_test_img_gray[0], (32, 32))
x_test_img_gray[0] = np.array(x_test_img_gray[0])

x_test_img_gray[1] = cv2.imread('4_test_1.png' , cv2.IMREAD_GRAYSCALE)
x_test_img_gray[1] = cv2.resize(x_test_img_gray[1], (32, 32))
x_test_img_gray[1] = np.array(x_test_img_gray[1])

x_test_img_gray[2] = cv2.imread('4_test_3.png' , cv2.IMREAD_GRAYSCALE)
x_test_img_gray[2] = cv2.resize(x_test_img_gray[2], (32, 32))
x_test_img_gray[2] = np.array(x_test_img_gray[2])

x_test_img_gray[3] = cv2.imread('8_test_6.png' , cv2.IMREAD_GRAYSCALE)
x_test_img_gray[3] = cv2.resize(x_test_img_gray[3], (32, 32))
x_test_img_gray[3] = np.array(x_test_img_gray[3])

x_test_img_gray = np.array(x_test_img_gray)

y_test_label = ['2', '4', '4 ', '8']
y_Test_OneHot =  utils.to_categorical(y_test_label)

x_Test = x_test_img_gray.reshape(4, dim).astype('float32')
x_Test_normalize = x_Test / 255

scores = model.evaluate(x_Test_normalize, y_Test_OneHot)
print('accuracy=',scores[1])

prediction = np.argmax(model.predict(x_Test_normalize), axis=-1)
print('prediction=', prediction)
'''

