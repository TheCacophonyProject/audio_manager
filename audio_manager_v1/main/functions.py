import main.parameters as parameters
from main.parameters import *

import sqlite3
from sqlite3 import Error
import requests
# import os
# import sys
import json
from pathlib import Path
from tkinter import filedialog
from tkinter import *
# import re
# from scipy.io import wavfile
# import shutil
# import send2trash
# import sounddevice as sd
# from pydub import AudioSegment
# from pydub.playback import play
# import librosa
import os
from scipy import signal
# from scipy.io import wavfile
from scipy.signal import butter, lfilter, freqz
import numpy as np
from scipy.ndimage.filters import maximum_filter
import pylab
import librosa.display
# import shlex
# import glob
import soundfile as sf
# import subprocess
from subprocess import PIPE, run
# from playsound import playsound
# from librosa.output import write_wav
from librosa import display, onset
# import matplotlib.pyplot as plt
# import acoustid
# import chromaprint
# from pyAudioAnalysis import audioBasicIO
# from pyAudioAnalysis import audioFeatureExtraction
# import pywt
# import shlex
from PIL import ImageTk,Image 


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
    url = server_endpoint + devices_endpoint
      
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
    global cacophony_user_token
    global cacophony_user_name
    global cacophony_user_password 
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



def update_recording_information_for_all_local_database_recordings():
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
       

def check_if_tag_alredy_in_database(server_Id):
    cur = get_database_connection().cursor()
    cur.execute("SELECT server_Id FROM tags WHERE server_Id = ?", (server_Id,))
    data=cur.fetchone()
    if data is None:
        return False
    else:
        return True


 
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
            
    
     
def get_unique_devices_stored_locally():
    cur = get_database_connection().cursor()
    cur.execute("SELECT DISTINCT deviceId, device_name, device_super_name FROM recordings") 
    rows = cur.fetchall()
    return rows   

def get_unique_recording_ids_that_have_been_tagged_with_this_tag_stored_locally(tag):
    print('tag', tag)
    cur = get_database_connection().cursor()
    cur.execute("SELECT DISTINCT recording_id FROM tags WHERE what = ?", (tag,)) 
    rows = cur.fetchall()
    return rows 


        
def get_onsets_stored_locally(onset_version):
    global version
    if onset_version:
        version_to_use = onset_version
    else:
        version_to_use = version
        
    cur = get_database_connection().cursor()
    cur.execute("SELECT version, recording_id, start_time_seconds, duration_seconds FROM onsets WHERE version = ? ORDER BY recording_id", (version_to_use)) 
    rows = cur.fetchall()
    return rows 


        
