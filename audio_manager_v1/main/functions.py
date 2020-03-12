
import main.parameters as parameters
from main.parameters import *

import sqlite3
from sqlite3 import Error
import requests

import json
from pathlib import Path
from tkinter import filedialog
from tkinter import *

import os
from scipy import signal

from scipy.signal import butter, lfilter, freqz
import numpy as np
from scipy.ndimage.filters import maximum_filter
import pylab
import librosa.display

import soundfile as sf

from subprocess import PIPE, run

from librosa import display, onset

from PIL import ImageTk,Image 

from datetime import datetime
from pytz import timezone
from pytz import all_timezones


# db_file = "/home/tim/Work/Cacophony/eclipse-workspace/audio_manager_v1/audio_analysis_db2.db"
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
    
def get_recordings_from_server_for_all_devices():
    sql = '''select distinct device_name, device_super_name from recordings'''
    cur = get_database_connection().cursor()  
    cur.execute(sql) 
    rows = cur.fetchall() 
    for row in rows:
        device_name = row[0]
        device_super_name = row[1]
        retrieve_available_recordings_from_server(device_name, device_super_name)
          
def retrieve_missing_recording_information():
    sql = ''' SELECT recording_id from recordings where recordingDateTime IS NULL '''
    cur = get_database_connection().cursor()  
   
    cur.execute(sql) 
    
    rows = cur.fetchall() 
    numberOfRows = len(rows)
    count = 0
    for row in rows:
        recording_id =  row[0]
        print("Processing ", count, " of ", numberOfRows)
        print("About to get recording information for ", recording_id)
        update_recording_information_for_single_recording(recording_id)
        count += 1
        
        
        
    
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
            print('Already have recording ',recording_id, ' so will not download')
       
    for recording_id in ids_of_recordings_to_still_to_download:
#         print('About to get token for downloading ',recording_id)
        token_for_retrieving_recording = get_token_for_retrieving_recording(recording_id)
        print('About to get recording ',recording_id)
        get_recording_from_server(token_for_retrieving_recording, recording_id, device_name, device_super_name)
        
        # Also get recording information from server
        update_recording_information_for_single_recording(recording_id)
     
    print('Finished retrieving recordings')  
#     print('Now going to retrieve tags')  
#     
#     # 19 Dec 2019 Decided not to get tags, but maybe later I'll put this on a separate button, as it could be useful to use tags that others have created.
# #     get_all_tags_for_all_devices_in_local_database() 
#     print('Finished retrieving tags') 
#     print('Finished all')  
        
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
    
    # Get the highest recording id for this device that has already been downloaded
    cur = get_database_connection().cursor()   
    cur.execute("SELECT MAX(recording_id) FROM recordings WHERE device_name = ?", (device_name,))
    rows = cur.fetchall() 
    current_max_recording_id_for_this_device = rows[0][0]
    if current_max_recording_id_for_this_device is None:
        current_max_recording_id_for_this_device = 0
    
        
    print('device_name ', device_name)
    print('max_recording_id ', current_max_recording_id_for_this_device)
    
    device_id = get_device_id_using_device_name(device_name)
    print('device_id is ', device_id)
    ids_recordings_for_device_name = []
    offset = 0
    while True:
        ids_of_recordings_to_download= get_ids_of_recordings_to_download_using_deviceId(device_id,offset, current_max_recording_id_for_this_device)
        print('ids_of_recordings_to_download ', ids_of_recordings_to_download)
        ids_recordings_for_device_name += ids_of_recordings_to_download
        
        # Check to see if the list from the server contains the previous max recording_id.  If it does, then don't get anymore ids
        
        if (len(ids_of_recordings_to_download) > 0):
            offset+=300
        else:
            break
    return ids_recordings_for_device_name

def get_ids_of_recordings_to_download_using_deviceId(deviceId, offset, current_max_recording_id):
    # This will get a list of the recording ids for every recording of length 59,60,61,62 from device_name
    user_token = get_cacophony_user_token()
   
    url = server_endpoint + query_available_recordings
    
    where_param = {}
    where_param['DeviceId'] = deviceId
    where_param['duration'] = 59,60,61,62
    
    grt_id_param = {}
    grt_id_param['$gt'] = current_max_recording_id
    where_param['id'] = grt_id_param
    
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
    recordingDateTimeNZ = convert_time_zones(recordingDateTime)
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
                   
#     update_recording_in_database(recordingDateTime, relativeToDawn, relativeToDusk, duration, locationLat, locationLong, version, batteryLevel, phoneModel, androidApiLevel, deviceId, nightRecording, device_name, recording_id, recordingDateTimeNZ)
    update_recording_in_database(recordingDateTime, relativeToDawn, relativeToDusk, duration, locationLat, locationLong, version, batteryLevel, phoneModel, androidApiLevel, deviceId, nightRecording, device_name, recording_id, recordingDateTimeNZ)
    print('Finished updating recording information for recording ', recording_id)
               
  
def update_recording_in_database(recordingDateTime, relativeToDawn, relativeToDusk, duration, locationLat, locationLong, version, batteryLevel, phoneModel,androidApiLevel, deviceId, nightRecording, device_name, recording_id, recordingDateTimeNZ):
    try:
