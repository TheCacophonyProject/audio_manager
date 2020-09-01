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

import io
import itertools
import sklearn.metrics
from datetime import datetime
# from tensorflow.summary import create_file_writer

import prepare_data_v2

BASE_FOLDER = '/home/tim/Work/Cacophony'
RUNS_FOLDER = '/Audio_Analysis/audio_classifier_runs/tensorflow_runs/' 
MODEL_RUN_NAME = "2020_09_01a"
run_sub_log_dir = "4-testing"


def create_model_basic(num_classes):
    # 8-DO(0.8-0.2-0.2-0.2-0.2) 
    model = Sequential()
    model.add(Conv2D(16, (3, 3), padding = "same", kernel_regularizer=regularizers.l2(0.0001), activation='relu', input_shape=(32, 32, 1)))
    model.add(Dropout(0.8))
    model.add(MaxPooling2D(2,2))             
    
    model.add(Conv2D(16, (3, 3), padding = "same", kernel_regularizer=regularizers.l2(0.0001), activation='relu'))            
    model.add(Dropout(0.2))
    model.add(MaxPooling2D(2,2))
    
    model.add(Conv2D(16, (3, 3), padding = "same", kernel_regularizer=regularizers.l2(0.0001), activation='relu'))            
    model.add(Dropout(0.2))
    model.add(MaxPooling2D(2,2))
    
    model.add(Conv2D(16, (3, 3), padding = "same", kernel_regularizer=regularizers.l2(0.0001), activation='relu'))            
    model.add(Dropout(0.2))
    model.add(MaxPooling2D(2,2))
    
    model.add(Conv2D(16, (3, 3), padding = "same", kernel_regularizer=regularizers.l2(0.0001), activation='relu'))            
    model.add(Dropout(0.2))
    model.add(MaxPooling2D(2,2))
        
    model.add(Flatten())    
    
    model.add(Dense(64, activation='relu'))    
    
    model.add(Dense(num_classes, activation="softmax")) 
    
    model.compile(optimizer=tf.keras.optimizers.Adam(1e-3), loss='categorical_crossentropy',  metrics=['accuracy'])
    
    return model



def get_callbacks():
    
                
    tensorflow_run_folder = BASE_FOLDER + RUNS_FOLDER + MODEL_RUN_NAME
    print("tensorflow_run_folder ", tensorflow_run_folder)
    checkpoint_path = tensorflow_run_folder + "/training_1/cp.ckpt"
    
    checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)
    
    log_dir = tensorflow_run_folder + "/logs/fit/" + run_sub_log_dir + "/"
    
    
    tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1, profile_batch=0) 
    
    # https://machinelearningmastery.com/how-to-stop-training-deep-neural-networks-at-the-right-time-using-early-stopping/
    # es_val_loss_callback = keras.callbacks.EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=30)
    earlystop_train_loss_callback = keras.callbacks.EarlyStopping(monitor='loss', mode='min', verbose=1, patience=30)
    
    
    
    return [checkpoint_callback, earlystop_train_loss_callback,tensorboard_callback]

    
# def train_model(model, train_dataset, val_dataset):
def train_model(model, train_x, train_y, val_x, val_y, ):
    print("Training started")
    
#     model.fit(train_dataset, 
#               epochs=100, 
#               validation_data=val_dataset)
    
#     model.fit(train_dataset, 
#               epochs=100, 
#               )

#     model.fit(train_x, train_y, 
#               epochs=100, 
#               )
#     https://keras.io/api/models/model_training_apis/
    model.fit(x=train_x, y=train_y, 
              validation_data=(val_x, val_y),
              epochs=100, 
              callbacks=get_callbacks(),
              )
    
#     model.fit(train_dataset, 
#               epochs=100, 
# #               callbacks=[es_callback, cp_callback, tensorboard_callback, es_train_loss_callback], 
#               callbacks=get_callbacks(),
#               validation_data=val_dataset)
    
# def evaluate_model(model, test_dataset):
#     model.evaluate(test_dataset)

def evaluate_model(model, val_examples, val_labels):
    print(model.evaluate(x=val_examples, y=val_labels))
    
    


def prepare_data_no_dataset(create_data, testing, display_image):
    # https://www.tensorflow.org/tutorials/load_data/numpy
    train_examples, val_examples, train_labels, val_labels, number_of_distinct_labels = prepare_data_v2.get_data(create_data=create_data, testing=testing, display_image=display_image) 
   
   
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
# def model_predict(model, test_dataset):
def plot_confusion_matrix(predictions_decoded, val_labels_decoded):
    from sklearn.metrics import confusion_matrix
   
#     cm = confusion_matrix(val_examples, val_predictions)
    cm = tf.math.confusion_matrix(val_labels_decoded, predictions_decoded)
    print("cm ")
    print(cm)
    
    plt.matshow(cm)
#             plt.title(actual_confirmed)
    plt.show()
          



      

def main():
    create_data=False

    testing=False # Only has an affect if create_data is True
    
    display_image = False # Only has an affect if create_data is True
    
    print("Started")
        
#     train_dataset, test_dataset, maximum_number_of_moreporks, test_examples, test_labels = prepare_data(create_data, testing)  
#     train_dataset, val_dataset, number_of_distinct_labels  = prepare_data(create_data, testing) 
    
    train_examples, val_examples, train_labels, val_labels, number_of_distinct_labels = prepare_data_no_dataset(create_data=create_data, testing=testing, display_image=display_image)
    print("train_examples shape ", train_examples.shape)
    print("train_labels shape ", train_labels.shape)    
    print("This run used ", len(train_labels), " training examples")
    
    print("val_examples shape is ", val_examples.shape)
    print("val_examples ndim is ", val_examples.ndim)
    print("val_examples size is ", val_examples.size)
    
    # get one example
    one_val_example = val_examples[:1]
    print("one_val_example ", one_val_example)
    
    val_labels_decoded = tf.argmax(val_labels, 1)
    print("val_labels_decoded ", val_labels_decoded)
    
    
    
#     model = create_model(number_of_distinct_labels)
    model = create_model_basic(number_of_distinct_labels)
   
#     model = create_regression_model()
    print(model.summary())
#     train_model(model, train_dataset, val_dataset)
    train_model(model, train_examples, train_labels, val_examples, val_labels)
#     evaluate_model(model, val_dataset)

    print("val_examples shape is ", val_examples.shape)
    print("val_examples ndim is ", val_examples.ndim)
    print("val_examples size is ", val_examples.size)
    
    # get one example
#     one_val_example = val_examples[:1]
#     print("one_val_example ", one_val_example)
#     
#     one_prediction = model.predict(one_val_example)
#     print("one_prediction ", one_prediction)
#     prediction_index_with_largest_value = tf.argmax(one_prediction, 1)
#     print("index_with_largest_value ", index_with_largest_value)
#     
    predictions = model(val_examples)
    predictions_decoded = tf.argmax(predictions, 1)
    
    
#     val_predictions = model(val_examples)
#     print(val_predictions)

    plot_confusion_matrix(predictions_decoded, val_labels_decoded)
    
#     model_predict(model, val_examples)
    
   
    
    print("This run used ", len(train_labels), " training examples")
    

if __name__ == '__main__':
    main()