def get_model_run_results(modelRunName, actualFilter, actualConfirmedFilter, predictedFilter):        
    cur = get_database_connection().cursor()
    
    if actualConfirmedFilter == 'not-used':
    
        if actualFilter == 'not-used' and predictedFilter == 'not-used':
            cur.execute("SELECT ID FROM model_run_result WHERE modelRunName = ? ORDER BY recording_id DESC, startTime ASC", (modelRunName,)) 
        elif actualFilter != 'not-used' and predictedFilter == 'not-used':
            cur.execute("SELECT ID FROM model_run_result WHERE modelRunName = ? AND actual = ? ORDER BY recording_id DESC, startTime ASC", (modelRunName, actualFilter)) 
        elif actualFilter == 'not-used' and predictedFilter != 'not-used':
            cur.execute("SELECT ID FROM model_run_result WHERE modelRunName = ? AND predictedByModel = ? ORDER BY recording_id DESC, startTime ASC", (modelRunName, predictedFilter)) 
        else:
            cur.execute("SELECT ID FROM model_run_result WHERE modelRunName = ? AND actual = ? AND predictedByModel = ? ORDER BY recording_id DESC, startTime ASC", (modelRunName, actualFilter, predictedFilter))
            
    elif actualConfirmedFilter == 'IS NULL':
    
        if actualFilter == 'not-used' and predictedFilter == 'not-used':
            cur.execute("SELECT ID FROM model_run_result WHERE modelRunName = ? AND actual_confirmed IS NULL ORDER BY recording_id DESC, startTime ASC", (modelRunName, )) 
        elif actualFilter != 'not-used' and predictedFilter == 'not-used':
            cur.execute("SELECT ID FROM model_run_result WHERE modelRunName = ? AND actual = ? AND actual_confirmed IS NULL ORDER BY recording_id DESC, startTime ASC", (modelRunName, actualFilter)) 
        elif actualFilter == 'not-used' and predictedFilter != 'not-used':
            cur.execute("SELECT ID FROM model_run_result WHERE modelRunName = ? AND actual_confirmed IS NULL AND predictedByModel = ? ORDER BY recording_id DESC, startTime ASC", (modelRunName, predictedFilter)) 
        else:
            cur.execute("SELECT ID FROM model_run_result WHERE modelRunName = ? AND actual = ? AND actual_confirmed IS NULL AND predictedByModel = ? ORDER BY recording_id DESC, startTime ASC", (modelRunName, actualFilter, predictedFilter)) 
    
            
    else: 
        if actualFilter == 'not-used' and predictedFilter == 'not-used':
            cur.execute("SELECT ID FROM model_run_result WHERE modelRunName = ? AND actual_confirmed = ? ORDER BY recording_id DESC, startTime ASC", (modelRunName, actualConfirmedFilter)) 
        elif actualFilter != 'not-used' and predictedFilter == 'not-used':
            cur.execute("SELECT ID FROM model_run_result WHERE modelRunName = ? AND actual = ? AND actual_confirmed = ? ORDER BY recording_id DESC, startTime ASC", (modelRunName, actualFilter, actualConfirmedFilter)) 
        elif actualFilter == 'not-used' and predictedFilter != 'not-used':
            cur.execute("SELECT ID FROM model_run_result WHERE modelRunName = ? AND actual_confirmed = ? AND predictedByModel = ? ORDER BY recording_id DESC, startTime ASC", (modelRunName, actualConfirmedFilter, predictedFilter)) 
        else:
            cur.execute("SELECT ID FROM model_run_result WHERE modelRunName = ? AND actual = ? AND actual_confirmed = ? AND predictedByModel = ? ORDER BY recording_id DESC, startTime ASC", (modelRunName, actualFilter, actualConfirmedFilter, predictedFilter)) 
    
    rows = cur.fetchall()
    return rows 

def get_model_run_result(database_ID):        
    cur = get_database_connection().cursor()
    cur.execute("SELECT ID, recording_id, startTime, duration, actual, predictedByModel, actual_confirmed FROM model_run_result WHERE ID = ?", (database_ID,)) 
    rows = cur.fetchall()
    return rows[0] 


    
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
    

    
def update_model_run_result(ID, actual_confirmed):
    if (actual_confirmed == 'None'): # This happens if the user does not select an option.  None causes issues later with creating the model as None is not valid class for the model
        return
    
    cur = get_database_connection().cursor()
   
    sql = ''' UPDATE model_run_result
              SET actual_confirmed = ?               
              WHERE ID = ?'''
    cur = get_database_connection().cursor()
    cur.execute(sql, (actual_confirmed, ID))
    
    get_database_connection().commit()      


    
def run_model(model_folder):
    # https://stackoverflow.com/questions/21406887/subprocess-changing-directory
    # https://stackoverflow.com/questions/1996518/retrieving-the-output-of-subprocess-call

    os.chdir(model_folder)  
    command = ['java', '--add-opens=java.base/java.lang=ALL-UNNAMED', '-jar', 'run.jar', 'shell=True']     
    
    result = run(command, stdout=PIPE, stderr=PIPE, text=True)
    
    return result

    
def classify_onsets_using_weka_model():

    model_folder = base_folder + '/' + run_folder + '/' + weka_model_folder
    
    # Need to check if run.jar is there, otherwise run.jar will break later on
    weka_run_jar_filename_path = model_folder + '/' + weka_run_jar_filename        
    if not os.path.isfile(weka_run_jar_filename_path):
        print(weka_run_jar_filename, " is missing") 
        return 
    
    # Need to check arff file is there, otherwise run.jar will break later on
    arff_filename_path = model_folder + '/' + weka_input_arff_filename        
    if not os.path.isfile(arff_filename_path):
        print(weka_input_arff_filename, " is missing") 
        return  
    
     # Need to check model file is there, otherwise run.jar will break later on
    weka_model_filename_path = model_folder + '/' + weka_model_filename        
    if not os.path.isfile(weka_model_filename_path):
        print(weka_model_filename_path, " is missing") 
        return    

    cur = get_database_connection().cursor()
