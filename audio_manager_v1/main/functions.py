import main.parameters
from main.parameters import *

import sqlite3
from sqlite3 import Error
import requests
import os
import sys
import json
from pathlib import Path
from tkinter import filedialog
from tkinter import *
import re
from scipy.io import wavfile
import shutil
import send2trash
import sounddevice as sd
from pydub import AudioSegment
from pydub.playback import play
import librosa
import os
from scipy import signal
from scipy.io import wavfile
from scipy.signal import butter, lfilter, freqz
import numpy as np
from scipy.ndimage.filters import maximum_filter
import pylab
import librosa.display
import shlex
import glob
import soundfile as sf
import subprocess
from subprocess import PIPE, run
from playsound import playsound
from librosa.output import write_wav
from librosa import display
import matplotlib.pyplot as plt
import acoustid
import chromaprint
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
import pywt
import shlex



#path to configs
# sys.path.append('/home/jonah/Documents/opensmile-2.3.0/config/')
sys.path.append('/home/tim/opensmile-2.3.0/config/')
#path to input files
search_path = '/home/tim/Work/Cacophony/opensmile_weka/TestAudioInput'
#path to where we want the output
arff_path = '/home/tim/Work/Cacophony/opensmile_weka/TestAudioOutput'


db_file = "/home/tim/Work/Cacophony/eclipse-workspace/audio_manager_v1/audio_analysis_db2.db"
conn = None

def get_database_connection():
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """

    # https://stackoverflow.com/questions/8587610/unboundlocalerror-local-variable-conn-referenced-before-assignment
    global conn
    if conn is None:
        try:
            conn = sqlite3.connect(db_file)           
        except Error as e:
            print(e)
  
    return conn       
    

def get_tags_from_server(device_id):
    print('about to get tags from server for device ', device_id)
    

def get_recordings_from_server(device_name, device_super_name):
    if not device_name:
        print('Device name can NOT be null')
        return
    
    if not device_super_name:
        print('Device Super name can NOT be null')
        return    
        
    print('About to get recordings from server')
    retrieve_available_recordings_from_server(device_name, device_super_name)
    
def get_latest_recording_id_from_local_db(device_name, device_super_name):
    # Need the last recording ID for this device, that we already have   

#     https://docs.python.org/2/library/sqlite3.html
    sql = ''' SELECT audio_file_id FROM audio_files WHERE device_super_name = ? ORDER BY audio_file_id DESC LIMIT 1'''
    cur = get_database_connection().cursor()  
   
    cur.execute(sql,(device_super_name,))   
 
    rows = cur.fetchall() 
    for row in rows:
        return row[0]
    
def retrieve_available_recordings_from_server(device_name, device_super_name):      

    recordings_folder = getRecordingsFolder()     

    ids_of_recordings_to_download = get_recording_ids_for_device_name(device_name)
    
    # remove ids of recordings that we already have
    already_downloaded = []
    for file in os.listdir(recordings_folder):
        already_downloaded.append(os.path.splitext(file)[0])
       
    already_downloaded_set = set(already_downloaded)  
        
    ids_of_recordings_to_still_to_download = []
    
    for recording_id in ids_of_recordings_to_download:
        if not recording_id in already_downloaded_set:
            ids_of_recordings_to_still_to_download.append(recording_id)
        else:
            print('Aleady have recording ',recording_id, ' so will not download')
       
    for recording_id in ids_of_recordings_to_still_to_download:
#         print('About to get token for downloading ',recording_id)
        token_for_retrieving_recording = get_token_for_retrieving_recording(recording_id)
        print('About to get recording ',recording_id)
        get_recording_from_server(token_for_retrieving_recording, recording_id, device_name, device_super_name)
        
        # Also get recording information from server
        update_recording_information_for_single_recording(recording_id)
     
    print('Finished retrieving recordings')  
    print('Now going to retrieve tags')  
    get_all_tags_for_all_devices_in_local_database()
    print('Finished retrieving tags') 
    print('Finished all')  
        
def get_recording_from_server(token_for_retrieving_recording, recording_id, device_name, device_super_name):
    try:
      
        recording_local_filename = getRecordingsFolder() + '/' + recording_id + '.m4a'
            
        # Don't download it if we already have it.       
       
        if not os.path.exists(recording_local_filename):
            url = server_endpoint + get_a_recording
            querystring = {"jwt":token_for_retrieving_recording}     
           
            resp_for_getting_a_recording = requests.request("GET", url, params=querystring)
           
            if resp_for_getting_a_recording.status_code != 200:
                # This means something went wrong.
                print('Error from server is: ', resp_for_getting_a_recording.text)
                return               
             
            with open(recording_local_filename, 'wb') as f:  
                f.write(resp_for_getting_a_recording.content)
                
            # Update local database
            insert_recording_into_database(recording_id,recording_id + '.m4a' ,device_name,device_super_name)
            
        else:
            print('\t\tAlready have recording ', str(recording_id) , ' - so will not download again\n')
    except Exception as e:
        print(e, '\n')
        print('\t\tUnable to download recording ' + str(recording_id), '\n')
        
def get_token_for_retrieving_recording(recording_id):
    user_token = get_cacophony_user_token()

    get_a_token_for_recording_endpoint = server_endpoint + get_a_token_for_getting_a_recording_url + recording_id

    headers = {'Authorization': user_token}

    resp_for_getting_a_recordingToken = requests.request("GET", get_a_token_for_recording_endpoint, headers=headers)
    if resp_for_getting_a_recordingToken.status_code != 200:
        sys.exit('Could not get download token - exiting')
    recording_data = resp_for_getting_a_recordingToken.json()
    recording_download_token = recording_data['downloadFileJWT']
    
    return recording_download_token
    
def get_recording_ids_for_device_name(device_name): 
        
    print('device_name ', device_name)
    
    device_id = get_device_id_using_device_name(device_name)
    print('device_id is ', device_id)
    ids_recordings_for_device_name = []
    offset = 0
    while True:
        ids_of_recordings_to_download= get_ids_of_recordings_to_download_using_deviceId(device_id,offset)
        print('ids_of_recordings_to_download ', ids_of_recordings_to_download)
        ids_recordings_for_device_name += ids_of_recordings_to_download
        if (len(ids_of_recordings_to_download) > 0):
            offset+=300
        else:
            break
    return ids_recordings_for_device_name

def get_ids_of_recordings_to_download_using_deviceId(deviceId, offset):
    # This will get a list of the recording ids for every recording of length 59,60,61,62 from device_name
    user_token = get_cacophony_user_token()
   
    url = server_endpoint + query_available_recordings
    
    where_param = {}
    where_param['DeviceId'] = deviceId
    where_param['duration'] = 59,60,61,62
    json_where_param = json.dumps(where_param) 
    querystring = {"offset":offset, "where":json_where_param}   
    
    headers = {'Authorization': user_token}  

    resp = requests.request("GET", url, headers=headers, params=querystring)
   
    if resp.status_code != 200:
        # This means something went wrong.
        print('Error from server is: ', resp.text)
        sys.exit('Could not download file - exiting')            
    
    data = resp.json() 
    
    
    recordings = data['rows'] 
    
    print('Number of recordings is ', len(recordings))

    ids_of_recordings_to_download = []    
    for recording in recordings:        
        recording_id = str(recording['id'])
        ids_of_recordings_to_download.append(recording_id)
        
    return ids_of_recordings_to_download    

def get_device_id_using_device_name(device_name):
    user_token = get_cacophony_user_token()
    url = server_endpoint + devices
      
    headers = {'Authorization': user_token}  

    resp = requests.request("GET", url, headers=headers)
   
    if resp.status_code != 200:
        # This means something went wrong.
        print('Error from server is: ', resp.text)
        sys.exit('Could not download file - exiting')
    
    data = resp.json()

    devices = data['devices'] 
    rows = devices['rows']
    for row in rows:
        devicename = row['devicename']        
        if devicename == device_name:
                device_id = row['id']
                return device_id     
            
def get_cacophony_user_token():
    if cacophony_user_token:
        return cacophony_user_token
    
    print('About to get user_token from server')
    username = cacophony_user_name
    if cacophony_user_password == '':
        cacophony_user_password = input("Enter password for Cacophony user " + username + " (or change cacophony_user_name in parameters file): ")
           
    requestBody = {"nameOrEmail": username, "password": cacophony_user_password }
    login_endpoint = server_endpoint + login_user_url
    resp = requests.post(login_endpoint, data=requestBody)
    if resp.status_code != 200:
        # This means something went wrong.
        sys.exit('Could not connect to Cacophony Server - exiting')
    
    data = resp.json()
    cacophony_user_token = data['token']
    return cacophony_user_token
    
def load_recordings_from_local_folder(device_name, device_super_name):
    
    input_folder = filedialog.askdirectory()

    recordings_folder = getRecordingsFolder()
    
    for filename in os.listdir( input_folder):
        recording_id = filename.replace('-','.').split('.')[0]
        filename2 = recording_id +'.m4a'

        insert_recording_into_database(recording_id,filename2,device_name,device_super_name)
        
        # Now move file to recordings folder
        audio_in_path = input_folder + '/' + filename       
        audio_out_path = recordings_folder + '/' + filename2
        
        print('Moving ', filename, ' to ', audio_out_path)
        os.rename(audio_in_path, audio_out_path)

        # Now need to get information about this recording from server
        update_recording_information_for_single_recording(recording_id)
        
def insert_recording_into_database(recording_id,filename,device_name,device_super_name):
    try:
        sql = ''' INSERT INTO recordings(recording_id,filename,device_name,device_super_name)
                  VALUES(?,?,?,?) '''
        cur = get_database_connection().cursor()
        cur.execute(sql, (recording_id,filename,device_name,device_super_name))
       
        get_database_connection().commit()
    except Exception as e:
        print(e, '\n')
        print('\t\tUnable to insert recording ' + str(recording_id), '\n')
        

def update_recordings_folder(recordings_folder):
    print("new_recording_folder ", recordings_folder)
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param recordings_folder:
    :return: project id
    """
    sql = ''' UPDATE settings
              SET downloaded_recordings_folder = ?               
              WHERE ID = 1'''
    cur = get_database_connection().cursor()
    cur.execute(sql, (recordings_folder,))
    get_database_connection().commit()      
        
