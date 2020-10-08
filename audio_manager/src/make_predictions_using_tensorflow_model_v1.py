'''
Created on 7 Oct. 2020

@author: tim
'''
'''
Created on 8 Sep. 2020

@author: tim
'''


import functions_v1 as functions
import parameters

import librosa
import pickle
import numpy as np

import tensorflow as tf






def update_database(model_run_name, recording_id, start_time_seconds, probability, prediction):      
    functions.save_prediction(model_run_name, recording_id, start_time_seconds, parameters.morepork_more_pork_call_duration, prediction, probability)
    

def get_filtered_recording_for_onset(recording_id):
#     recordings_folder_with_path = parameters.base_folder + '/' + parameters.downloaded_recordings_folder
    
    recordings_folder_with_path = parameters.base_folder_for_recordings + '/' + parameters.downloaded_recordings_folder
        
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
    
    recordings_folder_with_path = parameters.base_folder_for_recordings + '/' + parameters.downloaded_recordings_folder       
    filename = str(recording_id) + ".m4a"
    audio_in_path = recordings_folder_with_path + "/" + filename
    

    
    y, sr = librosa.load(audio_in_path, sr=None, mono=True)
    
    # Using Dennis's approach for calculating nfft
    slices_per_second = 13 # chosen to give a spectrogram length of 32 as have 32 mels and want a square image    
    nfft = int(sr / slices_per_second)
    hop_length=int(nfft / 2)
    
    current_start_position_in_seconds = 0    
    
    while True:
        current_start_position_in_sample_frames = current_start_position_in_seconds * sr
        current_end_position_in_sample_frames = current_start_position_in_sample_frames + 1.2 * sr
        y_part = y[int(current_start_position_in_sample_frames):int(current_end_position_in_sample_frames)]
         
        mfccs = librosa.feature.melspectrogram(y=y_part, sr=sr, n_mels=32, fmin=600,fmax=1100, hop_length=hop_length, n_fft=nfft) # https://librosa.org/doc/latest/generated/librosa.feature.melspectrogram.html
 
        # Have been having memory issues - so will save spectrogram as 0-255 integer values
        mfccs *= 255.0/mfccs.max()
        mfccs = np.uint8(mfccs)

        if mfccs.shape[1] < 32:   # need to change this to ? 
    
            # got to end of recording
            break
           
        else:
            
#             return mfccs_normalized          
            list_of_mfccs.append(mfccs)
            list_of_start_times.append(round(current_start_position_in_seconds, 2))
        
        current_start_position_in_seconds+=0.2
    
    return list_of_mfccs, list_of_start_times

def main():
    print(tf.__version__)
#     startDate = parameters.feb_2020_training_data_end_date
#     endDate = parameters.feb_2020_training_data_end_date
    
    startDate = parameters.march_2020_test_data_start_date
    endDate = parameters.march_2020_test_data_end_date
    
#     march_2020_test_data_start_date = '2020-03-01'
# march_2020_test_data_end_date
    
#     binary_or_multi_class = "multi_class"
    binary_or_multi_class = "binary"
    modelName = "vgg16_lr0.0004"
    model_run_name = "2020_10_08a" + "_" + modelName + "_" + binary_or_multi_class
 
#     BASE_FOLDER = '/home/tim/Work/Cacophony'
#     BASE_FOLDER = parameters.base_folder
#     
#     RUNS_FOLDER = '/Audio_Analysis/audio_classifier_runs/tensorflow_runs/' 
#     MODELS_FOLDER = "saved_models"
#     SAVED_MFCCS_FOLDER = "saved_mfccs"
#     
#     parameters.base_folder = '/home/tim/Work/Cacophony'
#     parameters.base_folder_for_recordings = '/media/tim/HDD1/Work/Cacophony'
#     parameters.downloaded_recordings_folder = 'audio_analysis/downloaded_recordings/all_recordings' # All the recordings
#     parameters.run_folder = 'Audio_Analysis/audio_classifier_runs' + '/' + model_run_name
    
    
#     model_location = "/home/tim/Work/Cacophony/Audio_Analysis/audio_classifier_runs/tensorflow_runs/saved_models/" + binary_or_multi_class + "/" + modelName +"/"
    
    model_location = parameters.base_folder + "/Audio_Analysis/audio_classifier_runs/tensorflow_runs/saved_models/" + binary_or_multi_class + "/" + modelName +"/"
    
    
    print("model_location is ", model_location)    
    class_mapping_file_path_name = model_location + "integer_to_sound_mapping.pkl"   
    print("multi_class_mapping_file_path_name is ", class_mapping_file_path_name)
    
    with open(class_mapping_file_path_name,"rb") as f:
        multi_class_integer_to_sound_mapping =  pickle.load(f)        
    print(multi_class_integer_to_sound_mapping)
    
    multi_class_model = tf.keras.models.load_model(model_location)
    # Check its architecture
    multi_class_model.summary()
             
    recording_ids = functions.get_recording_ids(startDate, endDate)
    number_of_recordings = len(recording_ids)
    recording_count = 0
    
    multi_class_count_of_moreporks = 0
    for recording_id in recording_ids:
        recording_id = recording_id[0]

        print("Processing recording id ", recording_id, "which is ", recording_count, " of ", number_of_recordings)            
        
        list_of_mfccs, list_of_start_times = get_array_of_mfcss_windows_for_recording(recording_id)
                
        # now create prediction for each step
                
        array_of_mfccs = np.array(list_of_mfccs) 
        
        # mfccs are stored as 0-255 integers, but model needs 0 - 1 floats
        array_of_mfccs = array_of_mfccs/255.                    

        predictions = multi_class_model(array_of_mfccs)
        predictions_decoded_int = tf.argmax(predictions, 1) 
        predictions_np_array = predictions_decoded_int.numpy()
        
        last_prediction = ""  # use this to notice when prediction changes, indicated a new prediction (to take car of overlapping sampling)
        time_count = 0 
        
        for prediction_np in predictions_np_array:
            prediction_decoded_str = multi_class_integer_to_sound_mapping.get(prediction_np)
            probability = predictions[time_count][prediction_np]
            probability_np = probability.numpy()
            probability_rounded_str = str(round(probability_np,6))
            
            prediction_changed = False
            if (prediction_decoded_str != last_prediction):
                prediction_changed = True                
                
            if (prediction_changed):
                if prediction_decoded_str == "morepork_more-pork":                    
                    multi_class_count_of_moreporks+=1
                    print("Multi-class model found a morepork_morepork call in recording ",recording_id, " at time ",  list_of_start_times[time_count])
                    print("So far, the multi-class model has predicted ", multi_class_count_of_moreporks, "morepork_more-pork calls")
                    
                update_database(model_run_name, recording_id, list_of_start_times[time_count], probability_rounded_str, prediction_decoded_str)
                    
            last_prediction = prediction_decoded_str
            
            
                    
            time_count+=1
                
        recording_count+=1       
        
   
    print("multi_class_count_of_moreporks is ", multi_class_count_of_moreporks)
        
            
        

if __name__ == '__main__':
    main()