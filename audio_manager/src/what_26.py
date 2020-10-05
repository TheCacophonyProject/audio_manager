
'''
Created on 29 Sep. 2020

@author: tim
'''


import parameters
import numpy as np
import datetime
import random
import sys
import os
import pickle
from pathlib import Path

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
from tensorflow.keras.layers import SpatialDropout2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import MaxPool2D
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Concatenate
from tensorflow.keras.layers.experimental import preprocessing
from tensorflow.keras import layers


from sklearn.metrics import confusion_matrix

import prepare_data_v26
# from builtins import True

# BASE_FOLDER = '/home/tim/Work/Cacophony'
BASE_FOLDER = parameters.base_folder
RUNS_FOLDER = '/Audio_Analysis/audio_classifier_runs/tensorflow_runs/' 

MODELS_FOLDER = "saved_models"
SAVED_MFCCS_FOLDER = "saved_mfccs"


def get_metrics():
    # https://www.tensorflow.org/tutorials/structured_data/imbalanced_data
    METRICS = [
      keras.metrics.TruePositives(name='tp'),
      keras.metrics.FalsePositives(name='fp'),
      keras.metrics.TrueNegatives(name='tn'),
      keras.metrics.FalseNegatives(name='fn'), 
      keras.metrics.BinaryAccuracy(name='accuracy'),
      keras.metrics.Precision(name='precision'),
      keras.metrics.Recall(name='recall'),
      keras.metrics.AUC(name='auc'),
      ]
    return METRICS

def create_model_basic(binary, num_classes):       
    
    model = Sequential()
    model.add(Conv2D(16, (3, 3), padding = "same", kernel_regularizer=regularizers.l2(0.0001), activation='relu', input_shape=(32, 32, 1)))
    model.add(MaxPooling2D(2,2))  
    model.add(SpatialDropout2D(0.8))           
    
    model.add(Conv2D(16, (3, 3), padding = "same", kernel_regularizer=regularizers.l2(0.0001), activation='relu'))          
    model.add(MaxPooling2D(2,2))
    model.add(SpatialDropout2D(0.2))
    
    model.add(Conv2D(16, (3, 3), padding = "same", kernel_regularizer=regularizers.l2(0.0001), activation='relu'))            
    model.add(MaxPooling2D(2,2))
    model.add(SpatialDropout2D(0.2))
    
    model.add(Conv2D(16, (3, 3), padding = "same", kernel_regularizer=regularizers.l2(0.0001), activation='relu'))            
    model.add(MaxPooling2D(2,2))
    model.add(SpatialDropout2D(0.2))
    
    model.add(Conv2D(32, (3, 3), padding = "same", kernel_regularizer=regularizers.l2(0.0001), activation='relu'))            
    model.add(MaxPooling2D(2,2))
    model.add(SpatialDropout2D(0.2))
            
    model.add(Flatten())    
    
    model.add(Dense(64, activation='relu'))  
    
    if binary:
        model.add(Dense(1, activation="sigmoid"))
        model.compile(optimizer=tf.keras.optimizers.Adam(1e-3), loss='binary_crossentropy',  metrics=['accuracy'])
    else:
        model.add(Dense(num_classes, activation="softmax"))
        model.compile(optimizer=tf.keras.optimizers.Adam(1e-3), loss='categorical_crossentropy',  metrics=['accuracy'])       
    
        
    return model

def create_functional_model_basic(binary, num_classes):
    # https://keras.io/guides/functional_api/
#  https://keras.io/guides/preprocessing_layers/
    input_shape = (32, 32, 1)
    inputs = keras.Input(shape=input_shape)
    
