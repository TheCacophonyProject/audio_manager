'''
Created on 15 Sep. 2020

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



from sklearn.metrics import confusion_matrix

import prepare_data_v18

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

def create_keras_builtin_model(keras_model_name, binary, number_of_distinct_labels, IMG_SIZE):
#     IMG_SIZE=32
    IMG_SHAPE = (IMG_SIZE, IMG_SIZE, 3)
    
    if keras_model_name == "InceptionResNetV2":
        builtin_model = tf.keras.applications.InceptionResNetV2(
        include_top=False, 
        weights='imagenet', 
        input_shape=IMG_SHAPE) 
        
        builtin_model.trainable=False # https://androidkt.com/how-to-use-vgg-model-in-tensorflow-keras/
        
    elif keras_model_name == "Xception":
        builtin_model=tf.keras.applications.Xception(input_shape=IMG_SHAPE,
                                               include_top=False,
                                               weights='imagenet', 
                                               )
        builtin_model.trainable=False # https://androidkt.com/how-to-use-vgg-model-in-tensorflow-keras/
        
    elif keras_model_name == "VGG16":
        builtin_model=tf.keras.applications.VGG16(input_shape=IMG_SHAPE,
                                               include_top=False,
                                               weights='imagenet',
                                               )
        builtin_model.trainable=False # https://androidkt.com/how-to-use-vgg-model-in-tensorflow-keras/
        
    elif keras_model_name == "VGG19":
        builtin_model=tf.keras.applications.VGG19(input_shape=IMG_SHAPE,
                                               include_top=False,
                                               weights='imagenet',
                                               )
        builtin_model.trainable=False # https://androidkt.com/how-to-use-vgg-model-in-tensorflow-keras/
            
    elif keras_model_name == "ResNet50":
        builtin_model=tf.keras.applications.ResNet50(input_shape=IMG_SHAPE,
                                               include_top=False,
                                               weights='imagenet',
                                               )
        builtin_model.trainable=False # https://androidkt.com/how-to-use-vgg-model-in-tensorflow-keras/
        
    elif keras_model_name == "ResNet101":
        builtin_model=tf.keras.applications.ResNet101(input_shape=IMG_SHAPE,
                                               include_top=False,
                                               weights='imagenet',
                                               )
        builtin_model.trainable=False # https://androidkt.com/how-to-use-vgg-model-in-tensorflow-keras/
        
    elif keras_model_name == "ResNet152":
        builtin_model=tf.keras.applications.ResNet152(input_shape=IMG_SHAPE,
                                               include_top=False,
                                               weights='imagenet',
                                               )
        builtin_model.trainable=False # https://androidkt.com/how-to-use-vgg-model-in-tensorflow-keras/
        
    elif keras_model_name == "ResNet50V2":
        builtin_model=tf.keras.applications.ResNet50V2(input_shape=IMG_SHAPE,
                                               include_top=False,
                                               weights='imagenet',
                                               )
        builtin_model.trainable=False # https://androidkt.com/how-to-use-vgg-model-in-tensorflow-keras/
        
    elif keras_model_name == "ResNet101V2":
        builtin_model=tf.keras.applications.ResNet101V2(input_shape=IMG_SHAPE,
                                               include_top=False,
                                               weights='imagenet',
                                               )
        builtin_model.trainable=False # https://androidkt.com/how-to-use-vgg-model-in-tensorflow-keras/
        
    elif keras_model_name == "ResNet152V2":
        builtin_model=tf.keras.applications.ResNet152V2(input_shape=IMG_SHAPE,
                                               include_top=False,
                                               weights='imagenet',
                                               )
        builtin_model.trainable=False # https://androidkt.com/how-to-use-vgg-model-in-tensorflow-keras/
        
    elif keras_model_name == "NASNetLarge":
        builtin_model=tf.keras.applications.NASNetLarge(input_shape=IMG_SHAPE,
                                               include_top=False,
                                               weights=None, # Can't use imagenet as docs say input images need to be 331, 331, 3)
                                               )
    
        
    
    else:
        print("No matching model found")
        return                    
    
    global_average_layer = tf.keras.layers.GlobalAveragePooling2D() # It looks like I wasn't using this for InceptionResNetV2 - will need to check
       
    if binary:
        prediction_layer = tf.keras.layers.Dense(units=1, activation="sigmoid")          
    else:
        prediction_layer = tf.keras.layers.Dense(number_of_distinct_labels,activation='softmax')

    model = Sequential([
        builtin_model,
        global_average_layer,
        prediction_layer
        ])
    
    opt = Adam(lr=0.001)

    if binary:      
        model.compile(optimizer=opt, loss='binary_crossentropy', metrics=['accuracy'])   
    else:    
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
    earlystop_train_loss_callback = keras.callbacks.EarlyStopping(monitor='loss', mode='min', verbose=1, patience=100)      
    
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
  
def prepare_data(binary, model_name, saved_mfccs_location, create_data, testing, display_image):
    # https://www.tensorflow.org/tutorials/load_data/numpy    
    train_examples, val_examples, train_labels, val_labels, number_of_distinct_labels, integer_to_sound_mapping, class_count = prepare_data_v18.get_data(binary=binary, saved_mfccs_location=saved_mfccs_location, create_data=create_data, testing=testing, display_image=display_image, keras_model_name=model_name) 
    
    # save integer to sound mapping - so can use it later in another program eg. when this model is used to do predictions
    if binary:
        binary_model_folder = BASE_FOLDER + RUNS_FOLDER + MODELS_FOLDER + "/binary/" + model_name + "/"
        Path(binary_model_folder).mkdir(parents=True, exist_ok=True) 
        mapping_file_path_name = binary_model_folder + "integer_to_sound_mapping.pkl"
    else:
        multi_class_model_folder = BASE_FOLDER + RUNS_FOLDER + MODELS_FOLDER + "/multi_class/" + model_name + "/"
        Path(multi_class_model_folder).mkdir(parents=True, exist_ok=True) 
        mapping_file_path_name =  multi_class_model_folder + "integer_to_sound_mapping.pkl"
        
    print(integer_to_sound_mapping)
    # https://pythonspot.com/save-a-dictionary-to-a-file/
    f = open(mapping_file_path_name,"wb")
    pickle.dump(integer_to_sound_mapping,f)
    f.close()
    
   
    return train_examples, val_examples, train_labels, val_labels, number_of_distinct_labels, integer_to_sound_mapping, class_count

def plot_confusion_matrix_3(binary, predictions_decoded, val_labels_decoded, integer_to_sound_mapping):
    # I struggled to get the correct labels for plotting the confusion matrix - if not all possible labels
    # occur in the data to be plotted - so did a big rigmarole to get the unique labels from a union
    # of predictions and actual values.
    print("About to plot confusion matrix")
#     print("type(predictions_decoded) ", type(predictions_decoded))
    predictions_decoded_np = np.array(predictions_decoded)    
#     print("type(predictions_decoded_np) ", type(predictions_decoded_np))
    predictions_decoded_list = predictions_decoded_np.tolist()
#     print("predictions_decoded_list ", predictions_decoded_list)
    
        
    val_labels_decoded_np = np.array(val_labels_decoded)
    val_labels_decoded_list = val_labels_decoded_np.tolist()
#     print("val_labels_decoded_list ", val_labels_decoded_list)
    
    concatenated_lists = predictions_decoded_list + val_labels_decoded_list
#     print("concatenated_lists ", concatenated_lists)
    
    concatenated_lists_unique = np.unique(np.array(concatenated_lists))
    
#     print("concatenated_lists_unique ", concatenated_lists_unique)
    
    
#     unique_predictions = np.unique(predictions_decoded_np) 
#     print("unique_predictions ", unique_predictions)
#     print(type(unique_predictions))
#     unique_val_labels = np.unique(val_labels_decoded_np)
#     print("unique_val_labels ", unique_val_labels)
#     
#     merged_unique_labels = np.concatenate([unique_predictions,unique_val_labels])
#     
#     print(merged_unique_labels)
       
#     labels = []
#   
#     for value in integer_to_sound_mapping:
#         sound = integer_to_sound_mapping.get(value)
#         labels.append(sound)    
        
    val_labels_decoded_names = []
    predictions_decoded_names = []  
   
    for value in predictions_decoded_np:
        predictions_decoded_names.append(integer_to_sound_mapping.get(value))        
         
    for value in val_labels_decoded_np:
        val_labels_decoded_names.append(integer_to_sound_mapping.get(value))              
     
#     cm = confusion_matrix(val_labels_decoded_names, predictions_decoded_names)
    cm = confusion_matrix(val_labels_decoded_names, predictions_decoded_names)
    
    
 
    print(cm)
#     print("len(cm) ", len(cm))
#     print("cm.shape ", cm.shape)
#     print("cm[0].shape[0] ", cm[0].shape[0])
#     print("cm.ndim ", cm.ndim)
#     print("len(predictions_decoded_names) ", len(predictions_decoded_names))
#     print("len(val_labels_decoded_names) ", len(val_labels_decoded_names))
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

def get_image_size(keras_model_name):
    # this needs to be updated manually when I create new data_images / sizes
    if keras_model_name == "Xception":
        return 128
        
    elif keras_model_name == "VGG16" or keras_model_name == "VGG19":
        return 128
    
    elif keras_model_name == "ResNet50" or keras_model_name == "ResNet101" or keras_model_name == "ResNet152":
        return 128
        
    elif keras_model_name == "ResNet50V2"  or keras_model_name == "ResNet101V2" or keras_model_name == "ResNet152V2":
        return 128 
        
    elif keras_model_name == "InceptionV3":
        return 128
            
    elif keras_model_name == "InceptionResNetV2":
        return 128
        
    elif keras_model_name == "NASNetLarge":
        return 128  
   
    else:    
        return 128
    

def main():   
#     keras_model_name = "my_model" 
    keras_model_name = "Xception"      

#     keras_model_name = "InceptionResNetV2" # Input size must be at least 75x75
#     keras_model_name = "NASNetLarge"
#     keras_model_name = "ResNet152"
#     keras_model_name = "VGG16"
#     keras_model_name = "image_format_0-255_3-channel" # Input size must be at least 75x75
    
#     run_sub_log_dir_multi_class = keras_model_name + "_4 " + "_multi_class"
#     run_sub_log_dir_binary = keras_model_name + "_4" + "_binary"
    
    model_run_name = "2020_09_17_" + keras_model_name + "_v2"    
#     model_name = "NASNetLarge"
    saved_mfccs = "version_3/"    
           
    binary=True       
    
#     convert_images_to_rgb = True # Needed for off-the-shelf Keras models such as VGG and ResNet    
               
    train_a_model=False # False implies it will load a trained model from disk
    load_model_from_checkpoints = True # If train_a_model is False, and this is True, model will load from check_point, otherwise from a saved_model
    save_model=True # Only applies if model is trained
    create_data=False # If True, creates mfccs from original audio files; if false loads previously saved mfccs files (created for each confirmed training onset)
    testing=False # Only has an affect if create_data is True
#     number_of_training_epochs = 1000
    number_of_training_epochs = 5
    
#     number_of_val_examples_for_confusion_matrix = 500
    
    if binary:
        model_location = BASE_FOLDER + RUNS_FOLDER + MODELS_FOLDER + "/binary/" + keras_model_name 
        checkpoint_path = BASE_FOLDER + RUNS_FOLDER + model_run_name + "/checkpoints/binary/training/cp.ckpt" 
        log_dir = BASE_FOLDER + RUNS_FOLDER + model_run_name + "/logs/fit/" + keras_model_name + "_binary/"            
    else:
        model_location = BASE_FOLDER + RUNS_FOLDER + MODELS_FOLDER + "/multi_class/" + keras_model_name   
        checkpoint_path = BASE_FOLDER + RUNS_FOLDER + model_run_name + "/checkpoints/multi_class/training/cp.ckpt"  
        log_dir = BASE_FOLDER + RUNS_FOLDER + model_run_name + "/logs/fit/" + keras_model_name + "_multi_class/"   
              
             
    print("model_location: ",model_location)
#     saved_mfccs_location = BASE_FOLDER + RUNS_FOLDER + SAVED_MFCCS_FOLDER + "/" + saved_mfccs + keras_model_name + "/"
    saved_mfccs_location = BASE_FOLDER + RUNS_FOLDER + SAVED_MFCCS_FOLDER + "/" + saved_mfccs  
    print("saved_mfccs_location: ", saved_mfccs_location)  
   
    display_image = False # Only has an affect if create_data is True
    
    print("Started") 
  
    train_examples, val_examples, train_labels, val_labels, number_of_distinct_labels, sound_to_integer_mapping, class_count = prepare_data(binary=binary, model_name=keras_model_name, saved_mfccs_location=saved_mfccs_location, create_data=create_data, testing=testing, display_image=display_image)
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
            
    model = create_keras_builtin_model(keras_model_name, binary, number_of_distinct_labels, get_image_size(keras_model_name))
    print(model.summary()) 
    
     
    if train_a_model: 
                
#         model = create_keras_builtin_model(keras_model_name, binary, number_of_distinct_labels, get_image_size(keras_model_name))
        
#         print(model.summary()) 
        
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
        
#     print("About to make predictions")
#     print("val_examples.shape ", val_examples.shape)   
#   
#     one_val_example = val_examples[:number_of_val_examples_for_confusion_matrix,:,:,:]
#     predictions = model.predict(val_examples)
#     predictions = model.predict(val_examples[:number_of_val_examples_for_confusion_matrix,:,:,:])
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
         
#         plot_confusion_matrix_3(binary, predictions_np_flattened_int, val_labels[:number_of_val_examples_for_confusion_matrix], sound_to_integer_mapping)
        plot_confusion_matrix_3(binary, predictions_np_flattened_int, val_labels, sound_to_integer_mapping)
  
    else: 
        predictions_decoded = tf.argmax(predictions, 1) 
         
#         plot_confusion_matrix_3(binary, predictions_decoded, val_labels_decoded[:number_of_val_examples_for_confusion_matrix], sound_to_integer_mapping)
        plot_confusion_matrix_3(binary, predictions_decoded, val_labels_decoded, sound_to_integer_mapping)

        # Evaluate the model on the test data using `evaluate`
#     print("Evaluate on test data")
#     results = model.evaluate(val_examples, val_labels, batch_size=128)
#     print("test loss, test acc:", results)
    
    # Generate predictions (probabilities -- the output of the last layer)
    # on new data using `predict`
#     print("Generate predictions for 3 samples")
#     predictions = model.predict(x_test[:3])
#     print("predictions shape:", predictions.shape)     
#     predictions = model.predict(val_examples[:number_of_val_examples_for_confusion_matrix,:,:,:])
#     print(predictions)
        
    print(model.summary())

    print("Finished")
    

if __name__ == '__main__':
    main()