#     cur.execute("SELECT recording_id, start_time_seconds, duration_seconds FROM onsets")  
    cur.execute("SELECT recording_id, start_time_seconds, duration_seconds FROM onsets ORDER BY recording_id DESC")
    onsets = cur.fetchall()  
    number_of_onsets = len(onsets)
    count = 0
    for onset in onsets:
        count += 1
        print('Processing onset', count, ' of ', number_of_onsets)
        print('onset', onset)
        recording_id = onset[0]
        start_time_seconds = onset[1]
        duration_seconds = onset[2]
        create_single_focused_mel_spectrogram_for_model_input(recording_id, start_time_seconds, duration_seconds)
        
        result = run_model(model_folder)
        if result.returncode == 0:
            print(result.stdout)
            if (int(result.stdout) == 0):
                predicted = 'morepork_more-pork'
                print('It is predicted to be a morepork\n')
                insert_model_run_result_into_database(parameters.model_run_name, recording_id, start_time_seconds, duration_seconds, None, predicted)
            else:
                predicted = 'unknown'
                print('It is predicted to be unknown\n')
                insert_model_run_result_into_database(parameters.model_run_name, recording_id, start_time_seconds, duration_seconds, None, predicted)
        
        else:
            print(result.stderr)


    
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
    print('audio_in_path ', audio_in_path)
    print('start_time ', start_time)
    print('duration ', duration)

    audio_out_path = base_folder + '/' + temp_folder + '/' + 'temp.wav'
    print('audio_out_path ', audio_out_path)
    y, sr = librosa.load(audio_in_path, sr=None) 
    y_amplified = np.int16(y/np.max(np.abs(y)) * 32767)
    y_amplified_start = sr * start_time
    y_amplified_end = (sr * start_time) + (sr * duration)
    y_amplified_to_play = y_amplified[int(y_amplified_start):int(y_amplified_end)]

    sf.write(audio_out_path, y_amplified_to_play, sr)

    os.system("aplay " + audio_out_path + " &")
 
    
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
  
    
def create_onsets(existing_tag_type):
    print("create_onsets")
    if existing_tag_type is None:
        create_onsets_in_local_db_using_recordings_folder()
    elif not existing_tag_type:
        create_onsets_in_local_db_using_recordings_folder()
    else:
        create_onsets_in_local_db_using_existing_tag_type(existing_tag_type)
        
def insert_onset_into_database(version, recording_id, start_time_seconds, duration_seconds):
    print('duration_seconds', duration_seconds)
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
    

    
def apply_band_pass_filter(y, sr):
#    y = highpass_filter(y, sr)
#     y = highpass_filter_with_parameters(y=y, sr=sr, filter_stop_freq=750, filter_pass_freq=800 )
#     y = highpass_filter_with_parameters(y=y, sr=sr, filter_stop_freq=700, filter_pass_freq=750 )
    y = highpass_filter_with_parameters(y=y, sr=sr, filter_stop_freq=600, filter_pass_freq=650 )
    y = apply_lowpass_filter(y, sr)    
    return y
    
def create_onsets_in_local_db_using_existing_tag_type(existing_tag_type):
    # Get recording names that have already been tagged with existing_tag_type e.g somewhere in the recording a morepork tag has already been created
    recording_ids_with_tag_type = get_unique_recording_ids_that_have_been_tagged_with_this_tag_stored_locally(existing_tag_type)
    count = 0
    number_of_recordings = len(recording_ids_with_tag_type)
    total_onset_pairs_including_more_than_20 = 0
    total_onset_pairs_including_not_including_more_20 = 0
    for recording_id_with_tag_type in recording_ids_with_tag_type:
        count+=1
        print('Processing recording ', count, ' of ', number_of_recordings, ' recordings.')
        recording_filename = str(recording_id_with_tag_type[0]) + '.m4a'
        count_of_onset_pairs_including_more_than_20, count_of_onset_pairs_including_not_including_more_20 = create_onsets_in_local_db(recording_filename)
        total_onset_pairs_including_more_than_20 += count_of_onset_pairs_including_more_than_20
        total_onset_pairs_including_not_including_more_20 += count_of_onset_pairs_including_not_including_more_20
        print('total_onset_pairs_including_more_than_20:', total_onset_pairs_including_more_than_20)
        print('total_onset_pairs_including_not_including_more_20:', total_onset_pairs_including_not_including_more_20, '\n')
    
    
