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

from sklearn.metrics import confusion_matrix

import prepare_data_v4

BASE_FOLDER = '/home/tim/Work/Cacophony'
RUNS_FOLDER = '/Audio_Analysis/audio_classifier_runs/tensorflow_runs/' 

MODELS_FOLDER = "saved_models"
SAVED_MFCCS_FOLDER = "saved_mfccs"




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



def get_callbacks(model_run_name, run_sub_log_dir):
    
                
    tensorflow_run_folder = BASE_FOLDER + RUNS_FOLDER + model_run_name
    print("tensorflow_run_folder ", tensorflow_run_folder)
    checkpoint_path = tensorflow_run_folder + "/training_1/cp.ckpt"
    
    checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,
                                                 save_weights_only=True,
                                                 save_best_only=True,
                                                 mode='auto',
                                                 verbose=1)
    
    log_dir = tensorflow_run_folder + "/logs/fit/" + run_sub_log_dir + "/"
    
    
    tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1, profile_batch=0) 
    
    # https://machinelearningmastery.com/how-to-stop-training-deep-neural-networks-at-the-right-time-using-early-stopping/
    # es_val_loss_callback = keras.callbacks.EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=30)
    earlystop_train_loss_callback = keras.callbacks.EarlyStopping(monitor='loss', mode='min', verbose=1, patience=30)
    
    
    return [checkpoint_callback, earlystop_train_loss_callback,tensorboard_callback]


def train_the_model(model_run_name, run_sub_log_dir,  model, train_x, train_y, val_x, val_y, ):
    print("Training started")
    

#     https://keras.io/api/models/model_training_apis/
    model.fit(x=train_x, y=train_y, 
              validation_data=(val_x, val_y),
              epochs=300, 
              callbacks=get_callbacks(model_run_name, run_sub_log_dir),
              )
   
    return model

def evaluate_model(model, val_examples, val_labels):
    print(model.evaluate(x=val_examples, y=val_labels))   
  
def prepare_data_no_dataset(model_run_name, saved_mfccs_location, create_data, testing, display_image):
    # https://www.tensorflow.org/tutorials/load_data/numpy
    train_examples, val_examples, train_labels, val_labels, number_of_distinct_labels, integer_to_sound_mapping = prepare_data_v4.get_data(model_run_name=model_run_name, saved_mfccs_location=saved_mfccs_location, create_data=create_data, testing=testing, display_image=display_image) 
 
    return train_examples, val_examples, train_labels, val_labels, number_of_distinct_labels, integer_to_sound_mapping


# def get_labels(unique_val_labels, sound_to_integer_mapping):
#     labels = []
#     for key, value in sound_to_integer_mapping.items():
#         labels.append(key)
#         
#     return labels
        

def plot_confusion_matrix_3(predictions_decoded, val_labels_decoded, integer_to_sound_mapping):
    predictions_decoded_np = np.array(predictions_decoded)
    val_labels_decoded_np = np.array(val_labels_decoded)
    
    unique_val_labels = np.unique(val_labels_decoded_np)
#     print(len(unique_val_labels))
    
#     lookup = create_integer_to_sound_mapping(sound_to_integer_mapping)
    labels = []
    for value in unique_val_labels:
        sound = integer_to_sound_mapping.get(value)
        labels.append(sound)        
    
    val_labels_decoded_names = []
    predictions_decoded_names = []    

#     print(labels)   
   
    for value in predictions_decoded_np:
        predictions_decoded_names.append(integer_to_sound_mapping.get(value))        
        
    for value in val_labels_decoded_np:
        val_labels_decoded_names.append(integer_to_sound_mapping.get(value))              
    
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
    
    
    
#     https://stackoverflow.com/questions/51759859/how-to-move-labels-from-bottom-to-top-without-adding-ticks
    plt.tick_params(axis='x', which='major', labelsize=10, labelbottom = False, bottom=False, top = False, labeltop=True)

    
    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-45, ha="right",
             rotation_mode="anchor")
    
    # Loop over data dimensions and create text annotations.
    for i in range(len(labels)):     
        for j in range(len(labels)):            
            text = ax.text(j, i, cm[i, j], ha="center", va="center", color="w")
    
    ax.set_title("Confusion Matrix")
    fig.tight_layout()
    # According to https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html
    # Confusion matrix whose i-th row and j-th column entry indicates the number of samples with true label being i-th class and prediced label being j-th class.
    ax.xaxis.set_label_position('top')
    plt.xlabel("Predicted") 
    plt.ylabel("Actual")
    plt.show()

def load_model(model_location):     
    model = tf.keras.models.load_model(model_location)

    # Check its architecture
    model.summary()
    return model

def main():       
    model_run_name = "2020_09_01a"
    run_sub_log_dir = "2-testing"
    model_name = "model_2"
    saved_mfccs = "version_1/"
           
    train_a_model=True # False implies it will load a trained model from disk
    save_model=True # Only applies if model is trained
    create_data=False # If True, creates mfccs from original audio files; if false loads previously saved mfccs files (created for each confirmed training onset)
    testing=False # Only has an affect if create_data is True
    
    model_location = BASE_FOLDER + RUNS_FOLDER + MODELS_FOLDER + "/" + model_name       
    print("model_location: ",model_location)
    saved_mfccs_location = BASE_FOLDER + RUNS_FOLDER + SAVED_MFCCS_FOLDER + "/" + saved_mfccs 
    print("saved_mfccs_location: ", saved_mfccs_location)  
   
    display_image = False # Only has an affect if create_data is True
    
    print("Started")        
  
    train_examples, val_examples, train_labels, val_labels, number_of_distinct_labels, sound_to_integer_mapping = prepare_data_no_dataset(model_run_name=model_run_name, saved_mfccs_location=saved_mfccs_location, create_data=create_data, testing=testing, display_image=display_image)

    
    # get one example
    one_val_example = val_examples[:1]
    print("one_val_example ", one_val_example)
    
    val_labels_decoded = tf.argmax(val_labels, 1)
    print("val_labels_decoded ", val_labels_decoded)    

    
    if train_a_model: 

        model = create_model_basic(number_of_distinct_labels)  
        print(model.summary())    
        model = train_the_model(model_run_name, run_sub_log_dir, model, train_examples, train_labels, val_examples, val_labels)
        print("This run used ", len(train_labels), " training examples")
        
        if save_model:
            #https://keras.io/guides/serialization_and_saving/
            model.save(model_location)
        
    else:
        # Load model from disk
        model = load_model(model_location)
 
    predictions = model(val_examples)
    predictions_decoded = tf.argmax(predictions, 1)   

    plot_confusion_matrix_3(predictions_decoded, val_labels_decoded, sound_to_integer_mapping)    

    print("Finished")
    

if __name__ == '__main__':
    main()