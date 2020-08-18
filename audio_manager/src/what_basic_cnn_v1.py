'''
Created on 18 Aug. 2020
This is based on the basic grid search using keras layers
@author: tim
'''

import parameters
import functions

import tensorflow as tf
from tensorflow import keras 

from keras.preprocessing import image

import numpy as np

RUN_FOLDER = "2020_08_18a"

def load_model():
    
    model_location_sub_folder = RUN_FOLDER + "/copied_from_ml_at_wintec/20200817-125845-extra-layers-4-dense-layers-1-dropout-0.2-filters-16-f_mult-3-epochs-500"
    model_location = parameters.base_folder + "/Audio_Analysis/audio_classifier_runs/tensorflow_runs/" + model_location_sub_folder
    print("model_location: ",model_location)
    
    model = tf.keras.models.load_model(model_location)

    # Check its architecture
    model.summary()
    return model

def test_model_against_march_test_data(model):
    march_onsets = functions.get_march_2020_version_7_onsets()
    count_of_march_onsets = len(march_onsets)
#     print("count_of_march_onsets ", count_of_march_onsets)
    count = 0
    count_of_morepork = 0
    for onset in march_onsets:
        try:
                       
            count+=1
            
            recording_id = onset[0]
            start_time_seconds = onset[1] 
            duration_seconds = onset[2] 
            device_super_name = onset[3]
            device_name = onset[4]
            recordingDateTime = onset[5]
            recordingDateTimeNZ = onset[6]
                
            
            path_of_image_to_predict = functions.get_single_create_focused_mel_spectrogram_return_path(recording_id=recording_id, start_time_seconds=start_time_seconds, duration_seconds=duration_seconds, run_folder=RUN_FOLDER)
#             print("path_of_image_to_predict: ", path_of_image_to_predict)
    #         https://www.youtube.com/watch?v=0kYIZE8Gl90
    
#             path_of_image_to_predict = "/home/tim/Work/Cacophony/2020_08_18a/temp_display_images/164136$9.4$morepork_more-pork.jpg"
#             path_of_image_to_predict = "/home/tim/Work/Cacophony/2020_08_18a/temp_display_images/164675$32.6$car.jpg"
            img = image.load_img(path_of_image_to_predict, color_mode="grayscale", target_size=(320,240)) #https://keras.io/api/preprocessing/image/
            input_arr = image.img_to_array(img)
#             print(input_arr)
            input_arr = np.array(input_arr).astype('float32')/255 # https://stackoverflow.com/questions/43017017/keras-model-predict-for-a-single-image
#             print(input_arr)
            input_arr = np.expand_dims(input_arr, axis=0)
#             images = np.vstack([input_arr])
#             classes = model.predict(images, batch_size=10)
#             print(classes[0])
            predictions = model.predict(input_arr)
           
#             print(predictions[0][0])
            what = "other"
            probability = predictions[0][0]
            if (probability < 0.5):
                count_of_morepork+=1
                what = "morepork_more-pork"
                print("less than one: recording_id: " , str(recording_id) , ", start_time_seconds: ", str(start_time_seconds))
                
            print("prediction " , str(count) , " of " , str(count_of_march_onsets) , " is: ", str(probability) , " count_of_morepork is: ", count_of_morepork)
            
            # insert result into database
            sql = ''' INSERT INTO model_run_result(modelRunName, recording_id, startTime, duration, predictedByModel, probability, device_super_name, device_name, recordingDateTime, recordingDateTimeNZ)
                  VALUES(?,?,?,?,?,?,?,?,?,?) '''
            cur = functions.get_database_connection().cursor()
            cur.execute(sql, (RUN_FOLDER, recording_id, start_time_seconds, duration_seconds, what, str(probability), device_super_name, device_name, recordingDateTime, recordingDateTimeNZ))
            functions.get_database_connection().commit()
            
        
        except Exception as e:
            print(e, '\n')
            print('Error processing onset ', onset)

def run():
    model = load_model()
    test_model_against_march_test_data(model=model)
    

run()