def create_onsets_in_local_db_using_recordings_folder():
    
    # First need to find out what recordings have previously been used to create onsets - as we don't want to repeat
    
    cur = get_database_connection().cursor()

    
    recordings_folder_with_path = base_folder + '/' + downloaded_recordings_folder
    total_number_of_files = len(os.listdir(recordings_folder_with_path))
    total_onset_pairs_including_more_than_40 = 0
    total_onset_pairs_including_not_including_more_40 = 0
    
    
    
    with os.scandir(recordings_folder_with_path) as entries:
        count = 0
        for entry in entries:   
            try:        
                print(entry.name)
                if entry.is_file():                  
                    filename = entry.name
                else:
                    continue
                 
                count+=1
                print('Processing recording ', count, ' of ', total_number_of_files, ' recordings.')
                recording_id = filename.split('.')[0]
                
                cur.execute("SELECT recording_id FROM onsets WHERE recording_id = ?", (recording_id,)) 
               
                result = cur.fetchall() 
    #             print('result ', result)
                if result:
                    print('recording_id' , recording_id, ' has been used')
                    continue
    #             else:
    #                 print('recording_id' , recording_id, ' has NOT been used')
                
                count_of_onset_pairs_including_more_than_40, count_of_onset_pairs_including_not_including_more_40 = create_onsets_in_local_db(filename)
                total_onset_pairs_including_more_than_40 += count_of_onset_pairs_including_more_than_40
                total_onset_pairs_including_not_including_more_40 += count_of_onset_pairs_including_not_including_more_40
                print('total_onset_pairs_including_more_than_40:', total_onset_pairs_including_more_than_40)
                print('total_onset_pairs_including_not_including_more_40:', total_onset_pairs_including_not_including_more_40, '\n')
            except Exception as e:
                print(e, '\n')
                print('Error processing file ', filename)
    
    
def create_onsets_in_local_db(filename): 
    try:
        recordings_folder_with_path = base_folder + '/' + downloaded_recordings_folder
        
        count_of_onset_pairs_including_more_than_40 = 0
        count_of_onset_pairs_including_not_including_more_40 = 0
        
        audio_in_path = recordings_folder_with_path + "/" + filename
        
        y, sr = librosa.load(audio_in_path)
        y = apply_band_pass_filter(y, sr)            
    
        onsets = find_paired_squawks_in_single_recordings(y, sr) # Its now time to call the pair_squawks onsets
        #print('paired_squawks_sec', paired_squawks_sec)
        number_of_onsets = len(onsets)
        if not number_of_onsets == 0:
            if number_of_onsets > 40:
                count_of_onset_pairs_including_more_than_40 += number_of_onsets
            else:                
                
                count_of_onset_pairs_including_more_than_40 += number_of_onsets
                count_of_onset_pairs_including_not_including_more_40 += number_of_onsets                        
           
                recording_id = filename.split('.')[0]  
#                 print('recording_id', recording_id)
                
                insert_onset_list_into_db(version, recording_id, onsets)
                
#         print('count_of_onset_pairs_including_more_than_20 ', count_of_onset_pairs_including_more_than_20)
#         print('count_of_onset_pairs_including_not_including_more_20 ', count_of_onset_pairs_including_not_including_more_20)
        return count_of_onset_pairs_including_more_than_40, count_of_onset_pairs_including_not_including_more_40 

    except Exception as e:
        print(e, '\n')
        print('Error processing file ', filename)
                
def insert_onset_list_into_db(version, recording_id, onsets):
    global squawk_duration_seconds
    prev_onset = -1
    for onset in onsets:
        if prev_onset == -1:
            print("onset " , onset)    
            insert_onset_into_database(version, recording_id, onset, squawk_duration_seconds)
            prev_onset =  onset
        else:
            if (onset - prev_onset) < (squawk_duration_seconds + 0.1):
                print("Onset too close to previous, not inserting into database " , onset) 
            else:
                prev_onset = onset 
                insert_onset_into_database(version, recording_id, onset, squawk_duration_seconds )
                print("Inserting onset into database " , onset)
                
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
    mel_spectrograms_out_folder_path = base_folder + '/' + run_folder + '/' + spectrograms_for_model_creation_folder 
    if not os.path.exists(mel_spectrograms_out_folder_path):
        os.makedirs(mel_spectrograms_out_folder_path)
       
    count = 0
