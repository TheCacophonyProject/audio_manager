'''
Created on 5 Sep 2019

@author: tim
'''

#  https://www.youtube.com/watch?v=A0gaXfM1UN0&t=343s
# https://www.youtube.com/watch?v=D8-snVfekto
# How to Program a GUI Application (with Python Tkinter)!
# https://www.tutorialspoint.com/python3/python_gui_programming

HEIGHT = 600
WIDTH = 1400

import tkinter as tk

from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
# from tkinter import ttk
# from tkinter import *

import os
from PIL import ImageTk,Image 

import main.functions as functions
import threading


LARGE_FONT= ("Verdana", 12)


class Main_GUI(tk.Tk):
    # comment
    
    def __init__(self, *args, **kwargs):
        
        
        tk.Tk.__init__(self, *args, **kwargs)        
        tk.Tk.wm_title(self, "Cacophony Audio Manager")
        # https://stackoverflow.com/questions/47829756/setting-frame-width-and-height?rq=1
        container = tk.Frame(self,width=WIDTH, height=HEIGHT)
        container.grid_propagate(False)        
        container.pack(side="top", fill="both", expand=True)        
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
       
        self.frames = {}
        
#         for F in (HomePage, SettingsPage, RecordingsPage, TaggingPage, ClipsPage, ArffPage, CreateWekaModelPage, EvaluateWekaModelPage, CreateOnsetsPage):
        for F in (HomePage, RecordingsPage, TaggingPage, ClipsPage, ArffPage, CreateWekaModelPage, EvaluateWekaModelPage, CreateOnsetsPage, CreateSpectrogramsPage, CreateTagsFromOnsetsPage, EvaluateWekaModelRunResultPage):
        
        
            frame = F(container, self)
            self.frames[F] = frame
            
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(HomePage)
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        
def qf(param):
    print(param)
        
