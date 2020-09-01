'''
Created on 1 Sept. 2020
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

import prepare_data_v3

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
    

#     https://keras.io/api/models/model_training_apis/
    model.fit(x=train_x, y=train_y, 
              validation_data=(val_x, val_y),
              epochs=2, 
              callbacks=get_callbacks(),
              )
    


def evaluate_model(model, val_examples, val_labels):
    print(model.evaluate(x=val_examples, y=val_labels))   
  


def prepare_data_no_dataset(create_data, testing, display_image):
    # https://www.tensorflow.org/tutorials/load_data/numpy
    train_examples, val_examples, train_labels, val_labels, number_of_distinct_labels, sound_to_integer_mapping = prepare_data_v3.get_data(create_data=create_data, testing=testing, display_image=display_image) 
   
   
    return train_examples, val_examples, train_labels, val_labels, number_of_distinct_labels, sound_to_integer_mapping


def create_integer_to_sound_mapping(sound_to_integer_mapping):

    print(sound_to_integer_mapping)
    integer_to_sound_mapping = {}
    for key, value in sound_to_integer_mapping.items():
#         print(item)
        integer_to_sound_mapping[value] = key
        
    print(integer_to_sound_mapping)
    return integer_to_sound_mapping

def get_labels(unique_val_labels, sound_to_integer_mapping):
    labels = []
    for key, value in sound_to_integer_mapping.items():
        labels.append(key)
        
    return labels

# def plot_confusion_matrix(predictions_decoded, val_labels_decoded, sound_to_integer_mapping):
#     print(type(val_labels_decoded))
#     from sklearn.metrics import confusion_matrix
#     integer_to_sound_mapping = create_integer_to_sound_mapping(sound_to_integer_mapping)
#     
#     # Very probably single line to do all this!
#     predictions_decoded_np = np.array(predictions_decoded)
#     predictions_decoded_list = []
#     for value in predictions_decoded_np:
#         print(value)
#         sound = integer_to_sound_mapping.get(value)
#         print("sound is ", sound)
#         predictions_decoded_list.append(sound)
#     predictions_decoded_list_tensor = tf.convert_to_tensor(predictions_decoded_list)
#     
#     val_labels_decoded_np = np.array(val_labels_decoded)
#     val_labels_decoded_list = []
#     for value in val_labels_decoded_np:
#         print(value)
#         sound = integer_to_sound_mapping.get(value)
#         print("sound is ", sound)
#         val_labels_decoded_list.append(sound)
#     val_labels_decoded_list_tensor = tf.convert_to_tensor(val_labels_decoded_list)
# 
# #     cm = tf.math.confusion_matrix(val_labels_decoded, predictions_decoded)
#     cm = tf.math.confusion_matrix(val_labels_decoded_list, predictions_decoded_list)
# #     cm = tf.math.confusion_matrix(val_labels_decoded_list_tensor, predictions_decoded_list_tensor)
#     print("cm ")
#     print(cm)
#     
#     plt.matshow(cm)
# 
#     plt.show()

# def plot_confusion_matrix_2(predictions_decoded, val_labels_decoded, sound_to_integer_mapping):
#     predictions_decoded_np = np.array(predictions_decoded)
#     val_labels_decoded_np = np.array(val_labels_decoded)
#     val_labels_decoded_names = []
#     predictions_decoded_names = []
#     
#     labels = get_labels(sound_to_integer_mapping)
#     print(labels)
#    
#     from sklearn.metrics import confusion_matrix
#     integer_to_sound_mapping = create_integer_to_sound_mapping(sound_to_integer_mapping)    
#     
#     for value in predictions_decoded_np:
#         val_labels_decoded_names.append(integer_to_sound_mapping.get(value))
#         
#     for value in val_labels_decoded_np:
#         predictions_decoded_names.append(integer_to_sound_mapping.get(value))
#         
# #     print(val_labels_decoded_names)
#     
#     
#     cm = confusion_matrix(val_labels_decoded_names, predictions_decoded_names)
#     
#     # https://stackoverflow.com/questions/3529666/matplotlib-matshow-labels
#     # https://matplotlib.org/gallery/images_contours_and_fields/image_annotated_heatmap.html#sphx-glr-gallery-images-contours-and-fields-image-annotated-heatmap-py
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
# #     cax = ax.matshow(cm, interpolation='nearest')
#     cax = ax.matshow(cm)
#     fig.colorbar(cax)
#     
#     ax.set_xticks(np.arange(len(labels)))
# #     ax.set_xticklabels(['']+labels, rotation='vertical')
#     ax.set_xticklabels(labels, rotation='vertical') # https://stackoverflow.com/questions/1221108/barchart-with-vertical-labels-in-python-matplotlib#:~:text=In%20general%2C%20to%20show%20any,the%20keyword%20rotation%3D'vertical'%20.&text=Maybe%20you%20can%20also%20find,ticks%20or%20the%20other%20elements.
#     
#     ax.set_yticks(np.arange(len(labels)))
# #     ax.set_yticklabels(['']+labels)
#     ax.set_yticklabels(labels)
#     
#     plt.show()
#     
#     
# #     print("cm ")
# #     print(cm)    
# #     plt.matshow(cm)  
# #     plt.show()
          
def plot_confusion_matrix_3(predictions_decoded, val_labels_decoded, sound_to_integer_mapping):
    predictions_decoded_np = np.array(predictions_decoded)
    val_labels_decoded_np = np.array(val_labels_decoded)
    
    unique_val_labels = np.unique(val_labels_decoded_np)
    print(len(unique_val_labels))
    
    lookup = create_integer_to_sound_mapping(sound_to_integer_mapping)
    labels = []
    for value in unique_val_labels:
        sound = lookup.get(value)
        labels.append(sound)
        
    
    val_labels_decoded_names = []
    predictions_decoded_names = []
    
#     labels = get_labels(unique_val_labels, sound_to_integer_mapping)
    print(labels)
   
    from sklearn.metrics import confusion_matrix
    integer_to_sound_mapping = create_integer_to_sound_mapping(sound_to_integer_mapping)    
    
    for value in predictions_decoded_np:
        predictions_decoded_names.append(integer_to_sound_mapping.get(value))
        
        
    for value in val_labels_decoded_np:
        val_labels_decoded_names.append(integer_to_sound_mapping.get(value))
        
        
#     print(val_labels_decoded_names)
    
    
    cm = confusion_matrix(val_labels_decoded_names, predictions_decoded_names)
    # https://matplotlib.org/3.1.1/gallery/images_contours_and_fields/image_annotated_heatmap.html
    fig, ax = plt.subplots()
    im = ax.imshow(cm)
    
    # We want to show all ticks...
    ax.set_xticks(np.arange(len(labels)))
    ax.set_yticks(np.arange(len(labels)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)
    
    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    
    # Loop over data dimensions and create text annotations.
    for i in range(len(labels)): 
#     loop_size = len(labels) - 1
#     for i in range(loop_size):        
        for j in range(len(labels)): 
#         for j in range(20):           
            text = ax.text(j, i, cm[i, j], ha="center", va="center", color="w")
    
    ax.set_title("Confusion Matrix")
    fig.tight_layout()
    plt.show()


def main():
    create_data=False

    testing=False # Only has an affect if create_data is True
    
    display_image = False # Only has an affect if create_data is True
    
    print("Started")
        
  
    train_examples, val_examples, train_labels, val_labels, number_of_distinct_labels, sound_to_integer_mapping = prepare_data_no_dataset(create_data=create_data, testing=testing, display_image=display_image)
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

    model = create_model_basic(number_of_distinct_labels)   

    print(model.summary())

    train_model(model, train_examples, train_labels, val_examples, val_labels)

    print("val_examples shape is ", val_examples.shape)
    print("val_examples ndim is ", val_examples.ndim)
    print("val_examples size is ", val_examples.size)    
 
    predictions = model(val_examples)
    predictions_decoded = tf.argmax(predictions, 1)   

    plot_confusion_matrix_3(predictions_decoded, val_labels_decoded, sound_to_integer_mapping)    

    print("This run used ", len(train_labels), " training examples")
    

if __name__ == '__main__':
    main()