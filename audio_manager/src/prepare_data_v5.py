'''
Created on 4 Sep. 2020

@author: tim
'''

import functions
import parameters
import librosa
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.utils import to_categorical 


BASE_FOLDER = '/home/tim/Work/Cacophony'
# MODEL_RUN_NAME = "2020_09_02a"
RUNS_FOLDER = '/Audio_Analysis/audio_classifier_runs/tensorflow_runs/' 

 
def create_integer_to_sound_mapping(sound_to_integer_mapping):

    print(sound_to_integer_mapping)
    integer_to_sound_mapping = {}
    for key, value in sound_to_integer_mapping.items():
#         print(item)
        integer_to_sound_mapping[value] = key
        
    print(integer_to_sound_mapping)
    return integer_to_sound_mapping


def group_non_morepork(array_of_labels_strings_all_classes):
    array_of_labels_strings_binary_classes = []
    for label in array_of_labels_strings_all_classes:
        if label != "morepork_more-pork":
            label = "other"
        array_of_labels_strings_binary_classes.append(label)
        
    return array_of_labels_strings_binary_classes

def encode_labels(sounds, binary):
    # https://www.educative.io/edpresso/how-to-perform-one-hot-encoding-using-keras
    
    if binary:
        sounds = group_non_morepork(sounds)
    
    total_sounds = np.unique(sounds)
    print("len(total_sounds) ", len(sounds))

    # map each sound to an integer
    sound_to_integer_mapping = {}
    for x in range(len(total_sounds)):
        sound_to_integer_mapping[total_sounds[x]] = x
    
    # integer representation
    for x in range(len(sounds)):
        sounds[x] = sound_to_integer_mapping[sounds[x]]
    
    if binary:
        sounds = np.array(sounds)
        sounds = sounds.astype(np.float)
    else:                
        sounds = to_categorical(sounds)  # one hot encoded
    
    integer_to_sound_mapping = create_integer_to_sound_mapping(sound_to_integer_mapping)
#     return one_hot_encode, mapping
    return sounds, integer_to_sound_mapping            

def get_onsets_stored_locally_for_recording_id(version_to_use, recording_id):
    cur = functions.get_database_connection().cursor()    
    cur.execute("SELECT start_time_seconds, duration_seconds, actual_confirmed FROM onsets WHERE version = ? AND recording_id = ? ORDER BY recording_id", (version_to_use, recording_id)) 
    rows = cur.fetchall()
    return rows

def get_filtered_recording_for_onset(recording_id, start_time):
    recordings_folder_with_path = parameters.base_folder + '/' + parameters.downloaded_recordings_folder
    filename = str(recording_id) + ".m4a"
    audio_in_path = recordings_folder_with_path + "/" + filename

    y, sr = librosa.load(audio_in_path, sr=22050, mono=True, offset=start_time, duration=0.7314) # chosen to give a square with the 32 mels
        
    y_filtered = functions.butter_bandpass_filter(y, parameters.morepork_min_freq, parameters.morepork_max_freq, sr)    
    
    return y_filtered, sr

def load_onset_audio(recording_id, start_time):
   
  
    y, sr = get_filtered_recording_for_onset(recording_id, start_time)
    mfccs = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=32, fmin=700,fmax=1000, hop_length=512) # https://librosa.org/doc/latest/generated/librosa.feature.melspectrogram.html
    
    max_value = np.max(mfccs)    

    mfccs_normalized = mfccs / max_value
    
    # As we are going to use a Conv2d layer in the model, it expects 3 dimensions, so need to expand
#     https://machinelearningmastery.com/a-gentle-introduction-to-channels-first-and-channels-last-image-formats-for-deep-learning/

    mfccs_normalized = np.expand_dims(mfccs_normalized, axis=2)    
    print("mfccs_normalized.shape ", mfccs_normalized.shape)
   
#     if mfccs_normalized.shape[1] < 2584:   # need to change this to ? 
    if mfccs_normalized.shape[1] < 32:   # need to change this to ? 

        return None # just throw it away
       
    else:
        return mfccs_normalized  


def get_all_training_onset_data(testing, display_image):
    