class HomePage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
       
        label = tk.Label(self, text="Home Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
#         settings_button = ttk.Button(self, text="Settings",
#                             command=lambda: controller.show_frame(SettingsPage))    
#         settings_button.pack()
        
        tagging_button = ttk.Button(self, text="Tagging",
                            command=lambda: controller.show_frame(TaggingPage))        
        tagging_button.pack()
        
        recordings_button = ttk.Button(self, text="Recordings",
                            command=lambda: controller.show_frame(RecordingsPage))        
        recordings_button.pack()
        
        clips_button = ttk.Button(self, text="Create audio clips",
                            command=lambda: controller.show_frame(ClipsPage))        
        clips_button.pack()
        
        arff_button = ttk.Button(self, text="Create Weka arff files",
                            command=lambda: controller.show_frame(ArffPage))        
        arff_button.pack()
        
        createWekaModelPage_button = ttk.Button(self, text="Create Weka Model",
                            command=lambda: controller.show_frame(CreateWekaModelPage))        
        createWekaModelPage_button.pack()
        
        evaluateWekaModelPage_button = ttk.Button(self, text="Evaluate Weka model",
                            command=lambda: controller.show_frame(EvaluateWekaModelPage))        
        evaluateWekaModelPage_button.pack()
        
        createOnsetsPage_button = ttk.Button(self, text="Create onsets",
                            command=lambda: controller.show_frame(CreateOnsetsPage))        
        createOnsetsPage_button.pack()
        
        createSpectrogramsPage_button = ttk.Button(self, text="Create Spectrograms",
                            command=lambda: controller.show_frame(CreateSpectrogramsPage))        
        createSpectrogramsPage_button.pack()
        
        createTagsFromOnsetsPage_button = ttk.Button(self, text="Create Tags from Onsets",
                            command=lambda: controller.show_frame(CreateTagsFromOnsetsPage))            
        
        createTagsFromOnsetsPage_button.pack()
        
        evaluateWekaModelRunResultPage_button = ttk.Button(self, text="Evaluate Weka model Run Result",
                            command=lambda: controller.show_frame(EvaluateWekaModelRunResultPage))        
        evaluateWekaModelRunResultPage_button.pack()
        
        
        
# class SettingsPage(tk.Frame):
#     
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         
# 
# #         recordings_Folder = gui_functions.getRecordingsFolderWithOutHome()
# #         recordings_Folder = functions.getRecordingsFolderWithOutHome()
#         
#         
#         # https://www.python-course.eu/tkinter_entry_widgets.php        
#         tk.Label(self,text="Recordings location").grid(column=0, columnspan=1, row=0)
# 
#         #https://stackoverflow.com/questions/16373887/how-to-set-the-text-value-content-of-an-entry-widget-using-a-button-in-tkinter
#         entryText = tk.StringVar()
#         recordings_folder_entry = tk.Entry(self, textvariable=entryText, width=80)
#         recordings_folder_entry.grid(row=0, column=1, columnspan=1)
#         entryText.set( recordings_Folder )
#         
# 
#         tk.Button(self, 
#                   text='Save', command=lambda: functions.saveSettings(recordings_folder_entry.get())).grid(row=6, 
#                                                                column=0, 
#                                                                sticky=tk.W, 
#                                                                pady=4)     
# 
#         tk.Button(self, 
#                   text='Back to Home', 
#                   command=lambda: controller.show_frame(HomePage)).grid(row=6, 
#                                             column=1, 
#                                             sticky=tk.W, 
#                                             pady=4)                  

        
class TaggingPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Tagging Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        get_tags_button = ttk.Button(self, text="Get tags from server",
                            command=lambda: functions.get_all_tags_for_all_devices_in_local_database())
        get_tags_button.pack()  
        
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        button1.pack() 
        
        

class RecordingsPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        title_label = ttk.Label(self, text="Recordings Page", font=LARGE_FONT)
#         label.pack(pady=10,padx=10)
        title_label.grid(column=0, columnspan=1, row=0)
        
        device_name_label = ttk.Label(self, text="Device name e.g fpF7B9AFNn6hvfVgdrJB").grid(column=0, columnspan=1, row=1)
             
        device_name = StringVar(value='fpF7B9AFNn6hvfVgdrJB')
        device_name_entry = tk.Entry(self,  textvariable=device_name, width=30).grid(column=1, columnspan=1, row=1)
        
        device_super_name_label = ttk.Label(self, text="Device Super name (e.g. Hammond Park").grid(column=2, columnspan=1, row=1)
        
        device_super_name = StringVar(value='Hammond Park')
        device_super_name_entry = tk.Entry(self,  textvariable=device_super_name, width=30).grid(column=3, columnspan=1,row=1)
       
        
        
        get_recordings_button = ttk.Button(self, text="Load Recordings from local folder",
                            command=lambda: functions.load_recordings_from_local_folder(device_name.get(), device_super_name.get())).grid(column=0, columnspan=2, row=2)
#         get_recordings_button = ttk.Button(self, text="Load Recordings from local folder",
#                             command=lambda: gui_functions.load_recordings_from_local_folder(device_super_name.get())).grid(column=0, columnspan=1, row=2)
 

        get_recording_information_from_server_button = ttk.Button(self, text="Get Recording Information for recordings imported from local file system",
                            command=lambda: functions.update_recording_information_for_all_local_database_recordings()).grid(column=0, columnspan=2, row=3)
              
        
        get_new_recordings_from_server_button = ttk.Button(self, text="Get New Recordings From Server",
                            command=lambda: functions.get_recordings_from_server(device_name.get(), device_super_name.get())).grid(column=0, columnspan=2, row=4)
        get_new_recordings_from_server_label = ttk.Label(self, text="This will get the recordings for the device in the device name box. It will also assign a super name from the Super Name box").grid(column=2, columnspan=3, row=4)  
                                               
        
        scan_local_folder_for_recordings_not_in_local_db_and_update_button = ttk.Button(self, text="Scan recordings folder for recordings not in local db and update",
                            command=lambda: functions.scan_local_folder_for_recordings_not_in_local_db_and_update(device_name.get(), device_super_name.get())).grid(column=0, columnspan=2, row=5)
                                                
        scan_label = ttk.Label(self, text="If you do NOT know the device name or super name enter unknown in the fields. The device name will be updated automatically").grid(column=2, columnspan=3, row=5)                   
                       
        
        back_to_home_button = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage)).grid(column=0, columnspan=1, row=6)
                            
                   
        
class ClipsPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        unique_tags = functions.get_unique_whats_from_local_db()
                
        title_label = ttk.Label(self, text="Clips Page", font=LARGE_FONT)
        title_label.grid(column=0, columnspan=1, row=0)        
              
        device_super_name_label = ttk.Label(self, text="Device Super name (e.g. Hammond Park)").grid(column=0, columnspan=1, row=1)        
        device_super_name = StringVar(value='Hammond Park')
        device_super_name_entry = tk.Entry(self,  textvariable=device_super_name, width=30).grid(column=1, columnspan=1,row=1)
        
        what_label = ttk.Label(self, text="What (e.g. more pork - classic)").grid(column=0, columnspan=1, row=2)      
                                    
        what = StringVar()
        what_combo = ttk.Combobox(self, textvariable=what, values=unique_tags)
        if len(unique_tags) > 0:
            what_combo.current(0)
            what_combo.grid(column=1, columnspan=1,row=2) 
                
                
        version_label = ttk.Label(self, text="Versions (e.g. morepork_base)").grid(column=0, columnspan=1, row=3)        
        version = StringVar(value='morepork_base')
        version_entry = tk.Entry(self,  textvariable=version, width=30).grid(column=1, columnspan=1,row=3)
        
        
        run_base_folder_label = ttk.Label(self, text="Base folder for output (e.g. /home/tim/Work/Cacophony/Audio_Analysis/audio_classifier_runs)").grid(column=0, columnspan=1, row=4)           
        run_base_folder_folder = StringVar(value='/home/tim/Work/Cacophony/Audio_Analysis/audio_classifier_runs')
        run_base_folder_entry = tk.Entry(self,  textvariable=run_base_folder_folder, width=110).grid(column=1, columnspan=1,row=4) 
        
        run_folder_label = ttk.Label(self, text="Output (sub)folder where clips will be created (e.g. 2019_09_17_1).").grid(column=0, columnspan=1, row=5)    
        run_folder = StringVar(value='2019_09_17_1')
        run_folder_entry = tk.Entry(self,  textvariable=run_folder, width=110).grid(column=1, columnspan=1,row=5) 
        
        
