import sys

# model_run_name='2019_11_28_1'
# model_run_name='2019_12_03_1'
model_run_name='2019_12_05_1'

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

relation_name = 'morepork_more-pork_vs_unknown'
class_names = 'morepork_more-pork,unknown'

weka_model_folder = 'weka_model'
weka_model_filename = "model.model"
weka_input_arff_filename = "input.arff"
weka_run_jar_filename = "run.jar"

onset_pairs_folder = 'onset_pairs'
# mel_spectrograms_folder = 'mel_spectrograms'
temp_display_images_folder = 'temp_display_images'
spectrograms_for_model_creation_folder = 'spectrograms_for_model_creation'
arff_file_for_weka_model_creation = 'arff_file_for_weka_model_creation.arff'
filtered_recordings_folder = 'filtered_recordings'
squawks_from_filtered_recordings = 'squawks_from_filtered_recordings'
basic_information_on_recordings_with_audio_tags_folder = 'basic_information_on_recordings_with_audio_tags'
full_information_on_recordings_with_tags_folder = 'full_information_on_recordings_with_tags'
ids_of_recordings_with_audio_tags_folder = 'ids_of_recordings_with_audio_tags'
list_of_tags_folder = 'list_of_tags'
files_for_testing_folder = 'files_for_testing'
tagged_recordings_folder = 'wavfiles'
version = '5'
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


db_file = "/home/tim/Work/Cacophony/eclipse-workspace/audio_manager_v1/audio_analysis_db2.db"
conn = None