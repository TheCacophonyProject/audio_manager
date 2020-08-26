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

    


def get_labels_for_recording_count_morepork(recording_id):
    version_to_use = 5
    confirmed_onsets = get_onsets_stored_locally_for_recording_id(version_to_use, recording_id)
    
   
    count_of_moreporks = 0
    for onset in confirmed_onsets:
#         start_time_seconds = onset[0]
#         duration_seconds = onset[1]
        actual_confirmed = onset[2]
        
        if actual_confirmed == 'morepork_more-pork':
            count_of_moreporks+=1
          
    print("count_of_moreporks ", count_of_moreporks)
    return count_of_moreporks



def load_single_audio_number_moreporks(recording_id):
    label_count_morepork = get_labels_for_recording_count_morepork(recording_id)
  
    y, sr = get_filtered_recording(recording_id)
    mfccs = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=32, fmin=700,fmax=1000, hop_length=512) # https://librosa.org/doc/latest/generated/librosa.feature.melspectrogram.html
    
    max_value = np.max(mfccs)
    
#     print(max_value)
    
    
#     mfccs_normalized = mfccs / np.max(np.abs(mfccs),axis=0)
    mfccs_normalized = mfccs / max_value
    
    print("mfccs_normalized.shape ", mfccs_normalized.shape)    
    mfccs_normalized = np.expand_dims(mfccs_normalized, axis=2)    
    print("mfccs_normalized.shape ", mfccs_normalized.shape)
   
    if mfccs_normalized.shape[1] < 2584:    

        reshaped_mfccs = np.zeros((32, 2584, 1))
        reshaped_mfccs[:mfccs_normalized.shape[0],:mfccs_normalized.shape[1]] = mfccs_normalized
       
#         print(reshaped_mfccs.shape)
        return reshaped_mfccs, label_count_morepork 
       
    else:
        return mfccs_normalized, label_count_morepork    
    


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
        print("mfccs.shape ", mfccs.shape)
        array_of_mfccs.append(mfccs)
        array_of_labels.append(labels)
              
        if testing:
            if count >= 99:
                break
    
#     result_mfccs = np.stack(array_of_mfccs, axis=-1)
#     result_labels = np.stack(array_of_labels, axis=-1)
    result_mfccs = np.stack(array_of_mfccs, axis=0)
    result_labels = np.stack(array_of_labels, axis=0)
    
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
        
    maximum_number_of_moreporks = np.max(array_of_labels)
    
    print("maximum_number_of_moreporks ", maximum_number_of_moreporks)
        
    print("array_of_mfccs shape is ", array_of_mfccs.shape)
    print("array_of_labels shape is ", array_of_labels.shape)

    X_train, X_test, y_train, y_test = train_test_split(array_of_mfccs,
                                                    array_of_labels,
                                                    test_size=0.33,
                                                    random_state=42)    
    
    print(X_train.shape)    
    print(X_test.shape)
    print(y_train.shape)    
    print(y_test.shape)
        
    print(X_train[:3])
    print(X_test[:3])
    print(y_train[:3])
    print(y_test[:3])
    
    return X_train, X_test, y_train, y_test, maximum_number_of_moreporks

def run(create_data, testing):
    print("Started")
    
    X_train, X_test, y_train, y_test, maximum_number_of_moreporks = get_data(create_data=create_data, testing=testing)  
       
    print(X_train.shape)
    print(X_test.shape)
    print(y_train.shape)
    print(y_test.shape)
    
    print("maximum_number_of_moreporks", maximum_number_of_moreporks)
       
    print("Finished")


# run(True) # True means create data from recordings and database, False means read in already saved numpy files

if __name__ == '__main__':
    # create_data=True means create data from recordings and database, False means read in already saved numpy files
    # testing=False means only create data for 3 recordings
    run(create_data=True, testing=True) 