#         create_clips_button = ttk.Button(self, text="Create Clips",
#                             command=lambda: gui_functions.create_clips(device_super_name.get(), what.get(), version.get(), run_base_folder_folder.get(),run_folder.get() )).grid(column=0, columnspan=2, row=6)
# 
        create_clips_button = ttk.Button(self, text="Create Clips",
                            command=lambda: functions.create_clips(device_super_name.get(), what.get(), version.get(), run_base_folder_folder.get(),run_folder.get() )).grid(column=0, columnspan=2, row=6)

                 
        back_to_home_button = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage)).grid(column=0, columnspan=1, row=7)

                
class ArffPage(tk.Frame):
    
    
    def choose_clip_folder(self, base_folder, run_folder):
        choosen_folder = functions.choose_clip_folder(base_folder, run_folder)
        # https://stackoverflow.com/questions/50227577/update-label-in-tkinter-when-calling-function
        self.clip_folder.set(choosen_folder)
        
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.clip_folder = StringVar(value='')
        openSmile_config_files = functions.getOpenSmileConfigFiles()
        arffTemplateFiles = functions.getArffTemplateFiles()
             
        title_label = ttk.Label(self, text="Create Arff Page", font=LARGE_FONT)
        title_label.grid(column=0, columnspan=1, row=0)    
        
        base_folder_label = ttk.Label(self, text="Base folder (e.g. /home/tim/Work/Cacophony/Audio_Analysis/audio_classifier_runs)").grid(column=0, columnspan=1, row=1)        
        base_folder = StringVar(value='/home/tim/Work/Cacophony/Audio_Analysis/audio_classifier_runs')
        base_folder_entry = tk.Entry(self,  textvariable=base_folder, width=80).grid(column=1, columnspan=1,row=1)    
        
        run_folder_label = ttk.Label(self, text="Run folder (e.g. 2019_09_17_1)").grid(column=0, columnspan=1, row=2)    
        run_folder = StringVar(value='2019_09_17_1')
        run_folder_entry = tk.Entry(self,  textvariable=run_folder, width=80).grid(column=1, columnspan=1,row=2) 
        

        choose_clip_folder_button = ttk.Button(self, text="Choose clip folder",
                            command=lambda: self.choose_clip_folder(base_folder.get(), run_folder.get())).grid(column=0, columnspan=1, row=3)
        self.clip_folder_entry = tk.Entry(self,  textvariable=self.clip_folder, width=80).grid(column=1, columnspan=1,row=3)  

          
        openSmile_config_file_label = ttk.Label(self, text="Name of openSMILE configuration file (e.g. morepork_unknown_label_morpork.conf)").grid(column=0, columnspan=1, row=4)      
        openSmile_config_file = StringVar()
        openSmile_config_combo = ttk.Combobox(self, textvariable=openSmile_config_file, values=openSmile_config_files, width=80)
        openSmile_config_combo.current(0)
        openSmile_config_combo.grid(column=1, columnspan=2,row=4) 
        
        create_arff_button = ttk.Button(self, text="Create Individual Arff Files for each audio file",
                            command=lambda: functions.create_arff_file(base_folder.get(), run_folder.get(), self.clip_folder.get(), openSmile_config_file.get())).grid(column=0, columnspan=1, row=5)
          
        arff_template_file_label = ttk.Label(self, text="Name of openSMILE template arff file (e.g. arff_template.mfcc.arff)").grid(column=0, columnspan=1, row=6)     
        arff_template_file = StringVar()
        arff_template_combo = ttk.Combobox(self, textvariable=arff_template_file, values=arffTemplateFiles, width=80)
        arff_template_combo.current(0)
        arff_template_combo.grid(column=1, columnspan=2,row=6)

        
        merge_arffs_button = ttk.Button(self, text="Merge Arffs",
                            command=lambda: functions.merge_arffs(base_folder.get(), run_folder.get(), arff_template_file.get())).grid(column=0, columnspan=1, row=7)
        
        back_to_home_button = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage)).grid(column=0, columnspan=1, row=8)   
                            
