'''
Created on 30 Sep. 2020

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

from sklearn import preprocessing
# from scipy.ndimage.interpolation import shift

from scipy.ndimage import shift
from numpy.random import normal

from sklearn.preprocessing import MinMaxScaler
# from sklearn.preprocessing import minmax_scale
from skimage.util import random_noise


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

def encode_labels_using_sound_to_integer_mapping(sounds, binary, sound_to_integer_mapping):
    # https://www.educative.io/edpresso/how-to-perform-one-hot-encoding-using-keras
    
    if binary:
        sounds = group_non_morepork(sounds)
    
#     total_sounds = np.unique(sounds)
    print("len(total_sounds) ", len(sounds))


    # integer representation
    for x in range(len(sounds)):
        sounds[x] = sound_to_integer_mapping[sounds[x]]
    
    if binary:
        sounds = np.array(sounds)
        sounds = sounds.astype(np.float)
    else:                
        sounds = to_categorical(sounds)  # one hot encoded    

    return sounds   

def create_sound_to_integer_mapping(sounds, binary):
    if binary:
        sounds = group_non_morepork(sounds)
    
    total_sounds = np.unique(sounds)
    print("len(total_sounds) ", len(sounds))

    # map each sound to an integer
    sound_to_integer_mapping = {}
    for x in range(len(total_sounds)):
        sound_to_integer_mapping[total_sounds[x]] = x
        
    return sound_to_integer_mapping                 


def get_filtered_recording(recording_id):
#     recordings_folder_with_path = parameters.base_folder + '/' + parameters.downloaded_recordings_folder
    recordings_folder_with_path = parameters.base_folder_for_recordings + '/' + parameters.downloaded_recordings_folder
    
    filename = str(recording_id) + ".m4a"
    audio_in_path = recordings_folder_with_path + "/" + filename


    y, sr = librosa.load(audio_in_path, sr=None, mono=True) # seems to give a spectrogram size of 64x69 - close enough - will chop to 64x64
         
    y_filtered = functions.butter_bandpass_filter(y, parameters.morepork_min_freq, parameters.morepork_max_freq, sr)    
    
    return y_filtered, sr

def load_training_data_audio(recording_id, start_time, y_full_recording, sr):
   
#     recording_id = 563200
#     start_time = 11.6

    if y_full_recording is None:  
        print(f"Recording {recording_id} has changed - going to load from file - start time is {start_time}")      
        y_full_recording, sr = get_filtered_recording(recording_id)
    else:
        print(f"Recording id is still {recording_id} and start time is now {start_time}")      
        
#     duration_secs = 0.6784 # seems to give a spectrogram size of 64x69 - close enough - will chop to 64x64
    duration_secs = 1.2 # seems to give a spectrogram size 
#     frame_start_position = start_time * sr
#     frame_end_position = (start_time + duration_secs) * sr 
    
    print(y_full_recording.shape)
    
    start_time_seconds_float = float(start_time)            
            
    start_position_array = int(sr * start_time_seconds_float)              
                       
    end_position_array = start_position_array + int((sr * duration_secs))
                       
    if end_position_array > y_full_recording.shape[0]:
        print('Clip would end after end of recording')
        return None, None, None # not sure if you have to return 3 Nones !
                
    y_part = y_full_recording[start_position_array:end_position_array]  
        
#     y_part = y_full_recording[frame_start_position:frame_end_position]

#     mfccs = librosa.feature.melspectrogram(y=y_part, sr=sr, n_mels=64, fmin=700,fmax=1100, hop_length=512, n_fft=8192)  #
    
    # Using Dennis's approach for calculating nfft
    slices_per_second = 13 # chosen to give a spectrogram length of 32 as have 32 mels and want a square image
    
    nfft = int(sr / slices_per_second)
    print("nfft ", nfft)
    hop_length=int(nfft / 2)
    print("hop_length ", hop_length)
    
    
#     mfccs = librosa.feature.melspectrogram(y=y_part, sr=sr, n_mels=32, fmin=600,fmax=1100, hop_length=1024, n_fft=2048)  #
    mfccs = librosa.feature.melspectrogram(y=y_part, sr=sr, n_mels=32, fmin=600,fmax=1100, hop_length=hop_length, n_fft=nfft)  #    
    print(mfccs.shape)

        # Going to create the mfccs as the Keras built-in models expect as input (which they then transform)
#     print("mfccs.max() ", mfccs.max())
#     mfccs *= 255.0/mfccs.max()      # https://stackoverflow.com/questions/1735025/how-to-normalize-a-numpy-array-to-within-a-certain-range
#     print("mfccs.max() ", mfccs.max())
      
#     mfccs = mfccs/mfccs.max()  # Going to scale for my model so don't have to do later (was getting memory issues)
    
    # Have been having memory issues - so will save spectrogram as 0-255 integer values
    mfccs *= 255.0/mfccs.max()
    mfccs = np.uint8(mfccs)
    print(mfccs[0])
    print(type(mfccs[0]))
    
   
    if mfccs.shape[1] < 32:   # all must be the same size
        print("mfccs.shape is less than 32", mfccs.shape)
        return None # just throw it away
 
    if mfccs.shape[1] > 32:   # all must be the same size
        print("mfccs.shape > 32 - will resize", mfccs.shape)
        mfccs = mfccs[:,:32]
        print("mfccs.shape 32?", mfccs.shape)
       
    mfccs = np.expand_dims(mfccs, axis=2)    
    print("mfccs.shape ", mfccs.shape)
    
    # Expand to 3 channel to look like rgb:
    # But don't use rgb for my model        
    #mfccs = tf.image.grayscale_to_rgb(tf.convert_to_tensor(mfccs))
   
    print(mfccs.shape)
       
    return mfccs ,sr , y_full_recording 


def get_all_training_data(testing, display_image, testing_number):    
    cur = functions.get_database_connection().cursor()   
    cur.execute("select recording_id, start_time_seconds, actual_confirmed FROM training_data ORDER BY recording_id") 
#     cur.execute("select recording_id, start_time_seconds, actual_confirmed FROM training_data WHERE sample_rate = '48000' ORDER BY recording_id") 
    training_data = cur.fetchall()
    
    number_of_training_examples = len(training_data)
    if testing:
        number_of_training_examples = testing_number
    
    # https://stackoverflow.com/questions/53135673/how-to-use-numpy-dstack-in-a-loop
    array_of_mfccs = []
    array_of_labels = []

    count = 0
    previous_recording_id = -1 # used to keep track if recording has changed, so can just load new recordings.
    for row in training_data:
        count+=1
        print("Processing ", count, " of ", number_of_training_examples)
        recording_id = row[0]
        start_time = row[1]
        actual_confirmed = row[2]
        
        if actual_confirmed == 'maybe_morepork_more-pork' or actual_confirmed == 'morepork_more-pork_part':
            continue # won't use them for training   
        else:
            print(actual_confirmed, " ", recording_id, " ", start_time)       
        
        if recording_id != previous_recording_id:
            y_full_recording = None
            sr = None
            
        previous_recording_id = recording_id
        
#         # test error catching
#         recording_id = -2
        
        try:
                
            mfccs, sr, y_full_recording = load_training_data_audio(recording_id, start_time, y_full_recording, sr)
            if mfccs is not None: 
    
                array_of_mfccs.append(mfccs)
                array_of_labels.append(actual_confirmed)                
                  
            if testing:
                if count >= number_of_training_examples:
                    break
                        
            if display_image: 
                try:                    
                    if actual_confirmed == "morepork_more-pork":                       
                        result = mfccs[:, :, 0]
                        print(result.shape)
            
                        plt.matshow(result)
                        plt.title(actual_confirmed)
        #                 plt.show()
        #                 plt.savefig("/home/tim/Temp/" + str(count) + ".jpg")
                        plt.savefig("/home/tim/Temp/" + str(count) + "-" + str(sr) + ".jpg")
                except:
                    pass
        except Exception as e:
            print(e, '\n')
            print(f'An error occurred creating spectrogram for recording: {recording_id} at start time: {start_time}')   
            continue
           
 
    result_mfccs = np.stack(array_of_mfccs, axis=0)
    result_labels = np.stack(array_of_labels, axis=0)
    
    print("result_mfccs shape is ", result_mfccs.shape)
    print("result_labels shape is ", result_labels.shape)
          
    return result_mfccs, result_labels

   
def get_data(binary, saved_mfccs_location, create_data, testing, display_image, testing_number, use_augmented_time_freq_data, create_augmented_time_freq_data, create_augmented_noise_data, use_augmented_noise_data):
    Path(saved_mfccs_location).mkdir(parents=True, exist_ok=True)
    
    array_of_all_possible_labels_filename = saved_mfccs_location + "array_of_all_possible_labels.npy"
    
    array_of_mfccs_training_filename = saved_mfccs_location + "array_of_mfccs_training.npy"
    array_of_labels_training_filename = saved_mfccs_location + "array_of_labels_training.npy"
    
    array_of_mfccs_validation_filename = saved_mfccs_location + "array_of_mfccs_validation.npy"
    array_of_labels_validation_filename = saved_mfccs_location + "array_of_labels_validation.npy"
    
    array_of_mfccs_training_augmented_time_freq_filename = saved_mfccs_location + "array_of_mfccs_training_augmented_time_freq.npy"
    array_of_labels_training_augmented_time_freq_filename = saved_mfccs_location + "array_of_labels_training_augmented_time_freq.npy"
    
    array_of_mfccs_training_augmented_gaussian_filename = saved_mfccs_location + "array_of_mfccs_training_augmented_gaussian.npy"
    array_of_labels_training_augmented_gaussian_filename = saved_mfccs_location + "array_of_labels_training_augmented_gaussian.npy"
    
    array_of_mfccs_training_augmented_salt_filename = saved_mfccs_location + "array_of_mfccs_training_augmented_salt.npy"
    array_of_labels_training_augmented_salt_filename = saved_mfccs_location + "array_of_labels_training_augmented_salt.npy"
    
    array_of_mfccs_training_augmented_pepper_filename = saved_mfccs_location + "array_of_mfccs_training_augmented_pepper.npy"
    array_of_labels_training_augmented_pepper_filename = saved_mfccs_location + "array_of_labels_training_augmented_pepper.npy"
    
    array_of_mfccs_training_augmented_salt_pepper_filename = saved_mfccs_location + "array_of_mfccs_training_augmented_salt_pepper.npy"
    array_of_labels_training_augmented_salt_pepper_filename = saved_mfccs_location + "array_of_labels_training_augmented_salt_pepper.npy"
    
#     sound_to_integer_mapping_filename = saved_mfccs_location + "sound_to_integer_mapping.npy"
      
   
           
    if create_data:
        array_of_mfccs, array_of_labels = get_all_training_data(testing=testing, display_image=display_image, testing_number=testing_number) 
       
        
        # Before splitting the data, create a sound_to_integer_mapping. Doing this before splitting, will ensure that any sounds
        # that only occur in one of training or validation, still occur in the mapping
        unique_labels = np.unique(array_of_labels)
        np.save(array_of_all_possible_labels_filename, unique_labels)
#         sound_to_integer_mapping = create_sound_to_integer_mapping(array_of_labels)
#         np.save(sound_to_integer_mapping_filename, sound_to_integer_mapping)
        
        # Now split it into training and validation   
        # According to https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation
        # setting random_state to an integer (same each time) will result in the same data in the train and test each time this is called
        # An example used 42 - presumably as it's the answer to the meaning of life       
                
        array_of_mfccs_training, array_of_mfccs_validation, array_of_labels_training, array_of_labels_validation = train_test_split(array_of_mfccs,
                                                    array_of_labels,
                                                    test_size=0.33,
                                                    random_state=42)           
                       
        np.save(array_of_mfccs_training_filename, array_of_mfccs_training)
        np.save(array_of_labels_training_filename, array_of_labels_training)
        np.save(array_of_mfccs_validation_filename, array_of_mfccs_validation)
        np.save(array_of_labels_validation_filename, array_of_labels_validation)        
        
    if create_augmented_time_freq_data:        
        
        array_of_mfccs_training = np.load(array_of_mfccs_training_filename)
        
        array_of_labels_training = np.load(array_of_labels_training_filename)        
        
        array_of_mfccs_training_augmented_time_freq, array_of_labels_training_augmented_time_freq = create_augmented_data_with_freq_time_shifts(array_of_mfccs_training, array_of_labels_training)
               
        np.save(array_of_mfccs_training_augmented_time_freq_filename, array_of_mfccs_training_augmented_time_freq)
        np.save(array_of_labels_training_augmented_time_freq_filename, array_of_labels_training_augmented_time_freq)
     
    if create_augmented_noise_data:
        # Needs augmented_time_freq_data to have been created
        
        array_of_mfccs_training_augmented_time_freq = np.load(array_of_mfccs_training_augmented_time_freq_filename)
        array_of_labels_training_augmented_time_freq = np.load(array_of_labels_training_augmented_time_freq_filename)  
            
        # Do each noise type separately
        # 1) gaussian
        array_of_mfccs_training_augmented_gaussian, array_of_labels_training_augmented_gaussian = create_augmented_data_with_noise(array_of_mfccs_training_augmented_time_freq, array_of_labels_training_augmented_time_freq, "gaussian")            
        np.save(array_of_mfccs_training_augmented_gaussian_filename, array_of_mfccs_training_augmented_gaussian)
        np.save(array_of_labels_training_augmented_gaussian_filename, array_of_labels_training_augmented_gaussian) 
         
        # Do each noise type separately
        # 2) salt
        array_of_mfccs_training_augmented_salt, array_of_labels_training_augmented_salt = create_augmented_data_with_noise(array_of_mfccs_training_augmented_time_freq, array_of_labels_training_augmented_time_freq, "salt")            
        np.save(array_of_mfccs_training_augmented_salt_filename, array_of_mfccs_training_augmented_salt)
        np.save(array_of_labels_training_augmented_salt_filename, array_of_labels_training_augmented_salt)
         
        # Do each noise type separately
        # 3) pepper
        array_of_mfccs_training_augmented_pepper, array_of_labels_training_augmented_pepper = create_augmented_data_with_noise(array_of_mfccs_training_augmented_time_freq, array_of_labels_training_augmented_time_freq, "pepper")            
        np.save(array_of_mfccs_training_augmented_pepper_filename, array_of_mfccs_training_augmented_pepper)
        np.save(array_of_labels_training_augmented_pepper_filename, array_of_labels_training_augmented_pepper)
         
        # Do each noise type separately
        # 4) salt_pepper
        array_of_mfccs_training_augmented_salt_pepper, array_of_labels_training_augmented_salt_pepper = create_augmented_data_with_noise(array_of_mfccs_training_augmented_time_freq, array_of_labels_training_augmented_time_freq, "s&p")            
        np.save(array_of_mfccs_training_augmented_salt_pepper_filename, array_of_mfccs_training_augmented_salt_pepper)
        np.save(array_of_labels_training_augmented_salt_pepper_filename, array_of_labels_training_augmented_salt_pepper)  
        
    # Now load data
   
    array_of_mfccs_training_to_use = np.load(array_of_mfccs_training_augmented_time_freq_filename) 
                
    array_of_labels_training_to_use = np.load(array_of_labels_training_augmented_time_freq_filename)   
    
    if use_augmented_time_freq_data:
#         read from previously saved augmented data
        array_of_mfccs_training_augmented_time_freq = np.load(array_of_mfccs_training_augmented_time_freq_filename) 
                      
        array_of_labels_training_augmented_time_freq = np.load(array_of_labels_training_augmented_time_freq_filename)  
        
        array_of_mfccs_training_to_use = np.append(array_of_mfccs_training_to_use, array_of_mfccs_training_augmented_time_freq, axis=0)            
        array_of_labels_training_to_use = np.append(array_of_labels_training_to_use, array_of_labels_training_augmented_time_freq, axis=0)       
        
    if use_augmented_noise_data:
        
        # 1) gaussian
        array_of_mfccs_training_augmented_gaussian = np.load(array_of_mfccs_training_augmented_gaussian_filename) 
                      
        array_of_labels_training_augmented_gaussian = np.load(array_of_labels_training_augmented_gaussian_filename)           
        
        array_of_mfccs_training_to_use = np.append(array_of_mfccs_training_to_use, array_of_mfccs_training_augmented_gaussian, axis=0)            
        array_of_labels_training_to_use = np.append(array_of_labels_training_to_use, array_of_labels_training_augmented_gaussian, axis=0)  
        
        # 2) salt
        array_of_mfccs_training_augmented_salt = np.load(array_of_mfccs_training_augmented_salt_filename) 
                           
        array_of_labels_training_augmented_salt = np.load(array_of_labels_training_augmented_salt_filename)           
         
        array_of_mfccs_training_to_use = np.append(array_of_mfccs_training_to_use, array_of_mfccs_training_augmented_salt, axis=0)            
        array_of_labels_training_to_use = np.append(array_of_labels_training_to_use, array_of_labels_training_augmented_salt, axis=0)  
         
        # 3) pepper
        array_of_mfccs_training_augmented_pepper = np.load(array_of_mfccs_training_augmented_pepper_filename) 
                    
        array_of_labels_training_augmented_pepper = np.load(array_of_labels_training_augmented_pepper_filename)           
         
        array_of_mfccs_training_to_use = np.append(array_of_mfccs_training_to_use, array_of_mfccs_training_augmented_pepper, axis=0)            
        array_of_labels_training_to_use = np.append(array_of_labels_training_to_use, array_of_labels_training_augmented_pepper, axis=0)  
         
        # 4) salt_pepper
        array_of_mfccs_training_augmented_salt_pepper = np.load(array_of_mfccs_training_augmented_salt_pepper_filename) 
                     
        array_of_labels_training_augmented_salt_pepper = np.load(array_of_labels_training_augmented_salt_pepper_filename)           
         
        array_of_mfccs_training_to_use = np.append(array_of_mfccs_training_to_use, array_of_mfccs_training_augmented_salt_pepper, axis=0)            
        array_of_labels_training_to_use = np.append(array_of_labels_training_to_use, array_of_labels_training_augmented_salt_pepper, axis=0)            
          
    # The mfccs's were stored as unit8, 0 - 255  
    # So now convert to 0-1 float64   
    array_of_mfccs_training_to_use = array_of_mfccs_training_to_use/255.         
         
    array_of_mfccs_validation_to_use = np.load(array_of_mfccs_validation_filename)   
   
    array_of_mfccs_validation_to_use = array_of_mfccs_validation_to_use/255.    
   
        
    array_of_labels_validation_to_use = np.load(array_of_labels_validation_filename) 
        
    # Create sound_to_integer_mapping
    unique_labels = np.load(array_of_all_possible_labels_filename)
    sound_to_integer_mapping  = create_sound_to_integer_mapping(unique_labels, binary)
    integer_to_sound_mapping = create_integer_to_sound_mapping(sound_to_integer_mapping)
    
    
    if binary:
        number_of_distinct_labels = 2
    else:
        number_of_distinct_labels = len(unique_labels)  
       
    # Count numbers in each class (training)
    class_count = pd.value_counts(array_of_labels_training_to_use)
#     print(class_count)       


    
    array_of_labels_training_to_use_encoded  = encode_labels_using_sound_to_integer_mapping(array_of_labels_training_to_use, binary, sound_to_integer_mapping)
    array_of_labels_validation_to_use_encoded  = encode_labels_using_sound_to_integer_mapping(array_of_labels_validation_to_use, binary, sound_to_integer_mapping)
          
          
    return array_of_mfccs_training_to_use, array_of_mfccs_validation_to_use, array_of_labels_training_to_use_encoded, array_of_labels_validation_to_use_encoded, number_of_distinct_labels, integer_to_sound_mapping, class_count


def create_augmented_data_with_freq_time_shifts(X_train, y_train):
    array_of_augmented_mfccs = []
    array_of_labels_for_augmented_mfccs = []    
    
    # load each mfccs
    # For each mfccs
    count = 0 # Keep track of what label to use for augmented data
    count_of_samples_to_augment = len(X_train)
    for non_shifted_sample in X_train:  
        print(f"Augmenting {count} of {count_of_samples_to_augment}")

        # Don't do 0, 0 as this would duplicated the original              
        for frequency_shift in [-4, -2, 2, 4]:
            for time_shift in [-10, -8, -6, -4, -2, 2, 4,  6, 8, 10]:
 
                shifted_sample = shift(non_shifted_sample, [frequency_shift,time_shift,0], mode='constant', cval=0) # https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.shift.html?highlight=shift
               
                # Uncomment next few lines to display and save images if you want to check them out.
#                 result = shifted_sample[:, :, 0]
#                 print(result.shape)                 
#                 plt.matshow(result)
#                 plt.title(f"{count}_2x2_shift_{frequency_shift}_{time_shift}")       
#                 plt.savefig(f"/home/tim/Temp/{count}_2x2_shift_{frequency_shift}_{time_shift}.jpg")                
                # End of display and save images if you want to check them out.
                
                array_of_augmented_mfccs.append(shifted_sample)
                array_of_labels_for_augmented_mfccs.append(y_train[count])
        
        count+=1
        
    return array_of_augmented_mfccs, array_of_labels_for_augmented_mfccs
 
# def augment_data_with_noise(X_train, y_train):
def create_augmented_data_with_noise(X_train, y_train, noise_mode): 
    # https://scikit-image.org/docs/stable/api/skimage.util.html?highlight=random_noise#skimage.util.random_noise
    
#     mfccs_before_noise, sr, y_full_recording = load_training_data_audio(535833, 40.8, None, None)  

    array_of_noisy_mfccs = []
    array_of_labels_for_noisy_mfccs = []   
    
    count_of_X_train = len(X_train)
    count=0
    for mfccs_before_noise, label in zip(X_train, y_train):        
        
#         if count > 1000:
#             break
        
        count+=1
        print(f"Adding {noise_mode} noise to {count} of {count_of_X_train}")          
   
        mfccs = mfccs_before_noise[:, :, 0]
        noisy_mfccs = random_noise(mfccs, mode=noise_mode) 
        
        # The random_noise function returned a float64 array between 0-1
        # So convert back to 0-255 unsigned int
        noisy_mfccs *= 255.0/noisy_mfccs.max()        
        noisy_mfccs = np.uint8(noisy_mfccs)
        
        noisy_mfccs = np.expand_dims(noisy_mfccs, axis=2)        
        array_of_noisy_mfccs.append(noisy_mfccs)
        array_of_labels_for_noisy_mfccs.append(label)   

    return array_of_noisy_mfccs, array_of_labels_for_noisy_mfccs
    
def test_augment_data_with_noise():
    # https://scikit-image.org/docs/stable/api/skimage.util.html?highlight=random_noise#skimage.util.random_noise
    
    mfccs_before_noise ,sr , y_full_recording = load_training_data_audio(535833, 40.8, None, None)  
      
    plt.matshow(mfccs_before_noise[:, :, 0])
    plt.title(f"noisy_before_noise")       
    plt.savefig(f"/home/tim/Temp/noisy_before_noise.jpg") 
#         
#         
    
    
#         array_of_noisy_mfccs = []
#         array_of_labels_for_noisy_mfccs = []           
    
    for noise_mode in ["gaussian", "salt", "pepper", "s&p", "speckle"]:

        mfccs = mfccs_before_noise[:, :, 0]       
        noisy_mfccs = random_noise(mfccs, mode=noise_mode)  
        
        # The random_noise function returned a float64 array between 0-1
        # So convert back to 0-255 unsigned int
        noisy_mfccs *= 255.0/noisy_mfccs.max()        
        noisy_mfccs = np.uint8(noisy_mfccs)
        
                    
                              
        plt.matshow(noisy_mfccs)    
        plt.title(f"noisy_variance_{noise_mode}")       
        plt.savefig(f"/home/tim/Temp/noisy_variance_{noise_mode}.jpg")    
        
        noisy_mfccs = np.expand_dims(noisy_mfccs, axis=2)
        
        print("noisy_mfccs_normalized.shape ", noisy_mfccs.shape)   
        
          
    
def run(create_data, testing, display_image):
    print("Started")
#     MODEL_RUN_NAME = "testing"
#     binary=True
# #     X_train, X_test, y_train, y_test, number_of_distinct_labels, sound_to_integer_mapping = get_data(create_data=create_data, testing=testing, display_image=display_image)
#     X_train, X_test, y_train, y_test, number_of_distinct_labels, integer_to_sound_mapping = get_data(MODEL_RUN_NAME, create_data=create_data, testing=testing, display_image=display_image)  
#      
#        
# 
#     
#     print("number_of_distinct_labels", number_of_distinct_labels)
#     
#     print("sound_to_integer_mapping ", integer_to_sound_mapping)
       
    print("Finished")




if __name__ == '__main__':
    # create_data=True means create data from recordings and database, False means read in already saved numpy files
    # testing=False means only create data for 3 recordings
    run(create_data=False, testing=True, display_image=False) 

