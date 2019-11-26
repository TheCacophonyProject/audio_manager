import sys

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
devices = '/api/v1/devices'

#### End of Cacophony Server Configuration

#### Local File Structure Configuration

#downloaded_recordings_folder = '/home/tim/Work/Cacophony/downloaded_recordings/all_recordings'

base_folder = '/home/tim/Work/Cacophony'
downloaded_recordings_folder = 'downloaded_recordings/all_recordings' # All the recordings
# downloaded_recordings_folder = 'downloaded_recordings/temp_for_testing' # Use this if doing a test
run_folder = 'Analysis_5' # Change this when doing a new analyis
temp_folder = 'Temp'

onset_pairs_folder = 'onset_pairs'
mel_spectrograms_folder = 'mel_spectrograms'
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