#     x = keras.Input(shape=input_shape)
   # x = preprocessing.Rescaling(1.0 / 255)(x) # I think this was breaking it - so now reshape before
    
    conv2d = Conv2D(64, (3, 3), padding = "same", kernel_regularizer=regularizers.l2(0.0001), activation='relu')
    x = conv2d(inputs)
    x = MaxPooling2D(2,2)(x) 
    x = SpatialDropout2D(0.8)(x)           
    
    x = Conv2D(32, (3, 3), padding = "same", kernel_regularizer=regularizers.l2(0.0001), activation='relu')(x)          
    x = MaxPooling2D(2,2)(x)
    x = SpatialDropout2D(0.2)(x)
    
    x = Conv2D(64, (3, 3), padding = "same", kernel_regularizer=regularizers.l2(0.0001), activation='relu')(x)            
    x = MaxPooling2D(2,2)(x)
    x = SpatialDropout2D(0.2)(x)
    
    x = Conv2D(128, (3, 3), padding = "same", kernel_regularizer=regularizers.l2(0.0001), activation='relu')(x)            
    x = MaxPooling2D(2,2)(x)
    x = SpatialDropout2D(0.2)(x)
    
    x = Conv2D(256, (3, 3), padding = "same", kernel_regularizer=regularizers.l2(0.0001), activation='relu')(x)            
    x = MaxPooling2D(2,2)(x)
    x = SpatialDropout2D(0.2)(x)
                
    x = Flatten()(x)    
    
    x = Dense(64, activation='relu')(x)  
    
    if binary:
        outputs = Dense(1, activation="sigmoid")(x) 
        model = keras.Model(inputs, outputs, name="functional_model_basic")
        model.compile(optimizer=tf.keras.optimizers.Adam(1e-3), loss='binary_crossentropy',  metrics=['accuracy'])
    else:
        outputs = Dense(num_classes, activation="softmax")(x) 
        model = keras.Model(inputs, outputs, name="functional_model_basic")
        model.compile(optimizer=tf.keras.optimizers.Adam(1e-3), loss='categorical_crossentropy',  metrics=['accuracy'])  
        
    return model    

def create_model_vgg16(binary, num_classes):
    
    # build the VGG16 network with ImageNet weights
    # https://towardsdatascience.com/step-by-step-vgg16-implementation-in-keras-for-beginners-a833c686ae6c
    model = Sequential()
    
    # vgg16 layer 1
#     model.add(Conv2D(input_shape=(224,224,3),filters=64,kernel_size=(3,3),padding="same", activation="relu"))
    model.add(Conv2D(input_shape=(32,32,1),filters=64,kernel_size=(3,3),padding="same", activation="relu"))
    
    # vgg16 layer 2
    model.add(Conv2D(filters=64,kernel_size=(3,3),padding="same", activation="relu"))
    model.add(MaxPool2D(pool_size=(2,2),strides=(2,2)))
    
    # vgg16 layer 3
    model.add(Conv2D(filters=128, kernel_size=(3,3), padding="same", activation="relu"))
    
    # vgg16 layer 4
    model.add(Conv2D(filters=128, kernel_size=(3,3), padding="same", activation="relu"))
    model.add(MaxPool2D(pool_size=(2,2),strides=(2,2)))
    
    # vgg16 layer 5
    model.add(Conv2D(filters=256, kernel_size=(3,3), padding="same", activation="relu"))
    
    # vgg16 layer 6
    model.add(Conv2D(filters=256, kernel_size=(3,3), padding="same", activation="relu"))
    
    # vgg16 layer 7
    model.add(Conv2D(filters=256, kernel_size=(3,3), padding="same", activation="relu"))
    model.add(MaxPool2D(pool_size=(2,2),strides=(2,2)))
    
    # vgg16 layer 8
    model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
    
    # vgg16 layer 9
    model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
     
    # vgg16 layer 10
    model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
    model.add(MaxPool2D(pool_size=(2,2),strides=(2,2)))
     
    # vgg16 layer 11
    model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
     
    # vgg16 layer 12
    model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
     
    # vgg16 layer 13
    model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
    model.add(MaxPool2D(pool_size=(2,2),strides=(2,2)))
     
    model.add(Flatten())
    
    
    # vgg16 layer 14
    model.add(Dense(units=4096,activation="relu"))
     
    # vgg16 layer 15
    model.add(Dense(units=4096,activation="relu"))

#     model.add(Dense(64, activation='relu'))
    
#     opt = Adam(lr=0.001)
    opt = Adam(lr=0.0001)

    if binary:
        model.add(Dense(units=1, activation="sigmoid"))
#         model.compile(optimizer=opt, loss=keras.losses.categorical_crossentropy, metrics=['accuracy'])
        model.compile(optimizer=opt, loss='binary_crossentropy', metrics=['accuracy'])
       
    
    else:
        model.add(Dense(units=num_classes, activation="softmax"))