class CreateWekaModelPage(tk.Frame):    
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.clip_folder = StringVar(value='')
        openSmile_config_files = functions.getOpenSmileConfigFiles()
        arffTemplateFiles = functions.getArffTemplateFiles()
             
        title_label = ttk.Label(self, text="Using Weka", font=LARGE_FONT)
        title_label.grid(column=0, columnspan=1, row=0)   
        
        weka_instructions = "To create a Weka model you will need to use the Weka program https://www.cs.waikato.ac.nz/ml/weka/downloading.html\n\
        Once Weka has been installed, you can run it from the weka directory (e.g. weka-3-8-3) using the command weka - jar weka.jar\n\
        These instructions are for how I originally used Weka, but may change in future.\n\
        In Weka, open Explorer, open the merged arff file that you previously created and stored (e.g. at /home/tim/Work/Cacophony/Audio_Analysis/audio_classifier_runs/mfcc_merge_morepork_unknown.arff)\
        Change to the Classify tab, press the choose button and select the model type e.g. Trees LMT.\
        Choose Cross validation, folds 10. Press the start button.\n\
        When finished, right click on the result and choose 'Save Model (e.g. in ... audio_classifier_runs/2019-09-17-1/model_run/model) The file extension is automatically .model.\n\
        You can now use this model in the next page"
        msg = tk.Message(self, text = weka_instructions)
        msg.config(bg='lightgreen', font=('times', 16), width=1200)
        msg.grid(column=0, columnspan=6, row=1)    
        
        
        back_to_home_button = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage)).grid(column=0, columnspan=1, row=8)                
        
class EvaluateWekaModelPage(tk.Frame):
    
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.clip_folder = StringVar(value='')
        openSmile_config_files = functions.getOpenSmileConfigFiles()
        arffTemplateFiles = functions.getArffTemplateFiles()
             
        title_label = ttk.Label(self, text="Evaluate a Weka model", font=LARGE_FONT)
        title_label.grid(column=0, columnspan=1, row=0)    
        
        weka_instructions = "The Weka model was created using arff files.  You can now run the model against the same training arff files \
        and save the results in the database.  Because the training arff files contained the expected result, you will be able to look at \
individual instances to determine if the model got it correct.  Use the Evaluate Weka model Run Result page to do this"

        msg = tk.Message(self, text = weka_instructions)
        msg.config(bg='lightgreen', font=('times', 16), width=1200)
        msg.grid(column=0, columnspan=6, row=1)   
        
        base_folder_label = ttk.Label(self, text="Base folder (e.g. /home/tim/Work/Cacophony/Audio_Analysis/audio_classifier_runs)").grid(column=0, columnspan=1, row=2)        
        base_folder = StringVar(value='/home/tim/Work/Cacophony/Audio_Analysis/audio_classifier_runs')
        base_folder_entry = tk.Entry(self,  textvariable=base_folder, width=80).grid(column=1, columnspan=1,row=2)    
        
        run_folder_label = ttk.Label(self, text="Run folder (e.g. 2019_09_17_1)").grid(column=0, columnspan=1, row=3)    
        run_folder = StringVar(value='2019_09_17_1')
        run_folder_entry = tk.Entry(self,  textvariable=run_folder, width=80).grid(column=1, columnspan=1,row=3) 
        
        arff_folder_label = ttk.Label(self, text="Arff folder - that has the same arff files that were used to create this model (e.g. )").grid(column=0, columnspan=1, row=4)    
        arff_folder = StringVar(value='arff_files')
        arff_folder_entry = tk.Entry(self,  textvariable=arff_folder, width=80).grid(column=1, columnspan=1,row=4) 
        
        modelRunName_label = ttk.Label(self, text="Model run name (usually same as run folder e.g. 2019_09_17_1)").grid(column=0, columnspan=1, row=5)    
        modelRunName = StringVar(value='2019_09_17_1')
        modelRunName_entry = tk.Entry(self,  textvariable=modelRunName, width=80).grid(column=1, columnspan=1,row=5) 
        
        evaluate_button = ttk.Button(self, text="Evaluate Model",
                            command=lambda: functions.process_arff_folder(base_folder.get(), run_folder.get(), arff_folder.get(), modelRunName.get())).grid(column=0, columnspan=1, row=7)
        
#         sqlite_instructions = "Once you have completed the previous step, use the separate 'DB Browser for SQLite' program to find interesting examples by using the 'Browse Data' tab in the 'model_run_result' table.\
#         For example, can filter the results, by typing unknown in the actual column filter, and morepork in the predictedByModel column filter.\
#         Then enter the enter recording id and start time in the fields below to play that clip"
#         msg = tk.Message(self, text = sqlite_instructions)
#         msg.config(bg='lightgreen', font=('times', 16), width=1200)
#         msg.grid(column=0, columnspan=6, row=8)   
#         
#         recording_id_label = ttk.Label(self, text="Recording ID (e.g. 240631").grid(column=0, columnspan=1, row=9)        
#         recording_id = StringVar(value='240631')
#         recording_id_entry = tk.Entry(self,  textvariable=recording_id, width=80).grid(column=1, columnspan=1,row=9)   
#         
#         start_time_label = ttk.Label(self, text="Start time (seconds) (e.g. 4.2").grid(column=0, columnspan=1, row=10)        
#         start_time = StringVar(value='4.2')
#         start_time_entry = tk.Entry(self,  textvariable=start_time, width=80).grid(column=1, columnspan=1,row=10) 
#         
#         duration_label = ttk.Label(self, text="Duration (seconds) e.g. 1.5").grid(column=0, columnspan=1, row=11)        
#         duration = StringVar(value='1.5')
#         duration_entry = tk.Entry(self,  textvariable=duration, width=80).grid(column=1, columnspan=1,row=11)  
#         
#         play_clip_button = ttk.Button(self, text="Play clip",
#                             command=lambda: functions.play_clip(recording_id.get(), start_time.get(), duration.get())).grid(column=0, columnspan=1, row=12)
#          
 

        back_to_home_button = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage)).grid(column=0, columnspan=1, row=15)   
                            
