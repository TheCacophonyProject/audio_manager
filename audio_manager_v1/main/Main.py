'''
Created on 5 Sep 2019

@author: tim
'''
from tkinter.messagebox import showinfo

#  https://www.youtube.com/watch?v=A0gaXfM1UN0&t=343s
# https://www.youtube.com/watch?v=D8-snVfekto
# How to Program a GUI Application (with Python Tkinter)!
# https://www.tutorialspoint.com/python3/python_gui_programming

HEIGHT = 1000
WIDTH = 1100

import tkinter as tk

from tkinter import ttk
from tkinter import *
from tkinter.ttk import *

# import os
from PIL import ImageTk,Image 

import main.functions as functions
import main.parameters as parameters
from main.parameters import *

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
        
        for F in (HomePage, RecordingsPage, TaggingPage, CreateWekaModelPage, ClassifyOnsetsUsingWekaModelPage, CreateOnsetsPage, CreateSpectrogramsPage, CreateTagsFromOnsetsPage, EvaluateWekaModelRunResultPage, CreateTagsOnCacophonyServerFromModelRunPage):
      
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
        
        instuctions_text = "Work through the steps for normal model iteration."
        instuctions_msg = tk.Message(self, text = instuctions_text)
        instuctions_msg.config(width=600)
        instuctions_msg.pack(pady=10,padx=10)
        
        recordings_button = ttk.Button(self, text="Step 1: Recordings (Do not always use)",
                            command=lambda: controller.show_frame(RecordingsPage))        
        recordings_button.pack()
        
        createOnsetsPage_button = ttk.Button(self, text="Step 2: Create onsets (Do not always use)",
                            command=lambda: controller.show_frame(CreateOnsetsPage))        
        createOnsetsPage_button.pack()
        
        classifyOnsetsUsingWekaModelPage_button = ttk.Button(self, text="Step 3: Classify Onsets Using Weka Model",
                            command=lambda: controller.show_frame(ClassifyOnsetsUsingWekaModelPage))        
        classifyOnsetsUsingWekaModelPage_button.pack()        
          
        evaluateWekaModelRunResultPage_button = ttk.Button(self, text="Step 4: Manually Evaluate Weka model Run Result",
                            command=lambda: controller.show_frame(EvaluateWekaModelRunResultPage))        
        evaluateWekaModelRunResultPage_button.pack()
        
        
        createWekaModelPage_button = ttk.Button(self, text="Step 5: Create Weka Model",
                            command=lambda: controller.show_frame(CreateWekaModelPage))        
        createWekaModelPage_button.pack()
        
              
        
        outside_normal_flow_label = tk.Label(self, text="Functions below here are outside normal model development iteration")
        outside_normal_flow_label.pack(pady=10,padx=10)
        
        createTagsOnCacophonyServerFromModelRunPage_button = ttk.Button(self, text="Step A: Create Tags On Cacophony Server From Model Run ",
                            command=lambda: controller.show_frame(CreateTagsOnCacophonyServerFromModelRunPage))        
        createTagsOnCacophonyServerFromModelRunPage_button.pack()
        
        other_or_no_longer_used_label = tk.Label(self, text="Functions below here probably no longer needed")
        other_or_no_longer_used_label.pack(pady=10,padx=10)       
              
               
        createTagsFromOnsetsPage_button = ttk.Button(self, text="Create Tags from Onsets",
                            command=lambda: controller.show_frame(CreateTagsFromOnsetsPage))         
        createTagsFromOnsetsPage_button.pack()
                
        
        createSpectrogramsPage_button = ttk.Button(self, text="Create Spectrograms",
                            command=lambda: controller.show_frame(CreateSpectrogramsPage))        
        createSpectrogramsPage_button.pack()
        
        tagging_button = ttk.Button(self, text="Tagging",
                            command=lambda: controller.show_frame(TaggingPage))        
        tagging_button.pack()
     
        
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
        title_label.grid(column=0, columnspan=1, row=0)
        
        device_name_label = ttk.Label(self, text="Device name e.g fpF7B9AFNn6hvfVgdrJB")
        device_name_label.grid(column=0, columnspan=1, row=1)
             
        device_name = StringVar(value='fpF7B9AFNn6hvfVgdrJB')
        device_name_entry = tk.Entry(self,  textvariable=device_name, width=30)
        device_name_entry.grid(column=1, columnspan=1, row=1)
        
        device_super_name_label = ttk.Label(self, text="Device Super name (e.g. Hammond Park)")
        device_super_name_label.grid(column=0, columnspan=1, row=2)
        
        device_super_name = StringVar(value='Hammond Park')
        device_super_name_entry = tk.Entry(self,  textvariable=device_super_name, width=30)
        device_super_name_entry.grid(column=1, columnspan=1,row=2)
       
        
        
        get_recordings_button = ttk.Button(self, text="Load Recordings from local folder ",
                            command=lambda: functions.load_recordings_from_local_folder(device_name.get(), device_super_name.get()))
        get_recordings_button.grid(column=0, columnspan=1, row=3)
        
        load_recordings_from_local_folder_instructions = "Useful if you have the recordings on a usb drive - not for downloading from server"

        msg1 = tk.Message(self, text = load_recordings_from_local_folder_instructions)
        msg1.config(width=600)
        msg1.grid(column=1, columnspan=2, row=3)  

        get_recording_information_from_server_button = ttk.Button(self, text="Get Recording Information for recordings imported from local file system",
                            command=lambda: functions.update_recording_information_for_all_local_database_recordings())
        get_recording_information_from_server_button.grid(column=0, columnspan=1, row=4)
        
        get_new_recordings_from_server_button = ttk.Button(self, text="Get New Recordings From Server",
                            command=lambda: functions.get_recordings_from_server(device_name.get(), device_super_name.get()))
        get_new_recordings_from_server_button.grid(column=0, columnspan=1, row=5)
        
        get_new_recordings_from_server_instructions = "This will get the recordings for the device in the device name box. It will also assign a super name from the Super Name box"


        msg2 = tk.Message(self, text = get_new_recordings_from_server_instructions)
        msg2.config(width=600)
        msg2.grid(column=1, columnspan=2, row=5)   
        
        scan_local_folder_for_recordings_not_in_local_db_and_update_button = ttk.Button(self, text="Scan recordings folder for recordings not in local db and update",
                            command=lambda: functions.scan_local_folder_for_recordings_not_in_local_db_and_update(device_name.get(), device_super_name.get()))
        scan_local_folder_for_recordings_not_in_local_db_and_update_button.grid(column=0, columnspan=1, row=6)
       
        scan_recordings_folder_instructions = "If you do NOT know the device name or super name enter unknown in the fields. The device name will be updated automatically"

        msg3 = tk.Message(self, text = scan_recordings_folder_instructions)
        msg3.config(width=600)
        msg3.grid(column=1, columnspan=1, row=6)               
        
        back_to_home_button = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        back_to_home_button.grid(column=0, columnspan=1, row=7)               