def getRecordingsFolder():

    cur = get_database_connection().cursor()
    cur.execute("select * from settings")
 
    rows = cur.fetchall()
    home = str(Path.home())
    print('home ', home)
 
    for row in rows:       
        return  home + '/' + row[0] 
    
    
def getRecordingsFolderWithOutHome():
    cur = get_database_connection().cursor()
    cur.execute("select * from settings")
 
    rows = cur.fetchall()   
 
    for row in rows:     
        return row[0] 
    
def saveSettings(recordings_folder):
    print('recordings_folder ', recordings_folder)
    #https://stackoverflow.com/questions/16856647/sqlite3-programmingerror-incorrect-number-of-bindings-supplied-the-current-sta
    update_recordings_folder(recordings_folder)
        
def update_recording_information_for_single_recording(recording_id):
    print('About to update recording information for recording ', recording_id)    
    recording_information = get_recording_information_for_a_single_recording(recording_id)
    print('recording_information ', recording_information)    
    if recording_information == None:        
        print('recording_information == None')     
        return
         
    recording = recording_information['recording']    
    recordingDateTime = recording['recordingDateTime']    
    relativeToDawn = recording['relativeToDawn']    
    relativeToDusk = recording['relativeToDusk']    
    duration = recording['duration'] 
       
    location = recording['location']        
    coordinates = location['coordinates']    
    locationLat = coordinates[0]    
    locationLong = coordinates[1]  
       
    version = recording['version']    
    batteryLevel = recording['batteryLevel']    
    
    additionalMetadata = recording['additionalMetadata']    
    phoneModel = additionalMetadata['Phone model']    
    androidApiLevel = additionalMetadata['Android API Level']  
    
    Device = recording['Device']    
    deviceId = Device['id']
    device_name = Device['devicename']
         
    nightRecording =  'false'
    
    if relativeToDusk is not None:
        if relativeToDusk > 0:
            nightRecording = 'true' 
    elif relativeToDawn is not None:
        if relativeToDawn < 0:
            nightRecording = 'true'   
                   
    update_recording_in_database(recordingDateTime, relativeToDawn, relativeToDusk, duration, locationLat, locationLong, version, batteryLevel, phoneModel, androidApiLevel, deviceId, nightRecording, device_name, recording_id)
    print('Finished updating recording information for recording ', recording_id)
               
def test_update_recording_information_for_single_recording():
    update_recording_information_for_single_recording('291047')
    
def update_recording_in_database(recordingDateTime, relativeToDawn, relativeToDusk, duration, locationLat, locationLong, version, batteryLevel, phoneModel,androidApiLevel, deviceId, nightRecording, device_name, recording_id):
    try:
        conn = get_database_connection()
        # https://www.sqlitetutorial.net/sqlite-python/update/
        sql = ''' UPDATE recordings 
                  SET recordingDateTime = ?,
                      relativeToDawn = ?,
                      relativeToDusk = ?,
                      duration = ?,
                      locationLat = ?,
                      locationLong = ?,
                      version = ?,
                      batteryLevel = ?,
                      phoneModel = ?,
                      androidApiLevel = ?,
                      deviceId = ?,
                      nightRecording = ?,
                      device_name = ?
                  WHERE recording_id = ? '''
        cur = get_database_connection().cursor()
        cur.execute(sql, (recordingDateTime, relativeToDawn, relativeToDusk, duration, locationLat, locationLong, version, batteryLevel, phoneModel, androidApiLevel, deviceId, nightRecording, device_name, recording_id))
        get_database_connection().commit()
    except Exception as e:
        print(e, '\n')
        print('\t\tUnable to insert recording ' + str(recording_id), '\n')
        
def test_update_recording_in_database():
    update_recording_in_database('2018-04-04T17:07:01.000Z', 3, 1, 2, -22.2, 178.1, '23b', 77, 'ZTE phone',7, 1234, 'true', 'grants shed3', 291047)
      
    
def get_recording_information_for_a_single_recording(recording_id):
    user_token = get_cacophony_user_token()

    get_a_token_for_recording_endpoint = server_endpoint + get_information_on_single_recording + recording_id

    headers = {'Authorization': user_token}

    resp_for_getting_a_recordingToken = requests.request("GET", get_a_token_for_recording_endpoint, headers=headers)
    if resp_for_getting_a_recordingToken.status_code != 200:
        print('Could not get download token')
        return None
    recording_data_for_single_recording = resp_for_getting_a_recordingToken.json()      
    
    return recording_data_for_single_recording     

def test_get_recording_information_for_a_single_recording():
    recording_data = get_recording_information_for_a_single_recording('197294')
    print('recording_data is: ', recording_data)