class CreateOnsetsPage(tk.Frame):    
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.clip_folder = StringVar(value='')
       
             
        title_label = ttk.Label(self, text="Create Onsets", font=LARGE_FONT)
        title_label.grid(column=0, columnspan=1, row=0)    
        
        onset_instructions = "Use this page to run the create onsets function that will create locations of \
interest in the db"
        msg = tk.Message(self, text = onset_instructions)
        msg.config(bg='lightgreen', font=('times', 16), width=1200)
        msg.grid(column=0, columnspan=6, row=1)   
        
        existing_tag_type_label = ttk.Label(self, text="Enter the name of an existing tag type - onsets will only be created from recordings that already been tagged with this type").grid(column=0, columnspan=1, row=2)        
        existing_tag_type = StringVar(value='more pork - classic')
        existing_tag_type_entry = tk.Entry(self,  textvariable=existing_tag_type, width=30).grid(column=1, columnspan=1,row=2)    
        
               
        run_button = ttk.Button(self, text="Run",
                            command=lambda: functions.create_onsets(existing_tag_type.get())).grid(column=0, columnspan=1, row=3)
        
       
        
       
 

        back_to_home_button = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage)).grid(column=0, columnspan=1, row=4)                  

class CreateSpectrogramsPage(tk.Frame):    
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.clip_folder = StringVar(value='')
       
             
        title_label = ttk.Label(self, text="Create Spectrograms", font=LARGE_FONT)
        title_label.grid(column=0, columnspan=1, row=0)    
        
        onset_instructions = "Use this page to run the create spectrogram function that will create spectrograms  \
in the spectrogram folder"
        msg = tk.Message(self, text = onset_instructions)
        msg.config(bg='lightgreen', font=('times', 16), width=1200)
        msg.grid(column=0, columnspan=6, row=1)   
        
        
        
        run_button = ttk.Button(self, text="Run",
                            command=lambda: functions.create_focused_mel_spectrogram_jps_using_onset_pairs()).grid(column=0, columnspan=1, row=2)
        
       
        
       
 

        back_to_home_button = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage)).grid(column=0, columnspan=1, row=3)                  

class CreateTagsFromOnsetsPage(tk.Frame):  
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.current_onset_array_pos = 0
                     
        title_label = ttk.Label(self, text="Create Tags From Onsets", font=LARGE_FONT)
        title_label.grid(column=0, columnspan=1, row=0)    
        
        onset_instructions = "Use this page to create Tags from onsets"
        
        msg = tk.Message(self, text = onset_instructions)
        msg.config(bg='lightgreen', font=('times', 16), width=1200)
        msg.grid(column=0, columnspan=6, row=1)   
        
        onset_version_label = ttk.Label(self, text="The version of the onset (field in onset table") 
        onset_version_label.grid(column=0, columnspan=1, row=2)       
        onset_version = StringVar(value='5')
        onset_version_entry = tk.Entry(self,  textvariable=onset_version, width=30)
        onset_version_entry.grid(column=1, columnspan=1,row=2)
        
        recording_id_label = ttk.Label(self, text="Recording Id") 
        recording_id_label.grid(column=0, columnspan=1, row=3)            
        self.recording_id = StringVar(value='0000000')
        self.recording_id_entry = tk.Entry(self,  textvariable=self.recording_id, width=30).grid(column=1, columnspan=1, row=3)
        
        start_time_label = ttk.Label(self, text="Start Time")
        start_time_label.grid(column=2, columnspan=1, row=3)        
        self.start_time = StringVar(value='0.0')
        self.start_time_entry = tk.Entry(self,  textvariable=self.start_time, width=30).grid(column=3, columnspan=1,row=3)
        
        load_onsets_button = ttk.Button(self, text="Load Onsets",command=lambda: get_onsets())
        load_onsets_button.grid(column=0, columnspan=1, row=4)                        

        self.spectrogram_label = ttk.Label(self, image=None)
        self.spectrogram_label.grid(column=0, columnspan=1, row=5)
        
        self.waveform_label = ttk.Label(self, image=None)
        self.waveform_label.grid(column=1, columnspan=1, row=5)

        
        
        
        previous_button = ttk.Button(self, text="Previous", command=lambda: previous_onset())
        previous_button.grid(column=0, columnspan=1, row=6)
                            
        play_button = ttk.Button(self, text="Play", command=lambda: functions.play_clip(str(self.current_onset_recording_id), float(self.current_onset_start_time),self.current_onset_duration))
        play_button.grid(column=1, columnspan=1, row=6)
                            
        next_button = ttk.Button(self, text="Next", command=lambda: next_onset())
        next_button.grid(column=2, columnspan=1, row=6)
                            
                             
        back_to_home_button = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(HomePage))
        back_to_home_button.grid(column=0, columnspan=1, row=7)    
                            
        def get_onsets():            
            self.onsets = functions.get_onsets_stored_locally(onset_version.get())            
            load_current_onset()          
          
            
        def next_onset():
            if self.current_onset_array_pos < (len(self.onsets)) -1:                        
                self.current_onset_array_pos +=1
                load_current_onset()