#     total_number_of_files = len(os.listdir(onset_pairs_folder_path))

    onsets = get_onsets_stored_locally('')   
       
    
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
            mel_spectrogram = librosa.feature.melspectrogram(y=y_part, sr=sr, n_mels=32, fmin=700,fmax=1000)
            
            pylab.axis('off') # no axis
            pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[]) # Remove the white edge
            librosa.display.specshow(mel_spectrogram, cmap='binary') #https://matplotlib.org/examples/color/colormaps_reference.html
            pylab.savefig(image_out_path, bbox_inches=None, pad_inches=0)
            pylab.close()
            
        except Exception as e:
            print(e, '\n')
            print('Error processing onset ', onset)

def create_spectrogram_jpg_files_for_next_model_run():
    mel_spectrograms_out_folder_path = base_folder + '/' + run_folder + '/' + spectrograms_for_model_creation_folder 
    if not os.path.exists(mel_spectrograms_out_folder_path):
        os.makedirs(mel_spectrograms_out_folder_path)
        
    # Also going to take this opportunity to create the model_run directory so it is available later in Weka for saving the model
    weka_model_folder_path = base_folder + '/' + run_folder + '/' + weka_model_folder 
    if not os.path.exists(weka_model_folder_path):
        os.makedirs(weka_model_folder_path)
  
    cur = get_database_connection().cursor()
#     cur.execute("SELECT DISTINCT actual_confirmed FROM model_run_result WHERE actual_confirmed IS NOT NULL") 
          
    count = 0
    
#     cur.execute("SELECT ID, recording_id, startTime, actual_confirmed FROM model_run_result WHERE actual_confirmed IS NOT NULL")
    cur.execute("SELECT ID, recording_id, startTime, actual_confirmed FROM model_run_result WHERE modelRunName = ? AND actual_confirmed IS NOT NULL", (model_run_name, ))  
    rows = cur.fetchall()  
    
    for row in rows:
        try:
            print('Processing row ', count, ' of ', len(rows), ' rows.')
            count+=1
            print('row ', row)
            recording_id = row[1] 
            start_time_seconds = row[2]
            actual_confirmed = row[3]       
#             
            audio_filename = str(recording_id) + '.m4a'
            audio_in_path = base_folder  + '/' + downloaded_recordings_folder + '/' +  audio_filename 
            image_out_name = actual_confirmed + '$' + str(recording_id) + '$' + str(start_time_seconds) + '.jpg'
            print('image_out_name', image_out_name)           
            
            image_out_path = mel_spectrograms_out_folder_path + '/' + image_out_name
             
            y, sr = librosa.load(audio_in_path, sr=None) 
             
            start_time_seconds_float = float(start_time_seconds)            
             
            start_position_array = int(sr * start_time_seconds_float)              
                        
            end_position_array = start_position_array + int((sr * morepork_more_pork_call_duration))
#                        
            if end_position_array > y.shape[0]:
                print('Clip would end after end of recording')
                continue
                 
            y_part = y[start_position_array:end_position_array]  
          
            mel_spectrogram = librosa.feature.melspectrogram(y=y_part, sr=sr, n_mels=32, fmin=700,fmax=1000)
             
            pylab.axis('off') # no axis
            pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[]) # Remove the white edge
            librosa.display.specshow(mel_spectrogram, cmap='binary') #https://matplotlib.org/examples/color/colormaps_reference.html
            pylab.savefig(image_out_path, bbox_inches=None, pad_inches=0)
            pylab.close()
             
        except Exception as e:
            print(e, '\n')
           
            
            
def get_single_create_focused_mel_spectrogram(recording_id, start_time_seconds, duration_seconds):

    temp_display_images_folder_path = base_folder + '/' + run_folder + '/' + temp_display_images_folder 
    if not os.path.exists(temp_display_images_folder_path):
        os.makedirs(temp_display_images_folder_path)         

    try:
        
        audio_filename = str(recording_id) + '.m4a'
        audio_in_path = base_folder + '/' + downloaded_recordings_folder + '/' +  audio_filename 
        image_out_name = 'temp_spectrogram.jpg'
        print('image_out_name', image_out_name)           
       
        image_out_path = temp_display_images_folder_path + '/' + image_out_name
        
        y, sr = librosa.load(audio_in_path, sr=None)      
               
        start_time_seconds_float = float(start_time_seconds)            
        
        start_position_array = int(sr * start_time_seconds_float)              
                   
        end_position_array = start_position_array + int((sr * duration_seconds))                  
                    
        y_part = y[start_position_array:end_position_array]  
        mel_spectrogram = librosa.feature.melspectrogram(y=y_part, sr=sr, n_mels=32, fmin=700,fmax=1000)
        
        pylab.axis('off') # no axis
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[]) # Remove the white edge
        librosa.display.specshow(mel_spectrogram, cmap='binary') #https://matplotlib.org/examples/color/colormaps_reference.html
        pylab.savefig(image_out_path, bbox_inches=None, pad_inches=0)
        pylab.close()
        
        return get_image(image_out_path)
        
    except Exception as e:
        print(e, '\n')
        print('Error processing onset ', onset)
        