#     version_to_use = 5
#     cur = functions.get_database_connection().cursor()    
#     cur.execute("select recording_id, start_time_seconds, actual_confirmed FROM onsets WHERE version = ? AND actual_confirmed IS NOT NULL ORDER BY recording_id", (version_to_use, )) 
#     onsets = cur.fetchall()
    
    cur = functions.get_database_connection().cursor()    
    cur.execute("select recording_id, start_time_seconds, actual_confirmed FROM training_data ORDER BY recording_id") 
    onsets = cur.fetchall()
    
    number_of_onsets = len(onsets)
    if testing:
        number_of_onsets = 100
    
    # https://stackoverflow.com/questions/53135673/how-to-use-numpy-dstack-in-a-loop
    array_of_mfccs = []
    array_of_labels = []

    count = 0
    for onset in onsets:
        count+=1
        print("Processing ", count, " of ", number_of_onsets)
        recording_id = onset[0]
        start_time = onset[1]
        actual_confirmed = onset[2]
        
        if actual_confirmed == 'maybe_morepork_more-pork' or actual_confirmed == 'morepork_more-pork_part':
            continue # won't use them for training          
                
        mfccs = load_onset_audio(recording_id, start_time)
        if mfccs is not None:

            array_of_mfccs.append(mfccs)
            array_of_labels.append(actual_confirmed)
              
        if testing:
            if count >= number_of_onsets:
                break
                    
        if display_image:
            result = mfccs[:, :, 0]
            print(result.shape)

            plt.matshow(result)
            plt.title(actual_confirmed)
            plt.show()
           
 
    result_mfccs = np.stack(array_of_mfccs, axis=0)
    result_labels = np.stack(array_of_labels, axis=0)
    
    print("result_mfccs shape is ", result_mfccs.shape)
    print("result_labels shape is ", result_labels.shape)
          
    return result_mfccs, result_labels


   
def get_data(binary, saved_mfccs_location, create_data, testing, display_image):
    Path(saved_mfccs_location).mkdir(parents=True, exist_ok=True)
    
    array_of_mfccs_filename = saved_mfccs_location + 'array_of_mfccs' 
    array_of_labels_filename = saved_mfccs_location + 'array_of_labels'
           
    if create_data:
        array_of_mfccs, array_of_labels = get_all_training_onset_data(testing=testing, display_image=display_image)    
        np.save(array_of_mfccs_filename, array_of_mfccs)
        np.save(array_of_labels_filename, array_of_labels)
        
    else:
        # read from previously saved data
        array_of_mfccs = np.load(array_of_mfccs_filename + ".npy")
        array_of_labels = np.load(array_of_labels_filename + ".npy")
        
    number_of_distinct_labels = len(np.unique(array_of_labels))
    
    if binary:
        number_of_distinct_labels = 2
     
#     print("number_of_distinct_labels ", number_of_distinct_labels)
    
    # Count numbers in each class
    class_count = pd.value_counts(array_of_labels)
    print(class_count)       

    array_of_labels, integer_to_sound_mapping = encode_labels(array_of_labels, binary)
   
    # According to https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation
    # setting random_state to an integer (same each time) will result in the same data in the train and test each time this is called
    # An example used 42 - presumably as it's the answer to the meaning of life
    X_train, X_test, y_train, y_test = train_test_split(array_of_mfccs,
                                                    array_of_labels,
                                                    test_size=0.33,
                                                    random_state=42)    
    

    
    return X_train, X_test, y_train, y_test, number_of_distinct_labels, integer_to_sound_mapping, class_count

def run(create_data, testing, display_image):
    print("Started")
    MODEL_RUN_NAME = "testing"
    binary=True
#     X_train, X_test, y_train, y_test, number_of_distinct_labels, sound_to_integer_mapping = get_data(create_data=create_data, testing=testing, display_image=display_image)
    X_train, X_test, y_train, y_test, number_of_distinct_labels, integer_to_sound_mapping = get_data(MODEL_RUN_NAME, create_data=create_data, testing=testing, display_image=display_image)  
     
       

    
    print("number_of_distinct_labels", number_of_distinct_labels)
    
    print("sound_to_integer_mapping ", integer_to_sound_mapping)
       
    print("Finished")




if __name__ == '__main__':
    # create_data=True means create data from recordings and database, False means read in already saved numpy files
    # testing=False means only create data for 3 recordings
    run(create_data=False, testing=True, display_image=False) 