#         model.compile(optimizer=opt, loss=keras.losses.categorical_crossentropy, metrics=['accuracy'])
        model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
       
    return model
    

def get_callbacks(checkpoint_path, log_dir):
    
                
#     tensorflow_run_folder = BASE_FOLDER + RUNS_FOLDER + model_run_name
#     print("tensorflow_run_folder ", tensorflow_run_folder)
#     checkpoint_path = tensorflow_run_folder + "/training_1/cp.ckpt"
    
    checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,
                                                 save_weights_only=True,
                                                 save_best_only=True,
                                                 mode='auto',
                                                 verbose=1)
    
#     log_dir = tensorflow_run_folder + "/logs/fit/" + run_sub_log_dir + "/"
    
    
    tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1, profile_batch=0) 
    
    # https://machinelearningmastery.com/how-to-stop-training-deep-neural-networks-at-the-right-time-using-early-stopping/
    # es_val_loss_callback = keras.callbacks.EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=30)
#     earlystop_train_loss_callback = keras.callbacks.EarlyStopping(monitor='loss', mode='min', verbose=1, patience=30)
    earlystop_train_loss_callback = keras.callbacks.EarlyStopping(monitor='loss', mode='min', verbose=1, patience=10)      
    
    return [checkpoint_callback, earlystop_train_loss_callback,tensorboard_callback]
#     return [earlystop_train_loss_callback,tensorboard_callback]


def train_the_model(model, train_x, train_y, val_x, val_y, number_of_training_epochs, checkpoint_path, log_dir):
    print("Training started")
    

#     https://keras.io/api/models/model_training_apis/
    model.fit(x=train_x, y=train_y, 
              validation_data=(val_x, val_y),
              epochs=number_of_training_epochs, 
              batch_size=32,
              callbacks=get_callbacks(checkpoint_path, log_dir),
              )
   
    return model

def evaluate_model(model, val_examples, val_labels):
    print(model.evaluate(x=val_examples, y=val_labels))   
  
def prepare_data(binary, model_name, saved_mfccs_location, create_data, testing, display_image, testing_number, use_augmented_time_freq_data, create_augmented_time_freq_data, create_augmented_noise_data, use_augmented_noise_data):
    # https://www.tensorflow.org/tutorials/load_data/numpy    
    train_examples, val_examples, train_labels, val_labels, number_of_distinct_labels, integer_to_sound_mapping, class_count = prepare_data_v26.get_data(binary=binary, saved_mfccs_location=saved_mfccs_location, create_data=create_data, testing=testing, display_image=display_image, testing_number=testing_number, use_augmented_time_freq_data=use_augmented_time_freq_data, create_augmented_time_freq_data=create_augmented_time_freq_data, create_augmented_noise_data=create_augmented_noise_data, use_augmented_noise_data=use_augmented_noise_data) 
    
    # save integer to sound mapping - so can use it later in another program eg. when this model is used to do predictions
    if binary:
        binary_model_folder = BASE_FOLDER + RUNS_FOLDER + MODELS_FOLDER + "/binary/" + model_name + "/"
        Path(binary_model_folder).mkdir(parents=True, exist_ok=True) 
#         mapping_file_path_name = binary_model_folder + "integer_to_sound_mapping.pkl"
    else:
        multi_class_model_folder = BASE_FOLDER + RUNS_FOLDER + MODELS_FOLDER + "/multi_class/" + model_name + "/"
        Path(multi_class_model_folder).mkdir(parents=True, exist_ok=True) 
#         mapping_file_path_name =  multi_class_model_folder + "integer_to_sound_mapping.pkl"
        
    print(integer_to_sound_mapping)
    # https://pythonspot.com/save-a-dictionary-to-a-file/
#     f = open(mapping_file_path_name,"wb")
#     pickle.dump(integer_to_sound_mapping,f)
#     f.close()
    
   
    return train_examples, val_examples, train_labels, val_labels, number_of_distinct_labels, integer_to_sound_mapping, class_count