class CreateWekaModelPage(tk.Frame):    
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        title_label = ttk.Label(self, text="Create a Weka model - using Weka https://www.cs.waikato.ac.nz/ml/weka/downloading.html", font=LARGE_FONT)
        title_label.grid(column=0, columnspan=1, row=0)   
        
        introduction_instructions = "Before we can use Weka to create a model, we first need to 1) create spectrograms (from the previously confirmed model_run_results) and 2) create an input arff file that lists those spectrograms"
        msg1 = tk.Message(self, text = introduction_instructions)
        msg1.config(width=600)
        msg1.grid(column=0, columnspan=2, row=1)  
        
        create_spectrograms_instructions = "Press the Create Spectrograms for Next Run button to create the spectrograms (from confirmed onsets) that will be used to train the next version/iteration of the model"
        create_spectrograms_msg = tk.Message(self, text = create_spectrograms_instructions)
        create_spectrograms_msg.config(width=600)
        create_spectrograms_msg.grid(column=0, columnspan=1, row=2)  
        
        create_spectrograms_button = ttk.Button(self, text="Create Spectrograms for Next Run", command=lambda: functions.create_spectrogram_jpg_files_for_next_model_run())
        create_spectrograms_button.grid(column=1, columnspan=1, row=2)
        
        create_arff_instructions = "Pressing the Create Arff file for Weka input button will put the names of the previously created spectrograms into an .arff file, that Weka will then use. You can find the file called " + arff_file_for_weka_model_creation + " in the " + model_run_name + " folder."
        create_arff_file_msg = tk.Message(self, text = create_arff_instructions)
        create_arff_file_msg.config(width=600)
        create_arff_file_msg.grid(column=0, columnspan=1, row=3)  
        
        create_arff_file_for_weka_button = ttk.Button(self, text="Create Arff file for Weka input", command=lambda: functions.create_arff_file_for_weka_image_filter_input())
        create_arff_file_for_weka_button.grid(column=1, columnspan=1, row=3)
        
        create_folders_instructions = "BEFORE pressing the next button, update the model_run_name parameter in the parameters file with a new name AND exit/close this program and restart to refresh - check it has.  It is currently set to " + model_run_name + " which is most likely the previous model run folder that you used - you don't want to use the same folder - it will end in tears!! (Once pressed, check that the folders have been created in the file system).  This will give you a place to save your next Weka model.model file. You can now press the Create folders for next run button to create all the necessary folders for the next iteration/run. "
        create_folders_msg = tk.Message(self, text = create_folders_instructions)
        create_folders_msg.config(width=600)
        create_folders_msg.grid(column=0, columnspan=1, row=4) 
        
        create_folders_button = ttk.Button(self, text="Create folders for next run. ",command=lambda: functions.create_folders_for_next_run())
        create_folders_button.grid(column=1, columnspan=1, row=4)  
        
        using_weka_instructions1 = "You are now ready to use Weka.  From a terminal command prompt, cd into the directory where Weka has been installed (e.g. weka-3-8-3) and launch Weka using the command: java -jar weka.jar"
        using_weka_msg1 = tk.Message(self, text = using_weka_instructions1)
        using_weka_msg1.config(width=800)
        using_weka_msg1.grid(column=0, columnspan=2, row=5)  
        
        using_weka_instructions2 = "These instructions are from the video: https://www.futurelearn.com/courses/advanced-data-mining-with-weka/0/steps/29486\ You will need to have installed the Image Filters Package into Weka."
        using_weka_msg2 = tk.Message(self, text = using_weka_instructions2)
        using_weka_msg2.config(width=800)
        using_weka_msg2.grid(column=0, columnspan=2, row=6)  
        
        using_weka_instructions3 = "In Weka, Press the Explorer button and then the Open file.. button to open the previously created .arff file. Now Press the Choose button below the Filter label and navigate to weka|filters|unsupervised|instance|imagefilter|EdgeHistogramFilter \
Then click on the Box with the name of the Filter (EdgeHistogramFilter) and paste in the path to image directory where all the spectrograms were created and press OK - it doesn't appear to have the ability to navigate to the directory.  Now press the Apply button to apply the filter."
        using_weka_msg3 = tk.Message(self, text = using_weka_instructions3)
        using_weka_msg3.config(width=800)
        using_weka_msg3.grid(column=0, columnspan=2, row=7)  
        
        using_weka_instructions4 = "The Weka image in the bottom right corner will do a dance while it is processing and when finished you should see a list of Attiributes (with the first being filename) and then MPEG-7 etc"
        using_weka_msg4 = tk.Message(self, text = using_weka_instructions4)
        using_weka_msg4.config(width=800)
        using_weka_msg4.grid(column=0, columnspan=2, row=8)  
        
        using_weka_instructions5 = "Now you need to remove the filename attribute by selecting the box and press the Remove button.  Now select the Classify tab (at the top). Press the Choose button and navigate to  Weka|classifiers|Trees|LMT.  Use Cross-validation Folds 10 and press start. The weka image does it's dance and then the results displayed"
        using_weka_msg5 = tk.Message(self, text = using_weka_instructions5)
        using_weka_msg5.config(width=800)
        using_weka_msg5.grid(column=0, columnspan=2, row=9) 
        
        using_weka_instructions6 = "To export the model, in the Result list, right mouse click and Choose Save model and save as model.model in the weka_model directory for this run (Create the directory if you did not follow the instructions above.)"
        using_weka_msg6 = tk.Message(self, text = using_weka_instructions6)
        using_weka_msg6.config(width=800)
        using_weka_msg6.grid(column=0, columnspan=2, row=10) 
        
        back_to_home_button = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        back_to_home_button.grid(column=0, columnspan=1, row=15)                
        
class ClassifyOnsetsUsingWekaModelPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.clip_folder = StringVar(value='')
          
        title_label = ttk.Label(self, text="Classify Onsets Using Weka Model", font=LARGE_FONT)
        title_label.grid(column=0, columnspan=1, row=0)    
        
        intro_msg = tk.Message(self, text = "This page will guide you through the process of using a Weka model to classify onsets.")
        intro_msg.config(bg='lightgreen', font=('times', 16), width=600)
        intro_msg.grid(column=0, columnspan=1, row=1)  
        
        run_folder_instructions = "The run_folder is currently set to: " + parameters.run_folder + " You may have already created folders for this run (just before you used Weka to create the Model), but if not press the Create Folders button."
        run_folder_msg = tk.Message(self, text = run_folder_instructions)
        run_folder_msg.config(width=600)
        run_folder_msg.grid(column=0, columnspan=1, row=2) 
        
        create_folders_button = ttk.Button(self, text="Create folders",command=lambda: functions.create_folders_for_next_run())
        create_folders_button.grid(column=1, columnspan=1, row=2)
        
        model_setup1_instructions = "You should have already created a new model.model file using Weka and saved it in " + parameters.run_folder + "/" + parameters.weka_model_folder + " folder.  Also from the previous run, copy the following files into the " + weka_model_folder + " folder: " + weka_input_arff_filename + ", " + weka_run_jar_filename + " Make sure you use the new model.model file that you created in Weka, NOT from the previous run."
        model_setup1_msg = tk.Message(self, text = model_setup1_instructions)
        model_setup1_msg.config(width=600)
        model_setup1_msg.grid(column=0, columnspan=1, row=3)  
        
        model_setup2_instructions = "If you don't have a run.jar file, it can be created from within Eclipse. Using the Java perspective, open the current code e.g. Main4.java and from the File menu, choose Export.. | Java | Runnable JAR file | Next | Launch configuration: | Main4-run_models_v1 (or the current version) | Export destination of the " + weka_model_folder + "folder | Library handling|Package required libraries into generated JAR | Finish" 
        model_setup2_msg = tk.Message(self, text = model_setup2_instructions)
        model_setup2_msg.config(width=600)
        model_setup2_msg.grid(column=0, columnspan=1, row=4)  
        
        model_setup3_instructions = "When all the files are copied, press the Classify Onsets Button.  This will start the process of creating a temporary spectrogram of each segment of audio corresponding to an onset, and using the Weka model to clasify it, and save the results in the model_run_result with the modelRunName of " + model_run_name
        model_setup3_msg = tk.Message(self, text = model_setup3_instructions)
        model_setup3_msg.config(width=600)
        model_setup3_msg.grid(column=0, columnspan=1, row=5)   
        
        evaluate_button = ttk.Button(self, text="Classify Onsets",command=lambda: functions.classify_onsets_using_weka_model())
        evaluate_button.grid(column=0, columnspan=1, row=15)     
        
#         update_instructions = 'Once the new model has been used to evaluate all the onsets, the new rows in the model_run_result table, need to be updated with previously confirmed sounds from the previous run (e.g. they are confirmed morepork, unknown, car etc). Enter the model run name in the box'
#         update_actual_confirmed_msg = tk.Message(self, text = update_instructions)
#         update_actual_confirmed_msg.config( width=600)
#         update_actual_confirmed_msg.grid(column=0, columnspan=1, row=16)   
#         
#         previous_model_run_name = StringVar(value='')
#         previous_model_run_entry = tk.Entry(self,  textvariable=previous_model_run_name, width=30)
#         previous_model_run_entry.grid(column=1, columnspan=1, row=16) 
#         
#         update_actual_confirmed_button = ttk.Button(self, text="Update Actual Confirmed",command=lambda: functions.update_latest_model_run_results_with_previous_confirmed(previous_model_run_name.get()))
#         update_actual_confirmed_button.grid(column=2, columnspan=1, row=16) 
        
        
        
             

        back_to_home_button = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(HomePage))  
        back_to_home_button.grid(column=0, columnspan=1, row=20) 
                            