#                 functions.play_clip(str(self.current_onset_recording_id), float(self.current_onset_start_time),self.current_onset_duration)
                
        def previous_onset():
            if self.current_onset_array_pos > 0:
                self.current_onset_array_pos -=1
                load_current_onset()
                
        def play_clip():
            functions.play_clip(str(self.current_onset_recording_id), float(self.current_onset_start_time),self.current_onset_duration)
                     
        def display_images():
            self.spectrogram_image = functions.get_single_create_focused_mel_spectrogram(self.current_onset_recording_id, self.current_onset_start_time, self.current_onset_duration)
            self.waveform_image = functions.get_single_waveform_image(self.current_onset_recording_id, self.current_onset_start_time, self.current_onset_duration)            
            
            self.spectrogram_label.config(image=self.spectrogram_image)
            self.waveform_label.config(image=self.waveform_image)
            
        def load_current_onset():
            
            current_onset = self.onsets[self.current_onset_array_pos]
             
            self.current_onset_recording_id = current_onset[1]      
            self.recording_id.set(self.current_onset_recording_id)
             
            self.current_onset_start_time = current_onset[2]
            self.start_time.set(self.current_onset_start_time)
            
            self.current_onset_duration = current_onset[3] 
            

            
            
            threading.Thread(target=play_clip(), args=(1,)).start()
            threading.Thread(target=display_images(), args=(1,)).start()
           
         
            
class EvaluateWekaModelRunResultPage(tk.Frame):    
    
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.current_model_run_result_array_pos = 0
        self.current_model_run_name_ID = 0        
        
        self.unique_model_run_names = functions.get_unique_model_run_names()            
                    
        title_label = ttk.Label(self, text="Evaluate Model Run Results", font=LARGE_FONT)
        title_label.grid(column=0, columnspan=1, row=0)   
        
        run_names_label = ttk.Label(self, text="Run Names")
        run_names_label.grid(column=0, columnspan=1, row=1)      
                                    
        self.run_name = StringVar()
        self.run_names_combo = ttk.Combobox(self, textvariable=self.run_name, values=self.unique_model_run_names)
        
        if len(self.unique_model_run_names) > 0:
            self.run_names_combo.current(0)
            self.run_names_combo.grid(column=1, columnspan=1,row=1)         

            
        refresh_model_run_names_button = ttk.Button(self, text="Refresh Unique Model Run Names",command=lambda: refresh_unique_model_run_names())
        refresh_model_run_names_button.grid(column=2, columnspan=1, row=1) 
        
        actual_filter_label = ttk.Label(self, text="Filter - Actual", font=LARGE_FONT)
        actual_filter_label.grid(column=0, columnspan=1, row=2)        
        self.actual_filter = tk.StringVar()
        actual_filter_radio_button_none = ttk.Radiobutton(self,text='No Filter', variable=self.actual_filter, value='no filter')
        actual_filter_radio_button_none.grid(column=0, columnspan=1, row=3)
        actual_filter_radio_button_morepork_classic = ttk.Radiobutton(self,text='morepork_more-pork', variable=self.actual_filter, value='morepork_more-pork')
        actual_filter_radio_button_morepork_classic.grid(column=0, columnspan=1, row=4)
        actual_filter_radio_button_unknown = ttk.Radiobutton(self,text='Unknown', variable=self.actual_filter, value='unknown')
        actual_filter_radio_button_unknown.grid(column=0, columnspan=1, row=5) 
        self.actual_filter.set('no filter')
        
        actual_confirmed_filter_label = ttk.Label(self, text="Filter - Actual Confirmed", font=LARGE_FONT)
        actual_confirmed_filter_label.grid(column=1, columnspan=1, row=2)        
        self.actual_confirmed_filter = tk.StringVar()
        actual_confirmed_filter_radio_button_none = ttk.Radiobutton(self,text='No Filter', variable=self.actual_confirmed_filter, value='no filter')
        actual_confirmed_filter_radio_button_none.grid(column=1, columnspan=1, row=3)
        actual_confirmed_filter_radio_button_morepork_classic = ttk.Radiobutton(self,text='morepork_more-pork', variable=self.actual_confirmed_filter, value='morepork_more-pork')
        actual_confirmed_filter_radio_button_morepork_classic.grid(column=1, columnspan=1, row=4)
        actual_confirmed_filter_radio_button_unknown = ttk.Radiobutton(self,text='Unknown', variable=self.actual_confirmed_filter, value='unknown')
        actual_confirmed_filter_radio_button_unknown.grid(column=1, columnspan=1, row=5) 
        self.actual_confirmed_filter.set('no filter')
        
        predicted_filter_label = ttk.Label(self, text="Filter - Predicted", font=LARGE_FONT)
        predicted_filter_label.grid(column=2, columnspan=1, row=2)        
        self.predicted_filter = tk.StringVar()
        predicted_filter_radio_button_none = ttk.Radiobutton(self,text='No Filter', variable=self.predicted_filter, value='no filter')
        predicted_filter_radio_button_none.grid(column=2, columnspan=1, row=3)
        predicted_filter_radio_button_morepork_classic = ttk.Radiobutton(self,text='morepork_more-pork', variable=self.predicted_filter, value='morepork_more-pork')
        predicted_filter_radio_button_morepork_classic.grid(column=2, columnspan=1, row=4)
        predicted_filter_radio_button_unknown = ttk.Radiobutton(self,text='Unknown', variable=self.predicted_filter, value='unknown')
        predicted_filter_radio_button_unknown.grid(column=2, columnspan=1, row=5) 
        self.predicted_filter.set('no filter')        
        
        load_run_results_button = ttk.Button(self, text="Load Run Results using Filters",command=lambda: get_run_results())
        load_run_results_button.grid(column=3, columnspan=1, row=3) 
        
        self.number_of_results_label_value = tk.StringVar()
        number_of_results_label_for_value = ttk.Label(self, textvariable=self.number_of_results_label_value)
        number_of_results_label_for_value.grid(column=3, columnspan=1, row=4)   
        
        self.recording_id_and_result_place_value = tk.StringVar()
        recording_id_label = ttk.Label(self, textvariable=self.recording_id_and_result_place_value) 
        recording_id_label.grid(column=0, columnspan=1, row=6) 
        self.recording_id_and_result_place_value.set("Recording Id")
                   