def update_recording_information_for_all_local_database_recordings():
#     conn = get_database_connection()
    cur = get_database_connection().cursor()
    cur.execute("SELECT recording_id, recordingDateTime FROM recordings")
 
    rows = cur.fetchall()
 
    for row in rows:
        # Don't update if we already have recordingDateTime
        recordingDateTime = row[1]
        if not recordingDateTime:
            print(recordingDateTime, ' is empty so will update record')
            recording_id = row[0]
            update_recording_information_for_single_recording(recording_id)
        print('Finished updating recording information')
    
def test_update_recording_information_for_all_local_database_recordings():
    update_recording_information_for_all_local_database_recordings()

def get_audio_recordings_with_tags_information_from_server(user_token, recording_type, deviceId):
    print('Retrieving recordings basic information from Cacophony Server\n')
    url = server_endpoint + query_available_recordings
    
    where_param = {}
    where_param['type'] = recording_type    
    where_param['DeviceId'] = deviceId
    json_where_param = json.dumps(where_param)
    querystring = {"tagMode":"tagged", "where":json_where_param}    
    headers = {'Authorization': user_token}  

    resp = requests.request("GET", url, headers=headers, params=querystring)
   
    if resp.status_code != 200:
        # This means something went wrong.
        print('Error from server is: ', resp.text)
        sys.exit('Could not download file - exiting')    
        
    
    data = resp.json()
   
    recordings = data['rows']
    
    return recordings   

def test_get_audio_recordings_with_tags_information_from_server():
    user_token = get_cacophony_user_token()
    recording_type = 'audio'
    deviceId = 379
    recordings = get_audio_recordings_with_tags_information_from_server(user_token, recording_type, str(deviceId))
    for recording in recordings:
        print(recording, '\n')

def get_and_store_tag_information_for_recording(recording_id, deviceId, device_name, device_super_name):
    single_recording_full_information = get_recording_information_for_a_single_recording(recording_id)
    recording = single_recording_full_information['recording']  
    tags = recording['Tags']   
    for tag in tags:
        server_Id = tag['id']
        what = tag['what']
        detail = tag['detail']
        confidence = tag['confidence']
        startTime = tag['startTime']
        duration = tag['duration']
        automatic = tag['automatic']
        version = tag['version']
        createdAt = tag['createdAt']
        tagger =tag['tagger']        
        tagger_username = tagger['username']
        what = tag['what']
        insert_tag_into_database(recording_id,server_Id, what, detail, confidence, startTime, duration, automatic, version, createdAt, tagger_username, deviceId, device_name, device_super_name)
    
    
def test_get_and_store_tag_information_for_recording():
    get_and_store_tag_information_for_recording(str(197294), 123)
    