class CreateOnsetsPage(tk.Frame):    
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.clip_folder = StringVar(value='')
       
             
        title_label = ttk.Label(self, text="Create Onsets", font=LARGE_FONT)
        title_label.grid(column=0, columnspan=1, row=0)    
        
        onset_instructions = "Use this page to run the create onsets function that will create locations of interest in the db"

        msg = tk.Message(self, text = onset_instructions)
        msg.config(bg='lightgreen', font=('times', 16), width=1200)
        msg.grid(column=0, columnspan=6, row=1)   
        
        existing_tag_type_message = "Leave this box empty to create onsets from ALL recordings that haven't yet had an onset created from them.  OR enter the name of an existing tag type - onsets will only be created from recordings that already been tagged with this type"
        existing_tag_type_msg = tk.Message(self, text = existing_tag_type_message)
        existing_tag_type_msg.config(width=600)
        existing_tag_type_msg.grid(column=0, columnspan=1, row=2) 

        existing_tag_type = StringVar()
        existing_tag_type_entry = tk.Entry(self,  textvariable=existing_tag_type, width=30)   
        existing_tag_type_entry.grid(column=1, columnspan=1,row=2) 
               
        run_button = ttk.Button(self, text="Run", command=lambda: functions.create_onsets(existing_tag_type.get()))
        run_button.grid(column=0, columnspan=1, row=3)        

        back_to_home_button = ttk.Button(self, text="Back to Home",command=lambda: controller.show_frame(HomePage))                            
        back_to_home_button.grid(column=0, columnspan=1, row=4)                  

class CreateSpectrogramsPage(tk.Frame):    
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.clip_folder = StringVar(value='')       
             
        title_label = ttk.Label(self, text="Create Spectrograms using ONSETs", font=LARGE_FONT)
        title_label.grid(column=0, columnspan=1, row=0)    
        
        onset_instructions = "Use this page to run the create spectrogram function that will create spectrograms in the spectrogram folder"
        msg = tk.Message(self, text = onset_instructions)
        msg.config(bg='lightgreen', font=('times', 17), width=1000)
        msg.grid(column=0, columnspan=2, row=1)  
                
        run_button = ttk.Button(self, text="Run", command=lambda: functions.create_focused_mel_spectrogram_jps_using_onset_pairs())
        run_button.grid(column=0, columnspan=1, row=2) 
        
        spectrogram_folder_instructions = "The spectrograms will be created in the folder: " + base_folder + '/' + run_folder + " This can be changed in the python parameters file"
        folder_msg = tk.Message(self, text = spectrogram_folder_instructions)
        folder_msg.config(width=600)
        folder_msg.grid(column=1, columnspan=1, row=2)    

        back_to_home_button = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(HomePage))
        back_to_home_button.grid(column=0, columnspan=1, row=3)                  

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
        self.unique_locations = functions.get_unique_locations()            
                    
        title_label = ttk.Label(self, text="Evaluate Model Run Results", font=LARGE_FONT)
        title_label.grid(column=0, columnspan=1, row=0)   
        
        refresh_model_run_names_button = ttk.Button(self, text="Refresh Unique Model Run Names",command=lambda: refresh_unique_model_run_names())
        refresh_model_run_names_button.grid(column=0, columnspan=1, row=2) 
        
        run_names_label = ttk.Label(self, text="Run Names")
        run_names_label.grid(column=1, columnspan=1, row=1)      
                                    
        self.run_name = StringVar()
        self.run_names_combo = ttk.Combobox(self, textvariable=self.run_name, values=self.unique_model_run_names)
        
        if len(self.unique_model_run_names) > 0:
            self.run_names_combo.current(0)
            self.run_names_combo.grid(column=1, columnspan=1,row=2) 
            self.run_names_combo.current(len(self.unique_model_run_names) - 1)       
            
        location_filter_label = ttk.Label(self, text="Location Filter")
        location_filter_label.grid(column=2, columnspan=1, row=1)      
                                    
        self.location_filter = StringVar()
        self.location_filter_combo = ttk.Combobox(self, textvariable=self.location_filter, values=self.unique_locations)
        
        if len(self.unique_locations) > 0:
            self.location_filter_combo.current(0)
            self.location_filter_combo.grid(column=2, columnspan=1,row=2) 
       
        
