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

BASE_FOLDER = '/home/tim/Work/Cacophony'
RUNS_FOLDER = '/Audio_Analysis/audio_classifier_runs/tensorflow_runs/' 
MODEL_RUN_NAME = "2020_08_24a"
run_sub_log_dir = "1"



def create_model(num_classes):
    # https://www.youtube.com/watch?v=x_VrgWTKkiM&list=PLQY2H8rRoyvwLbzbnKJ59NkZvQAW9wLbx&index=14
    # https://www.youtube.com/watch?v=u2TjZzNuly8&list=PLQY2H8rRoyvwLbzbnKJ59NkZvQAW9wLbx&index=15
    print("num_classes ", num_classes)
    model = keras.models.Sequential()
     
    model.add(Conv2D(64,(3, 3), padding = "same", input_shape=(32, 32, 1))) 
    model.add(Activation("relu"))
    model.add(MaxPooling2D(2,2)) 
     
    model.add(Conv2D(64,(3, 3), padding = "same"))  
    model.add(Activation("relu"))    
    model.add(MaxPooling2D(2,2)) 
     
    model.add(Conv2D(128,(3, 3), padding = "same"))  
    model.add(Activation("relu"))    
    model.add(MaxPooling2D(2,2)) 
     
    model.add(Conv2D(128,(3, 3), padding = "same"))  
    model.add(Activation("relu"))    
    model.add(MaxPooling2D(2,2)) 
     
    model.add(Flatten())
     
    model.add(Dropout(0.5))
     
    model.add(Dense(512, activation = "relu"))
     
    model.add(Dense(num_classes, activation="softmax")) 
    
   
#     
#     model.compile(optimizer=tf.keras.optimizers.Adam(1e-6), loss='sparse_categorical_crossentropy',  metrics=['accuracy'])
    model.compile(optimizer=tf.keras.optimizers.Adam(1e-6), loss='categorical_crossentropy',  metrics=['accuracy'])
#     
#     model.compile(optimizer='rmsprop', loss='sparse_categorical_crossentropy',  metrics=['accuracy'])
    return model
    
#     model.add(Conv2D(8,(3, 3), padding = "same", input_shape=(32, 32, 1)))
#     model.add(Conv2D(8,(3, 3), padding = "same"))  
#     model.add(Activation("relu"))
#     model.add(MaxPooling2D(2,2))     
#      
#     model.add(Conv2D(8,(3, 3), padding = "same"))  
#     model.add(Activation("relu"))    
#     model.add(MaxPooling2D(2,2)) 
#      
#     model.add(Conv2D(8,(3, 3), padding = "same"))  
#     model.add(Activation("relu"))    
#     model.add(MaxPooling2D(2,2))
#      
#     model.add(Conv2D(8,(3, 3), padding = "same"))  
#     model.add(Activation("relu"))    
#     model.add(MaxPooling2D(2,2))
#      
#     model.add(Flatten())
#      
#     model.add(Dense(64, activation = "relu"))
#      
#     model.add(Dense(num_classes, activation="softmax"))       
#      
#     model.compile(optimizer=tf.keras.optimizers.Adam(1e-6), loss='sparse_categorical_crossentropy',  metrics=['accuracy'])
#       
#     return model
    
#     print("num_classes ", num_classes)
#     model = keras.models.Sequential()
# #     model.add(Conv2D(4,(3, 3), padding = "same", input_shape=(32, 2584, 1))) 
#     model.add(Conv2D(4,(3, 3), padding = "same", input_shape=(32, 32, 1))) 
#     model.add(Activation("relu"))
#     model.add(MaxPooling2D(2,2))     
#      
#     model.add(Conv2D(8,(3, 3), padding = "same"))  
#     model.add(Activation("relu"))    
#     model.add(MaxPooling2D()) 
#      
#     model.add(Flatten())
#      
#     model.add(Dense(64, activation = "relu"))
#      
#     model.add(Dense(num_classes, activation="softmax"))       
#      
#     model.compile(optimizer=tf.keras.optimizers.Adam(1e-5), loss='sparse_categorical_crossentropy',  metrics=['accuracy'])
#      
#     return model

# def create_regression_model():
#     
#     model = keras.models.Sequential()
#     model.add(Conv2D(16,(3, 3), padding = "same", input_shape=(32, 2584, 1)))  
# #     model.add(Conv2D(16,(3, 3), padding = "same", input_shape=(32, 2584)))   
# #     model.add(Conv2D(16,(3, 3), padding = "same", input_shape=(2584, 32, 1)))
# #     model.add(Conv2D(16,(3, 3), padding = "same", input_shape=(None, 32, 2584)))    
#     
#     model.add(BatchNormalization())
#     model.add(Activation("relu"))
#     model.add(MaxPooling2D(2,2))     
#     
#     model.add(Conv2D(16,(3, 3), padding = "same"))    
#     model.add(BatchNormalization())      
#     model.add(Activation("relu"))    
#     model.add(Conv2D(16,(3, 3), padding = "same"))
#     model.add(BatchNormalization())    
#     model.add(Activation("relu"))
#     model.add(MaxPooling2D()) 
#     
#     model.add(Flatten())
#     
#     model.add(Dense(64, activation = "relu"))
#     model.add(Dropout(0.5))
#     model.add(Dense(1))       
#     
#     model.compile(optimizer=tf.keras.optimizers.Adam(), loss='mse',  metrics=['accuracy'])
#     
#     return model

