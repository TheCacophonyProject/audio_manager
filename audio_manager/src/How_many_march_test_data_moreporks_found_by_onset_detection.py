'''
Created on 22 Aug. 2020

@author: tim
'''

import functions
import parameters




def run():
    print("Started")
    march_test_data_moreporks = functions.get_march_2020_test_data_for_morepork_morepork()
    print(len(march_test_data_moreporks))
    
    
    count_of_matching_onsets_test_moreporks = 0
    for march_test_data_morepork in march_test_data_moreporks:
        recording_id = march_test_data_morepork[0]
        start_time_seconds = march_test_data_morepork[1]
        
        
        # see if this has a matching onset
        count = functions.find_matching_onset(recording_id, start_time_seconds)
        print("Count ", count)
        if count > 0:
            count_of_matching_onsets_test_moreporks+=1
            
        print("count_of_matching_onsets_test_moreporks ", count_of_matching_onsets_test_moreporks)
        
        
    
    
    
    
    
    
run()