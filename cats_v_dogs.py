# -*- coding: utf-8 -*-
"""Cats_V_Dogs.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VxHLAtCUj55QTumMjmxIMPQJSjWcM21z
"""

from google.colab import files
files.upload() #upload kaggle.json

!pip install -q kaggle
!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!ls ~/.kaggle
!chmod 600 /root/.kaggle/kaggle.json

!kaggle datasets download -d tongpython/cat-and-dog

!unzip /content/cat-and-dog.zip

import tensorflow as tf
from tensorflow.keras.layers import Conv2D, Dense, MaxPooling2D, Dropout, BatchNormalization, Flatten
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   rotation_range = 40,
                                   width_shift_range = 0.2,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   fill_mode = 'nearest'
                                   )
train_generator =train_datagen.flow_from_directory ('/content/training_set/training_set',
    target_size=(300,300), batch_size = 128,class_mode= 'categorical',shuffle = True)

test_datagen = ImageDataGenerator(rescale = 1./255)
test_generator = test_datagen.flow_from_directory(
    '/content/test_set/test_set',
    target_size = (300,300),batch_size =128, class_mode = 'categorical',shuffle=True
)

model = Sequential()
model.add(Conv2D(32,3, input_shape =(300,300,3), kernel_initializer='he_normal', padding='same', activation = 'relu' ))
model.add(MaxPooling2D(2,2))
model.add(BatchNormalization(axis = -1))
model.add(Dropout(0.25))

model.add(Conv2D(64,4, kernel_initializer = 'he_normal', padding= 'same', activation = 'relu'))
model.add(BatchNormalization(axis =-1))
model.add(MaxPooling2D(2,2))
model.add(Dropout(0.25))

model.add(Conv2D(64,4, kernel_initializer = 'he_normal', padding= 'same', activation = 'relu'))
model.add(BatchNormalization(axis =-1))
model.add(MaxPooling2D(2,2))
model.add(Dropout(0.25))

model.add(Conv2D(128,4, kernel_initializer = 'he_normal', padding= 'same', activation = 'relu'))
model.add(BatchNormalization(axis =-1))
model.add(MaxPooling2D(2,2))
model.add(Dropout(0.25))

model.add(Conv2D(256,4, kernel_initializer = 'he_normal', padding= 'same', activation = 'relu'))
model.add(BatchNormalization(axis =-1))
model.add(MaxPooling2D(2,2))
model.add(Dropout(0.25))


model.add(Flatten())
model.add(Dense(512 , activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))
model.add(Dense(256, activation='relu'))
model.add(Dense(2, activation='softmax'))

model.compile(loss = 'categorical_crossentropy', metrics=['accuracy'], optimizer= tf.keras.optimizers.Adam())

model.fit(train_generator, validation_data=test_generator,epochs=30, steps_per_epoch=len(train_generator))

from google.colab import drive
drive.mount('/content/drive')

model.save('/content/drive/My Drive/Cats_v_Dogs')

from google.colab import files
files.upload()

import cv2
import numpy as np
img = cv2.imread('/content/download.jpeg')
img = cv2.resize(img,(300,300))
img = np.reshape(img,[-1,300,300,3])
img= img/255.0

prediction = (np.argmax(model.predict(img)))
if prediction == 1:
  print('DOG')
else:
  print('CAT')