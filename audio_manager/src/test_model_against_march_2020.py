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
import pickle
import numpy as np

import tensorflow as tf


BASE_FOLDER = '/home/tim/Work/Cacophony'
RUNS_FOLDER = '/Audio_Analysis/audio_classifier_runs/tensorflow_runs/' 

MODELS_FOLDER = "saved_models"
SAVED_MFCCS_FOLDER = "saved_mfccs"

def update_database(model_run_name, recording_id, start_time_seconds, probability, prediction):      
    functions.insert_model_run_result(model_run_name, recording_id, start_time_seconds, parameters.morepork_more_pork_call_duration, prediction, probability)
    

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
    model_run_name_base = "2020_09_07" 
    model_name = "model_1"
    saved_mfccs = "version_1/"
    
    binary_model_location = BASE_FOLDER + RUNS_FOLDER + MODELS_FOLDER + "/binary/" + model_name   
    multi_class_model_location = BASE_FOLDER + RUNS_FOLDER + MODELS_FOLDER + "/multi_class/" + model_name
    
    
    binary_mapping_file_path_name = binary_model_location + "/integer_to_sound_mapping.pkl"   
    with open(binary_mapping_file_path_name,"rb") as f:
        binary_integer_to_sound_mapping =  pickle.load(f)
        
    multi_class_mapping_file_path_name = multi_class_model_location + "/integer_to_sound_mapping.pkl"   
    with open(multi_class_mapping_file_path_name,"rb") as f:
        multi_class_integer_to_sound_mapping =  pickle.load(f)
        
    print(multi_class_integer_to_sound_mapping)
    
      
    binary_model = what_v12.load_model(binary_model_location)
    multi_class_model = what_v12.load_model(multi_class_model_location)
        
    march_recordings_2020_ids = functions.get_march_2020_recording_ids()
    number_of_recordings = len(march_recordings_2020_ids)
    recording_count = 0
    binary_count_of_moreporks = 0
    multi_class_count_of_moreporks = 0
    for recording_id in march_recordings_2020_ids:
        recording_id = recording_id[0]
#         recording_id = "319256" # for testing
        print("Processing recording id ", recording_id, "which is ", recording_count, " of ", number_of_recordings)               

        list_of_mfccs, list_of_start_times = get_array_of_mfcss_windows_for_recording(recording_id)
        
        # now create prediction for each step
        array_of_mfccs = np.array(list_of_mfccs) 
        
        # First use binary model
        model_run_name = model_run_name_base + "_binary" 
        predictions = binary_model(array_of_mfccs)
        proto_tensor = tf.make_tensor_proto(predictions)
        predictions_np = tf.make_ndarray(proto_tensor)
        predictions_np_flattened = predictions_np.reshape(-1)
        predictions_np_flattened_rounded = tf.round(predictions_np_flattened)
                      
        last_prediction = ""  # use this to notice when prediction changes, indicated a new prediction (to take car of overlapping sampling)
        time_count = 0        

        for prediction_number in predictions_np_flattened_rounded:        
            
            prediction_number = int(prediction_number)
            prediction = binary_integer_to_sound_mapping.get(prediction_number)
            
            
            prediction_changed = False
            if (prediction != last_prediction):
                prediction_changed = True
                last_prediction = prediction
           
#             if prediction == 0:
            if prediction == "morepork_more-pork":
#                 print("morepork_morepork")
                if (prediction_changed):
                    
                    binary_count_of_moreporks+=1
                    probability = predictions_np_flattened[time_count]
                    probability_rounded_str = str(round(probability,6))
                    update_database(model_run_name, recording_id, list_of_start_times[time_count], probability_rounded_str, prediction)
                    print("Binary model found a morepork_morepork call in recording ",recording_id, " at time ",  list_of_start_times[time_count])
                    print("So far the binary model has predicted ", binary_count_of_moreporks, "morepork_more-pork calls")
                last_prediction = "morepork_more-pork" 
            else:
                last_prediction = "other"
                
            time_count+=1
            
        # Second use multi-class model
        model_run_name = model_run_name_base + "_multi_class" 
        predictions = multi_class_model(array_of_mfccs)
#         print(predictions)
        predictions_decoded_int = tf.argmax(predictions, 1) 
#         print(predictions_decoded_int)
        predictions_np_array = predictions_decoded_int.numpy()
        
        last_prediction = ""  # use this to notice when prediction changes, indicated a new prediction (to take car of overlapping sampling)
        time_count = 0 
        
        for prediction_np in predictions_np_array:
            prediction_decoded_str = multi_class_integer_to_sound_mapping.get(prediction_np)
#             print(prediction_decoded_str)
#             print(predictions[time_count])
#             print(predictions[time_count][prediction_np])
            probability = predictions[time_count][prediction_np]
#             print(probability)
            probability_np = probability.numpy()
            probability_rounded_str = str(round(probability_np,6))
#             print(probability_rounded_str)
            
            prediction_changed = False
            if (prediction_decoded_str != last_prediction):
                prediction_changed = True
                
                
            if (prediction_changed):
                if prediction_decoded_str == "morepork_more-pork":                    
                    multi_class_count_of_moreporks+=1
                    print("Multi-class model found a morepork_morepork call in recording ",recording_id, " at time ",  list_of_start_times[time_count])
                    print("So far, the multi-class model has predicted ", multi_class_count_of_moreporks, "morepork_more-pork calls")
                    
                # save prediction to database
                if prediction_decoded_str != "white_noise":
                    update_database(model_run_name, recording_id, list_of_start_times[time_count], probability_rounded_str, prediction_decoded_str)
                    
            last_prediction = prediction_decoded_str
            
                              
            time_count+=1
                
        recording_count+=1       
        
    print("binary_count_of_moreporks is ", binary_count_of_moreporks)
    print("multi_class_count_of_moreporks is ", multi_class_count_of_moreporks)
        
            
        

if __name__ == '__main__':
    main()