#         actual_filter_label = ttk.Label(self, text="Filter - Tags from Server", font=LARGE_FONT)
#         actual_filter_label.grid(column=0, columnspan=1, row=2)        
#         self.actual_filter = tk.StringVar()
#         actual_filter_radio_button_none = ttk.Radiobutton(self,text='Not Used', variable=self.actual_filter, value='not_used')
#         actual_filter_radio_button_none.grid(column=0, columnspan=1, row=3)
#         actual_filter_radio_button_morepork_classic = ttk.Radiobutton(self,text='morepork_more-pork', variable=self.actual_filter, value='morepork_more-pork')
#         actual_filter_radio_button_morepork_classic.grid(column=0, columnspan=1, row=4)
#         actual_filter_radio_button_unknown = ttk.Radiobutton(self,text='Unknown', variable=self.actual_filter, value='unknown')
#         actual_filter_radio_button_unknown.grid(column=0, columnspan=1, row=5) 
#         self.actual_filter.set('not_used')
        
        actual_confirmed_filter_label = ttk.Label(self, text="Filter - Actual Confirmed", font=LARGE_FONT)
        actual_confirmed_filter_label.grid(column=0, columnspan=2, row=3)   
             
        self.actual_confirmed_filter = tk.StringVar()
        actual_confirmed_filter_radio_button_none = ttk.Radiobutton(self,text='Not Used', variable=self.actual_confirmed_filter, value='not_used')
        actual_confirmed_filter_radio_button_none.grid(column=0, columnspan=1, row=13)        
        actual_confirmed_filter_radio_button_null = ttk.Radiobutton(self,text='Null Filter (ie nothing in DB table)', variable=self.actual_confirmed_filter, value='IS NULL')
        actual_confirmed_filter_radio_button_null.grid(column=0, columnspan=1, row=14)        
        actual_confirmed_filter_radio_button_morepork_classic = ttk.Radiobutton(self,text='morepork_more-pork', variable=self.actual_confirmed_filter, value='morepork_more-pork')
        actual_confirmed_filter_radio_button_morepork_classic.grid(column=0, columnspan=1, row=15)
        actual_confirmed_filter_radio_button_unknown = ttk.Radiobutton(self,text='Unknown', variable=self.actual_confirmed_filter, value='unknown')
        actual_confirmed_filter_radio_button_unknown.grid(column=0, columnspan=1, row=16) 
        actual_confirmed_filter_radio_button_unknown = ttk.Radiobutton(self,text='Dove', variable=self.actual_confirmed_filter, value='dove')
        actual_confirmed_filter_radio_button_unknown.grid(column=0, columnspan=1, row=17) 
        actual_confirmed_filter_radio_button_unknown = ttk.Radiobutton(self,text='Duck', variable=self.actual_confirmed_filter, value='duck')
        actual_confirmed_filter_radio_button_unknown.grid(column=0, columnspan=1, row=18) 
        actual_confirmed_filter_radio_button_unknown = ttk.Radiobutton(self,text='Dog', variable=self.actual_confirmed_filter, value='dog')
        actual_confirmed_filter_radio_button_unknown.grid(column=0, columnspan=1, row=19) 
        actual_confirmed_filter_radio_button_unknown = ttk.Radiobutton(self,text='Human', variable=self.actual_confirmed_filter, value='human')
        actual_confirmed_filter_radio_button_unknown.grid(column=0, columnspan=1, row=20) 
        actual_confirmed_filter_radio_button_unknown = ttk.Radiobutton(self,text='Siren', variable=self.actual_confirmed_filter, value='siren')
        actual_confirmed_filter_radio_button_unknown.grid(column=0, columnspan=1, row=21) 
        actual_confirmed_filter_radio_button_unknown = ttk.Radiobutton(self,text='Bird', variable=self.actual_confirmed_filter, value='bird')
        actual_confirmed_filter_radio_button_unknown.grid(column=0, columnspan=1, row=22) 
        actual_confirmed_filter_radio_button_unknown = ttk.Radiobutton(self,text='Car', variable=self.actual_confirmed_filter, value='car')
        actual_confirmed_filter_radio_button_unknown.grid(column=0, columnspan=1, row=23) 
        actual_confirmed_filter_radio_button_unknown = ttk.Radiobutton(self,text='Rumble', variable=self.actual_confirmed_filter, value='rumble')
        actual_confirmed_filter_radio_button_unknown.grid(column=0, columnspan=1, row=24)
        actual_confirmed_filter_radio_button_unknown = ttk.Radiobutton(self,text='White noise', variable=self.actual_confirmed_filter, value='white_noise')
        actual_confirmed_filter_radio_button_unknown.grid(column=1, columnspan=1, row=13)
        actual_confirmed_filter_radio_button_unknown = ttk.Radiobutton(self,text='Plane', variable=self.actual_confirmed_filter, value='plane')
        actual_confirmed_filter_radio_button_unknown.grid(column=1, columnspan=1, row=14)
        actual_confirmed_filter_radio_button_unknown = ttk.Radiobutton(self,text='Cow', variable=self.actual_confirmed_filter, value='cow')
        actual_confirmed_filter_radio_button_unknown.grid(column=1, columnspan=1, row=15)
        actual_confirmed_filter_radio_button_unknown = ttk.Radiobutton(self,text='Buzzy_insect', variable=self.actual_confirmed_filter, value='buzzy_insect')
        actual_confirmed_filter_radio_button_unknown.grid(column=1, columnspan=1, row=16)
        actual_confirmed_filter_radio_button_unknown = ttk.Radiobutton(self,text='Morepork more-pork Part', variable=self.actual_confirmed_filter, value='morepork_more-pork_part')
        actual_confirmed_filter_radio_button_unknown.grid(column=1, columnspan=1, row=17)
        actual_confirmed_filter_radio_button_unknown = ttk.Radiobutton(self,text='Hammering', variable=self.actual_confirmed_filter, value='hammering')
        actual_confirmed_filter_radio_button_unknown.grid(column=1, columnspan=1, row=18)
        self.actual_confirmed_filter.set('not_used')
        
        predicted_filter_label = ttk.Label(self, text="Filter - Predicted", font=LARGE_FONT)
        predicted_filter_label.grid(column=2, columnspan=2, row=3)  
        
        
        
              
        self.predicted_filter = tk.StringVar()        
        predicted_filter_radio_button_none = ttk.Radiobutton(self,text='Not Used', variable=self.predicted_filter, value='not_used')
        predicted_filter_radio_button_none.grid(column=2, columnspan=1, row=13)
        predicted_filter_radio_button_morepork_classic = ttk.Radiobutton(self,text='Morepork more-pork', variable=self.predicted_filter, value='morepork_more-pork')
        predicted_filter_radio_button_morepork_classic.grid(column=2, columnspan=1, row=14)
        predicted_filter_radio_button_unknown = ttk.Radiobutton(self,text='Unknown', variable=self.predicted_filter, value='unknown')
        predicted_filter_radio_button_unknown.grid(column=2, columnspan=1, row=15) 
        predicted_filter_radio_button_unknown = ttk.Radiobutton(self,text='Dove', variable=self.predicted_filter, value='dove')
        predicted_filter_radio_button_unknown.grid(column=2, columnspan=1, row=16) 
        predicted_filter_radio_button_unknown = ttk.Radiobutton(self,text='Duck', variable=self.predicted_filter, value='duck')
        predicted_filter_radio_button_unknown.grid(column=2, columnspan=1, row=17) 
        predicted_filter_radio_button_unknown = ttk.Radiobutton(self,text='Dog', variable=self.predicted_filter, value='dog')
        predicted_filter_radio_button_unknown.grid(column=2, columnspan=1, row=18) 
        predicted_filter_radio_button_unknown = ttk.Radiobutton(self,text='Human', variable=self.predicted_filter, value='human')
        predicted_filter_radio_button_unknown.grid(column=2, columnspan=1, row=19) 
        predicted_filter_radio_button_unknown = ttk.Radiobutton(self,text='Siren', variable=self.predicted_filter, value='siren')
        predicted_filter_radio_button_unknown.grid(column=2, columnspan=1, row=20) 
        predicted_filter_radio_button_unknown = ttk.Radiobutton(self,text='Bird', variable=self.predicted_filter, value='bird')
        predicted_filter_radio_button_unknown.grid(column=2, columnspan=1, row=21) 
        predicted_filter_radio_button_unknown = ttk.Radiobutton(self,text='Car', variable=self.predicted_filter, value='car')
        predicted_filter_radio_button_unknown.grid(column=2, columnspan=1, row=22)
        predicted_filter_radio_button_unknown = ttk.Radiobutton(self,text='Rumble', variable=self.predicted_filter, value='rumble')
        predicted_filter_radio_button_unknown.grid(column=2, columnspan=1, row=23)
        predicted_filter_radio_button_unknown = ttk.Radiobutton(self,text='White noise', variable=self.predicted_filter, value='white_noise')
        predicted_filter_radio_button_unknown.grid(column=3, columnspan=1, row=13)  
        predicted_filter_radio_button_unknown = ttk.Radiobutton(self,text='Plane', variable=self.predicted_filter, value='plane')
        predicted_filter_radio_button_unknown.grid(column=3, columnspan=1, row=14)
        predicted_filter_radio_button_unknown = ttk.Radiobutton(self,text='Cow', variable=self.predicted_filter, value='cow')
        predicted_filter_radio_button_unknown.grid(column=3, columnspan=1, row=15)  
        predicted_filter_radio_button_unknown = ttk.Radiobutton(self,text='Buzzy insect', variable=self.predicted_filter, value='buzzy_insect')
        predicted_filter_radio_button_unknown.grid(column=3, columnspan=1, row=16)
        predicted_filter_radio_button_unknown = ttk.Radiobutton(self,text='Morepork more-pork Part', variable=self.predicted_filter, value='morepork_more-pork_part')
        predicted_filter_radio_button_unknown.grid(column=3, columnspan=1, row=17) 
        predicted_filter_radio_button_unknown = ttk.Radiobutton(self,text='Hammering', variable=self.predicted_filter, value='hammering')
        predicted_filter_radio_button_unknown.grid(column=3, columnspan=1, row=18) 
        self.predicted_filter.set('not_used')    
        
        run_probability_label = ttk.Label(self, text="Probability")
        run_probability_label.grid(column=2, columnspan=1, row=25)  
        
        self.predicted_probability_filter = tk.StringVar()
        predicted_probability_filter_radio_button_greater_than = ttk.Radiobutton(self,text='Greater than', variable=self.predicted_probability_filter, value='greater_than')
        predicted_probability_filter_radio_button_greater_than.grid(column=2, columnspan=1, row=26)
        predicted_probability_filter_radio_button_less_than = ttk.Radiobutton(self,text='Less than', variable=self.predicted_probability_filter, value='less_than')
        predicted_probability_filter_radio_button_less_than.grid(column=3, columnspan=1, row=26)
        self.predicted_probability_filter_value = StringVar(value='')
        self.predicted_probability_filter_entry = tk.Entry(self,  textvariable=self.predicted_probability_filter_value, width=10).grid(column=2, columnspan=1,row=27)    
        predicted_probability_filter_radio_button_not_used = ttk.Radiobutton(self,text='Not used', variable=self.predicted_probability_filter, value='not_used')
        predicted_probability_filter_radio_button_not_used.grid(column=3, columnspan=1, row=27)
        
        
        self.predicted_probability_filter.set('not_used')        
       
        
        
        load_run_results_button = ttk.Button(self, text="Load Run Results using Filters",command=lambda: get_run_results())
        load_run_results_button.grid(column=0, columnspan=1, row=28) 
        
        self.number_of_results_label_value = tk.StringVar()
        number_of_results_label_for_value = ttk.Label(self, textvariable=self.number_of_results_label_value)
        number_of_results_label_for_value.grid(column=0, columnspan=1, row=29)   
        
        self.recording_id_and_result_place_value = tk.StringVar()
        recording_id_label = ttk.Label(self, textvariable=self.recording_id_and_result_place_value) 
        recording_id_label.grid(column=0, columnspan=1, row=30) 
        self.recording_id_and_result_place_value.set("Recording Id")
                   
        start_time_label = ttk.Label(self, text="Start Time")
        start_time_label.grid(column=1, columnspan=1, row=29)        
        self.start_time = StringVar(value='0.0')
        self.start_time_entry = tk.Entry(self,  textvariable=self.start_time, width=30).grid(column=1, columnspan=1,row=30)
        
        self.location_recorded_value = tk.StringVar()
        location_recorded_label = ttk.Label(self, textvariable=self.location_recorded_value) 
        location_recorded_label.grid(column=2, columnspan=1, row=29) 
        self.location_recorded_value.set("Location: ")   
        
        self.when_recorded_value = tk.StringVar()
        when_recorded_label = ttk.Label(self, textvariable=self.when_recorded_value) 
        when_recorded_label.grid(column=2, columnspan=1, row=30) 
        self.when_recorded_value.set("When: ")     
        
        self.spectrogram_label = ttk.Label(self, image=None)
        self.spectrogram_label.grid(column=0, columnspan=1, row=31)
        
        self.waveform_label = ttk.Label(self, image=None)
        self.waveform_label.grid(column=1, columnspan=1, row=31)
        
