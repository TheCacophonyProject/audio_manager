'''
Created on 11 Aug. 2020
Playing with turning a sound into a fourier transform
@author: tim
'''


import parameters

import librosa
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
from pathlib import Path

import functions

def run():
    recording_id = 577666
    start_time = 1
    duration = 1
    
    audio_in_path = functions.getRecordingsFolder() + '/' + str(recording_id) + '.m4a'
    print('audio_in_path ', audio_in_path)
    print('start_time ', 1)
    print('duration ', 1)

    audio_out_folder = '/home/tim/Work/Temp/'    
       
    Path(audio_out_folder).mkdir(parents=True, exist_ok=True)
    
    audio_out_folder_filename = audio_out_folder  + str(recording_id)  + '.wav'
    
#     audio_in_path = '/home/tim/Work/Cacophony/downloaded_recordings/all_recordings/' + recording_id + '.m4a'

    
    print('audio_out_folder_filename ', audio_out_folder_filename)
    
    y, sr = librosa.load(audio_in_path, sr=16000)
#     y, sr = librosa.load(audio_in_path, sr=None) 
    y_start = sr * start_time
    y_end = (sr * start_time) + (sr * duration)
    y_time_clipped = y[int(y_start):int(y_end)]
    
#     y_time_clipped_amplified = np.int16(y_time_clipped/np.max(np.abs(y_time_clipped)) * 32767) # can't remember where 32767 came from :-(
    
    
    
    y_time_clipped_amplified_filtered = functions.butter_bandpass_filter(y_time_clipped, parameters.morepork_min_freq, parameters.morepork_max_freq, sr)    
  

    sf.write(audio_out_folder_filename, y_time_clipped_amplified_filtered, sr)
#     sf.write(audio_out_folder_filename, y_time_clipped_amplified_filtered, 16000)
#     print("Running")
#     audio_filename = str(577666) + '.m4a'
#     audio_in_path = parameters.base_folder + '/' + parameters.downloaded_recordings_folder + '/' +  audio_filename 
# 
#     y, sr = librosa.load(audio_in_path)
#     print(y.shape)
#     
# #     print("sr is ", sr)
#     
#     time_interval_between_samples = 1/sr
# #     print("time_interval_between_samples is ", time_interval_between_samples)
#     
#     y2 = np.expand_dims(y, axis=1)
#     
#     print(y2.shape)
# #     print(type(y))
# #     
# #     print(len(y))
# #     
# #     print(y.ndim)
#     
# #     arr2 = np.empty((0, 2), float)
# #     arr2 = np.array([[0.0],[0.0]])
# #     arr = np.empty([len(y),2])
# #     print(arr.ndim)
# #     print(arr)
# #     print("arr shpae is: ", arr.shape)
# #     
# #     time=0
# #     for i in range(len(y)):
# #         arr[i,0]=time
# #         arr[i,1]=y[i]
# #         time+=time_interval_between_samples
# #    
#     time = 0#     
#     for i in range(len(y)):
#         np.append(arr2, [time,i], axis=1)        
#         time+=time_interval_between_samples
#     
#     plt.plot(arr)
#     plt.show()


run()