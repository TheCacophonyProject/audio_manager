'''
Created on 24 Aug. 2020

@author: tim
'''

import functions
import parameters
import librosa
import matplotlib.pyplot as plt
import numpy as np

from sklearn.model_selection import train_test_split


BASE_FOLDER = '/home/tim/Work/Cacophony'
MODEL_RUN_NAME = "2020_08_24a"
RUNS_FOLDER = '/Audio_Analysis/audio_classifier_runs/tensorflow_runs/' 

MODEL_RUN_NAME = "2020_08_24a"    
         
def what_to_integer_lookup(what): # https://stackoverflow.com/questions/60208/replacements-for-switch-statement-in-python
    return {
        'bird': 1,
        'buzzy_insect': 2,
        'car': 3,
        'car_horn': 4,
        'chainsaw': 5,
        'cow': 6,
        'crackle': 7,
        'dog': 8,
        'dove': 9,
        'duck': 10,
        'fire_work': 11,
        'frog': 12,
        'hammering': 13,
        'hand_saw': 14,
        'human': 15,
        'maybe_morepork_more-pork': 16,
        'morepork_more-pork': 17,
        'morepork_more-pork_part': 18,
        'music': 19,
        'plane': 20,
        'rumble': 21,
        'siren': 22,
        'unknown': 23,
        'water': 24,
        'white_noise': 25         
    }.get(what, 0)    # 0 is default if what not found
    


def get_onsets_stored_locally_for_recording_id(version_to_use, recording_id):
    cur = functions.get_database_connection().cursor()    
    cur.execute("SELECT start_time_seconds, duration_seconds, actual_confirmed FROM onsets WHERE version = ? AND recording_id = ? ORDER BY recording_id", (version_to_use, recording_id)) 
    rows = cur.fetchall()
    return rows

def get_filtered_recording(recording_id):
    recordings_folder_with_path = parameters.base_folder + '/' + parameters.downloaded_recordings_folder
    filename = str(recording_id) + ".m4a"
    audio_in_path = recordings_folder_with_path + "/" + filename
    y, sr = librosa.load(audio_in_path, sr=22050, mono=True, offset=0.0, duration=60.0)
#     y_filtered = apply_band_pass_filter(y, sr)
        
    y_filtered = functions.butter_bandpass_filter(y, parameters.morepork_min_freq, parameters.morepork_max_freq, sr)    
#     y_filtered_reduced_noise = functions.noise_reduce(y_filtered, sr) 

#     fig, (ax1, ax2, ax3) = plt.subplots(1, 3)  # Create a figure containing a single axes.
#     ax1.plot(y)  # Plot some data on the axes. 
#     ax2.plot(y_filtered)  # Plot some data on the axes. 
#     ax3.plot(y_filtered_reduced_noise)  # Plot some data on the axes.
#     plt.show()

    
    return y_filtered, sr
#     return y_filtered_reduced_noise, sr

    
def get_labels_for_recording(recording_id):
    version_to_use = 5
    confirmed_onsets = get_onsets_stored_locally_for_recording_id(version_to_use, recording_id)
    
    # convert onset to time series
    # Create an array of zeros for 60 seconds
    label_array = np.zeros(shape=2584)
    print(label_array)
    
    for onset in confirmed_onsets:
        start_time_seconds = onset[0]
        duration_seconds = onset[1]
        actual_confirmed = onset[2]
        
        start_index = int(start_time_seconds * 2584 / 60)
        end_index = int((start_time_seconds + duration_seconds)  * 2584 / 60)
        if end_index >= 2584 - 1:
            end_index = 2584 - 1
        
        i = start_index
        while i <  end_index:
            label_array[i] = what_to_integer_lookup(actual_confirmed)
            i+=1
      
    return label_array

def get_labels_for_recording_count_morepork(recording_id):
    version_to_use = 5
    confirmed_onsets = get_onsets_stored_locally_for_recording_id(version_to_use, recording_id)
    
   
    count_of_moreporks = 0
    for onset in confirmed_onsets:
        start_time_seconds = onset[0]
        duration_seconds = onset[1]
        actual_confirmed = onset[2]
        
        if actual_confirmed == 'morepork_more-pork':
            count_of_moreporks+=1
          
    return count_of_moreporks

def load_single_audio(recording_id):
    label_array = get_labels_for_recording(recording_id)
  
    y, sr = get_filtered_recording(recording_id)
    mfccs = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=32, fmin=700,fmax=1000, hop_length=512) # https://librosa.org/doc/latest/generated/librosa.feature.melspectrogram.html
    
    max_value = np.max(mfccs)
    
#     print(max_value)
    
    
#     mfccs_normalized = mfccs / np.max(np.abs(mfccs),axis=0)
    mfccs_normalized = mfccs / max_value
   
    if mfccs_normalized.shape[1] < 2584:    

        reshaped_mfccs = np.zeros((32, 2584))
        reshaped_mfccs[:mfccs_normalized.shape[0],:mfccs_normalized.shape[1]] = mfccs_normalized
       
#         print(reshaped_mfccs.shape)
        return reshaped_mfccs, label_array 
       
    else:
        return mfccs, label_array