#         self.recording_id = StringVar(value='0000000')
#         self.recording_id_entry = tk.Entry(self,  textvariable=self.recording_id, width=30).grid(column=1, columnspan=1, row=6)
        
        start_time_label = ttk.Label(self, text="Start Time")
        start_time_label.grid(column=2, columnspan=1, row=6)        
        self.start_time = StringVar(value='0.0')
        self.start_time_entry = tk.Entry(self,  textvariable=self.start_time, width=30).grid(column=3, columnspan=1,row=6)
        
        
        self.spectrogram_label = ttk.Label(self, image=None)
        self.spectrogram_label.grid(column=0, columnspan=1, row=7)
        
        self.waveform_label = ttk.Label(self, image=None)
        self.waveform_label.grid(column=1, columnspan=1, row=7)        
        
        actual_label = ttk.Label(self, text="Actual", font=LARGE_FONT)
        actual_label.grid(column=0, columnspan=1, row=8) 
        
        self.actual_label_value = tk.StringVar()
        actual_label_for_value = ttk.Label(self, textvariable=self.actual_label_value)
        actual_label_for_value.grid(column=0, columnspan=1, row=9)         
        
        actual_label_confirmed = ttk.Label(self, text="Actual Confirmed", font=LARGE_FONT)
        actual_label_confirmed.grid(column=1, columnspan=1, row=8)
        actual_label_confirmed2 = ttk.Label(self, text="(The default is the same as Actual - select to change and save)")
        actual_label_confirmed2.grid(column=1, columnspan=1, row=9) 
        
        self.actual_confirmed = tk.StringVar()

        actual_confirmed_radio_button_morepork_classic = ttk.Radiobutton(self,text='morepork_more-pork', variable=self.actual_confirmed, value='morepork_more-pork',command=lambda: confirm_actual())
        actual_confirmed_radio_button_morepork_classic.grid(column=1, columnspan=1, row=10)   
                      
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Unknown', variable=self.actual_confirmed, value='unknown',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=1, columnspan=1, row=11)   
        
       
        predicted_label = ttk.Label(self, text="Predicted (by last model run)", font=LARGE_FONT)
        predicted_label.grid(column=2, columnspan=1, row=8)         

        
        self.predicted_label_value = tk.StringVar()
        predicted_label_value_for_value = ttk.Label(self, textvariable=self.predicted_label_value)
        predicted_label_value_for_value.grid(column=2, columnspan=1, row=9) 
        
        
        previous_button = ttk.Button(self, text="Previous", command=lambda: previous_run_result())
        previous_button.grid(column=0, columnspan=1, row=15)
                            
        play_button = ttk.Button(self, text="Play Again", command=lambda: functions.play_clip(str(self.current_model_run_name_recording_id), float(self.current_model_run_name_start_time),self.current_model_run_name_duration))
        play_button.grid(column=1, columnspan=1, row=15)
                            
        next_button = ttk.Button(self, text="Confirm Actual and move Next", command=lambda: next_run_result())
        next_button.grid(column=2, columnspan=1, row=15)
        
        
        back_to_home_button = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(HomePage))
        back_to_home_button.grid(column=0, columnspan=1, row=20) 
        

        def confirm_actual():
            print('self.actual_confirmed.get() ', self.actual_confirmed.get())
            functions.update_model_run_result(self.current_model_run_name_ID, self.actual_confirmed.get())
           
        
        def refresh_unique_model_run_names():
            self.unique_model_run_names = functions.get_unique_model_run_names()
            self.run_names_combo['values'] = self.unique_model_run_names  
            
        def get_run_result():    
            self.run_result = functions.get_model_run_result(int(self.current_model_run_name_ID))   
            self.current_model_run_result_array_pos = 0      
            load_current_model_run_result() 
      
        def get_run_results():    
            print('run_names_combo.get()', self.run_names_combo.get())   
            print('Actual Filter', self.actual_filter.get())   
            print('Predicted Filter', self.predicted_filter.get())        
            self.run_results = functions.get_model_run_results(self.run_names_combo.get(), self.actual_filter.get(), self.actual_confirmed_filter.get(), self.predicted_filter.get())
            number_of_results_returned = len(self.run_results)
            print('number_of_results_returned ', number_of_results_returned)
            self.number_of_results_label_value.set("Number of results: " + str(number_of_results_returned))
            if number_of_results_returned > 0:
                first_result = self.run_results[0]
                self.current_model_run_name_ID = first_result[0]
                print('self.current_model_run_name_ID ', self.current_model_run_name_ID)