#         conn = get_database_connection()
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
                      device_name = ?,
                      recordingDateTimeNZ = ?
                  WHERE recording_id = ? '''
        cur = get_database_connection().cursor()
        cur.execute(sql, (recordingDateTime, relativeToDawn, relativeToDusk, duration, locationLat, locationLong, version, batteryLevel, phoneModel, androidApiLevel, deviceId, nightRecording, device_name, recordingDateTimeNZ, recording_id))
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
    # Use this is the tag was created in this application, rather than being downloaded from the server - becuase some fields are missing e.g. server_Id
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

def get_model_run_results(modelRunName, actualConfirmedFilter, predictedFilter, predicted_probability_filter, predicted_probability_filter_value_str, location_filter, actual_confirmed_other, predicted_other, used_to_create_model_filter, recording_id_filter_value):   
       
    if location_filter =='Not Used':
        location_filter ='not_used'
         
    sqlBuilding = "SELECT ID FROM model_run_result WHERE modelRunName = '" + modelRunName + "'"
    
    if actualConfirmedFilter !='not_used':
        sqlBuilding += " AND "
        if actualConfirmedFilter == "IS NULL":
            if actual_confirmed_other == 'off':
                sqlBuilding += "actual_confirmed IS NULL"
            else: # Everything other is checked
                sqlBuilding += "actual_confirmed IS NOT NULL"
        else:
            if actual_confirmed_other == 'off':
                sqlBuilding +=  "actual_confirmed = '" + actualConfirmedFilter + "'"
            else: # Everything other is checked
                sqlBuilding +=  "actual_confirmed <> '" + actualConfirmedFilter + "'"
                
            
    if predictedFilter !='not_used':
        sqlBuilding += " AND "
        if predictedFilter == "IS NULL":
            if predicted_other == 'off':
                sqlBuilding += "predictedByModel IS NULL"
            else:
                sqlBuilding += "predictedByModel IS NOT NULL"
        else:
            if predicted_other == 'off':
                sqlBuilding +=  "predictedByModel = '" + predictedFilter + "'"
            else:
                sqlBuilding +=  "predictedByModel <> '" + predictedFilter + "'"
            
    if location_filter !='not_used':
        sqlBuilding += " AND "
        sqlBuilding +=  "device_super_name = '" + location_filter + "'"
        
    if (predicted_probability_filter_value_str == '') or (predicted_probability_filter == 'not_used'):
        predicted_probability_filter = 'not_used'
    else:    
        if predicted_probability_filter == 'greater_than':  
            probabilty_comparator = '>'
#             predicted_probability_filter_value = float(predicted_probability_filter_value_str)    
        elif predicted_probability_filter == 'less_than': 
            probabilty_comparator = '<'
#             predicted_probability_filter_value = float(predicted_probability_filter_value_str)    
        sqlBuilding += " AND "
#         sqlBuilding += " probability " + probabilty_comparator + " '" + predicted_probability_filter_value + "'"
        sqlBuilding += " probability " + probabilty_comparator + " '" + predicted_probability_filter_value_str + "'"
        
    if used_to_create_model_filter != 'not_used':
        sqlBuilding += " AND "
        if used_to_create_model_filter == 'yes':
            sqlBuilding +=  "used_to_create_model = 1"
        else:
#             sqlBuilding +=  "used_to_create_model = 0"
            sqlBuilding +=  "used_to_create_model IS NULL"
            
    if recording_id_filter_value:
        sqlBuilding += " AND "        
        sqlBuilding +=  "recording_id = '" + recording_id_filter_value + "'"
        
        
    sqlBuilding += " ORDER BY recording_id DESC, startTime ASC"
        
    print("The sql is: ", sqlBuilding)
    cur = get_database_connection().cursor()
    cur.execute(sqlBuilding)
#     cur.execute("SELECT ID FROM model_run_result WHERE modelRunName = '2019_12_11_1' ORDER BY recording_id DESC, startTime ASC")
    rows = cur.fetchall()
    return rows

def get_model_run_result(database_ID):        
    cur = get_database_connection().cursor()
    cur.execute("SELECT ID, recording_id, startTime, duration, actual, predictedByModel, actual_confirmed, probability, device_super_name FROM model_run_result WHERE ID = ?", (database_ID,)) 
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
            filename = recording_id + '.m4a'
            insert_recording_into_database(recording_id,filename, device_name,device_super_name) # The device name will be updated next when getting infor from server
            # Now update this recording with information from server
            update_recording_information_for_single_recording(recording_id)
           


    
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
    cur = get_database_connection().cursor()
    sql = ''' UPDATE model_run_result
              SET actual_confirmed = ?               
              WHERE ID = ?'''
    if (actual_confirmed == 'None') or (actual_confirmed == 'not_used'): # Must not put None into the db as the model breaks - instead convert to Null as descrived here - https://johnmludwig.blogspot.com/2018/01/null-vs-none-in-sqlite3-for-python.html
        cur.execute(sql, (None, ID))
    else:
        cur.execute(sql, (actual_confirmed, ID))
    
    get_database_connection().commit()    
    
def update_onset(recording_id, start_time_seconds, actual_confirmed):
    cur = get_database_connection().cursor()
    if (actual_confirmed == 'None') or (actual_confirmed == 'not_used'): # Must not put None into the db as the model breaks - instead convert to Null as descrived here - https://johnmludwig.blogspot.com/2018/01/null-vs-none-in-sqlite3-for-python.html
        cur.execute("UPDATE onsets SET actual_confirmed = ? WHERE recording_id = ? AND start_time_seconds = ?", (None, recording_id, start_time_seconds))   
    else:        
        cur.execute("UPDATE onsets SET actual_confirmed = ? WHERE recording_id = ? AND start_time_seconds = ?", (actual_confirmed, recording_id, start_time_seconds))  
        
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
    

    
    # Need to check model file is there, otherwise run.jar will break later on
    weka_model_filename_path = model_folder + '/' + weka_model_filename        
    if not os.path.isfile(weka_model_filename_path):
        print(weka_model_filename_path, " is missing") 
        return    

# As it takes about 24 hours to process all the onsets, I've split processing in to two stages - 
# first it does all the onsets that already have an actual_confirmed entry - 
# this might only take a minute or two as there are very few of them
# then it does the rest.  It is now OK to stop this process before it has finished as I'll probably never look at all the predictions - unless going to create tags on the server

    cur = get_database_connection().cursor()
    cur.execute("SELECT recording_id, start_time_seconds, duration_seconds, actual_confirmed, device_super_name, device_name, recordingDateTime, recordingDateTimeNZ FROM onsets WHERE actual_confirmed IS NOT NULL ORDER BY recording_id DESC")
    
    onsetsWithActualConfirmed = cur.fetchall()  
    number_of_onsets = len(onsetsWithActualConfirmed)
    count = 0
    print('Processing onsets with actual_confirmed entry')
    for onsetWithActualConfirmed in onsetsWithActualConfirmed:
        count += 1        
        print('Processing onset', count, ' of ', number_of_onsets)
        classify_onsets_using_weka_model_helper(onsetWithActualConfirmed, model_folder)
    
    cur2 = get_database_connection().cursor()
    cur2.execute("SELECT recording_id, start_time_seconds, duration_seconds, actual_confirmed, device_super_name, device_name, recordingDateTime, recordingDateTimeNZ FROM onsets WHERE actual_confirmed IS NULL ORDER BY recording_id DESC")
    onsetsWithNoActualConfirmed = cur2.fetchall()  
    number_of_onsets = len(onsetsWithNoActualConfirmed)
    count = 0
    print('Processing onsets with NO actual_confirmed entry')
    for onsetWithNoActualConfirmed in onsetsWithNoActualConfirmed:
        count += 1        
        print('Processing onset', count, ' of ', number_of_onsets)
        classify_onsets_using_weka_model_helper(onsetWithNoActualConfirmed, model_folder)   
        
def update_onsets_with_edge_histogram_features():  
    model_folder = base_folder + '/' + run_folder + '/' + weka_model_folder
    
    # Need to check if run.jar is there, otherwise run.jar will break later on
    get_edge_histogram_jar_filename_path = model_folder + '/' + get_edge_histogram_jar_filename        
    if not os.path.isfile(get_edge_histogram_jar_filename_path):
        print(get_edge_histogram_jar_filename_path, " is missing") 
        return 
        
    # Need to check model file is there, otherwise run.jar will break later on
    weka_model_filename_path = model_folder + '/' + weka_model_filename        
    if not os.path.isfile(weka_model_filename_path):
        print(weka_model_filename_path, " is missing") 
        return  
    
    cur = get_database_connection().cursor()
    cur.execute("SELECT ID, recording_id, start_time_seconds, duration_seconds  FROM onsets WHERE MPEG7_Edge_Histogram0 IS NULL ORDER BY recording_id DESC")
#     cur.execute("SELECT ID, recording_id, start_time_seconds, duration_seconds  FROM onsets WHERE MPEG7_Edge_Histogram0 IS NULL AND device_super_name = 'chow' ORDER BY recording_id DESC")

   
    onsetsWithNoEdgeHistogramData = cur.fetchall()  
    number_of_onsets = len(onsetsWithNoEdgeHistogramData)
    count = 0
    print('Processing onsets with with No EdgeHistogram Data')
    for onsetWithNoEdgeHistogramData in onsetsWithNoEdgeHistogramData:
        count += 1        
        
        ID = onsetWithNoEdgeHistogramData[0]
        recording_id = onsetWithNoEdgeHistogramData[1]
        start_time_seconds = onsetWithNoEdgeHistogramData[2]
        duration_seconds = onsetWithNoEdgeHistogramData[3]  
        
        print('Processing onset', count, ' of ', number_of_onsets)
        create_single_focused_mel_spectrogram_for_model_input(recording_id, start_time_seconds, duration_seconds)
                
        os.chdir(model_folder)  
        command = ['java', '--add-opens=java.base/java.lang=ALL-UNNAMED', '-jar', 'getEdgeHistogramFeatures.jar', 'shell=True']     
    
        result = run(command, stdout=PIPE, stderr=PIPE, text=True)   
        if result.returncode == 0:
#             print(result.stdout)
          
            result_stdout = result.stdout
            result_stdout_parts = result_stdout.split(',')
#             print('length', len(result_stdout_parts))
#             print('result_stdout_parts', result_stdout_parts)
            sql = '''UPDATE onsets
                SET MPEG7_Edge_Histogram0 = ?, 
                MPEG7_Edge_Histogram1 = ?,
                MPEG7_Edge_Histogram2 = ?,
                MPEG7_Edge_Histogram3 = ?,
                MPEG7_Edge_Histogram4 = ?,
                MPEG7_Edge_Histogram5 = ?,
                MPEG7_Edge_Histogram6 = ?,
                MPEG7_Edge_Histogram7 = ?,
                MPEG7_Edge_Histogram8 = ?,
                MPEG7_Edge_Histogram9 = ?,
                
                MPEG7_Edge_Histogram10 = ?, 
                MPEG7_Edge_Histogram11 = ?,
                MPEG7_Edge_Histogram12 = ?,
                MPEG7_Edge_Histogram13 = ?,
                MPEG7_Edge_Histogram14 = ?,
                MPEG7_Edge_Histogram15 = ?,
                MPEG7_Edge_Histogram16 = ?,
                MPEG7_Edge_Histogram17 = ?,
                MPEG7_Edge_Histogram18 = ?,
                MPEG7_Edge_Histogram19 = ?,
                
                MPEG7_Edge_Histogram20 = ?,
                MPEG7_Edge_Histogram21 = ?,
                MPEG7_Edge_Histogram22 = ?,
                MPEG7_Edge_Histogram23 = ?,
                MPEG7_Edge_Histogram24 = ?,
                MPEG7_Edge_Histogram25 = ?,
                MPEG7_Edge_Histogram26 = ?,
                MPEG7_Edge_Histogram27 = ?,
                MPEG7_Edge_Histogram28 = ?,
                MPEG7_Edge_Histogram29 = ?,
                
                MPEG7_Edge_Histogram30 = ?,
                MPEG7_Edge_Histogram31 = ?,
                MPEG7_Edge_Histogram32 = ?,
                MPEG7_Edge_Histogram33 = ?,
                MPEG7_Edge_Histogram34 = ?,
                MPEG7_Edge_Histogram35 = ?,
                MPEG7_Edge_Histogram36 = ?,
                MPEG7_Edge_Histogram37 = ?,
                MPEG7_Edge_Histogram38 = ?,
                MPEG7_Edge_Histogram39 = ?,
                
                MPEG7_Edge_Histogram40 = ?, 
                MPEG7_Edge_Histogram41 = ?,
                MPEG7_Edge_Histogram42 = ?,
                MPEG7_Edge_Histogram43 = ?,
                MPEG7_Edge_Histogram44 = ?,
                MPEG7_Edge_Histogram45 = ?,
                MPEG7_Edge_Histogram46 = ?,
                MPEG7_Edge_Histogram47 = ?,
                MPEG7_Edge_Histogram48 = ?,
                MPEG7_Edge_Histogram49 = ?,
                
                MPEG7_Edge_Histogram50 = ?, 
                MPEG7_Edge_Histogram51 = ?,
                MPEG7_Edge_Histogram52 = ?,
                MPEG7_Edge_Histogram53 = ?,
                MPEG7_Edge_Histogram54 = ?,
                MPEG7_Edge_Histogram55 = ?,
                MPEG7_Edge_Histogram56 = ?,
                MPEG7_Edge_Histogram57 = ?,
                MPEG7_Edge_Histogram58 = ?,
                MPEG7_Edge_Histogram59 = ?,
                
                MPEG7_Edge_Histogram60 = ?,
                MPEG7_Edge_Histogram61 = ?,
                MPEG7_Edge_Histogram62 = ?,
                MPEG7_Edge_Histogram63 = ?,
                MPEG7_Edge_Histogram64 = ?,
                MPEG7_Edge_Histogram65 = ?,
                MPEG7_Edge_Histogram66 = ?,
                MPEG7_Edge_Histogram67 = ?,
                MPEG7_Edge_Histogram68 = ?,
                MPEG7_Edge_Histogram69 = ?,
                
                MPEG7_Edge_Histogram70 = ?,
                MPEG7_Edge_Histogram71 = ?,
                MPEG7_Edge_Histogram72 = ?,
                MPEG7_Edge_Histogram73 = ?,
                MPEG7_Edge_Histogram74 = ?,
                MPEG7_Edge_Histogram75 = ?,
                MPEG7_Edge_Histogram76 = ?,
                MPEG7_Edge_Histogram77 = ?,
                MPEG7_Edge_Histogram78 = ?,
                MPEG7_Edge_Histogram79 = ?          
                                                           
                WHERE ID = ?'''
            
#             print('sql ', sql)           
        
            cur.execute(sql, (result_stdout_parts[1],
                              result_stdout_parts[2], 
                              result_stdout_parts[3], 
                              result_stdout_parts[4], 
                              result_stdout_parts[4], 
                              result_stdout_parts[6], 
                              result_stdout_parts[7], 
                              result_stdout_parts[8], 
                              result_stdout_parts[9],
                              
                              result_stdout_parts[10], 
                              result_stdout_parts[11],                             
                              result_stdout_parts[12], 
                              result_stdout_parts[13], 
                              result_stdout_parts[14], 
                              result_stdout_parts[14], 
                              result_stdout_parts[16], 
                              result_stdout_parts[17], 
                              result_stdout_parts[18], 
                              result_stdout_parts[19],
                              
                              result_stdout_parts[20],                              
                              result_stdout_parts[21],
                              result_stdout_parts[22], 
                              result_stdout_parts[23], 
                              result_stdout_parts[24], 
                              result_stdout_parts[24], 
                              result_stdout_parts[26], 
                              result_stdout_parts[27], 
                              result_stdout_parts[28], 
                              result_stdout_parts[29],
                              
                              result_stdout_parts[30],                              
                              result_stdout_parts[31],
                              result_stdout_parts[32], 
                              result_stdout_parts[33], 
                              result_stdout_parts[34], 
                              result_stdout_parts[34], 
                              result_stdout_parts[36], 
                              result_stdout_parts[37], 
                              result_stdout_parts[38], 
                              result_stdout_parts[39],
                              
                              result_stdout_parts[40],                              
                              result_stdout_parts[41],
                              result_stdout_parts[42], 
                              result_stdout_parts[43], 
                              result_stdout_parts[44], 
                              result_stdout_parts[44], 
                              result_stdout_parts[46], 
                              result_stdout_parts[47], 
                              result_stdout_parts[48], 
                              result_stdout_parts[49],
                              
                              result_stdout_parts[50],                              
                              result_stdout_parts[51],
                              result_stdout_parts[52], 
                              result_stdout_parts[53], 
                              result_stdout_parts[54], 
                              result_stdout_parts[54], 
                              result_stdout_parts[56], 
                              result_stdout_parts[57], 
                              result_stdout_parts[58], 
                              result_stdout_parts[59],
                              
                              result_stdout_parts[60],                              
                              result_stdout_parts[61],
                              result_stdout_parts[62], 
                              result_stdout_parts[63], 
                              result_stdout_parts[64], 
                              result_stdout_parts[64], 
                              result_stdout_parts[66], 
                              result_stdout_parts[67], 
                              result_stdout_parts[68], 
                              result_stdout_parts[69],
                              
                              result_stdout_parts[70],                              
                              result_stdout_parts[71],
                              result_stdout_parts[72], 
                              result_stdout_parts[73], 
                              result_stdout_parts[74], 
                              result_stdout_parts[74], 
                              result_stdout_parts[76], 
                              result_stdout_parts[77], 
                              result_stdout_parts[78], 
                              result_stdout_parts[79],
                              
                              result_stdout_parts[80],                               
                              
                              ID)) 
               
            get_database_connection().commit()
            
        else:
            print(result.stderr)
           
def classify_onsets_using_weka_model_helper(onset, model_folder):     
    print('onset', onset)
    recording_id = onset[0]
    start_time_seconds = onset[1]
    duration_seconds = onset[2]
    actual_confirmed = onset[3]
    device_super_name = onset[4] 
    device_name = onset[5] 
    recordingDateTime = onset[6] 
    recordingDateTimeNZ = onset[7]
    
    # Skip if it already exists
    cur = get_database_connection().cursor()
    cur.execute("SELECT ID FROM model_run_result WHERE modelRunName = ? AND recording_id = ? AND startTime = ? AND duration = ?", (model_run_name, recording_id, start_time_seconds, duration_seconds)) 
    row = cur.fetchone()
    if row != None:
        print("Already done this one")
        return  
   
    create_single_focused_mel_spectrogram_for_model_input(recording_id, start_time_seconds, duration_seconds)
    
    # Create the input.arff file for this onset
    arff_filename_path = model_folder + '/' + weka_input_arff_filename  
    create_input_arff_file_for_single_onset_prediction(arff_filename_path, device_super_name)
    
    # Need to check arff file is there, otherwise run.jar will break later on
#     arff_filename_path = model_folder + '/' + weka_input_arff_filename        
    if not os.path.isfile(arff_filename_path):
        print(weka_input_arff_filename, " is missing") 
        return  
       
    result = run_model(model_folder)
    
    if result.returncode == 0:
        print(result.stdout)
        
        classNumber = (int)(result.stdout.split(",")[0])   
        
        predicted_class_name = parameters.class_names.split(",")[classNumber] 
        
        probability = result.stdout.split(",")[1]      
 
        print('It is predicted to be  ' , predicted_class_name, ' with probability of ',probability,  '\n')
        insert_model_run_result_into_database(parameters.model_run_name, recording_id, start_time_seconds, duration_seconds, None, predicted_class_name, probability, actual_confirmed, device_super_name, device_name, recordingDateTime, recordingDateTimeNZ)
    
    else:
        print(result.stderr)
              

    
def insert_model_run_result_into_database(modelRunName, recording_id, startTime, duration, actual, predictedByModel, probability, actual_confirmed, device_super_name, device_name, recordingDateTime, recordingDateTimeNZ):
       
    try:
        cur = get_database_connection().cursor()
        if actual_confirmed:
            sql = ''' INSERT INTO model_run_result(modelRunName, recording_id, startTime, duration, actual, predictedByModel, probability, actual_confirmed, device_super_name, device_name, recordingDateTime, recordingDateTimeNZ)
                      VALUES(?,?,?,?,?,?,?,?,?,?,?,?) '''
            cur.execute(sql, (modelRunName, recording_id, startTime, duration, actual, predictedByModel, probability, actual_confirmed, device_super_name, device_name, recordingDateTime, recordingDateTimeNZ))
        else:
            sql = ''' INSERT INTO model_run_result(modelRunName, recording_id, startTime, duration, actual, predictedByModel, probability, device_super_name, device_name, recordingDateTime, recordingDateTimeNZ)
                      VALUES(?,?,?,?,?,?,?,?,?,?,?) '''
            cur.execute(sql, (modelRunName, recording_id, startTime, duration, actual, predictedByModel, probability, device_super_name, device_name, recordingDateTime, recordingDateTimeNZ))
        
        get_database_connection().commit()
    except Exception as e:
        print(e, '\n')
        print('\t\tUnable to insert result' + str(recording_id) + ' ' + str(startTime), '\n')  
    
def play_clip(recording_id, start_time, duration, applyBandPassFilter):
    audio_in_path = getRecordingsFolder() + '/' + recording_id + '.m4a'
    print('audio_in_path ', audio_in_path)
    print('start_time ', start_time)
    print('duration ', duration)

    audio_out_path = base_folder + '/' + temp_folder + '/' + 'temp.wav'
    print('audio_out_path ', audio_out_path)
    y, sr = librosa.load(audio_in_path, sr=None) 
    if applyBandPassFilter:
        y = apply_band_pass_filter(y, sr)
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
  

        
def insert_onset_into_database(version, recording_id, start_time_seconds, duration_seconds):
    
    print('duration_seconds', duration_seconds)
    cur1 = get_database_connection().cursor()
    cur1.execute("SELECT device_super_name, device_name, recordingDateTime, recordingDateTimeNZ FROM recordings WHERE recording_id = ?", (recording_id,)) 
    rows = cur1.fetchall() 
    device_super_name = rows[0][0]  
    device_name = rows[0][1]
    recordingDateTime = rows[0][2]  
    recordingDateTimeNZ = rows[0][3] 
    
#     recordingDateTimeNZ = convert_time_zones(recordingDateTime)
    
    try:     
        sql = ''' INSERT INTO onsets(version, recording_id, start_time_seconds, duration_seconds, device_super_name, device_name, recordingDateTime, recordingDateTimeNZ)
                  VALUES(?,?,?,?,?,?,?,?) '''
        cur2 = get_database_connection().cursor()
        cur2.execute(sql, (version, recording_id, start_time_seconds, duration_seconds, device_super_name, device_name, recordingDateTime, recordingDateTimeNZ))
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
    y = highpass_filter_with_parameters(y=y, sr=sr, filter_stop_freq=600, filter_pass_freq=650 )
    y = apply_lowpass_filter(y, sr)    
    return y
    
# def create_onsets_in_local_db_using_existing_tag_type(existing_tag_type):
#     # Get recording names that have already been tagged with existing_tag_type e.g somewhere in the recording a morepork tag has already been created
#     recording_ids_with_tag_type = get_unique_recording_ids_that_have_been_tagged_with_this_tag_stored_locally(existing_tag_type)
#     count = 0
#     number_of_recordings = len(recording_ids_with_tag_type)
#     total_onset_pairs_including_more_than_20 = 0
#     total_onset_pairs_including_not_including_more_20 = 0
#     for recording_id_with_tag_type in recording_ids_with_tag_type:
#         count+=1
#         print('Processing recording ', count, ' of ', number_of_recordings, ' recordings.')
#         recording_filename = str(recording_id_with_tag_type[0]) + '.m4a'
#         count_of_onset_pairs_including_more_than_20, count_of_onset_pairs_including_not_including_more_20 = create_onsets_in_local_db(recording_filename)
#         total_onset_pairs_including_more_than_20 += count_of_onset_pairs_including_more_than_20
#         total_onset_pairs_including_not_including_more_20 += count_of_onset_pairs_including_not_including_more_20
#         print('total_onset_pairs_including_more_than_20:', total_onset_pairs_including_more_than_20)
#         print('total_onset_pairs_including_not_including_more_20:', total_onset_pairs_including_not_including_more_20, '\n')
        
   
def create_onsets_in_local_db_using_recordings_folder():
    
    # First need to find out what recordings have previously been used to create onsets - as we don't want to repeat
    
    cur = get_database_connection().cursor()
  
#     recordings_folder_with_path = base_folder + '/' + downloaded_recordings_folder
#     total_number_of_files = len(os.listdir(recordings_folder_with_path))
    total_onset_pairs_including_more_than_40 = 0
    total_onset_pairs_including_not_including_more_40 = 0
    
    # https://stackoverflow.com/questions/2686254/how-to-select-all-records-from-one-table-that-do-not-exist-in-another-table
    # It is possible that some recordings will not produce any onsets, so will also write to recording table that the recording has been processed.
    # Perhaps if I was starting again, I could drop the sub query (if I update the recordings db so show that the old ones have been processed.

    cur.execute("SELECT recording_id, filename,  recordingDateTime FROM recordings WHERE processed_for_onsets IS NULL AND recording_id NOT IN (SELECT recording_id FROM onsets) ORDER BY recording_id DESC")
    recordings_with_no_onsets = cur.fetchall()
    print('There are ', len(recordings_with_no_onsets), ' recordings with no onsets')     
      
    

    count = 0
    number_of_recordings_with_no_onsets = len(recordings_with_no_onsets)
    for recording_with_no_onsets in recordings_with_no_onsets: 
        try: 
            count += 1
            recording_id = recording_with_no_onsets[0]
            filename = recording_with_no_onsets[1]
           
            
            print('Processing ',count, ' of ', number_of_recordings_with_no_onsets)
            print('Recording id is ', recording_with_no_onsets) 
            count_of_onset_pairs_including_more_than_40, count_of_onset_pairs_including_not_including_more_40 = create_onsets_in_local_db(filename)
            
            # Update recordings table to show that this recording has been processed for onsets
#             cur2 = get_database_connection().cursor()
            cur.execute("UPDATE recordings SET processed_for_onsets = 1 WHERE recording_id = ?", (recording_id,))  
            get_database_connection().commit()
            
            total_onset_pairs_including_more_than_40 += count_of_onset_pairs_including_more_than_40
            total_onset_pairs_including_not_including_more_40 += count_of_onset_pairs_including_not_including_more_40
            print('total_onset_pairs_including_more_than_40:', total_onset_pairs_including_more_than_40)
            print('total_onset_pairs_including_not_including_more_40:', total_onset_pairs_including_not_including_more_40, '\n')
        except Exception as e:
#             print(e, '\n')
            print('Error processing file ', recording_id, '\n')
            cur.execute("UPDATE recordings SET processed_for_onsets = -1 WHERE recording_id = ?", (recording_id,))  
            get_database_connection().commit()
    

    
    
def create_onsets_in_local_db(filename): 
    try:
        recordings_folder_with_path = base_folder + '/' + downloaded_recordings_folder
        
        count_of_onset_pairs_including_more_than_40 = 0
        count_of_onset_pairs_including_not_including_more_40 = 0
        
        audio_in_path = recordings_folder_with_path + "/" + filename
        
        # Some recordings are not available
        if not os.path.isfile(audio_in_path):
            print("This recording is not available ", filename)
            # Update the db to say that it has been processed
            
            
            
        
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

                insert_onset_list_into_db(version, recording_id, onsets)
                
        return count_of_onset_pairs_including_more_than_40, count_of_onset_pairs_including_not_including_more_40 

    except Exception:
#         print(e, '\n')
        pass
                
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
                insert_onset_into_database(version, recording_id, onset, squawk_duration_seconds)
                print("Inserting onset into database " , onset)
                

    

def find_paired_squawks_in_single_recordings(y, sr):

    squawks = FindSquawks(y, sr)
    squawks_secs = []

    for squawk in squawks:
        squawk_start = squawk['start']
        squawk_start_sec = squawk_start / sr
        squawks_secs.append(round(squawk_start_sec, 1))
      
    paired_squawks_sec = []
    prev_squawk_sec = None
    
    for squawk_sec in enumerate(squawks_secs):      
        if prev_squawk_sec == None:
            prev_squawk_sec = squawk_sec
            continue     
        
        time_between_squawks = squawk_sec[1] - prev_squawk_sec[1]
        
        if time_between_squawks < 0.8: # sr is one second, so hoping this is the second part of more pork
            paired_squawks_sec.append(prev_squawk_sec[1])
        
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
    onsets = get_onsets_stored_locally('')   
      
#     for entry in os.scandir(onset_pairs_folder_path): 
    for onset in onsets:
        try:
            print('Processing onset ', count, ' of ', len(onsets), ' onsets.')
            count+=1    

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
            mel_spectrogram = librosa.feature.melspectrogram(y=y_part, sr=sr, n_mels=32, fmin=700,fmax=1000)
            
            pylab.axis('off') # no axis
            pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[]) # Remove the white edge
            librosa.display.specshow(mel_spectrogram, cmap='binary') #https://matplotlib.org/examples/color/colormaps_reference.html
            pylab.savefig(image_out_path, bbox_inches=None, pad_inches=0)
            pylab.close()
            
        except Exception as e:
            print(e, '\n')
            print('Error processing onset ', onset)

def create_spectrogram_jpg_files_for_next_model_run_or_model_test(testing):
    
    cur = get_database_connection().cursor()
    
    if testing:
        mel_spectrograms_out_folder_path = base_folder + '/' + run_folder + '/' + spectrograms_for_model_testing_folder 
        cur.execute("SELECT ID, recording_id, startTime, actual_confirmed FROM model_run_result WHERE modelRunName = ? AND actual_confirmed IS NOT NULL AND used_to_create_model IS NULL", (model_run_name, )) 
    else:        
        mel_spectrograms_out_folder_path = base_folder + '/' + run_folder + '/' + spectrograms_for_model_creation_folder 
        cur.execute("SELECT ID, recording_id, startTime, actual_confirmed FROM model_run_result WHERE modelRunName = ? AND actual_confirmed IS NOT NULL", (model_run_name, ))
        
        # Also going to take this opportunity to create the model_run directory so it is available later in Weka for saving the model
        weka_model_folder_path = base_folder + '/' + run_folder + '/' + weka_model_folder 
        if not os.path.exists(weka_model_folder_path):
            os.makedirs(weka_model_folder_path)
        
    if not os.path.exists(mel_spectrograms_out_folder_path):
        os.makedirs(mel_spectrograms_out_folder_path)
        
        
  

    count = 0
    

    rows = cur.fetchall()  
    
    for row in rows:
        try:
            print('Processing row ', count, ' of ', len(rows), ' rows.')
            count+=1
            print('row ', row)
            recording_id = row[1] 
            start_time_seconds = row[2]
            actual_confirmed = row[3]  
            
            if not actual_confirmed:
                # actual_confirmed will be null for testing
                actual_confirmed = "unknown"
#             
            audio_filename = str(recording_id) + '.m4a'
            audio_in_path = base_folder  + '/' + downloaded_recordings_folder + '/' +  audio_filename 
            
            # Also need the device super name in the filename so that it can be used by the model
            cur1 = get_database_connection().cursor()    
            cur1.execute("select distinct device_super_name from recordings where recording_id = ?", (recording_id,))      
            device_super_name = cur1.fetchall()
            print('device_super_name', device_super_name[0][0])
                
#             print('recording_id ', recording_id)
            
#             image_out_name = actual_confirmed + '$' + str(recording_id) + '$' + str(start_time_seconds) + '.jpg'
            image_out_name = device_super_name[0][0] + '$' + actual_confirmed + '$' + str(recording_id) + '$' + str(start_time_seconds) + '.jpg'
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
#         print('image_out_name', image_out_name)           
       
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
        
#         return get_image(image_out_path)
        
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

def get_unique_locations(table_name):   
    cur = get_database_connection().cursor()
    if table_name == 'recordings':
        cur.execute("SELECT DISTINCT device_super_name FROM recordings") 
    else:
        cur.execute("SELECT DISTINCT device_super_name FROM tags") 
    rows = cur.fetchall()  
    
    unique_locations = []
    unique_locations.append('Not Used')
    for row in rows:
        unique_locations.append(row[0])        
        
    return unique_locations  



    
def create_arff_file_for_weka_image_filter_input(test_arff):
    
    run_folder_path = base_folder + '/' + run_folder
    
    if test_arff:
        spectrograms_folder_path = run_folder_path + '/' + spectrograms_for_model_testing_folder
        f= open(run_folder_path + '/' + arff_file_for_weka_model_testing,"w+")
    else:        
        spectrograms_folder_path = run_folder_path + '/' + spectrograms_for_model_creation_folder 
        f= open(run_folder_path + '/' + arff_file_for_weka_model_creation,"w+") 
    
   
#     f= open(run_folder_path + '/' + arff_file_for_weka_model_creation,"w+")
    f.write('@relation ' + relation_name + '\r\n')
    f.write('@attribute filename string' + '\r\n')
    # Add in the device super names attribute
    # Get list of unique 
    cur = get_database_connection().cursor()    
#     cur.execute("select distinct device_super_name from model_run_result where modelRunName = ?", (model_run_name,))    
    cur.execute("select distinct device_super_name from recordings") # This means that any device has had recordings downloaded will be included in arff file header. Previously I was using model_run_result, which wouldn't have new names.   
    device_super_names = cur.fetchall()
    numberOfSuperNames = len(device_super_names)
    print('numberOfSuperNames ', numberOfSuperNames)
    
    device_super_names_str = ''
    print(device_super_names_str)
    
    count = 0
    for device_super_name in device_super_names:  
        count+=1    
        print(device_super_name[0])  
        device_super_names_str+= device_super_name[0]
        if count < numberOfSuperNames: # Do not want a comma at the end of the string for arff format
            device_super_names_str+= ', '
   
    print(device_super_names_str)
    f.write('@attribute deviceSuperName {' + device_super_names_str +'}' + '\r\n')
    
    f.write('@attribute class {' + class_names +'}' + '\r\n')
    f.write('@data' + '\r\n')    
     
   
    for filename in os.listdir(spectrograms_folder_path):
        filename_parts = filename.split('$')
        deviceSuperName = filename_parts[0]
        class_type = filename_parts[1]
        print('image', filename)
        print('class_type', class_type)
#         f.write(filename +',' + class_type + '\r\n')deviceSuperName
        f.write(filename +',' + deviceSuperName +',' + class_type + '\r\n')
        
    f.close()
    
   
    
def create_arff_file_for_weka(test_arff):
#  IF test_arff IS true, then just create an arff file for a single onset - to be used to give to the model for a class prediction
    
    run_folder_path = base_folder + '/' + run_folder
    
    if test_arff:       
        f= open(run_folder_path + '/' + arff_file_for_weka_model_testing,"w+")
    else:
        f= open(run_folder_path + '/' + arff_file_for_weka_model_creation,"w+") 
        f_csv_file_for_keeping_track_of_onsets_used_to_create_model = open(run_folder_path + '/' + csv_file_for_keeping_track_of_onsets_used_to_create_model,"w+") 
       
#     f= open(run_folder_path + '/' + arff_file_for_weka_model_creation,"w+")
    f.write('@relation ' + relation_name + '\r\n')
#     f.write('@attribute filename string' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram0\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram1\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram2\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram3\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram4\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram5\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram6\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram7\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram8\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram9\' numeric' + '\r\n')
    
    f.write('@attribute \'MPEG-7 Edge Histogram10\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram11\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram12\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram13\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram14\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram15\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram16\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram17\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram18\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram19\' numeric' + '\r\n')
    
    f.write('@attribute \'MPEG-7 Edge Histogram20\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram21\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram22\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram23\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram24\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram25\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram26\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram27\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram28\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram29\' numeric' + '\r\n')
    
    f.write('@attribute \'MPEG-7 Edge Histogram30\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram31\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram32\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram33\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram34\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram35\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram36\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram37\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram38\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram39\' numeric' + '\r\n')
    
    f.write('@attribute \'MPEG-7 Edge Histogram40\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram41\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram42\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram43\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram44\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram45\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram46\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram47\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram48\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram49\' numeric' + '\r\n')
    
    f.write('@attribute \'MPEG-7 Edge Histogram50\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram51\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram52\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram53\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram54\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram55\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram56\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram57\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram58\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram59\' numeric' + '\r\n')
    
    f.write('@attribute \'MPEG-7 Edge Histogram60\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram61\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram62\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram63\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram64\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram65\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram66\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram67\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram68\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram69\' numeric' + '\r\n')
    
    f.write('@attribute \'MPEG-7 Edge Histogram70\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram71\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram72\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram73\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram74\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram75\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram76\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram77\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram78\' numeric' + '\r\n')
    f.write('@attribute \'MPEG-7 Edge Histogram79\' numeric' + '\r\n')
    


    # Add in the device super names attribute
    # Get list of unique 
    cur = get_database_connection().cursor()    
#     cur.execute("select distinct device_super_name from model_run_result where modelRunName = ?", (model_run_name,))    
    cur.execute("select distinct device_super_name from recordings") # This means that any device has had recordings downloaded will be included in arff file header. Previously I was using model_run_result, which wouldn't have new names.   
    device_super_names = cur.fetchall()
    numberOfSuperNames = len(device_super_names)
    print('numberOfSuperNames ', numberOfSuperNames)
    
    device_super_names_str = ''
    print(device_super_names_str)
    
    count = 0
    for device_super_name in device_super_names:  
        count+=1    
        print(device_super_name[0])  
        device_super_names_str+= device_super_name[0]
        if count < numberOfSuperNames: # Do not want a comma at the end of the string for arff format
            device_super_names_str+= ', '
   
    print(device_super_names_str)
    f.write('@attribute deviceSuperName {' + device_super_names_str +'}' + '\r\n')
    
    f.write('@attribute class {' + class_names +'}' + '\r\n')
    f.write('@data' + '\r\n')    
    
    sql = '''SELECT
        MPEG7_Edge_Histogram0,
        MPEG7_Edge_Histogram1,
        MPEG7_Edge_Histogram2,
        MPEG7_Edge_Histogram3,
        MPEG7_Edge_Histogram4,
        MPEG7_Edge_Histogram5,
        MPEG7_Edge_Histogram6,
        MPEG7_Edge_Histogram7,
        MPEG7_Edge_Histogram8,
        MPEG7_Edge_Histogram9,
        
        MPEG7_Edge_Histogram10, 
        MPEG7_Edge_Histogram11,
        MPEG7_Edge_Histogram12,
        MPEG7_Edge_Histogram13,
        MPEG7_Edge_Histogram14,
        MPEG7_Edge_Histogram15,
        MPEG7_Edge_Histogram16,
        MPEG7_Edge_Histogram17,
        MPEG7_Edge_Histogram18,
        MPEG7_Edge_Histogram19,
        
        MPEG7_Edge_Histogram20,
        MPEG7_Edge_Histogram21,
        MPEG7_Edge_Histogram22,
        MPEG7_Edge_Histogram23,
        MPEG7_Edge_Histogram24,
        MPEG7_Edge_Histogram25,
        MPEG7_Edge_Histogram26,
        MPEG7_Edge_Histogram27,
        MPEG7_Edge_Histogram28,
        MPEG7_Edge_Histogram29,
        
        MPEG7_Edge_Histogram30,
        MPEG7_Edge_Histogram31,
        MPEG7_Edge_Histogram32,
        MPEG7_Edge_Histogram33,
        MPEG7_Edge_Histogram34,
        MPEG7_Edge_Histogram35,
        MPEG7_Edge_Histogram36,
        MPEG7_Edge_Histogram37,
        MPEG7_Edge_Histogram38,
        MPEG7_Edge_Histogram39,
        
        MPEG7_Edge_Histogram40, 
        MPEG7_Edge_Histogram41,
        MPEG7_Edge_Histogram42,
        MPEG7_Edge_Histogram43,
        MPEG7_Edge_Histogram44,
        MPEG7_Edge_Histogram45,
        MPEG7_Edge_Histogram46,
        MPEG7_Edge_Histogram47,
        MPEG7_Edge_Histogram48,
        MPEG7_Edge_Histogram49,
        
        MPEG7_Edge_Histogram50, 
        MPEG7_Edge_Histogram51,
        MPEG7_Edge_Histogram52,
        MPEG7_Edge_Histogram53,
        MPEG7_Edge_Histogram54,
        MPEG7_Edge_Histogram55,
        MPEG7_Edge_Histogram56,
        MPEG7_Edge_Histogram57,
        MPEG7_Edge_Histogram58,
        MPEG7_Edge_Histogram59,
        
        MPEG7_Edge_Histogram60,
        MPEG7_Edge_Histogram61,
        MPEG7_Edge_Histogram62,
        MPEG7_Edge_Histogram63,
        MPEG7_Edge_Histogram64,
        MPEG7_Edge_Histogram65,
        MPEG7_Edge_Histogram66,
        MPEG7_Edge_Histogram67,
        MPEG7_Edge_Histogram68,
        MPEG7_Edge_Histogram69,
        
        MPEG7_Edge_Histogram70,
        MPEG7_Edge_Histogram71,
        MPEG7_Edge_Histogram72,
        MPEG7_Edge_Histogram73,
        MPEG7_Edge_Histogram74,
        MPEG7_Edge_Histogram75,
        MPEG7_Edge_Histogram76,
        MPEG7_Edge_Histogram77,
        MPEG7_Edge_Histogram78,
        MPEG7_Edge_Histogram79,        
                
        device_super_name, 
        actual_confirmed,
        recording_id,
        start_time_seconds
            
    
        FROM onsets
        
        WHERE actual_confirmed IS NOT NULL AND MPEG7_Edge_Histogram0 IS NOT NULL
        '''
    cur.execute(sql)      
    confirmedOnsets = cur.fetchall()
    
    for confirmedOnset in confirmedOnsets:
        f.write(str(confirmedOnset[0]) +',' + 
                str(confirmedOnset[1]) +',' + 
                str(confirmedOnset[2]) +',' +
                str(confirmedOnset[3]) +',' +
                str(confirmedOnset[4]) +',' +
                str(confirmedOnset[5]) +',' +
                str(confirmedOnset[6]) +',' +
                str(confirmedOnset[7]) +',' +
                str(confirmedOnset[8]) +',' +
                str(confirmedOnset[9]) +',' +
                
                str(confirmedOnset[10]) +',' + 
                str(confirmedOnset[11]) +',' + 
                str(confirmedOnset[12]) +',' +
                str(confirmedOnset[13]) +',' +
                str(confirmedOnset[14]) +',' +
                str(confirmedOnset[15]) +',' +
                str(confirmedOnset[16]) +',' +
                str(confirmedOnset[17]) +',' +
                str(confirmedOnset[18]) +',' +
                str(confirmedOnset[19]) +',' +
                
                str(confirmedOnset[20]) +',' + 
                str(confirmedOnset[21]) +',' + 
                str(confirmedOnset[22]) +',' +
                str(confirmedOnset[23]) +',' +
                str(confirmedOnset[24]) +',' +
                str(confirmedOnset[25]) +',' +
                str(confirmedOnset[26]) +',' +
                str(confirmedOnset[27]) +',' +
                str(confirmedOnset[28]) +',' +
                str(confirmedOnset[29]) +',' +
                
                str(confirmedOnset[30]) +',' + 
                str(confirmedOnset[31]) +',' + 
                str(confirmedOnset[32]) +',' +
                str(confirmedOnset[33]) +',' +
                str(confirmedOnset[34]) +',' +
                str(confirmedOnset[35]) +',' +
                str(confirmedOnset[36]) +',' +
                str(confirmedOnset[37]) +',' +
                str(confirmedOnset[38]) +',' +
                str(confirmedOnset[39]) +',' +
                
                str(confirmedOnset[40]) +',' + 
                str(confirmedOnset[41]) +',' + 
                str(confirmedOnset[42]) +',' +
                str(confirmedOnset[43]) +',' +
                str(confirmedOnset[44]) +',' +
                str(confirmedOnset[45]) +',' +
                str(confirmedOnset[46]) +',' +
                str(confirmedOnset[47]) +',' +
                str(confirmedOnset[48]) +',' +
                str(confirmedOnset[49]) +',' +
                
                str(confirmedOnset[50]) +',' + 
                str(confirmedOnset[51]) +',' + 
                str(confirmedOnset[52]) +',' +
                str(confirmedOnset[53]) +',' +
                str(confirmedOnset[54]) +',' +
                str(confirmedOnset[55]) +',' +
                str(confirmedOnset[56]) +',' +
                str(confirmedOnset[57]) +',' +
                str(confirmedOnset[58]) +',' +
                str(confirmedOnset[59]) +',' +
                
                str(confirmedOnset[60]) +',' + 
                str(confirmedOnset[61]) +',' + 
                str(confirmedOnset[62]) +',' +
                str(confirmedOnset[63]) +',' +
                str(confirmedOnset[64]) +',' +
                str(confirmedOnset[65]) +',' +
                str(confirmedOnset[66]) +',' +
                str(confirmedOnset[67]) +',' +
                str(confirmedOnset[68]) +',' +
                str(confirmedOnset[69]) +',' +
                
                str(confirmedOnset[70]) +',' + 
                str(confirmedOnset[71]) +',' + 
                str(confirmedOnset[72]) +',' +
                str(confirmedOnset[73]) +',' +
                str(confirmedOnset[74]) +',' +
                str(confirmedOnset[75]) +',' +
                str(confirmedOnset[76]) +',' +
                str(confirmedOnset[77]) +',' +
                str(confirmedOnset[78]) +',' +
                str(confirmedOnset[79]) +',' +
              
                confirmedOnset[80] +',' +           # This is deviceSuperName
                confirmedOnset[81] + '\r\n')        # This is confirmed sound/class type   
        f_csv_file_for_keeping_track_of_onsets_used_to_create_model.write(parameters.model_run_name + "," + str(confirmedOnset[82]) + "," + str(confirmedOnset[83]) + '\r\n') 
     
   
#     for filename in os.listdir(spectrograms_folder_path):
#         filename_parts = filename.split('$')
#         deviceSuperName = filename_parts[0]
#         class_type = filename_parts[1]
#         print('image', filename)
#         print('class_type', class_type)
# #         f.write(filename +',' + class_type + '\r\n')deviceSuperName
#         f.write(filename +',' + deviceSuperName +',' + class_type + '\r\n')
        
    f.close()
    f_csv_file_for_keeping_track_of_onsets_used_to_create_model.close();
          
            
def create_folders_for_next_run():
    next_run_folder = parameters.base_folder + '/' + run_folder
    if not os.path.exists(next_run_folder):
        os.makedirs(next_run_folder) 
        
        
    weka_model_folder_path = parameters.base_folder + '/' + run_folder + '/' + weka_model_folder  
    if not os.path.exists(weka_model_folder_path):
        os.makedirs(weka_model_folder_path) 
        
    spectrograms_for_model_creation_folder_path = parameters.base_folder + '/' + run_folder + '/' + spectrograms_for_model_creation_folder  
    if not os.path.exists(spectrograms_for_model_creation_folder_path):
        os.makedirs(spectrograms_for_model_creation_folder_path) 
        
    single_spectrogram_for_classification_folder_path = parameters.base_folder + '/' + run_folder + '/' + weka_model_folder + '/' + single_spectrogram_for_classification_folder  
    if not os.path.exists(single_spectrogram_for_classification_folder_path):
        os.makedirs(single_spectrogram_for_classification_folder_path) 
        
def get_single_recording_info_from_local_db(recording_id):

    cur = get_database_connection().cursor()
    cur.execute("SELECT device_super_name, recordingDateTime FROM recordings WHERE recording_id = ?", (recording_id,))  
  
    recordings = cur.fetchall()
     
    single_recording =  recordings[0]   
    device_super_name = single_recording[0]
    recordingDateTime = single_recording[1]
    
    date_time_obj = datetime.strptime(recordingDateTime, "%Y-%m-%dT%H:%M:%S.000Z")    
    date_time_obj_Zulu = timezone('Zulu').localize(date_time_obj)

#     fmt = "%Y-%m-%d %H:%M:%S %Z%z"
#     fmt = "%Y-%m-%d %H:%M:%S"
    fmt = "%Y-%m-%d %H:%M"
    
    date_time_obj_NZ = date_time_obj_Zulu.astimezone(timezone('Pacific/Auckland'))

    return device_super_name, date_time_obj_NZ.strftime(fmt)

def update_onsets_with_latest_model_run_actual_confirmed():
    cur = get_database_connection().cursor()
    previous_model_run = "2019_12_05_1"
    
    cur.execute("SELECT recording_id, startTime, actual_confirmed FROM model_run_result WHERE actual_confirmed IS NOT NULL AND modelRunName = ?", (previous_model_run,)) 
    
    confirmed_rows = cur.fetchall()
    
    for confirmed_row in confirmed_rows:
       
        recording_id = confirmed_row[0]
        startTime = confirmed_row[1]
        actual_confirmed = confirmed_row[2]
        
        print(recording_id, ' ', startTime, ' ', actual_confirmed)
        
        cur2 = get_database_connection().cursor()                
        cur2.execute("UPDATE onsets SET actual_confirmed = ? WHERE recording_id = ? AND start_time_seconds = ?", (actual_confirmed, recording_id, startTime))  
                
        get_database_connection().commit()
    

def update_onsets_device_super_name():
    # Used to back fill recording_id into onsets table
    cur = get_database_connection().cursor()
    cur.execute("SELECT ID, recording_id FROM onsets ") 
    onsets = cur.fetchall()
    count = 0
    total = len(onsets)
    for onset in onsets:
        count+=1
        print('Updating ', count, ' of ', total)
        ID = onset[0]
        recording_id = onset[1]
        
        cur1 = get_database_connection().cursor()
        cur1.execute("SELECT device_super_name FROM recordings WHERE recording_id = ?", (recording_id,)) 
        rows = cur1.fetchall() 
        device_super_name = rows[0][0]
        
        cur2 = get_database_connection().cursor()                
        cur2.execute("UPDATE onsets SET device_super_name = ? WHERE ID = ?", (device_super_name, ID))  
                
        get_database_connection().commit()
        
def update_model_run_result_device_super_name():
    # Used to back fill recording_id into onsets table
    cur = get_database_connection().cursor()
    cur.execute("SELECT ID, recording_id FROM model_run_result ") 
    model_run_results = cur.fetchall()
    count = 0
    total = len(model_run_results)
    for model_run_result in model_run_results:
        count+=1
        print('Updating ', count, ' of ', total)
        ID = model_run_result[0]
        recording_id = model_run_result[1]
        
        cur1 = get_database_connection().cursor()
        cur1.execute("SELECT device_super_name FROM recordings WHERE recording_id = ?", (recording_id,)) 
        rows = cur1.fetchall() 
        device_super_name = rows[0][0]
        
        cur2 = get_database_connection().cursor()                
        cur2.execute("UPDATE model_run_result SET device_super_name = ? WHERE ID = ?", (device_super_name, ID))  
                
        get_database_connection().commit()
        
        
def test_query():        
    cur = get_database_connection().cursor()
#     cur.execute("SELECT ID, device_super_name FROM model_run_result WHERE modelRunName = '2019_12_11_1' AND device_super_name = 'Hammond Park' ORDER BY recording_id DESC, startTime ASC")
    cur.execute("SELECT ID, device_super_name FROM model_run_result WHERE modelRunName = '2019_12_11_1' ORDER BY recording_id DESC, startTime ASC")  
    model_run_results = cur.fetchall() 
    count = 0
    total = len(model_run_results)
    for model_run_result in model_run_results:
        count+=1
        print('Processing ', count, ' of ', total)
        ID = model_run_result[0]
        device_super_name = model_run_result[1] 
        print('ID is ', ID, ' device_super_name is ', device_super_name) 
        if count > 20:
            break  
    


def add_tag_to_recording(user_token, recordingId, json_data):
    url = parameters.server_endpoint + parameters.tags_url
    

    payload = "recordingId=" + recordingId + \
        "&tag=" \
        + json_data        
        
    headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Authorization': user_token
            }

    response = requests.request("POST", url, data=payload, headers=headers)

    return response

def test_add_tag_to_recording():
    user_token = get_cacophony_user_token()
    tag = {}
    tag['animal'] = 'bigBirdYY'
    tag['startTime'] = 1
    tag['duration'] = 2
    tag['automatic'] = True
    tag['confidence'] = 0.9
    tag['confirmed'] = True
    json_tag = json.dumps(tag)
    resp = add_tag_to_recording(user_token, "158698", json_tag)
    print('resp is: ', resp.text)

def create_local_tags_from_model_run_result():
    # This will create tags on the local db for using the latest model_run_result
    # Only model_run_results with a probablility >= probability_cutoff_for_tag_creation will used
    cur = get_database_connection().cursor()
    cur.execute("SELECT modelRunName, recording_id, startTime, duration, predictedByModel, probability, actual_confirmed, device_super_name, device_name FROM model_run_result WHERE probability >= ? AND modelRunName = ? AND predictedByModel = ?", (probability_cutoff_for_tag_creation, model_run_name, predictedByModel_tag_to_create)) 
    model_run_results = cur.fetchall()
    count = 0
    for model_run_result in model_run_results:
        try:
            modelRunName = model_run_result[0]
            recording_id = model_run_result[1]
            startTime = model_run_result[2]
            duration = model_run_result[3]
            predictedByModel = model_run_result[4] 
            probability = model_run_result[5] # probability
            actual_confirmed = model_run_result[6]
            device_super_name = model_run_result[7]
            device_name = model_run_result[8]
            
            automatic = 'True'
            created_locally = 1 # 1 is true as using integer in db
            
            now = datetime.now(timezone('Zulu')) 
            fmt = "%Y-%m-%dT%H:%M:%S %Z"
            createdAtDate = now.strftime(fmt)
                  
            confirmed_by_human = 0 # using 0 is false in db
            # If actual_confirmed is NOT NULL, then only create a tag if actual_confirmed == predictedByModel
            if actual_confirmed:
                if actual_confirmed != predictedByModel:
                    print(actual_confirmed, ' ', predictedByModel)
                    print('actual_confirmed != predictedByModel')
                    continue # Don't create tag if actual_confirmed is not the same as predicted (I'm not tempted to upload actual_confirmed, as this would make model look better than it is)
                else:
                    count +=1
                    print('Inserting tag ', count, ' for: ', recording_id, ' ', predictedByModel)
                    confirmed_by_human = 1
                 
            
            cur1 = get_database_connection().cursor()
           
            sql = ''' INSERT INTO tags(modelRunName, recording_id, startTime, duration, what, confidence, device_super_name, device_name, version, automatic, confirmed_by_human, created_locally, createdAt, tagger_username)
                          VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
            cur1.execute(sql, (modelRunName, recording_id, startTime, duration, predictedByModel, probability, device_super_name, device_name, model_version, automatic, confirmed_by_human, created_locally, createdAtDate, cacophony_user_name))
            
            get_database_connection().commit()
        except Exception as e:
            print(e, '\n')
            print('Error processing modelRunName ', modelRunName)
        
    print('Finished creating ', count, ' tags in local database')

