import sys



model_run_name='2020_05_04_1'



model_version = '000002' # update this to be the same as the name of the model stored in the model_run_result folder. Cacophony API says: version (hex coded, e.g. 0x0110 would be v1.10)

probability_cutoff_for_tag_creation = 0.5

predictedByModel_tag_to_create = 'morepork_more-pork'

recordings_for_creating_test_data_start_date = '2020-03-01'
recordings_for_creating_test_data_end_date = '2020-04-01' # Note, this will be interpreted as the first second of the day, so won't include results for this day.

first_test_data_recording_id = 537910
last_test_data_recording_id = 563200

#### Cacophony Server Configuration
server_endpoint = 'https://api.cacophony.org.nz' # Production
# server_endpoint = 'https://api-test.cacophony.org.nz'  # Test

cacophony_user_name = 'timhot' # change as needed
cacophony_user_password = '' # code will prompt for this, so don't store here.
cacophony_user_token = ''

login_user_url = '/authenticate_user'
query_available_recordings = '/api/v1/recordings/'
get_information_on_single_recording = '/api/v1/recordings/'
get_a_token_for_getting_a_recording_url = '/api/v1/recordings/' # should change the name of this
get_a_recording = '/api/v1/signedUrl'
tags_url = '/api/v1/tags'
groups = '/api/v1/groups'
devices_endpoint = '/api/v1/devices'

#### End of Cacophony Server Configuration

#### Local File Structure Configuration

#downloaded_recordings_folder = '/home/tim/Work/Cacophony/downloaded_recordings/all_recordings'

base_folder = '/home/tim/Work/Cacophony'


downloaded_recordings_folder = 'downloaded_recordings/all_recordings' # All the recordings
# downloaded_recordings_folder = 'downloaded_recordings/temp_for_testing' # Use this if doing a test
#run_folder = 'Analysis_5' # Change this when doing a new analyis


run_folder = 'Audio_Analysis/audio_classifier_runs' + '/' + model_run_name
# exported_jars_folder = 'exported_jars'
single_spectrogram_for_classification_folder = 'images'
temp_folder = 'Temp'
# arff_folder_for_next_run = 'arff_folder_for_next_run'

relation_name = model_run_name
class_names = 'morepork_more-pork,unknown,siren,dog,duck,dove,human,bird,car,rumble,white_noise,cow,buzzy_insect,plane,hammering,frog,morepork_more-pork_part,chainsaw,crackle,car_horn,water,fire_work,maybe_morepork_more-pork,music,hand_saw'

weka_model_folder = 'weka_model'
weka_model_filename = "model.model"
weka_input_arff_filename = "input.arff"
weka_run_jar_filename = "run.jar"
get_edge_histogram_jar_filename = "getEdgeHistogramFeatures.jar"

onset_pairs_folder = 'onset_pairs'
# mel_spectrograms_folder = 'mel_spectrograms'
temp_display_images_folder = 'temp_display_images'
spectrograms_for_model_creation_folder = 'spectrograms_for_model_creation'
spectrograms_for_model_testing_folder = 'spectrograms_for_model_testing'
arff_file_for_weka_model_creation = 'arff_file_for_weka_model_creation.arff'
csv_file_for_keeping_track_of_onsets_used_to_create_model = 'csv_file_for_keeping_track_of_onsets_used_to_create_model.csv'
arff_file_for_weka_model_testing = 'arff_file_for_weka_model_testing.arff'
filtered_recordings_folder = 'filtered_recordings'
squawks_from_filtered_recordings = 'squawks_from_filtered_recordings'
basic_information_on_recordings_with_audio_tags_folder = 'basic_information_on_recordings_with_audio_tags'
full_information_on_recordings_with_tags_folder = 'full_information_on_recordings_with_tags'
ids_of_recordings_with_audio_tags_folder = 'ids_of_recordings_with_audio_tags'
list_of_tags_folder = 'list_of_tags'
files_for_testing_folder = 'files_for_testing'
tagged_recordings_folder = 'wavfiles'
version = '5'
onset_version = '7'
initial_locatation_for_choosing_arff_file_dialog = "/home/tim/Work/Cacophony/Audio_Analysis/audio_classifier_runs/"

squawk_duration_seconds = 0.8
morepork_more_pork_call_duration = 0.9

#### End of Local File Structure Configuration


# database = "audio_analysis_db"

# conn = gui_functions.create_connection(db_file)

name_of_latest_file_containing_basic_information_of_recordings_with_audio_tags = ''
name_of_latest_file_containing_ids_of_recordings_with_audio_tags = ''
file_containing_list_of_recording_with_full_information = ''
name_of_file_containing_list_of_tags = ''


#tagged_recordings_as_array_pickles_folder = 'tagged_recordings_as_array_pickles'
hop_length = 256



arff_file_to_process = '/arff_file_to_process'

#path to configs
# sys.path.append('/home/jonah/Documents/opensmile-2.3.0/config/')
sys.path.append('/home/tim/opensmile-2.3.0/config/')
#path to input files
search_path = '/home/tim/Work/Cacophony/opensmile_weka/TestAudioInput'
#path to where we want the output
arff_path = '/home/tim/Work/Cacophony/opensmile_weka/TestAudioOutput'


db_file = "/home/tim/Work/Cacophony/Audio_Analysis/audio_analysis_db2.db"

# db_file = "/home/tim/Work/Cacophony/eclipse-workspace/audio_manager_v1/audio_analysis_db2.db"
# db_file = "/home/tim/Work/Cacophony/Audio_Analysis/temp/audio_analysis_db2.db"
# db_file = "/home/tim/Work/Cacophony/Audio_Analysis/audio_analysis_db2_clone_test.db"
# db_file = "/home/tim/Work/Cacophony/Audio_Analysis/temp/audio_analysis_db3.db"
# db_file = "/home/tim/Work/Cacophony/Audio_Analysis/temp/audio_analysis_db2.db"
# db_file = "/home/tim/Work/Cacophony/Audio_Analysis/temp/audio_analysis_db4.db"
# db_file = "/home/tim/Work/Cacophony/Audio_Analysis/audio_analysis_db2_a.db"

# test_data_canvas_width = 500
# test_data_canvas_height = 2000
# test_data_canvas_width = 1000
# test_data_canvas_height = 2000
test_data_canvas_height = 1000
# test_data_canvas_width = 2380
test_data_canvas_width = 2455

conn = None


# tensorflow_run_name = '2020_06_08_1'
# tensorflow_run_name = '2020_06_10_1'
# tensorflow_run_folder = base_folder + '/Audio_Analysis/audio_classifier_runs/tensorflow_runs' + '/' + tensorflow_run_name
tensorflow_spectrogram_images = base_folder + '/Audio_Analysis/audio_classifier_runs/tensorflow_runs/images_morepork_other'