#             print(self.run_results)   
                     
                load_current_model_run_result() 
#             get_run_result()
            
       

        def next_run_result(): 
            confirm_actual()           
          
            if self.current_model_run_result_array_pos < (len(self.run_results)) -1:
#                 self.confirm_actual()
                self.current_model_run_result_array_pos +=1
                self.current_model_run_name_ID = self.run_results[self.current_model_run_result_array_pos][0]
                load_current_model_run_result()
             
        def previous_run_result():
            if self.current_model_run_result_array_pos > 0:
                self.current_model_run_result_array_pos -=1
                self.current_model_run_name_ID = self.run_results[self.current_model_run_result_array_pos][0]
                load_current_model_run_result()
                
        def play_clip():
            functions.play_clip(str(self.current_model_run_name_recording_id), float(self.current_model_run_name_start_time),self.current_model_run_name_duration)
                     
        def display_images():
            self.spectrogram_image = functions.get_single_create_focused_mel_spectrogram(self.current_model_run_name_recording_id, self.current_model_run_name_start_time, self.current_model_run_name_duration)
            self.waveform_image = functions.get_single_waveform_image(self.current_model_run_name_recording_id, self.current_model_run_name_start_time, self.current_model_run_name_duration)            
            
            self.spectrogram_label.config(image=self.spectrogram_image)
            self.waveform_label.config(image=self.waveform_image)
            
        def load_current_model_run_result():
            

            self.run_result = functions.get_model_run_result(int(self.current_model_run_name_ID))  

            print('self.run_result', self.run_result)
            
            print('ID', self.run_result[0])
            
            self.current_model_run_name_recording_id = self.run_result[1]      
            
            self.recording_id_and_result_place_value.set("Recording Id: " + str(self.current_model_run_name_recording_id) + " Result: " + str(self.current_model_run_result_array_pos))
              
            self.current_model_run_name_start_time = self.run_result[2]
            self.start_time.set(self.current_model_run_name_start_time)
            
            self.current_model_run_name_duration = self.run_result[3]
            self.current_model_run_name_duration = 0.7 # The original length of 1.5 is too long for a morepork  
            
            self.current_model_run_name_actual = self.run_result[4] 
          
            self.current_model_run_name_predicted = self.run_result[5]             
            self.current_model_run_name_actual_confirmed = self.run_result[6] 

            self.actual_label_value.set(self.current_model_run_name_actual)

            
            # Set the radio button
            print('current_model_run_name_actual_confirmed', self.current_model_run_name_actual_confirmed)
            if self.current_model_run_name_actual_confirmed == 'morepork_more-pork':
                self.actual_confirmed.set('morepork_more-pork')
            elif self.current_model_run_name_actual_confirmed == 'unknown':
                self.actual_confirmed.set('unknown')
            else:
                self.actual_confirmed.set(self.current_model_run_name_actual)
                
#             print('current_model_run_name_predicted', self.current_model_run_name_predicted)
#             if self.current_model_run_name_predicted == 'morepork':
#                 self.predicted.set('morepork')
#             elif self.current_model_run_name_predicted == 'unknown':
#                 self.predicted.set('unknown')

            self.predicted_label_value.set(self.current_model_run_name_predicted)

            
            
            threading.Thread(target=play_clip(), args=(1,)).start()
            threading.Thread(target=display_images(), args=(1,)).start()
                                                                                
        
app = Main_GUI()
app.mainloop() 