def update_device_name_onsets_when_missing():
    cur = get_database_connection().cursor()
    cur.execute("SELECT ID, recording_id FROM onsets WHERE device_name IS NULL")  
    onsets_with_null_device_name = cur.fetchall()
    count = 0
    for onset_with_null_device_name in onsets_with_null_device_name:
        count+=1
        print('Updating ', count, ' of ', len(onsets_with_null_device_name))
        ID = onset_with_null_device_name[0]
        recording_id = onset_with_null_device_name[1]
        
        cur1 = get_database_connection().cursor()
        cur1.execute("SELECT device_name FROM recordings WHERE recording_id = ?", (recording_id,)) 
        rows = cur1.fetchall() 
        device_name = rows[0][0]
        
        cur2 = get_database_connection().cursor()                
        cur2.execute("UPDATE onsets SET device_name = ? WHERE ID = ?", (device_name, ID))  
                
        get_database_connection().commit()
        
def update_device_name_model_run_result_when_missing():
    cur = get_database_connection().cursor()
    cur.execute("SELECT ID, recording_id FROM model_run_result WHERE device_name IS NULL")  
    onsets_with_null_device_name = cur.fetchall()
    count = 0
    for onset_with_null_device_name in onsets_with_null_device_name:
        count+=1
        print('Updating ', count, ' of ', len(onsets_with_null_device_name))
        ID = onset_with_null_device_name[0]
        recording_id = onset_with_null_device_name[1]
        
        cur1 = get_database_connection().cursor()
        cur1.execute("SELECT device_name FROM recordings WHERE recording_id = ?", (recording_id,)) 
        rows = cur1.fetchall() 
        device_name = rows[0][0]
        
        cur2 = get_database_connection().cursor()                
        cur2.execute("UPDATE model_run_result SET device_name = ? WHERE ID = ?", (device_name, ID))  
                
        get_database_connection().commit()   
    print('Finished updating model_run_result device_names') 

