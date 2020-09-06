'''
Created on 2 Sep. 2020
Use model to perform a sliding window across march 2020 recordings and find moreporks

Use this to learn how to input data into Tensorflow from numpy arrays
@author: tim
'''

import functions
import parameters
import prepare_data_v5
import what_v12
import librosa

import numpy as np

import tensorflow as tf


BASE_FOLDER = '/home/tim/Work/Cacophony'
RUNS_FOLDER = '/Audio_Analysis/audio_classifier_runs/tensorflow_runs/' 

MODELS_FOLDER = "saved_models"
SAVED_MFCCS_FOLDER = "saved_mfccs"

def update_database(model_run_name, recording_id, start_time_seconds, probability):      
    functions.insert_model_run_result(model_run_name, recording_id, start_time_seconds, parameters.morepork_more_pork_call_duration, "morepork_more-pork", probability)
    

def get_filtered_recording_for_onset(recording_id):
    recordings_folder_with_path = parameters.base_folder + '/' + parameters.downloaded_recordings_folder
    filename = str(recording_id) + ".m4a"
    audio_in_path = recordings_folder_with_path + "/" + filename

    y, sr = librosa.load(audio_in_path, sr=22050, mono=True) # chosen to give a square with the 32 mels
        
    y_filtered = functions.butter_bandpass_filter(y, parameters.morepork_min_freq, parameters.morepork_max_freq, sr)    
    
    return y_filtered, sr

def get_array_of_mfcss_windows_for_recording(recording_id):
    list_of_mfccs = []
    list_of_start_times = []
    # A window is 32 bins long, and slides by 0.2 seconds
    # So will have just under 60 / 0.2 = 300 windows for a 60 sec recording (just under as last start position has to be 0.8 secs before end of recording
    # This was used to create spectrogram for training model: y, sr = librosa.load(audio_in_path, sr=22050, mono=True, offset=start_time, duration=0.7314) 
    y, sr = get_filtered_recording_for_onset(recording_id)
    
    current_start_position_in_seconds = 0
    
    
    while True:
        current_start_position_in_sample_frames = current_start_position_in_seconds * sr
        current_end_position_in_sample_frames = current_start_position_in_sample_frames + 0.7314 * sr
        y_part = y[int(current_start_position_in_sample_frames):int(current_end_position_in_sample_frames)]
         
        mfccs = librosa.feature.melspectrogram(y=y_part, sr=sr, n_mels=32, fmin=700,fmax=1000, hop_length=512) # https://librosa.org/doc/latest/generated/librosa.feature.melspectrogram.html
            
        max_value = np.max(mfccs)    
    
        mfccs_normalized = mfccs / max_value
        
        # As we are going to use a Conv2d layer in the model, it expects 3 dimensions, so need to expand
    #     https://machinelearningmastery.com/a-gentle-introduction-to-channels-first-and-channels-last-image-formats-for-deep-learning/
    
        mfccs_normalized = np.expand_dims(mfccs_normalized, axis=2)    
#         print("mfccs_normalized.shape ", mfccs_normalized.shape)
       
    #     if mfccs_normalized.shape[1] < 2584:   # need to change this to ? 
        if mfccs_normalized.shape[1] < 32:   # need to change this to ? 
    
            # got to end of recording
            break
           
        else:
            
#             return mfccs_normalized  
        
            list_of_mfccs.append(mfccs_normalized)
            list_of_start_times.append(round(current_start_position_in_seconds, 2))
        
        current_start_position_in_seconds+=0.2
    
    return list_of_mfccs, list_of_start_times

def main():
    run_sub_log_dir = "10-multi_class"
    model_run_name = "2020_09_07_binary"    
    model_name = "model_1"
    saved_mfccs = "version_1/"
    
    binary_model_location = BASE_FOLDER + RUNS_FOLDER + MODELS_FOLDER + "/binary/" + model_name   
    multi_class_model_location = BASE_FOLDER + RUNS_FOLDER + MODELS_FOLDER + "/multi_class/" + model_name
    
    binary_model = what_v12.load_model(binary_model_location)
    multi_class_model = what_v12.load_model(multi_class_model_location)
        
    march_recordings_2020_ids = functions.get_march_2020_recording_ids()
    number_of_recordings = len(march_recordings_2020_ids)
    recording_count = 0
    count_of_moreporks = 0
    for recording_id in march_recordings_2020_ids:
        recording_id = recording_id[0]
        recording_id = "319256" # for testing
        print("Processing recording id ", recording_id, "which is ", recording_count, " of ", number_of_recordings)
               
#         list_of_mfccs = []
#         list_of_start_times = []       
#         cursor_time_position = 0
#         time_step = 0.2
#         while (cursor_time_position + 0.8) < 60: # don't go beyond end of 60 sec recordings
#             mfccs = prepare_data_v5.load_onset_audio(recording_id, cursor_time_position)
#             if mfccs is not None:
#                 list_of_mfccs.append(mfccs)
#                 list_of_start_times.append(cursor_time_position)
#                 cursor_time_position+=time_step
        # 1) Get spectrogram for whold recording
        
        
        # 2) Create array of mfccs by sliding a window across spectrogram taking out parts
        list_of_mfccs, list_of_start_times = get_array_of_mfcss_windows_for_recording(recording_id)
        
        # now create prediction for each step
        array_of_mfccs = np.array(list_of_mfccs) 
        
        # First use binary model
#         predictions = binary_model(array_of_mfccs)
#         rounded_predictions = tf.round(predictions)
#         proto_tensor = tf.make_tensor_proto(rounded_predictions)
#         predictions_np = tf.make_ndarray(proto_tensor)
#         predictions_np_flattened = predictions_np.reshape(-1)
#         predictions_np_flattened_int = predictions_np_flattened.astype(int)

        predictions = binary_model(array_of_mfccs)
#         rounded_predictions = tf.round(predictions)
        proto_tensor = tf.make_tensor_proto(predictions)
        predictions_np = tf.make_ndarray(proto_tensor)
        predictions_np_flattened = predictions_np.reshape(-1)
#         predictions_np_flattened = predictions_np_flattened
        predictions_np_flattened_rounded = tf.round(predictions_np_flattened)
      
        
        
        last_prediction = 1  # use this to notice when prediction changes, indicated a new prediction (to take car of overlapping sampling)
        
        time_count = 0
        
#         for prediction in predictions_np_flattened_int:
        for prediction in predictions_np_flattened_rounded:

            prediction = int(prediction)
            prediction_changed = False
#             print(prediction)
            if (prediction != last_prediction):
                prediction_changed = True
                last_prediction = prediction
           
            if prediction == 0:
                print("morepork_morepork")
                if (prediction_changed):
                    print("A new morepork_morepork call - count this one in recording ",recording_id, " at time ",  list_of_start_times[time_count])
                  
                    count_of_moreporks+=1
#                     probability = str(predictions_np_flattened[time_count])
                    probability = predictions_np_flattened[time_count]
                    probability_rounded_str = str(round(probability,6))
                    update_database(model_run_name, recording_id, list_of_start_times[time_count], probability_rounded_str)
                    print("So far have found ", count_of_moreporks, " moreporks")
                last_prediction = 0 
            else:
#                 print("other")
                last_prediction = 1
                
            time_count+=1
                
        recording_count+=1       
        
    print("count_of_moreporks is ", count_of_moreporks)
        
            
        

if __name__ == '__main__':
    main()