#         actual_label = ttk.Label(self, text="Tags from Server", font=LARGE_FONT)
#         actual_label.grid(column=0, columnspan=1, row=30) 
        
#         self.actual_label_value = tk.StringVar()
#         actual_label_for_value = ttk.Label(self, textvariable=self.actual_label_value)
#         actual_label_for_value.grid(column=0, columnspan=1, row=41)         
        
        actual_label_confirmed = ttk.Label(self, text="Actual Confirmed", font=LARGE_FONT)
        actual_label_confirmed.grid(column=0, columnspan=2, row=40)
#         actual_label_confirmed2 = ttk.Label(self, text="(The default is the same as Actual - select to change and save)")
#         actual_label_confirmed2.grid(column=0, columnspan=1, row=41) 
        
        self.actual_confirmed = tk.StringVar()

        actual_confirmed_radio_button_morepork_classic = ttk.Radiobutton(self,text='Morepork more-pork', variable=self.actual_confirmed, value='morepork_more-pork',command=lambda: confirm_actual())
        actual_confirmed_radio_button_morepork_classic.grid(column=0, columnspan=1, row=42) 
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Unknown', variable=self.actual_confirmed, value='unknown',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=0, columnspan=1, row=43)
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Dove', variable=self.actual_confirmed, value='dove',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=0, columnspan=1, row=44)   
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Duck', variable=self.actual_confirmed, value='duck',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=0, columnspan=1, row=45) 
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Dog', variable=self.actual_confirmed, value='dog',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=0, columnspan=1, row=46) 
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Human', variable=self.actual_confirmed, value='human',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=0, columnspan=1, row=47)   
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Siren', variable=self.actual_confirmed, value='siren',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=0, columnspan=1, row=48)
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Bird', variable=self.actual_confirmed, value='bird',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=0, columnspan=1, row=49) 
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Car', variable=self.actual_confirmed, value='car',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=0, columnspan=1, row=50)
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Rumble', variable=self.actual_confirmed, value='rumble',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=0, columnspan=1, row=51)
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='White noise', variable=self.actual_confirmed, value='white_noise',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=1, columnspan=1, row=42)
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Plane', variable=self.actual_confirmed, value='plane',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=1, columnspan=1, row=43)
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Cow', variable=self.actual_confirmed, value='cow',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=1, columnspan=1, row=44) 
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Buzzy insect', variable=self.actual_confirmed, value='buzzy_insect',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=1, columnspan=1, row=45) 
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Morepork more-pork Part', variable=self.actual_confirmed, value='morepork_more-pork_part',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=1, columnspan=1, row=46) 
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Hammering', variable=self.actual_confirmed, value='hammering',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=1, columnspan=1, row=47)    
       
        predicted_label = ttk.Label(self, text="Predicted (by last model run)", font=LARGE_FONT)
        predicted_label.grid(column=2, columnspan=1, row=40)       
        
        self.predicted_label_value = tk.StringVar()
        predicted_label_value_for_value = ttk.Label(self, textvariable=self.predicted_label_value)
        predicted_label_value_for_value.grid(column=2, columnspan=1, row=41) 
        
        previous_button = ttk.Button(self, text="Previous", command=lambda: previous_run_result())
        previous_button.grid(column=0, columnspan=1, row=60)
                            
        play_button = ttk.Button(self, text="Play Again", command=lambda: functions.play_clip(str(self.current_model_run_name_recording_id), float(self.current_model_run_name_start_time),self.current_model_run_name_duration, True))
        play_button.grid(column=1, columnspan=1, row=60)
        play_button = ttk.Button(self, text="Play Unfiltered", command=lambda: functions.play_clip(str(self.current_model_run_name_recording_id), float(self.current_model_run_name_start_time),self.current_model_run_name_duration, False))
        play_button.grid(column=1, columnspan=1, row=61)
                            
        confirm_next_button = ttk.Button(self, text="Next", command=lambda: next_run_result())
        confirm_next_button.grid(column=2, columnspan=1, row=60)
        
        next_button = ttk.Button(self, text="Unselect", command=lambda: unselect_actual_confirmed())
        next_button.grid(column=2, columnspan=1, row=61)
        
        back_to_home_button = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(HomePage))
        back_to_home_button.grid(column=0, columnspan=1, row=61) 
        
        def create_spectrograms():
            functions.create_spectrogram_jpg_files_for_next_model_run()

        def confirm_actual():
            print('self.actual_confirmed.get() ', self.actual_confirmed.get())
            functions.update_model_run_result(self.current_model_run_name_ID, self.actual_confirmed.get())
            functions.update_onset(self.current_model_run_name_recording_id, self.current_model_run_name_start_time, self.actual_confirmed.get())
        
        def unselect_actual_confirmed():
            self.actual_confirmed.set('not_used')
            confirm_actual()
        
        def refresh_unique_model_run_names():
            self.unique_model_run_names = functions.get_unique_model_run_names()
            self.run_names_combo['values'] = self.unique_model_run_names  
            
        def get_run_result():    
            self.run_result = functions.get_model_run_result(int(self.current_model_run_name_ID))   
            self.current_model_run_result_array_pos = 0      
            load_current_model_run_result() 
      
        def get_run_results():    
            print('run_names_combo.get()', self.run_names_combo.get())   