def upload_tags_for_all_locations_to_cacophony_server():
    print("About to upload ALL tags to Cacophony Server")
    
    sql = '''select distinct device_super_name from tags'''
    cur = get_database_connection().cursor()  
    cur.execute(sql) 
    rows = cur.fetchall() 
    for row in rows:        
        device_super_name = row[0]
        upload_tags_to_cacophony_server(device_super_name)

def upload_tags_to_cacophony_server(location_filter):
    print("About to upload tags to Cacophony Server")
    user_token = get_cacophony_user_token()
    cur = get_database_connection().cursor()
    
    if location_filter !='not_used':
        cur.execute("SELECT ID, recording_id, startTime, duration, what, automatic, confidence, confirmed_by_human, modelRunName FROM tags WHERE modelRunName = ? AND (copied_to_server IS NULL OR copied_to_server = 0) AND device_super_name = ?", (model_run_name, location_filter))   
    else:            
        cur.execute("SELECT ID, recording_id, startTime, duration, what, automatic, confidence, confirmed_by_human, modelRunName FROM tags WHERE modelRunName = ? AND (copied_to_server IS NULL OR copied_to_server = 0)", (model_run_name,))   
    
    tags_to_send_to_server = cur.fetchall()
    count_of_tags_to_send_to_server = len(tags_to_send_to_server)
    
    if count_of_tags_to_send_to_server < 1:
        print('There are no tags to process :-(')
        return 
    
    count = 0
    for tag_to_send_to_server in tags_to_send_to_server:
        try:
            count+=1
            print('Processing ', count, ' of ', count_of_tags_to_send_to_server)
            ID = tag_to_send_to_server[0]
            recording_id = tag_to_send_to_server[1]
            recording_id_str = str(recording_id)
            startTime = tag_to_send_to_server[2]
            duration = tag_to_send_to_server[3]
            what = tag_to_send_to_server[4]
            automatic_str = tag_to_send_to_server[5]
            
            automatic_bool = (automatic_str == 'True')
            confidence = tag_to_send_to_server[6]
            confirmed_by_human_int = tag_to_send_to_server[7]
            confirmed_by_human_bool = bool(confirmed_by_human_int)
            

                
            tag = {}
            tag['what'] = what
            tag['startTime'] = str(startTime)
            tag['duration'] = str(duration)
            tag['automatic'] = automatic_bool
            tag['confidence'] = str(confidence)
            tag['confirmed'] = confirmed_by_human_bool
            json_tag = json.dumps(tag)

            resp = add_tag_to_recording(user_token, recording_id_str, json_tag)
            resp_dict = json.loads(resp.text)
            
            cur2 = get_database_connection().cursor()  
            
            print('Going to update tags table for recording: ', recording_id_str, ' startTime: ', startTime, ' at ', location_filter, ' with a ', what)
                          
            if resp.ok:                
                success = resp_dict['success']
                print('success is: ', success)
                if success:
                    
                    cur2.execute("UPDATE tags SET copied_to_server = ? WHERE ID = ?", (1, ID)) 
                     
                else:
                    print('Error processing ', recording_id_str, ' ', resp.text)
                    cur2.execute("UPDATE tags SET copied_to_server = ? WHERE ID = ?", (-1, ID))
                
            else:
                error_message = resp_dict['message']
                print('Server returned the error: ', error_message)
                cur2.execute("UPDATE tags SET copied_to_server = ? WHERE ID = ?", (-1, ID))
                
            get_database_connection().commit() 
        
        except Exception as e:
            print(e, '\n')
            print('Error processing tag ', recording_id_str,  ' ', resp.text)