def get_callbacks():
    
                
    tensorflow_run_folder = BASE_FOLDER + RUNS_FOLDER + MODEL_RUN_NAME
    print("tensorflow_run_folder ", tensorflow_run_folder)
    checkpoint_path = tensorflow_run_folder + "/training_1/cp.ckpt"
    
    cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)
    log_dir = "logs/fit/" + run_sub_log_dir
    tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1, profile_batch=0) 
    
    # https://machinelearningmastery.com/how-to-stop-training-deep-neural-networks-at-the-right-time-using-early-stopping/
    # es_val_loss_callback = keras.callbacks.EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=30)
    es_train_loss_callback = keras.callbacks.EarlyStopping(monitor='loss', mode='min', verbose=1, patience=30)
    
#     return [cp_callback, es_train_loss_callback,tensorboard_callback]
    return [cp_callback, es_train_loss_callback]
    
# def train_model(model, train_dataset, val_dataset):
def train_model(model, train_x, train_y, val_x, val_y, ):
    print("Training started")
    
#     model.fit(train_dataset, 
#               epochs=100, 
#               validation_data=val_dataset)
    
#     model.fit(train_dataset, 
#               epochs=100, 
#               )

    model.fit(train_x, train_y, 
              epochs=100, 
              )
    
    
#     model.fit(train_dataset, 
#               epochs=100, 
# #               callbacks=[es_callback, cp_callback, tensorboard_callback, es_train_loss_callback], 
#               callbacks=get_callbacks(),
#               validation_data=val_dataset)
    
def evaluate_model(model, test_dataset):
    model.evaluate(test_dataset)


def prepare_data_no_dataset(create_data, testing):
    # https://www.tensorflow.org/tutorials/load_data/numpy
    train_examples, val_examples, train_labels, val_labels, number_of_distinct_labels = prepare_data_v2.get_data(create_data=create_data, testing=testing) 
   
   
    return train_examples, val_examples, train_labels, val_labels, number_of_distinct_labels

# def prepare_data(create_data, testing):
#     # https://www.tensorflow.org/tutorials/load_data/numpy
#     train_examples, val_examples, train_labels, val_labels, number_of_distinct_labels = prepare_data_v2.get_data(create_data=create_data, testing=testing) 
#    
#     print("np.max(train_examples) ", np.max(train_examples))
#     print("np.min(train_examples) ", np.min(train_examples))
#     
#     
#     print("train_examples.shape ", train_examples.shape)
#     print("val_examples.shape ", val_examples.shape)
#     print("train_labels.shape ", train_labels.shape)
#     print("val_labels.shape ", val_labels.shape)
#    
#     # https://www.tensorflow.org/tutorials/load_data/numpy
#     train_dataset = tf.data.Dataset.from_tensor_slices((train_examples, train_labels))
#     for a, b in train_dataset:
#         print("a ", a.shape)
#         print("b ", b.shape)
#         break
#     
# #     train_dataset_spec = tf.data.DatasetSpec.from_value(train_dataset)
# #     print(train_dataset_spec)    
# #     for elem in train_dataset.as_numpy_iterator():
# #         print(elem)
# #         print(len(elem))
# #         print(elem[1])
#         
# 
#     val_dataset = tf.data.Dataset.from_tensor_slices((val_examples, val_labels))
#     
#     BATCH_SIZE = 100
# #     BATCH_SIZE = 8
#     SHUFFLE_BUFFER_SIZE = 1000
#      
#     train_dataset = train_dataset.shuffle(SHUFFLE_BUFFER_SIZE).batch(BATCH_SIZE, drop_remainder=True)
#     
#     for c, d in train_dataset:
#         print(c.shape)
#         print(d.shape)
#         break
#     
#     val_dataset = val_dataset.batch(BATCH_SIZE)
#     
# #     return train_dataset, val_dataset, maximum_number_of_moreporks, val_examples, val_labels
#     return train_dataset, val_dataset, number_of_distinct_labels

# def use_model(model, val_examples, val_labels):
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

    testing=True # Only has an affect if create_data is True
    
    print("Started")
        
#     train_dataset, test_dataset, maximum_number_of_moreporks, test_examples, test_labels = prepare_data(create_data, testing)  
#     train_dataset, val_dataset, number_of_distinct_labels  = prepare_data(create_data, testing) 
    
    train_examples, val_examples, train_labels, val_labels, number_of_distinct_labels = prepare_data_no_dataset(create_data, testing)
    print("train_examples shape ", train_examples.shape)
    print("train_labels shape ", train_labels.shape)
    
    
    model = create_model(number_of_distinct_labels)
   
#     model = create_regression_model()
    print(model.summary())
#     train_model(model, train_dataset, val_dataset)
    train_model(model, train_examples, train_labels, val_examples, val_labels)
#     evaluate_model(model, val_dataset)
#     
#     model_predict(model, val_dataset)

    evaluate_model(model, val_examples, val_labels)
    
    model_predict(model, val_examples, val_labels)
    

if __name__ == '__main__':
    main()