#             print('Actual Filter', self.actual_filter.get())   
            print('Predicted Filter', self.predicted_filter.get())        
#             self.run_results = functions.get_model_run_results(self.run_names_combo.get(), self.actual_filter.get(), self.actual_confirmed_filter.get(), self.predicted_filter.get())
            self.run_results = functions.get_model_run_results(self.run_names_combo.get(), self.actual_confirmed_filter.get(), self.predicted_filter.get(), self.predicted_probability_filter.get(), self.predicted_probability_filter_value.get(), self.location_filter_combo.get())
                                       
            number_of_results_returned = len(self.run_results)
            print('number_of_results_returned ', number_of_results_returned)
            self.number_of_results_label_value.set("Number of results: " + str(number_of_results_returned))
            if number_of_results_returned > 0:
                first_result = self.run_results[0]
                self.current_model_run_name_ID = first_result[0]
                print('self.current_model_run_name_ID ', self.current_model_run_name_ID)                     
                load_current_model_run_result()

        def next_run_result():
          
            if self.current_model_run_result_array_pos < (len(self.run_results)) -1:
                self.current_model_run_result_array_pos +=1
                self.current_model_run_name_ID = self.run_results[self.current_model_run_result_array_pos][0]
                load_current_model_run_result()
                
                   
             
        def previous_run_result():
            if self.current_model_run_result_array_pos > 0:
                self.current_model_run_result_array_pos -=1
                self.current_model_run_name_ID = self.run_results[self.current_model_run_result_array_pos][0]
                load_current_model_run_result()
                
        def play_clip():
            functions.play_clip(str(self.current_model_run_name_recording_id), float(self.current_model_run_name_start_time),self.current_model_run_name_duration,True)
                     
        def display_images():
            self.spectrogram_image = functions.get_single_create_focused_mel_spectrogram(self.current_model_run_name_recording_id, self.current_model_run_name_start_time, self.current_model_run_name_duration)
            self.waveform_image = functions.get_single_waveform_image(self.current_model_run_name_recording_id, self.current_model_run_name_start_time, self.current_model_run_name_duration)            
            
            self.spectrogram_label.config(image=self.spectrogram_image)
            self.waveform_label.config(image=self.waveform_image)
            
        def load_current_model_run_result():

            self.run_result = functions.get_model_run_result(int(self.current_model_run_name_ID)) 
            
            self.current_model_run_name_recording_id = self.run_result[1]    
            
            self.recording_id_and_result_place_value.set("Recording Id: " + str(self.current_model_run_name_recording_id) + " Result: " + str(self.current_model_run_result_array_pos))              

            device_super_name, recordingDateTime = functions.get_single_recording_info_from_local_db(self.current_model_run_name_recording_id)
            
            self.location_recorded_value.set(str(device_super_name))
            self.when_recorded_value.set(str(recordingDateTime))