def create_single_focused_mel_spectrogram_for_model_input(recording_id, start_time_seconds, duration_seconds):

    mel_spectrograms_out_folder_path = base_folder + '/' + run_folder + '/' + weka_model_folder + '/' + single_spectrogram_for_classification_folder 
    if not os.path.exists(mel_spectrograms_out_folder_path):
        os.makedirs(mel_spectrograms_out_folder_path)  
        
   

    try:
        
        audio_filename = str(recording_id) + '.m4a'
        audio_in_path = base_folder + '/' + downloaded_recordings_folder + '/' +  audio_filename 
        image_out_name = 'input_image.jpg'
        print('image_out_name', image_out_name)           
       
        image_out_path = mel_spectrograms_out_folder_path + '/' + image_out_name
        
        y, sr = librosa.load(audio_in_path, sr=None)      
               
        start_time_seconds_float = float(start_time_seconds)            
        
        start_position_array = int(sr * start_time_seconds_float)              
                   
        end_position_array = start_position_array + int((sr * duration_seconds))                  
                    
        y_part = y[start_position_array:end_position_array]  
        mel_spectrogram = librosa.feature.melspectrogram(y=y_part, sr=sr, n_mels=32, fmin=700,fmax=1000)
        
        pylab.axis('off') # no axis
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[]) # Remove the white edge
        librosa.display.specshow(mel_spectrogram, cmap='binary') #https://matplotlib.org/examples/color/colormaps_reference.html
        pylab.savefig(image_out_path, bbox_inches=None, pad_inches=0)
        pylab.close()
        
        return get_image(image_out_path)
        
    except Exception as e:
        print(e, '\n')
        print('Error processing onset ', onset)
        

    
        
def get_single_waveform_image(recording_id, start_time_seconds, duration_seconds):

    temp_display_images_folder_path = base_folder + '/' + run_folder + '/' + temp_display_images_folder 
    if not os.path.exists(temp_display_images_folder_path):
        os.makedirs(temp_display_images_folder_path)         

    try:
        
        audio_filename = str(recording_id) + '.m4a'
        audio_in_path = base_folder + '/' + downloaded_recordings_folder + '/' +  audio_filename 
        image_out_name = 'temp_waveform.jpg'
        print('image_out_name', image_out_name)           
       
        image_out_path = temp_display_images_folder_path + '/' + image_out_name
        
        y, sr = librosa.load(audio_in_path, sr=None) 
        
        start_time_seconds_float = float(start_time_seconds)            
        
        start_position_array = int(sr * start_time_seconds_float)              
                   
        end_position_array = start_position_array + int((sr * duration_seconds))                  
                    
        y_part = y[start_position_array:end_position_array]  
        
        
        
        pylab.axis('off') # no axis
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[]) # Remove the white edge
        librosa.display.waveplot(y=y_part, sr=sr)
        pylab.savefig(image_out_path, bbox_inches=None, pad_inches=0)
        pylab.close()
        
        return get_image(image_out_path)
        
    except Exception as e:
        print(e, '\n')
        print('Error processing onset ', onset)
               
def get_image(image_name_path): 
        
    image = Image.open(image_name_path)
    [imageSizeWidth, imageSizeHeight] = image.size
    image = image.resize((int(imageSizeWidth/2),int(imageSizeHeight/2)), Image.ANTIALIAS)
    spectrogram_image = ImageTk.PhotoImage(image)
    return spectrogram_image

def get_unique_model_run_names():   
    cur = get_database_connection().cursor()
    cur.execute("SELECT DISTINCT modelRunName FROM model_run_result") 
    rows = cur.fetchall()  
    
    unique_model_run_names = []
    for row in rows:
        unique_model_run_names.append(row[0])
        
    return unique_model_run_names  