def update_model_run_results_with_onsets_used_to_create_model(model_run_name, csv_filename):
    print(model_run_name)   
    print("\n")   
    print(csv_filename)   
    
    # Extract onsets from csv file.
    with open(csv_filename) as fp:
        line = fp.readline()        
        while line:
          
            lineParts = line.split(',')
            recording_id = lineParts[1]
            start_time = lineParts[2]
            print('recording id is ', recording_id, '\n')
            print('start time is ', start_time, '\n\n')
            
            # now update model_run_result
            cur = get_database_connection().cursor()                
            cur.execute("UPDATE model_run_result SET used_to_create_model = 1 WHERE modelRunName = ? AND recording_id = ? AND startTime = ?", (model_run_name, recording_id, start_time))  
            
                        
            get_database_connection().commit()  
                
            line = fp.readline()
            
    print("Finished updating model run result table") 



def add_device_names_to_arff():
    input_filename = 'arff_file_for_weka_model_creation_image_filtered.arff'
    input_filename_path = parameters.base_folder + '/' + parameters.run_folder + '/' + input_filename
    
    if not os.path.isfile(input_filename_path):
        print(input_filename_path + ' does not exist - stopping')
    
    
    output_filename_path = parameters.base_folder + '/' + parameters.run_folder + '/device_names_added_' + input_filename
    # Get list of unique 
    cur = get_database_connection().cursor()    
    cur.execute("select distinct device_super_name from model_run_result where modelRunName = ?", (model_run_name,))      
    device_super_names = cur.fetchall()
    numberOfSuperNames = len(device_super_names)
    print('numberOfSuperNames ', numberOfSuperNames)
    
    device_super_names_str = ''
    print(device_super_names_str)
    
    count = 0
    for device_super_name in device_super_names:  
        count+=1    
        print(device_super_name[0])  
        device_super_names_str+= device_super_name[0]
        if count < numberOfSuperNames: # Do not want a comma at the end of the string for arff format
            device_super_names_str+= ', '
   
    print(device_super_names_str)
    
    print('input_filename_path ', input_filename_path)
    print('output_filename_path ', output_filename_path)
    
    f_output_filename_path=open(output_filename_path,'w+')
    
    with open(input_filename_path) as fp:
        line = fp.readline()
        data_found = False 
        first_attribute_found = False       
        while line:
            # First need to add the extra @attribute definition
            if not first_attribute_found:
                if line.startswith('@attribute'):
                    first_attribute_found = True
                    # Add in the new attribute description