def plot_confusion_matrix_3(binary, predictions_decoded, val_labels_decoded, integer_to_sound_mapping):
    # I struggled to get the correct labels for plotting the confusion matrix - if not all possible labels
    # occur in the data to be plotted - so did a big rigmarole to get the unique labels from a union
    # of predictions and actual values.
    print("About to plot confusion matrix")

    predictions_decoded_np = np.array(predictions_decoded)    
    predictions_decoded_list = predictions_decoded_np.tolist()

    val_labels_decoded_np = np.array(val_labels_decoded)
    val_labels_decoded_list = val_labels_decoded_np.tolist()
    
    concatenated_lists = predictions_decoded_list + val_labels_decoded_list
    
    concatenated_lists_unique = np.unique(np.array(concatenated_lists))    

        
    val_labels_decoded_names = []
    predictions_decoded_names = []  
   
    for value in predictions_decoded_np:
        predictions_decoded_names.append(integer_to_sound_mapping.get(value))        
         
    for value in val_labels_decoded_np:
        val_labels_decoded_names.append(integer_to_sound_mapping.get(value))              
     
#     cm = confusion_matrix(val_labels_decoded_names, predictions_decoded_names)
    cm = confusion_matrix(val_labels_decoded_names, predictions_decoded_names)
    
    
 
    print(cm)

    # https://matplotlib.org/3.1.1/gallery/images_contours_and_fields/image_annotated_heatmap.html
    fig, ax = plt.subplots()
    im = ax.imshow(cm)
    
    
    labels = []
#   
    for value in concatenated_lists_unique:
        sound = integer_to_sound_mapping.get(value)
        labels.append(sound)  
    
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
#     number_of_rows_columns_in_cm = cm.n_labels
    for i in range(len(cm)):     
        for j in range(len(cm)):            
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
#     https://keras.io/api/applications/densenet/#densenet121-function
    model_name = "vgg16_lr0.0004" 

    model_run_name = "2020_10_01_" + model_name + "_1"  # Set image input to 32x32 
    
    saved_mfccs = "version_8_with_separate_noise_files_255x255_unit/"    
           
    binary=True    
                       
    train_a_model=False # False implies it will load a trained model from disk
    load_model_from_checkpoints = True # If train_a_model is False, and this is True, model will load from check_point, otherwise from a saved_model
    save_model=True # Only applies if model is trained
    create_data=False # If True, creates mfccs from original audio files; if false loads previously saved mfccs files (created for each confirmed training onset)
    testing=False # Only has an affect if create_data is True
    testing_number = 100 # Only has an affect if create_data is True
    create_augmented_time_freq_data = False # Only has an effect if use_augmented_data = True: Then if create_augmented_time_freq_data = True, creates and saves augmented data from the loaded original mfccs, or if create_augmented_time_freq_data = False, it will attempt to load saved augmented data
    use_augmented_time_freq_data = True
    create_augmented_noise_data=False
    use_augmented_noise_data=True   
    number_of_training_epochs = 100
    
    display_image = False # Only has an affect if create_data is True
    
#     if builtin_model_trainable:
    if binary:
        model_location = BASE_FOLDER + RUNS_FOLDER + MODELS_FOLDER + "/binary_trainable/" + model_name 
        checkpoint_path = BASE_FOLDER + RUNS_FOLDER + model_run_name + "/checkpoints/binary_trainable/training/cp.ckpt" 
        log_dir = BASE_FOLDER + RUNS_FOLDER + model_run_name + "/logs/fit/" + model_name + "_binary_trainable/"            
    else:
        model_location = BASE_FOLDER + RUNS_FOLDER + MODELS_FOLDER + "/multi_class_trainable/" + model_name   
        checkpoint_path = BASE_FOLDER + RUNS_FOLDER + model_run_name + "/checkpoints/multi_class_trainable/training/cp.ckpt"  
        log_dir = BASE_FOLDER + RUNS_FOLDER + model_run_name + "/logs/fit/" + model_name + "_multi_class_trainable/"   
            
