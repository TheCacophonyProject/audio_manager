'''
Created on 26 Aug. 2020
This will take the mel spectrums directly without going via pics
It will not rely on onsets, but instead look at whole recording (or sliding window)
Train in whole recordings with labels of has morepork / no morepork or maybe how many moreporks

Use this to learn how to input data into Tensorflow from numpy arrays
@author: tim
'''

import numpy as np
import datetime
import random
import sys
import os

import time
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import regularizers
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.layers import Activation



import prepare_data_v2

def create_model(num_classes):
    print("num_classes ", num_classes)
    model = keras.models.Sequential()
    model.add(Conv2D(16,(3, 3), padding = "same", input_shape=(32, 2584, 1)))  
#     model.add(Conv2D(16,(3, 3), padding = "same", input_shape=(32, 2584)))   
#     model.add(Conv2D(16,(3, 3), padding = "same", input_shape=(2584, 32, 1)))
#     model.add(Conv2D(16,(3, 3), padding = "same", input_shape=(None, 32, 2584)))    
    
    model.add(BatchNormalization())
    model.add(Activation("relu"))
    model.add(MaxPooling2D(2,2))     
    
    model.add(Conv2D(16,(3, 3), padding = "same"))    
    model.add(BatchNormalization())      
    model.add(Activation("relu"))    
    model.add(Conv2D(16,(3, 3), padding = "same"))
    model.add(BatchNormalization())    
    model.add(Activation("relu"))
    model.add(MaxPooling2D()) 
    
    model.add(Flatten())
    
    model.add(Dense(64, activation = "relu"))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation="softmax"))       
    
    model.compile(optimizer=tf.keras.optimizers.Adam(), loss='sparse_categorical_crossentropy',  metrics=['accuracy'])
    
    return model

def create_regression_model():
    
    model = keras.models.Sequential()
    model.add(Conv2D(16,(3, 3), padding = "same", input_shape=(32, 2584, 1)))  
#     model.add(Conv2D(16,(3, 3), padding = "same", input_shape=(32, 2584)))   
#     model.add(Conv2D(16,(3, 3), padding = "same", input_shape=(2584, 32, 1)))
#     model.add(Conv2D(16,(3, 3), padding = "same", input_shape=(None, 32, 2584)))    
    
    model.add(BatchNormalization())
    model.add(Activation("relu"))
    model.add(MaxPooling2D(2,2))     
    
    model.add(Conv2D(16,(3, 3), padding = "same"))    
    model.add(BatchNormalization())      
    model.add(Activation("relu"))    
    model.add(Conv2D(16,(3, 3), padding = "same"))
    model.add(BatchNormalization())    
    model.add(Activation("relu"))
    model.add(MaxPooling2D()) 
    
    model.add(Flatten())
    
    model.add(Dense(64, activation = "relu"))
    model.add(Dropout(0.5))
    model.add(Dense(1))       
    
    model.compile(optimizer=tf.keras.optimizers.Adam(), loss='mse',  metrics=['accuracy'])
    
    return model

def train_model(model, train_dataset):
    print("Training started")
    model.fit(train_dataset, epochs=10)
    
def evaluate_model(model, test_dataset):
    model.evaluate(test_dataset)
    
def prepare_data(create_data, testing):
    # https://www.tensorflow.org/tutorials/load_data/numpy
    train_examples, test_examples, train_labels, test_labels, maximum_number_of_moreporks = prepare_data_v2.get_data(create_data=create_data, testing=testing) 
    
    train_dataset = tf.data.Dataset.from_tensor_slices((train_examples, train_labels))
    test_dataset = tf.data.Dataset.from_tensor_slices((test_examples, test_labels))
    
    BATCH_SIZE = 64
    SHUFFLE_BUFFER_SIZE = 100
    
    train_dataset = train_dataset.shuffle(SHUFFLE_BUFFER_SIZE).batch(BATCH_SIZE)
    test_dataset = test_dataset.batch(BATCH_SIZE)
    
    return train_dataset, test_dataset, maximum_number_of_moreporks, test_examples, test_labels

# def use_model(model, test_examples, test_labels):
def model_predict(model, test_dataset):
#     example_batch = train_dataset[:3]
#     example_result = model.predict(example_batch)
#     print(example_result)
#     test_predictions = model.predict(test_examples, test_labels)
    test_predictions = model.predict(test_dataset)
    
    print("test_predictions")
    print(test_predictions)

    

def main():
    create_data=False
#     create_data=False
#     testing=True # Only has an affect if create_data is True
    testing=False # Only has an affect if create_data is True
    
    print("Started")
        
    train_dataset, test_dataset, maximum_number_of_moreporks, test_examples, test_labels = prepare_data(create_data, testing)    
    
    model = create_model(maximum_number_of_moreporks)
#     model = create_regression_model()
    print(model.summary())
    train_model(model, train_dataset)
    evaluate_model(model, test_dataset)
    
    model_predict(model, test_dataset)
    

if __name__ == '__main__':
    main()