#                     f_output_filename_path.write('@attribute deviceName { sunny, overcast }\n')
                    f_output_filename_path.write('@attribute deviceName { ' + device_super_names_str +' }\n')
            
            if not data_found:
                if line.startswith('@data'):
                    data_found = TRUE
#                     continue # data will start on next line
                f_output_filename_path.write(line)
            else:
                # Need to find the device name for this recording id
                line_parts = line.split('$')
                recording_id = line_parts[1]
                
                cur2 = get_database_connection().cursor()    
                cur2.execute("select distinct device_super_name from recordings where recording_id = ?", (recording_id,))      
                device_super_name = cur2.fetchall()
                print('device_super_name', device_super_name[0][0])
                
                print('recording_id ', recording_id)
#                 f_output_filename_path.write('adeviceName,' + line)
                f_output_filename_path.write(device_super_name[0][0] + ',' + line)
                
            print(line)
            line = fp.readline()
            
    f_output_filename_path.close()    
            
   

def create_input_arff_file_for_single_onset_prediction(output_filename_path, device_super_name_for_this_onset):
    
#     arff_filename_path = model_folder + '/' + weka_input_arff_filename 
    
#     output_filename_path = parameters.base_folder + '/' + parameters.run_folder + '/weka_model/input.arff'
    f_output_filename_path=open(output_filename_path,'w+')
    f_output_filename_path.write('@relation morepork_more-pork_vs\n')
    f_output_filename_path.write('@attribute filename string\n')
    
    # Add in the device super names attribute
    # Get list of unique 
    cur = get_database_connection().cursor()    
    cur.execute("select distinct device_super_name from recordings")      
    device_super_names = cur.fetchall()
    numberOfSuperNames = len(device_super_names)