def insert_tag_into_database(recording_id,server_Id, what, detail, confidence, startTime, duration, automatic, version, createdAt, tagger_username, deviceId, device_name, device_super_name ):
    # Use this for tags that have been downloaded from the server
    try:
        if check_if_tag_alredy_in_database(server_Id) == True:
            print('tag exists')
            return
        else:
            print('going to insert tag')

        sql = ''' INSERT INTO tags(recording_id,server_Id, what, detail, confidence, startTime, duration, automatic, version, createdAt, tagger_username, deviceId, device_name, device_super_name)
                  VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
        cur = get_database_connection().cursor()
        cur.execute(sql, (recording_id,server_Id, what, detail, confidence, startTime, duration, automatic, version, createdAt, tagger_username, deviceId, device_name, device_super_name))
        get_database_connection().commit()
    except Exception as e:
        print(e, '\n')
        print('\t\tUnable to insert tag ' + str(recording_id), '\n')   
        
def insert_locally_created_tag_into_database(recording_id,what, detail, confidence, startTime, duration, createdAt, tagger_username, deviceId, device_name, device_super_name ):
    # Use this is the tag was created in this application, rather than being downloaded from the server - becuase some fiels are mission e.g. server_Id
    try:        

        sql = ''' INSERT INTO tags(recording_id, what, detail, confidence, startTime, duration, createdAt, tagger_username, deviceId, device_name, device_super_name)
                  VALUES(?,?,?,?,?,?,?,?,?,?,?) '''
        cur = get_database_connection().cursor()
        cur.execute(sql, (recording_id, what, detail, confidence, startTime, duration, createdAt, tagger_username, deviceId, device_name, device_super_name))
        get_database_connection().commit()
    except Exception as e:
        print(e, '\n')
        print('\t\tUnable to insert tag ' + str(recording_id), '\n')   
       
def test_insert_tag_into_database():
    insert_tag_into_database(1,135940, 'bat', 'detail', 'confidence', 1.2, 2.5, 'automatic', 256, '2019-06-20T04:14:24.811Z', 'timhot', 'deviceId', 'device_name', 'device_super_name')
    
def check_if_tag_alredy_in_database(server_Id):
    cur = get_database_connection().cursor()
    cur.execute("SELECT server_Id FROM tags WHERE server_Id = ?", (server_Id,))
    data=cur.fetchone()
    if data is None:
        return False
    else:
        return True

def test_check_if_tag_alredy_in_database(): 
    check_if_tag_alredy_in_database(135939)  
 
def get_all_tags_for_all_devices_in_local_database():
    user_token = get_cacophony_user_token()
    unique_devices = get_unique_devices_stored_locally()

    for unique_device in unique_devices:  
        deviceId = unique_device[0]
        device_name = unique_device[1]
        device_super_name = unique_device[2]        
      
        recording_type = 'audio'
        recordings_with_tags = get_audio_recordings_with_tags_information_from_server(user_token, recording_type, deviceId)

        for recording_with_tag in recordings_with_tags:
            print('device is', deviceId, '\n') 
            recording_id =recording_with_tag['id']
            print('recording_id ', recording_id, '\n')
            get_and_store_tag_information_for_recording(str(recording_id), deviceId, device_name, device_super_name)
    print('Finished getting tags from server')
            
def test_get_all_tags_for_all_devices_in_local_database():
    get_all_tags_for_all_devices_in_local_database()            
     
def get_unique_devices_stored_locally():
    cur = get_database_connection().cursor()
    cur.execute("SELECT DISTINCT deviceId, device_name, device_super_name FROM recordings") 
    rows = cur.fetchall()
    return rows   
    
     
def test_get_unique_devices_stored_locally():
    unique_devices = get_unique_devices_stored_locally()
    for unique_device in unique_devices:
        print(unique_device, '\n')
        
def get_onsets_stored_locally():
    cur = get_database_connection().cursor()
    cur.execute("SELECT version, recording_id, start_time_seconds, duration_seconds FROM onsets WHERE version = ?", (version)) 
    rows = cur.fetchall()
    return rows 

def test_get_onsets_stored_locally():
    onsets = get_onsets_stored_locally()
    for onset in onsets:
        print(onset) 
    
def scan_local_folder_for_recordings_not_in_local_db_and_update(device_name, device_super_name):
    recordings_folder = getRecordingsFolder()
    for filename in os.listdir(recordings_folder):
        recording_id = filename.replace('-','.').split('.')[0]
        print(recording_id)
        cur = get_database_connection().cursor()
        cur.execute("SELECT * FROM recordings WHERE recording_id = ?",(recording_id,))
        
        # https://stackoverflow.com/questions/16561362/python-how-to-check-if-a-result-set-is-empty
        row = cur.fetchone()
        if row == None:
           # Get the information for this recording from server and insert into local db
    #            update_recording_information_for_single_recording(recording_id)
            filename = recording_id + '.m4a'
            insert_recording_into_database(recording_id,filename, device_name,device_super_name) # The device name will be updated next when getting infor from server
            # Now update this recording with information from server
            update_recording_information_for_single_recording(recording_id)
        
def test_scan_local_folder_for_recordings_not_in_local_db_and_update():
    scan_local_folder_for_recordings_not_in_local_db_and_update('grants shed')
           
def create_tags_from_folder_of_unknown_images():
    # This will probably only get used to recreate the unknown tags from the unknown images - as I'm not sure where the text file of this is/exists
    home = str(Path.home())
    unknown_images_folder =  home + '/Work/Cacophony/images/unknown'
    for filename in os.listdir(unknown_images_folder):
        fileparts = filename.replace('_','.').split('.')
        recording_id = fileparts[0]
        print('recording_id ', recording_id)
        startWholeSecond = fileparts[1]
        print('startWholeSecond ', startWholeSecond)
        startPartSecond = fileparts[2]
        print('startPartSecond ', startPartSecond)
        startTimeSeconds = startWholeSecond + '.' + startPartSecond
        insert_locally_created_tag_into_database(recording_id=recording_id, what='unknown', detail=None, confidence=None, startTime=startTimeSeconds, duration=1.5, createdAt='2019-06-20T05:39:28.391Z', tagger_username='timhot', deviceId=378, device_name='fpF7B9AFNn6hvfVgdrJB', device_super_name='Hammond Park')
    print('Finished creating unknown tags from image files')
    
def test_create_tags_from_folder_of_unknown_images():
    create_tags_from_folder_of_unknown_images()
    
def update_local_tags_with_version():
    # This is probably only used the once to modify intial rows to indicate they are from my first morepork tagging of Hammond Park
    cur = get_database_connection().cursor()
    cur.execute("select ID from tags")
 
    rows = cur.fetchall()     
 
    for row in rows:              
        ID =  row[0] 
        print('ID ', ID) 
        sql = ''' UPDATE tags
                  SET version = ?               
                  WHERE ID = ?'''
        cur = get_database_connection().cursor()
        cur.execute(sql, ('morepork_base', ID))
    
    get_database_connection().commit()    
    
def test_update_local_tags_with_version():
    update_local_tags_with_version()
    

    
# def create_clips(device_super_name, what, version, clips_ouput_folder):
def create_clips(device_super_name, what, version, run_base_folder, run_folder):
    print(device_super_name, what, version, run_base_folder, run_folder) 
#     what_without_spaces = re.sub(' ', '', what)
#     what_without_spaces_dashes = re.sub('-', '_', what_without_spaces) 
#     clips_ouput_folder = run_base_folder + '/' + run_folder + '/' + 'audio_clips' + '/' + what_without_spaces_dashes
# 
#     
#     sql = ''' SELECT recording_Id, startTime, duration FROM tags WHERE device_super_name=? AND what=? AND version=? '''          
#     cur = get_database_connection().cursor()
#     cur.execute(sql, (device_super_name, what, version,)) 
#     rows = cur.fetchall()  
#     
#     count = 0
#  
#     for row in rows: 
#         print('Creating clip ', count, ' of ', len(rows))
#         recording_Id = row[0]
#         start_time_seconds = row[1]
#         duration_seconds = row[2]
#         create_wav_clip(recording_Id, start_time_seconds, duration_seconds, clips_ouput_folder)   
#         count = count + 1     
    
def create_wav_clip(recording_Id, start_time_seconds, duration_seconds, clips_ouput_folder):
    print(recording_Id)
    audio_in_path = getRecordingsFolder() + '/' + str(recording_Id) + '.m4a'
#     audio_out_folder = getRecordingsFolder() + '/' + what
    if not os.path.exists(clips_ouput_folder):
#         os.mkdir(clips_ouput_folder)
        os.makedirs(clips_ouput_folder)    
    
    audio_out_path = clips_ouput_folder + '/' + str(recording_Id) + '_' + str(start_time_seconds) + '_' + str(duration_seconds) + '.wav'
#     print('audio_in_path ', audio_in_path)
#     print('audio_out_path ', audio_out_path)
#     if not os.path.exists(audio_in_path):
#         print('Can not find ', audio_in_path)
#     else:
#         print('Found it')
        
    create_wav(audio_in_path, audio_out_path, start_time_seconds, duration_seconds)
     
        
def create_folder(folder_to_create):
    if folder_to_create is None:
        print("Please enter a folder name")
        return
    if not folder_to_create:
        print("Please enter a folder name")
        return
    
    if not os.path.exists(folder_to_create):
        os.mkdir(folder_to_create)
        print("Folder " , folder_to_create ,  " Created ")    
    
      


            
def run_processDir():
    processDir(search_path,arff_path)
    
    
def create_wav(audio_in_path, audio_out_path, start_time_seconds, duration_seconds): 
    print('start_time_seconds ', start_time_seconds) 
    print('duration_seconds ', duration_seconds)  
    y, sr = librosa.load(audio_in_path) 
    
    clip_start_array = int((sr * start_time_seconds))
    print('clip_start_array ', clip_start_array)
    clip_end_array = clip_start_array + int((sr * duration_seconds))    
 
     
    if clip_end_array > y.shape[0]:
        print('Clip would end after end of recording')
        return
     
    clip_call_by_array = y[clip_start_array:clip_end_array]  
     
     
 
     
    #Save the file 
#     wavfile.write(filename=audio_out_path, rate=sr, data=clip_call_by_array)
#     sf.write(file, data, samplerate, subtype, endian, format, closefd)
#     sf.write(file=audio_out_path, data=clip_call_by_array, samplerate=sr, subtype, endian, format, closefd)
    # https://pysoundfile.readthedocs.io/en/0.9.0/
    sf.write(audio_out_path, clip_call_by_array, sr, 'PCM_24')
#     sf.write(audio_out_path, y, sr, 'PCM_24')      
    

#     run_processDir()


def test_create_wav():
    create_wav('/home/tim/Work/Cacophony/opensmile_weka/m4a_files/161945.m4a', '/home/tim/Work/Cacophony/opensmile_weka/TestAudioInput/161945.wav')  
    create_wav('/home/tim/Work/Cacophony/opensmile_weka/m4a_files/161946.m4a', '/home/tim/Work/Cacophony/opensmile_weka/TestAudioInput/161946.wav')  
    processDir(search_path,arff_path)

        
def create_arff_file(base_folder, run_folder, clip_folder, openSmile_config_file):
    clip_folder_without_spaces = re.sub(' ', '_', clip_folder)
    print('base_folder ', base_folder)
    cwd = os.getcwd()
       
    openSmile_config_file_template = cwd + '/template_files/openSmile_config_files/' + openSmile_config_file
    print('openSmile_config_file_template ', openSmile_config_file_template)
    openSmile_config_file_for_this_run = base_folder + '/' + run_folder + '/' + openSmile_config_file
    print('openSmile_config_file_for_this_run ', openSmile_config_file_for_this_run)
    shutil.copy2(openSmile_config_file_template, openSmile_config_file_for_this_run)
    
#     arff_template_file_path = cwd + '/template_files/' + arff_template_file
#     arff_template_file_for_this_run = base_folder + '/' + run_folder + '/' + arff_template_file
#     shutil.copy2(arff_template_file_path, arff_template_file_for_this_run)
    
    print('clip_folder', clip_folder_without_spaces)
   
    
    searchDir = base_folder + '/' + run_folder + '/audio_clips/' + clip_folder_without_spaces
    arffDir = base_folder + '/' + run_folder + '/arff_files' 
    if not os.path.exists(arffDir):
        os.mkdir(arffDir)
    
    print('searchDir', searchDir)
    print('arffDir', arffDir)
    
    processDir(searchDir, arffDir, openSmile_config_file_for_this_run)
    
# First version written by Jonah Dearden
def processDir( searchDir, arffDir, openSmile_config_file_for_this_run):
    print('openSmile_config_file_for_this_run ', openSmile_config_file_for_this_run)
    
    os.chdir(searchDir)
    i=0
    list_of_files=[]
    # https://www.tutorialspoint.com/python/os_walk.htm
    for root,dir,files in os.walk(searchDir):
        for f in files:
            if re.match(r'.*\.wav',f):
                list_of_files.append(root+'/'+f)
                
    os.chdir(arffDir)
    
    for i in list_of_files: 
        print(i)
    
    print('openSmile_config_file_for_this_run ', openSmile_config_file_for_this_run)
    
    for i in list_of_files:     
        name1=re.sub(r'(' + searchDir + '/)(.*)(\.wav)',r'\2',i)
        os.system('SMILExtract -C ' + openSmile_config_file_for_this_run + ' -I '+i+' -O '+arffDir+'/'+name1+'.mfcc.arff')
 

       
def merge_arffs(base_folder, run_folder, arff_template_file):
    #path to directory with arffs
    arffDir = base_folder + '/' + run_folder + '/arff_files'
    arrf_filename = re.sub('_template', '', arff_template_file)
    cwd = os.getcwd()
    arff_template_file_path = cwd + '/template_files/arff_template_files/' + arff_template_file
    arff_template_file_for_this_run = base_folder + '/' + run_folder + '/arff_files/' + arrf_filename
    shutil.copy2(arff_template_file_path, arff_template_file_for_this_run)
    
    os.chdir(arffDir)
    
    counter = 0

    #Opens joinedArff.arff and appends
    with open(arrf_filename, "a") as f:
        #for each file with the .arff ext in the directroy
        for file in glob.glob("*.arff"):
            #Open the file and read line 996
            print(file)
            a = open(file, "r")
            lines = a.readlines()
    
            x = lines[995]
            #Replace class label if necessary
            #This is unnecessary if you have already assigned the classes using the OpenSmile conf.
            #x = x.replace("unknown", "person")
            #Writes that line to the joinedArff file
            f.write(x + "\n")
            a.close()
    
    f.close()   
    
    arff_template_file_for_this_run_in_run_folder = base_folder + '/' + run_folder + '/' + arrf_filename
#     os.rename(arff_template_file_for_this_run, arff_template_file_for_this_run_in_run_folder)
    shutil.move(arff_template_file_for_this_run, arff_template_file_for_this_run_in_run_folder)
    
    print('Merged arff file created in ', base_folder, '/',run_folder)
    
def get_unique_whats_from_local_db():
    cur = get_database_connection().cursor()
    cur.execute("SELECT DISTINCT what FROM tags") 
    rows = cur.fetchall()  
    
    unique_whats = []
    for row in rows:
         unique_whats.append(row[0])
    return unique_whats  

def getOpenSmileConfigFiles():
    cwd = os.getcwd()
    openSmileConfigFileDir = cwd + '/template_files/openSmile_config_files/'
    openSmileConfigFiles = []
    for file in os.listdir(openSmileConfigFileDir):
        openSmileConfigFiles.append(file)        
   
    return openSmileConfigFiles
    
def getArffTemplateFiles():
    cwd = os.getcwd()
    arrTemplateFileDir = cwd + '/template_files/arff_template_files/'

    arffTemplateFiles = []
    for file in os.listdir(arrTemplateFileDir):
#         print(file)
        arffTemplateFiles.append(file)        
   
    return arffTemplateFiles     



def choose_clip_folder(base_folder, run_folder):
    start_folder = base_folder + '/' + run_folder + '/audio_clips/'
    clip_folder = filedialog.askdirectory(initialdir=start_folder,  title = "Open the folder you want (Just selecting it won't choose it)")
    parts = re.split('/', clip_folder)
    clip_folder =  parts[len(parts)-1]     
    return clip_folder      

def run_model(model_folder):
    #https://stackoverflow.com/questions/21406887/subprocess-changing-directory
    # https://stackoverflow.com/questions/1996518/retrieving-the-output-of-subprocess-call

    os.chdir(model_folder)  
    command = ['java', '-jar', 'run.jar', 'shell=True']    
    
    result = run(command, stdout=PIPE, stderr=PIPE, text=True)
#     if result.returncode == 0:
#         return result.stdout
#     else:
#         return result.stderr
    return result


def test_run_model():
    base_folder = '/home/tim/Work/Cacophony/Audio_Analysis/audio_classifier_runs'
    run_folder = '2019_09_17_1'
    model_folder = base_folder + '/' + run_folder + '/model_run'
    
    result = run_model(model_folder)
    if result.returncode == 0:
        print(result.stdout)
    else:
        print(result.stderr)
    
#     print(run_model(model_folder) )   
    
def process_arff_folder(base_folder, run_folder, arff_files, modelRunName):
    folder_to_process = base_folder + '/' + run_folder + '/' + arff_files
    model_folder = base_folder + '/' + run_folder + '/model_run'
    for arffFile in os.listdir(folder_to_process):
        try:
            fileparts = arffFile.replace('_','.').split('.')
            recording_id = fileparts[0]       
            startTime = fileparts[1] + '.' + fileparts[2]       
            duration = fileparts[3] + '.' + fileparts[4]    
            
            arff_input_file = folder_to_process + '/' + arffFile
            arff_file_in_model_folder = model_folder + '/input.arff'       
            shutil.copy(arff_input_file, arff_file_in_model_folder)
            prediction = run_model(model_folder)
            if prediction.returncode == 0:
                model_prediction = json.loads(prediction.stdout)
                actual = model_prediction.get('actual')
                predictedByModel = model_prediction.get('predicted')
                print(prediction.stdout)
                print('actual ', actual)
                print('predictedByModel ', predictedByModel)
                
                insert_model_run_result_into_database(modelRunName, recording_id, startTime, duration, actual, predictedByModel)
#                 send2trash.send2trash(arff_input_file)
            else:
                print(prediction.stderr)
        except Exception as e:
            print(e, '\n')
    print('Finished processing arff folder')   
        
            
    
       
def test_process_arff_folder():
    base_folder = '/home/tim/Work/Cacophony/Audio_Analysis/audio_classifier_runs'
    run_folder = '2019_09_17_1'
    arff_files_to_process = 'arff_files_to_process'
    modelRunName = '2019_09_17_1'
    process_arff_folder(base_folder, run_folder, arff_files_to_process, modelRunName)
    
def insert_model_run_result_into_database(modelRunName, recording_id, startTime, duration, actual, predictedByModel):
    # Use this for tags that have been downloaded from the server
    try:
        sql = ''' INSERT INTO model_run_result(modelRunName, recording_id, startTime, duration, actual, predictedByModel)
                  VALUES(?,?,?,?,?,?) '''
        cur = get_database_connection().cursor()
        cur.execute(sql, (modelRunName, recording_id, startTime, duration, actual, predictedByModel))
        get_database_connection().commit()
    except Exception as e:
        print(e, '\n')
        print('\t\tUnable to insert result' + str(recording_id) + ' ' + str(startTime), '\n')   
        
def play_clip(recording_id, start_time, duration):
    audio_in_path = getRecordingsFolder() + '/' + recording_id + '.m4a'
    audio_out_path = '/home/tim/Temp/temp.wav'
#     audio_in_path = '/home/tim/Temp/dog.wav'
    print('audio_in_path ', audio_in_path)
#     playsound(audio_in_path)
#     song = AudioSegment.from_wav(audio_in_path)
#     play(song)
#     os.system("play " + audio_in_path)

   
    y, sr = librosa.load(audio_in_path, sr=None) 
    
#     print('sr ', sr)
#     print(y)
#     print(y.shape)
    y_amplified = np.int16(y/np.max(np.abs(y)) * 32767)
    print(y_amplified)
    y_amplified_start = sr * start_time
    y_amplified_end = y_amplified_start + (sr * duration)
    y_amplified_to_play = y_amplified[int(y_amplified_start):int(y_amplified_end)]
    y_to_play = y[int(y_amplified_start):int(y_amplified_end)]
#     librosa.output.write_wav(audio_out_path, y_amplified_to_play, sr)
    os.system("play " + audio_out_path)
# #     sd.play(y_amplified_to_play, sr)
# #     sd.play(y_amplified, sr)
#     sd.play(y, sr)
    print('finished')
    
def play_clip2():
    start_time = 18
    duration = 2
    audio_in_path = getRecordingsFolder() + '/218113.m4a'
    audio_out_path = '/home/tim/Temp/temp.wav'
    y, sr = librosa.load(audio_in_path, sr=None) 
    y_amplified = np.int16(y/np.max(np.abs(y)) * 32767)
    y_amplified_start = sr * start_time
    y_amplified_end = (sr * start_time) + (sr * duration)
    y_amplified_to_play = y_amplified[int(y_amplified_start):int(y_amplified_end)]
    y_to_play = y[int(y_amplified_start):int(y_amplified_end)]
#     sf.write(audio_out_path, y_to_play, sr, 'PCM_24')
    sf.write(audio_out_path, y_to_play, sr)
    os.system("play " + audio_out_path)
    
def play_clip3():
    start_time = 14.5
    duration = 1.5
    audio_in_path = getRecordingsFolder() + '/218113.m4a'
    audio_out_path = '/home/tim/Temp/temp.wav'
    y, sr = librosa.load(audio_in_path, sr=None) 
    y_amplified = np.int16(y/np.max(np.abs(y)) * 32767)
    y_amplified_start = sr * start_time
    y_amplified_end = (sr * start_time) + (sr * duration)
    y_amplified_to_play = y_amplified[int(y_amplified_start):int(y_amplified_end)]
#     y_to_play = y[int(y_amplified_start):int(y_amplified_end)]
    sf.write(audio_out_path, y_amplified_to_play, sr)
    song = AudioSegment.from_wav(audio_out_path)
    play(song)  
    
def play_clip4():
    start_time = 17
    duration = 3
    audio_in_path = getRecordingsFolder() + '/218113.m4a'
    audio_out_path = '/home/tim/Temp/temp.wav'
    y, sr = librosa.load(audio_in_path, sr=None) 
    y_amplified = np.int16(y/np.max(np.abs(y)) * 32767)
    y_amplified_start = sr * start_time
    y_amplified_end = (sr * start_time) + (sr * duration)
#     y_amplified_to_play = y_amplified[int(y_amplified_start):int(y_amplified_end)]
    y_to_play = y[int(y_amplified_start):int(y_amplified_end)]
    sd.play(y, 44100)
    
    
def test_play_clip():
#     play_clip('218113', 4.5, 1.5)
    play_clip2()
    
def create_arff_file_headder(output_folder, arff_filename, comments, relation, attribute_labels, attribute_features): 
   
         
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  
        
    output_path_filename = output_folder + "/" + arff_filename
        
    f= open(output_path_filename,"w+")   
    f.write(comments)
    f.write("\n") 
    f.write(relation)
    f.write("\n") 
    f.write("\n") 
    for attribute_label in attribute_labels:
        f.write(attribute_label)
        f.write("\n")   
    for attribute_feature in attribute_features:
        f.write(attribute_feature)
        f.write("\n")   
        
    f.write("\n")    
    
    f.write("@data")  
    f.write("\n")  
    f.write("\n")  
        
    f.close()
    
        
def test_create_arff_file_header():
    run_base_folder = "/home/tim/Work/Cacophony/Audio_Analysis/audio_classifier_runs"
    run_folder = "/test_run"
    arff_filename = "test_arff.arff"
    arff_output_folder = "/arff_folder"
    output_folder = run_base_folder + run_folder + arff_output_folder
    comments = "% Multi-label test"
    relation = "@relation \'Audio: -C 3\'"
    attribute_labels = []
    attribute_labels.append("@attribute morepork-classic {0,1}")
    attribute_labels.append("@attribute cicada {0,1}")
    attribute_labels.append("@attribute dog {0,1}")
    
    attribute_features = []
    attribute_features.append("@attribute mel1 numeric")
    attribute_features.append("@attribute mel2 numeric")
    
    
    create_arff_file_headder(output_folder, arff_filename, comments, relation, attribute_labels, attribute_features)

def append_data_to_arff_file(output_path_filename, data):
    f=open(output_path_filename, "a")    
    
    for line in data:
        f.write(line)
        f.write("\n")  
        
    f.close()
        
def test_append_data_to_arff_file():
    run_base_folder = "/home/tim/Work/Cacophony/Audio_Analysis/audio_classifier_runs"
    run_folder = "/test_run"
    arff_filename = "test_arff.arff"
    arff_output_folder = "/arff_folder"
    output_folder = run_base_folder + run_folder + arff_output_folder
    output_path_filename = output_folder + "/" + arff_filename
    
    data = []
      
    data.append("0,1,1,0.9,0.7")
    data.append("0,1,0,0.6,0.7")
    data.append("0,0,1,0.1,0.3")
    append_data_to_arff_file(output_path_filename, data)
        

    
# #https://dsp.stackexchange.com/questions/41184/high-pass-filter-in-python-scipy/41185#41185
# def highpass_filter_with_parameters(y, sr, filter_stop_freq, filter_pass_freq ):
#     filter_order = 1001
# 
#     # High-pass filter
#     nyquist_rate = sr / 2.
#     desired = (0, 0, 1, 1)
#     bands = (0, filter_stop_freq, filter_pass_freq, nyquist_rate)
#     filter_coefs = signal.firls(filter_order, bands, desired, nyq=nyquist_rate)
#     
#     # Apply high-pass filter
#     filtered_audio = signal.filtfilt(filter_coefs, [1], y)
#     return filtered_audio
# 
# # https://stackoverflow.com/questions/25191620/creating-lowpass-filter-in-scipy-understanding-methods-and-units
# def butter_lowpass(cutoff, fs, order=5):
#     nyq = 0.5 * fs
#     normal_cutoff = cutoff / nyq
#     b, a = butter(order, normal_cutoff, btype='low', analog=False)
#     return b, a
# 
# def butter_lowpass_filter(data, cutoff, fs, order=5):
#     b, a = butter_lowpass(cutoff, fs, order=order)
#     y = lfilter(b, a, data)
#     return y
# 
# def apply_lowpass_filter(y, sr):
#     # Filter requirements.
#     order = 6
#    
#     cutoff = 1000  # desired cutoff frequency of the filter, Hz
#     
#     y = butter_lowpass_filter(y, cutoff, sr, order)
#     
#     return y
# def apply_band_pass_filter(y, sr):
#     y = highpass_filter_with_parameters(y=y, sr=sr, filter_stop_freq=750, filter_pass_freq=800 )
#     y = apply_lowpass_filter(y, sr)    
#     return y

# def extract_melspectrogram(audio_in):
# #     y, sr = librosa.load(audio_in, res_type='kaiser_fast') 
# #     y, sr = librosa.load(audio_in, mono=True, duration=30)
#     y, sr = librosa.load(audio_in, mono=True, duration=3) 
# #     y_filtered = apply_band_pass_filter(y, sr)
# #     y = apply_band_pass_filter(y, sr)
#     print(sr)
#     print("\n")
# #     print(y)
# #     mel_spectrogram = librosa.feature.melspectrogram(y=y_filtered, sr=sr, fmin=100, fmax=2000)
# #     mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
# #     mel_spectrogram = librosa.feature.melspectrogram(y=y_filtered, sr=sr)
# 
# #     mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, fmin=500, fmax=1000)
# #     mel_spectrogram_800_1000_freq = librosa.feature.melspectrogram(y=y_part, sr=sr, n_fft=int(sr/10), hop_length=int(sr/10), n_mels=10, fmin=800,fmax=1000)
#     mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=int(sr/10), hop_length=int(sr/10), n_mels=10, fmin=600,fmax=1000)
#     print("mel_spectrogram \n")
#     print(mel_spectrogram.shape)
#     np.set_printoptions(threshold=np.inf)
#     print(mel_spectrogram)
#     
#    
# #     librosa.display.specshow(mel_spectrogram, x_axis='time', y_axis='mel', sr=sr,fmax=2000)
#     librosa.display.specshow(mel_spectrogram, x_axis='time', y_axis='mel')
#     plt.colorbar(format='%+2.0f dB')
#     plt.title('Mel-frequency spectrogram')
#     plt.tight_layout()
#     plt.show()
    
# def test_extract_melspectrogram():
#     audio_in = "/home/tim/Work/Cacophony/Audio_Analysis/temp/235980.m4a"
#     extract_melspectrogram(audio_in)   


def fingerprint():
    duration, fp_encoded = acoustid.fingerprint_file("/home/tim/Work/Cacophony/Audio_Analysis/temp/morepork.mp3")
    fingerprint, version = chromaprint.decode_fingerprint(fp_encoded)
    print(fingerprint)
    
#     fig = plt.figure()
#     bitmap = np.transpose(np.array([[b == '1' for b in list('{:32b}'.format(i & 0xffffffff))] for i in fingerprint]))
#     plt.imshow(bitmap)

    librosa.display.specshow(fingerprint)
#     plt.colorbar(format='%+2.0f dB')
    plt.title('Finger print')
    plt.tight_layout()
    plt.show()
    
def test_fingerprint():
    fingerprint()
    
def featureExtraction():
    w = pywt.Wavelet('db3')
    print(w)
    
def test_featureExtraction():
    featureExtraction()
    
# def pyAudioAnalysisFeatureExtraction():
#     audio_in = "/home/tim/Work/Cacophony/Audio_Analysis/temp/235980.m4a"
#     y, sr = librosa.load(audio_in, mono=True, duration=3) 
#     F, f_names = audioFeatureExtraction.stFeatureExtraction(y, sr, 0.050*sr, 0.025*sr);
#     print(f_names)
#     print(F[1])
#     
#     mt_features, st_features, mid_feature_names = audioFeatureExtraction.mtFeatureExtraction(y, ar, mt_win, mt_step, st_win, st_step)
#     
# def test_pyAudioAnalysisFeatureExtraction():
#     pyAudioAnalysisFeatureExtraction()
    
def librosaFeatureExtraction():
    audio_in = "/home/tim/Work/Cacophony/Audio_Analysis/temp/235980.m4a"
    y, sr = librosa.load(audio_in, mono=True) 
#     tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units="time")
#     print(tempo)
#     print(beats)    
    S = np.abs(librosa.stft(y))
    comps, acts = librosa.decompose.decompose(S, n_components=1)
    np.set_printoptions(threshold=np.inf)
    print(comps)
#     print(acts)
    
   
def test_librosaFeatureExtraction():
    librosaFeatureExtraction()
    
def create_onsets():
    print("create_onsets")
    create_squawk_pairs(base_folder, downloaded_recordings_folder, run_folder)
    

def insert_onset_into_database(version, recording_id, start_time_seconds, duration_seconds):
    # Use this is the tag was created in this application, rather than being downloaded from the server - becuase some fiels are mission e.g. server_Id
    try:     
        sql = ''' INSERT INTO onsets(version, recording_id, start_time_seconds, duration_seconds)
                  VALUES(?,?,?,?) '''
        cur = get_database_connection().cursor()
        cur.execute(sql, (version, recording_id, start_time_seconds, duration_seconds))
        get_database_connection().commit()
    except Exception as e:
        print(e, '\n')
        print('\t\tUnable to insert onest ' + str(recording_id), '\n')   
       
def test_insert_onset_into_database():
    insert_onset_into_database('Analysis_5', 1234, 3.2, 0.6)
    

# https://stackoverflow.com/questions/25191620/creating-lowpass-filter-in-scipy-understanding-methods-and-units
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def apply_lowpass_filter(y, sr):
    # Filter requirements.
    order = 6
   
#     cutoff = 1000  # desired cutoff frequency of the filter, Hz
    cutoff = 900  # desired cutoff frequency of the filter, Hz
    
    y = butter_lowpass_filter(y, cutoff, sr, order)
    
    return y
    


#https://dsp.stackexchange.com/questions/41184/high-pass-filter-in-python-scipy/41185#41185
def highpass_filter_with_parameters(y, sr, filter_stop_freq, filter_pass_freq ):
  
  filter_order = 1001

  # High-pass filter
  nyquist_rate = sr / 2.
  desired = (0, 0, 1, 1)
  bands = (0, filter_stop_freq, filter_pass_freq, nyquist_rate)
  filter_coefs = signal.firls(filter_order, bands, desired, nyq=nyquist_rate)

  # Apply high-pass filter
  filtered_audio = signal.filtfilt(filter_coefs, [1], y)
  return filtered_audio
    
# def test_lowpass_filter():
#     filename = '153003.m4a'
#     audio_in_path = './' + parameters.downloaded_recordings_folder + '/' + str(filename) 
#     y, sr = librosa.load(audio_in_path, sr=None)
#     plot_mel_scaled_power_spectrogram (y, sr)
#     y = apply_lowpass_filter(y, sr)
#     plot_mel_scaled_power_spectrogram (y, sr)
    
def apply_band_pass_filter(y, sr):
#    y = highpass_filter(y, sr)
#     y = highpass_filter_with_parameters(y=y, sr=sr, filter_stop_freq=750, filter_pass_freq=800 )
#     y = highpass_filter_with_parameters(y=y, sr=sr, filter_stop_freq=700, filter_pass_freq=750 )
    y = highpass_filter_with_parameters(y=y, sr=sr, filter_stop_freq=600, filter_pass_freq=650 )
    y = apply_lowpass_filter(y, sr)    
    return y
    

    
def create_squawk_pairs(base_folder, recordings_folder, run_folder):
#     inputFolder = base_folder + '/' + recordings_to_process_folder
#     onset_pairs_output_folder = base_folder + '/' + run_folder + '/' + onset_pairs_folder
    recordings_folder_with_path = base_folder + '/' + recordings_folder
    
#     if not os.path.exists(onset_pairs_output_folder):
#         os.makedirs(onset_pairs_output_folder)
   
    count_of_onset_pairs_including_more_than_20 = 0
    count_of_onset_pairs_including_not_including_more_20 = 0
    
    count = 0
    total_number_of_files = len(os.listdir(recordings_folder_with_path))
#    for filename in os.listdir(input_folder):
    with os.scandir(recordings_folder_with_path) as entries:
        for entry in entries:
            try:
                print(entry.name)
                if entry.is_file():                  
                    filename = entry.name
                else:
                    continue
            
                count+=1
                print('Processing file ', count, ' of ', total_number_of_files, ' files.')
        #    filename = '225217.wav'
           
                audio_in_path = recordings_folder_with_path + "/" + filename
                
                y, sr = librosa.load(audio_in_path)
                y = apply_band_pass_filter(y, sr)            
            
                paired_squawks_sec = find_paired_squawks_in_single_recordings(y, sr)
                #print('paired_squawks_sec', paired_squawks_sec)
                number_of_paired_squawks = len(paired_squawks_sec)
                if not number_of_paired_squawks == 0:
                    if number_of_paired_squawks > 20:
                        count_of_onset_pairs_including_more_than_20 += number_of_paired_squawks
                    else:
                        count_of_onset_pairs_including_more_than_20 += number_of_paired_squawks
                        count_of_onset_pairs_including_not_including_more_20 += number_of_paired_squawks                        
                   
                        recording_id = filename.split('.')[0]  
                        print('recording_id', recording_id)
#                         output_filename = onset_pairs_output_folder +'/' + filename.split('.')[0] + '.txt'
#                         print('output_filename', output_filename)
                       
#                         f = open(output_filename, 'w')
#                         json.dump(paired_squawks_sec, f)
#                         f.close()
                        
                        insert_paird_squawks_into_db(version, recording_id, paired_squawks_sec)
                        
                print('count_of_onset_pairs_including_more_than_20 ', count_of_onset_pairs_including_more_than_20)
                print('count_of_onset_pairs_including_not_including_more_20 ', count_of_onset_pairs_including_not_including_more_20)
        
            except Exception as e:
                print(e, '\n')
                print('Error processing file ', filename)
                
def insert_paird_squawks_into_db(version, recording_id, paired_squawks_sec):
    for paired_squawk_sec in paired_squawks_sec:
        print("paired_squawk_sec " , paired_squawk_sec)
    
    insert_onset_into_database(version, recording_id, paired_squawk_sec, squawk_duration_seconds)
                
def find_paired_squawks_in_single_recordings(y, sr):
#    y, sr = librosa.load(audio_in_path)
    squawks = FindSquawks(y, sr)
#    print('squawks ', squawks)
    squawks_secs = []
#    print(squawks)
    for squawk in squawks:
        squawk_start = squawk['start']
#        print('squawk_start ', squawk_start, '\n')
        squawk_start_sec = squawk_start / sr
#        print('squawk_start_sec ', squawk_start_sec, '\n\n')
        squawks_secs.append(round(squawk_start_sec, 1))
    
#    print('squawks ,' squawks, '\n')
    
    paired_squawks_sec = []
    prev_squawk_sec = None
    
    for squawk_sec in enumerate(squawks_secs):      
        if prev_squawk_sec == None:
            prev_squawk_sec = squawk_sec
            continue     
        
        time_between_squawks = squawk_sec[1] - prev_squawk_sec[1]
#        print('time_between_squawks ', time_between_squawks)
        
        if time_between_squawks < 0.8: # sr is one second, so hoping this is the second part of more pork
#            print('Going to keep squawk\n')
            paired_squawks_sec.append(prev_squawk_sec[1])
#        else:
#             print('Going to Disguard squawk\n')
        
        prev_squawk_sec = squawk_sec
        
    return paired_squawks_sec

def FindSquawks(source, sampleRate):
    result = []
    source = source / max(source)
    startIndex = None
    stopIndex = None
    smallTime = int(sampleRate*0.1)
    tolerance = 0.2
    for index in range(source.shape[0]):
        if not startIndex:
            if abs(source[index]) > tolerance:
                startIndex = index
                stopIndex = index
            continue
        if abs(source[index]) > tolerance:
            stopIndex = index
        elif index > stopIndex+smallTime:
            duration = (stopIndex-startIndex)/sampleRate
            if duration > 0.05:
                squawk = {'start': startIndex,
                          'stop': stopIndex, 'duration': duration}
                squawk['rms'] = rms(source[startIndex:stopIndex])
                result.append(squawk)
            startIndex = None
    return result

def rms(x):
        # Root-Mean-Square
    return np.sqrt(x.dot(x)/x.size)

def create_focused_mel_spectrogram_jps_using_onset_pairs():
#     onset_pairs_folder_path = base_folder + '/' + onset_pairs_folder
#     audio_files_input_folder_path = base_folder + '/' + audio_files_input_folder
    mel_spectrograms_out_folder_path = base_folder + '/' + run_folder + '/' + mel_spectrograms_folder 
    if not os.path.exists(mel_spectrograms_out_folder_path):
        os.makedirs(mel_spectrograms_out_folder_path)
       
    count = 0
#     total_number_of_files = len(os.listdir(onset_pairs_folder_path))

    onsets = get_onsets_stored_locally()   
       
    
#     for entry in os.scandir(onset_pairs_folder_path): 
    for onset in onsets:
        try:
            print('Processing onset ', count, ' of ', len(onsets), ' onsets.')
            count+=1
    
#                 duration_seconds = 1.5
            version_from_onset = onset[0] 
            recording_id = onset[1] 
            start_time_seconds = onset[2]
            duration_seconds = onset[3]
            
            audio_filename = str(recording_id) + '.m4a'
            audio_in_path = base_folder + '/' + downloaded_recordings_folder + '/' +  audio_filename 
            image_out_name = version_from_onset + '_' + str(recording_id) + '_' + str(start_time_seconds) + '_' + str(duration_seconds) + '.jpg'
            print('image_out_name', image_out_name)           
           
            image_out_path = mel_spectrograms_out_folder_path + '/' + image_out_name
            
            y, sr = librosa.load(audio_in_path, sr=None) 
            
            start_time_seconds_float = float(start_time_seconds)            
            
            start_position_array = int(sr * start_time_seconds_float)              
                       
            end_position_array = start_position_array + int((sr * duration_seconds))
                       
            if end_position_array > y.shape[0]:
                print('Clip would end after end of recording')
                continue
                
            y_part = y[start_position_array:end_position_array]  
            #                 mel_spectrogram = librosa.feature.melspectrogram(y=y_part, sr=sr, n_fft=int(sr/10), hop_length=int(sr/10), n_mels=10, fmin=650,fmax=900)
            #                 mel_spectrogram = librosa.feature.melspectrogram(y=y_part, sr=sr, n_fft=int(sr/10), hop_length=int(sr/10), n_mels=10, fmin=650,fmax=900)
            mel_spectrogram = librosa.feature.melspectrogram(y=y_part, sr=sr, n_mels=32, fmin=650,fmax=900)
            
            pylab.axis('off') # no axis
            pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[]) # Remove the white edge
            librosa.display.specshow(mel_spectrogram, cmap='binary') #https://matplotlib.org/examples/color/colormaps_reference.html
            pylab.savefig(image_out_path, bbox_inches=None, pad_inches=0)
            pylab.close()
            
        except Exception as e:
            print(e, '\n')
            print('Error processing onset ', onset)
                







    