def create_arff_file_for_weka_image_filter_input():

    run_folder_path = base_folder + '/' + run_folder
    f= open(run_folder_path + '/' + arff_file_for_weka_model_creation,"w+")
    f.write('@relation ' + relation_name + '\r\n')
    f.write('@attribute filename string' + '\r\n')
    f.write('@attribute class {' + class_names +'}' + '\r\n')
    f.write('@data' + '\r\n')    
    
    spectrograms_for_model_creation_folder_path = run_folder_path + '/' + spectrograms_for_model_creation_folder    
   
    for filename in os.listdir(spectrograms_for_model_creation_folder_path):
        filename_parts = filename.split('$')
        class_type = filename_parts[0]
        print('image', filename)
        print('class_type', class_type)
        f.write(filename +',' + class_type + '\r\n')      
        
    f.close()
    
def update_latest_model_run_results_with_previous_confirmed():
    
    # First find rows that have been confirmed
    # Then using recording_id and startTime these confirmed rows, find unconfirmed rows with the same recording_id and startTime
    # Then update these unconfirmed rows with the confirmed value e.g. could be morepork_morepork or unknown
    
    cur = get_database_connection().cursor()
    cur.execute("SELECT recording_id, startTime, actual_confirmed FROM model_run_result WHERE actual_confirmed IS NOT NULL") 
 
    confirmed_rows = cur.fetchall()
    
    for confirmed_row in confirmed_rows:
       
        recording_id = confirmed_row[0]
        startTime = confirmed_row[1]
        actual_confirmed = confirmed_row[2]
        
        print(recording_id, ' ', startTime, ' ', actual_confirmed)
        
        cur2 = get_database_connection().cursor()
        cur2.execute("SELECT ID, recording_id, startTime, actual_confirmed FROM model_run_result WHERE actual_confirmed IS NULL AND recording_id = ? AND startTime = ?", (recording_id,startTime))  
        matching_unconfirmed_rows = cur2.fetchall()
        if len(matching_unconfirmed_rows) > 0:
            print('Match Found')
            for matching_unconfirmed_row in matching_unconfirmed_rows:
                matching_unconfirmed_row_ID = matching_unconfirmed_row[0]
                matching_unconfirmed_row_recording_id = matching_unconfirmed_row[1]
                print('Updating actual_confirmed value in recording_id ', matching_unconfirmed_row_recording_id, ' to be ', actual_confirmed)
                
                cur3 = get_database_connection().cursor()
                cur3.execute("UPDATE model_run_result SET actual_confirmed = ? WHERE ID = ?", (actual_confirmed, matching_unconfirmed_row_ID))  
                
                get_database_connection().commit()
       
                
            
def create_folders_for_next_run():
    next_run_folder = parameters.base_folder + '/' + run_folder
    if not os.path.exists(next_run_folder):
        os.makedirs(next_run_folder) 
        
#     next_exported_jars_folder = parameters.base_folder + '/' + run_folder + '/' + exported_jars_folder  
#     if not os.path.exists(next_exported_jars_folder):
#         os.makedirs(next_exported_jars_folder) 
        
#     next_arff_folder_for_next_run = parameters.base_folder + '/' + run_folder + '/' + arff_folder_for_next_run  
#     if not os.path.exists(next_arff_folder_for_next_run):
#         os.makedirs(next_arff_folder_for_next_run) 
#         
    
        
    weka_model_folder_path = parameters.base_folder + '/' + run_folder + '/' + weka_model_folder  
    if not os.path.exists(weka_model_folder_path):
        os.makedirs(weka_model_folder_path) 
        
    spectrograms_for_model_creation_folder_path = parameters.base_folder + '/' + run_folder + '/' + spectrograms_for_model_creation_folder  
    if not os.path.exists(spectrograms_for_model_creation_folder_path):
        os.makedirs(spectrograms_for_model_creation_folder_path) 
        
    single_spectrogram_for_classification_folder_path = parameters.base_folder + '/' + run_folder + '/' + weka_model_folder + '/' + single_spectrogram_for_classification_folder  
    if not os.path.exists(single_spectrogram_for_classification_folder_path):
        os.makedirs(single_spectrogram_for_classification_folder_path) 
        
        
           
        
            
    
    
    
    
    



































    