#     print('numberOfSuperNames ', numberOfSuperNames)
    
    device_super_names_str = ''
#     print(device_super_names_str)
    
    count = 0
    for device_super_name in device_super_names:  
        count+=1    
#         print(device_super_name[0])  
        device_super_names_str+= device_super_name[0]
        if count < numberOfSuperNames: # Do not want a comma at the end of the string for arff format
            device_super_names_str+= ', '
   
#     print(device_super_names_str)
    f_output_filename_path.write('@attribute deviceSuperName {' + device_super_names_str +'}' + '\r\n')
    
    f_output_filename_path.write('@attribute class {' + class_names +'}' + '\r\n')
    f_output_filename_path.write('@data' + '\r\n')  
#     f_output_filename_path.write('input_image.jpg,unknown' + '\r\n')
    f_output_filename_path.write('input_image.jpg,' + device_super_name_for_this_onset + ',unknown' + '\r\n')    
   
    
    f_output_filename_path.close()




def update_onsets_with_datetime():
    cur = get_database_connection().cursor()
    cur.execute("select ID, recording_id from onsets where recordingDateTime IS NULL")      
    onsets = cur.fetchall()
    numOfOnsets = len(onsets)
    count = 0
    
    for onset in onsets:
        print('Processing ' + str(count) + ' of ' + str(numOfOnsets))
        ID = onset[0]
        recording_id = onset[1]
        print(str(ID) + " " + str(recording_id))
        cur.execute("select recordingDateTime from recordings where recording_id = ?", (recording_id,)) 
        recordingDateTime_results = cur.fetchall()
        recordingDateTime = recordingDateTime_results[0][0]
        print(recordingDateTime)
        
        sql = ''' UPDATE onsets
                SET recordingDateTime = ?               
                WHERE ID = ?'''
        
        cur.execute(sql, (recordingDateTime, ID))
        count+=1
        get_database_connection().commit() 
    