def load_single_audio_number_moreporks(recording_id):
    label_count_morepork = get_labels_for_recording(recording_id)
  
    y, sr = get_filtered_recording(recording_id)
    mfccs = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=32, fmin=700,fmax=1000, hop_length=512) # https://librosa.org/doc/latest/generated/librosa.feature.melspectrogram.html
    
    max_value = np.max(mfccs)
    
#     print(max_value)
    
    
#     mfccs_normalized = mfccs / np.max(np.abs(mfccs),axis=0)
    mfccs_normalized = mfccs / max_value
   
    if mfccs_normalized.shape[1] < 2584:    

        reshaped_mfccs = np.zeros((32, 2584))
        reshaped_mfccs[:mfccs_normalized.shape[0],:mfccs_normalized.shape[1]] = mfccs_normalized
       
#         print(reshaped_mfccs.shape)
        return reshaped_mfccs, label_count_morepork 
       
    else:
        return mfccs, label_count_morepork    
    
# def get_all_training_recording_data(testing):
#     version_to_use = 5
#     cur = functions.get_database_connection().cursor()    
#     cur.execute("select distinct recording_id FROM onsets WHERE version = ? AND actual_confirmed IS NOT NULL ORDER BY recording_id", (version_to_use, )) 
#     unique_recording_ids = cur.fetchall()
#     
#     number_of_distinct_recordings = len(unique_recording_ids)
#     if testing:
#         number_of_distinct_recordings = 3
#     
#     # https://stackoverflow.com/questions/53135673/how-to-use-numpy-dstack-in-a-loop
#     array_of_mfccs = []
#     array_of_labels = []
# 
#     count = 0
#     for unique_recording_id in unique_recording_ids:
#         count+=1
#         print("Processing ", count, " of ", number_of_distinct_recordings)
#         recording_id = unique_recording_id[0]
#         mfccs, labels = load_single_audio(recording_id)
#         array_of_mfccs.append(mfccs)
#         array_of_labels.append(labels)
#               
#         if testing:
#             if count >= 3:
#                 break
#     
#     result_mfccs = np.stack(array_of_mfccs, axis=-1)
#     result_labels = np.stack(array_of_labels, axis=-1)
#     
# #     print("result_mfccs shape is ", result_mfccs.shape)
# #     print("result_labels shape is ", result_labels.shape)

def get_all_training_recording_data_morepork(testing):
    version_to_use = 5
    cur = functions.get_database_connection().cursor()    
    cur.execute("select distinct recording_id FROM onsets WHERE version = ? AND actual_confirmed IS NOT NULL ORDER BY recording_id", (version_to_use, )) 
    unique_recording_ids = cur.fetchall()
    
    number_of_distinct_recordings = len(unique_recording_ids)
    if testing:
        number_of_distinct_recordings = 3
    
    # https://stackoverflow.com/questions/53135673/how-to-use-numpy-dstack-in-a-loop
    array_of_mfccs = []
    array_of_labels = []

    count = 0
    for unique_recording_id in unique_recording_ids:
        count+=1
        print("Processing ", count, " of ", number_of_distinct_recordings)
        recording_id = unique_recording_id[0]
        mfccs, labels = load_single_audio_number_moreporks(recording_id)
        array_of_mfccs.append(mfccs)
        array_of_labels.append(labels)
              
        if testing:
            if count >= 3:
                break
    
    result_mfccs = np.stack(array_of_mfccs, axis=-1)
    result_labels = np.stack(array_of_labels, axis=-1)
    
#     print("result_mfccs shape is ", result_mfccs.shape)
#     print("result_labels shape is ", result_labels.shape)
    
    return result_mfccs, result_labels
    
def get_data(create_data, testing):
    array_of_mfccs_filename = BASE_FOLDER + RUNS_FOLDER +  MODEL_RUN_NAME + "/" + 'array_of_mfccs' 
    array_of_labels_filename = BASE_FOLDER + RUNS_FOLDER +  MODEL_RUN_NAME + "/" + 'array_of_labels'
           
    if create_data:
        array_of_mfccs, array_of_labels = get_all_training_recording_data_morepork(testing=testing)    
        np.save(array_of_mfccs_filename, array_of_mfccs)
        np.save(array_of_labels_filename, array_of_labels)
        
    else:
        # read from previously saved data
        array_of_mfccs = np.load(array_of_mfccs_filename + ".npy")
        array_of_labels = np.load(array_of_labels_filename + ".npy")
        
    print("array_of_mfccs shape is ", array_of_mfccs.shape)
    print("array_of_labels shape is ", array_of_labels.shape)

    X_train, X_test, y_train, y_test = train_test_split(array_of_mfccs,
                                                    array_of_labels,
                                                    test_size=0.33,
                                                    random_state=42)    
    
    return X_train, X_test, y_train, y_test

def run(create_data, testing):
    print("Started")
    
    X_train, X_test, y_train, y_test = get_data(create_data=create_data, testing=testing)  
       
    print(X_train.shape)
    print(X_test.shape)
    print(y_train.shape)
    print(y_test.shape)
       
    print("Finished")


# run(True) # True means create data from recordings and database, False means read in already saved numpy files

if __name__ == '__main__':
    # create_data=True means create data from recordings and database, False means read in already saved numpy files
    # testing=False means only create data for 3 recordings
    run(create_data=True, testing=True) 