#     else:        
#         if binary:
#             model_location = BASE_FOLDER + RUNS_FOLDER + MODELS_FOLDER + "/binary_not_trainable/" + model_name 
#             checkpoint_path = BASE_FOLDER + RUNS_FOLDER + model_run_name + "/checkpoints/binary_not_trainable/training/cp.ckpt" 
#             log_dir = BASE_FOLDER + RUNS_FOLDER + model_run_name + "/logs/fit/" + model_name + "_binary_not_trainable/"            
#         else:
#             model_location = BASE_FOLDER + RUNS_FOLDER + MODELS_FOLDER + "/multi_class_not_trainable/" + model_name   
#             checkpoint_path = BASE_FOLDER + RUNS_FOLDER + model_run_name + "/checkpoints/multi_class_not_trainable/training/cp.ckpt"  
#             log_dir = BASE_FOLDER + RUNS_FOLDER + model_run_name + "/logs/fit/" + model_name + "_multi_class_not_trainable/"   
              
             
    print("model_location: ",model_location)
    saved_mfccs_location = BASE_FOLDER + RUNS_FOLDER + SAVED_MFCCS_FOLDER + "/" + saved_mfccs  
    print("saved_mfccs_location: ", saved_mfccs_location)  
       
    print("Started") 
  
    train_examples, val_examples, train_labels, val_labels, number_of_distinct_labels, sound_to_integer_mapping, class_count = prepare_data(binary=binary, model_name=model_name, saved_mfccs_location=saved_mfccs_location, create_data=create_data, testing=testing, display_image=display_image, testing_number=testing_number, use_augmented_time_freq_data=use_augmented_time_freq_data, create_augmented_time_freq_data=create_augmented_time_freq_data, create_augmented_noise_data=create_augmented_noise_data, use_augmented_noise_data=use_augmented_noise_data)
    print("train_examples.shape ", train_examples.shape) 
    print("val_examples.shape ", val_examples.shape)  
    print("train_labels.shape ", train_labels.shape)  
    print("val_labels.shape ", val_labels.shape)    
    # get one example
    one_val_example = val_examples[:1,:,:,:]
    print("one_val_example ", one_val_example)
     
    if binary:   
        print("val_labels.shape ", val_labels.shape)    
        print("one val_labels ", val_labels[:100])  
    else:
        val_labels_decoded = tf.argmax(val_labels, 1) # Returns the index with the largest value across axes of a tensor. - https://www.tensorflow.org/api_docs/python/tf/math/argmax
        print("val_labels", val_labels)
            
#     model = create_model_basic(binary, number_of_distinct_labels)
    model = create_model_vgg16(binary, number_of_distinct_labels)
#     model = create_functional_model_basic(binary, number_of_distinct_labels)
    
    
    
    print(model.summary()) 
    
     
    if train_a_model: 
                        
        if binary:
            model = train_the_model(model, train_examples, train_labels, val_examples, val_labels, number_of_training_epochs, checkpoint_path, log_dir)
        else:
            model = train_the_model(model, train_examples, train_labels, val_examples, val_labels, number_of_training_epochs, checkpoint_path, log_dir)           
        
        print("This run used ", len(train_labels), " training examples")
        
        if save_model:
            #https://keras.io/guides/serialization_and_saving/
            model.save(model_location)
        
    else:  # https://www.tensorflow.org/tutorials/keras/save_and_load
        if load_model_from_checkpoints:
            model.load_weights(checkpoint_path)            
        else:
            # Load model from fully saved model
            model = load_model(model_location)
        

    predictions = model.predict(val_examples)
    print(predictions)
   
    print(class_count)
       
    if binary:
        # Sorry about the following mess - just trying to get an array of integers in the correct format
        # for giving to the confusion matrix
        #  - must be a simpler way
        rounded_predictions = tf.round(predictions)
        proto_tensor = tf.make_tensor_proto(rounded_predictions)
        predictions_np = tf.make_ndarray(proto_tensor)
        predictions_np_flattened = predictions_np.reshape(-1)
        predictions_np_flattened_int = predictions_np_flattened.astype(int)
        # end of the mess         

        plot_confusion_matrix_3(binary, predictions_np_flattened_int, val_labels, sound_to_integer_mapping)
  
    else: 
        predictions_decoded = tf.argmax(predictions, 1)          

        plot_confusion_matrix_3(binary, predictions_decoded, val_labels_decoded, sound_to_integer_mapping)

               
    print(model.summary())

    print("Finished")
    

if __name__ == '__main__':
    main()