#     get_database_connection().commit()    
             
        
def find_suitable_probability_cutoff():
    cur = get_database_connection().cursor()
    
    sql = '''
    select device_super_name, device_name, probability, used_to_create_model, recording_id, startTime, predictedByModel, actual_confirmed,  strftime('%m', recordingDateTime) as month, strftime('%Y', recordingDateTime) as year
    from model_run_result
    where modelRunName = '2020_02_08_1' and actual_confirmed is not null
    order by probability DESC
    '''
    
    
    cur.execute(sql)      
    model_run_results = cur.fetchall()
    model_run_result = len(model_run_results)
    count = 0
    
    for model_run_result in model_run_results:
        device_super_name = model_run_result[0]
        device_name = model_run_result[1]
        probability = model_run_result[2]
        used_to_create_model = model_run_result[3]
        recording_id = model_run_result[4]
        startTime = model_run_result[5]
        predictedByModel = model_run_result[6]
        actual_confirmed = model_run_result[7]
        month = model_run_result[8]
        year = model_run_result[9]
        print(device_super_name, " ", device_name, " ", probability, " ", used_to_create_model, " ", recording_id, " ", startTime , " ",predictedByModel, " ", actual_confirmed , " ",month , " ", year)
      

def convert_time_zones(day_time_from_database):
    # recording ID is  319810 - server says time is Thu Jun 13 2019, 06:42:00
#     day_time_from_database = '2019-06-12T18:42:00.000Z'
    day_time_from_database_00_format = datetime.fromisoformat(day_time_from_database.replace('Z', '+00:00'))
    print('day_time_from_database_00_format: ', day_time_from_database_00_format)
    nz = timezone('NZ')
    day_time_nz = day_time_from_database_00_format.astimezone(nz)
    print('day_time_nz: ', day_time_nz)
    return day_time_nz
    
def update_table_with_NZ_time():
    table_name = 'recordings'
    
    cur = get_database_connection().cursor()
    cur.execute("select ID, recordingDateTime from " + table_name + " where recordingDateTimeNZ IS NULL")      
    records = cur.fetchall()
    numOfRecords = len(records)
    count = 0
    
    for record in records:
        try:        
        
            ID = record[0]
            recordingDateTime = record[1]
            
            print('Processing ID ' + str(ID) + " which is " + str(count) + ' of ' + str(numOfRecords))
            
            recordingDateTimeNZ = convert_time_zones(recordingDateTime)
            
            sql = ''' UPDATE ''' + table_name + ''' 
                    SET recordingDateTimeNZ = ?               
                    WHERE ID = ?'''
            
            cur.execute(sql, (recordingDateTimeNZ, ID))
            count+=1
            get_database_connection().commit() 
            
        except Exception as e:
            print(str(e))
            print("Error processing ID " + str(ID))
        
    
