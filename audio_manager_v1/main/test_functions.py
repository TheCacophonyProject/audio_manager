import main.functions as functions

# Uncomment a test to run it :-)


print('hello')

# functions.update_onsets_with_latest_model_run_actual_confirmed()

# functions.update_onsets_device_super_name()

# functions.update_model_run_result_device_super_name()

functions.test_query()
    

# def test_update_recording_in_database():
#     update_recording_in_database('2018-04-04T17:07:01.000Z', 3, 1, 2, -22.2, 178.1, '23b', 77, 'ZTE phone',7, 1234, 'true', 'grants shed3', 291047)
#    
# def test_get_recording_information_for_a_single_recording():
#     recording_data = get_recording_information_for_a_single_recording('197294')
#     print('recording_data is: ', recording_data)
#     
# def test_update_recording_information_for_all_local_database_recordings():
#     update_recording_information_for_all_local_database_recordings()
#     
# def test_get_audio_recordings_with_tags_information_from_server():
#     user_token = get_cacophony_user_token()
#     recording_type = 'audio'
#     deviceId = 379
#     recordings = get_audio_recordings_with_tags_information_from_server(user_token, recording_type, str(deviceId))
#     for recording in recordings:
#         print(recording, '\n')
#         
# def test_get_and_store_tag_information_for_recording():
#     get_and_store_tag_information_for_recording(str(197294), 123)
#     
# def test_insert_tag_into_database():
#     insert_tag_into_database(1,135940, 'bat', 'detail', 'confidence', 1.2, 2.5, 'automatic', 256, '2019-06-20T04:14:24.811Z', 'timhot', 'deviceId', 'device_name', 'device_super_name')
#     
# def test_check_if_tag_alredy_in_database(): 
#     check_if_tag_alredy_in_database(135939)  
#     
# def test_get_all_tags_for_all_devices_in_local_database():
#     get_all_tags_for_all_devices_in_local_database()        
# 
# def test_get_unique_recording_ids_that_have_been_tagged_with_this_tag_stored_locally():
#     recording_ids = get_unique_recording_ids_that_have_been_tagged_with_this_tag_stored_locally("more pork - classic")  
#     for recording_id in recording_ids:
#         print(recording_id)    
#      
# def test_get_unique_devices_stored_locally():
#     unique_devices = get_unique_devices_stored_locally()
#     for unique_device in unique_devices:
#         print(unique_device, '\n')
#         
# def test_get_onsets_stored_locally():
#     onsets = get_onsets_stored_locally()
#     for onset in onsets:
#         print(onset) 
#         
# def test_get_model_run_result():
#     result = get_model_run_result(163)
#     print('result', result)
#     
# def test_scan_local_folder_for_recordings_not_in_local_db_and_update():
#     scan_local_folder_for_recordings_not_in_local_db_and_update('grants shed')
#     
# def test_create_tags_from_folder_of_unknown_images():
#     create_tags_from_folder_of_unknown_images()
#     
# def test_update_local_tags_with_version():
#     update_local_tags_with_version()
#     
# def test_update_model_run_result():    
#     update_model_run_result(17, 'tim was here')
# 
# def test_run_model():
#     base_folder = '/home/tim/Work/Cacophony/Audio_Analysis/audio_classifier_runs'
#     run_folder = '2019_11_28_1'
#     model_folder = base_folder + '/' + run_folder + '/exported_jars'
#     
#     result = run_model(model_folder)
#     if result.returncode == 0:
#         print(result.stdout)
#     else:
#         print(result.stderr)
#         
# def test_play_clip():
#     play_clip('171696', 20.7, 0.8)
#     
# def test_create_onsets_with_existing_tag():
#     create_onsets("more pork - classic")  
#       
# def test_create_onsets_with_null_existing_tag():
# #     This should use the recordings folder
#     create_onsets(None)     
#     
# def test_insert_onset_into_database():
#     insert_onset_into_database('Analysis_5', 1234, 3.2, 0.6)
#  
# def test_get_single_waveform_image():
#     image_out = get_single_waveform_image('161943', 1.0, 0.7)
#     print('image_out ', image_out)   
#     
# def test_play_array():
#     play_array("161943", "1", "2.2")
#     
# def test_update_recording_information_for_single_recording():
#     update_recording_information_for_single_recording('291047')


    
    
    
    