#             self.recorded_at_value.set(str(device_super_name) + " " + str(recordingDateTime))  
              
            self.current_model_run_name_start_time = self.run_result[2]
            self.start_time.set(self.current_model_run_name_start_time)
            
            self.current_model_run_name_duration = self.run_result[3]
            self.current_model_run_name_duration = 0.7 # The original length of 1.5 is too long for a morepork  
            
#             self.current_model_run_name_actual = self.run_result[4] 
          
            self.current_model_run_name_predicted = self.run_result[5]             
            self.current_model_run_name_actual_confirmed = self.run_result[6] 
            
#             roundedProbabilityStr = "{0:.2f}".format(self.run_result[7])
            
#             self.current_model_run_name_probability = self.run_result[7]  
#             self.current_model_run_name_probability = self.run_result[7]
            if self.run_result[7]:
                self.current_model_run_name_probability = "{0:.2f}".format(self.run_result[7])
            else:
                self.current_model_run_name_probability = '?'

#             self.actual_label_value.set(self.current_model_run_name_actual)
            
            # Set the radio button
            print('current_model_run_name_actual_confirmed', self.current_model_run_name_actual_confirmed)
            if self.current_model_run_name_actual_confirmed == 'morepork_more-pork':
                self.actual_confirmed.set('morepork_more-pork')
            elif self.current_model_run_name_actual_confirmed == 'unknown':
                self.actual_confirmed.set('unknown')
            elif self.current_model_run_name_actual_confirmed == 'dove':
                self.actual_confirmed.set('dove')
            elif self.current_model_run_name_actual_confirmed == 'duck':
                self.actual_confirmed.set('duck')
            elif self.current_model_run_name_actual_confirmed == 'dog':
                self.actual_confirmed.set('dog')
            elif self.current_model_run_name_actual_confirmed == 'human':
                self.actual_confirmed.set('human')
            elif self.current_model_run_name_actual_confirmed == 'siren':
                self.actual_confirmed.set('siren')
            elif self.current_model_run_name_actual_confirmed == 'bird':
                self.actual_confirmed.set('bird')
            elif self.current_model_run_name_actual_confirmed == 'car':
                self.actual_confirmed.set('car')
            elif self.current_model_run_name_actual_confirmed == 'rumble':
                self.actual_confirmed.set('rumble')
            elif self.current_model_run_name_actual_confirmed == 'white_noise':
                self.actual_confirmed.set('white_noise')
            elif self.current_model_run_name_actual_confirmed == 'plane':
                self.actual_confirmed.set('plane')
            elif self.current_model_run_name_actual_confirmed == 'cow':
                self.actual_confirmed.set('cow') 
            elif self.current_model_run_name_actual_confirmed == 'buzzy_insect':
                self.actual_confirmed.set('buzzy_insect')
            elif self.current_model_run_name_actual_confirmed == 'morepork_more-pork_part':
                self.actual_confirmed.set('morepork_more-pork_part')
            elif self.current_model_run_name_actual_confirmed == 'hammering':
                self.actual_confirmed.set('hammering')  
            else:
#                 self.actual_confirmed.set(None) 
                self.actual_confirmed.set('not_set')   
#             else:
#                 self.actual_confirmed.set(self.current_model_run_name_actual)

#             self.predicted_label_value.set(self.current_model_run_name_predicted)
            self.predicted_label_value.set(self.current_model_run_name_predicted + ' with ' + self.current_model_run_name_probability + ' probability')
            
            threading.Thread(target=play_clip(), args=(1,)).start()
            threading.Thread(target=display_images(), args=(1,)).start()
            
class CreateTagsOnCacophonyServerFromModelRunPage(tk.Frame):  
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.current_onset_array_pos = 0
                     
        title_label = ttk.Label(self, text="Create Tags On Cacophony Server / Still to do - will modify create from onsets page", font=LARGE_FONT)
        title_label.grid(column=0, columnspan=1, row=0)    
                                                                               
        
app = Main_GUI()
app.mainloop() 