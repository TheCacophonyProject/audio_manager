'''
Created on 5 Sep 2019
Modified 17 12 2019a

@author: tim

'''
from tkinter.messagebox import showinfo
from threading import Thread
from pylint.test import test_self

import time


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
from tkinter import filedialog


# import os
from PIL import ImageTk,Image 

import main.functions as functions
import main.parameters as parameters
from main.parameters import *
# import datetime

from datetime import datetime
import calendar

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
        
#         for F in (HomePage, RecordingsPage, TaggingPage, CreateWekaModelPage, ClassifyOnsetsUsingWekaModelPage, CreateOnsetsPage, CreateSpectrogramsPage, CreateTagsFromOnsetsPage, EvaluateWekaModelRunResultPage, CreateTagsOnCacophonyServerFromModelRunPage, ModelAccuracyAnalysisPage, CreateTestDataPage):
        for F in (HomePage, RecordingsPage, CreateWekaModelPage, ClassifyOnsetsUsingWekaModelPage, CreateOnsetsPage, EvaluateWekaModelRunResultPage, CreateTagsOnCacophonyServerFromModelRunPage, ModelAccuracyAnalysisPage, CreateTestDataPage):
          
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
        
        instuctions_text2 = "SQLite is used as the database, without any wrapper (such as GRDB) to allow for concurrent db write access.  This means if you run two versions of this application at once, you will get errors."
        instuctions_msg2 = tk.Message(self, text = instuctions_text2)
        instuctions_msg2.config(width=600)
        instuctions_msg2.pack(pady=10,padx=10)
        
        instuctions_text3 = "Keep an eye on the Console - you will need to enter your Cacophony server password, and view other messages"
        instuctions_msg3 = tk.Message(self, text = instuctions_text3)
        instuctions_msg3.config(width=600)
        instuctions_msg3.pack(pady=10,padx=10)
        
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
        
        modelAccuracyAnalysisPage_button = ttk.Button(self, text="Step 5: Model Accuracy Analysis",
                            command=lambda: controller.show_frame(ModelAccuracyAnalysisPage))        
        modelAccuracyAnalysisPage_button.pack()
        
        createWekaModelPage_button = ttk.Button(self, text="Step 6: Create Weka Model",
                            command=lambda: controller.show_frame(CreateWekaModelPage))        
        createWekaModelPage_button.pack()  
        
        outside_normal_flow_label = tk.Label(self, text="Functions below here are outside normal model development iteration")
        outside_normal_flow_label.pack(pady=10,padx=10)
        
        createTagsOnCacophonyServerFromModelRunPage_button = ttk.Button(self, text="Step A: Create Tags On Cacophony Server From Model Run ",
                            command=lambda: controller.show_frame(CreateTagsOnCacophonyServerFromModelRunPage))        
        createTagsOnCacophonyServerFromModelRunPage_button.pack()
        
        createTestDataPage_button = ttk.Button(self, text="Create test data ",
                            command=lambda: controller.show_frame(CreateTestDataPage))        
        createTestDataPage_button.pack()
        
#         createTestPage_button = ttk.Button(self, text="Create test page ",
#                             command=lambda: controller.show_frame(CreateTestPage))        
#         createTestPage_button.pack()
        


class RecordingsPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        title_label = ttk.Label(self, text="Recordings Page", font=LARGE_FONT)
        title_label.grid(column=0, columnspan=1, row=0)
        
        device_name_label = ttk.Label(self, text="Device name e.g hammond_park_v2")
        device_name_label.grid(column=0, columnspan=1, row=1)
             
        device_name = StringVar(value='hammond_park_v2')
        device_name_entry = tk.Entry(self,  textvariable=device_name, width=30)
        device_name_entry.grid(column=1, columnspan=1, row=1)
        
        device_super_name_label = ttk.Label(self, text="Device Super name (e.g. Hammond_Park)")
        device_super_name_label.grid(column=0, columnspan=1, row=2)
        
        device_super_name = StringVar(value='Hammond_Park')
        device_super_name_entry = tk.Entry(self,  textvariable=device_super_name, width=30)
        device_super_name_entry.grid(column=1, columnspan=1,row=2)
               
#         get_recordings_button = ttk.Button(self, text="Load Recordings from local folder ",
#                             command=lambda: functions.load_recordings_from_local_folder(device_name.get(), device_super_name.get()))
#         get_recordings_button.grid(column=0, columnspan=1, row=3)
#         
#         load_recordings_from_local_folder_instructions = "Useful if you have the recordings on a usb drive - not for downloading from server"
# 
#         msg1 = tk.Message(self, text = load_recordings_from_local_folder_instructions)
#         msg1.config(width=600)
#         msg1.grid(column=1, columnspan=2, row=3)  
# 
#         get_recording_information_from_server_button = ttk.Button(self, text="Get Recording Information for recordings imported from local file system",
#                             command=lambda: functions.update_recording_information_for_all_local_database_recordings())
#         get_recording_information_from_server_button.grid(column=0, columnspan=1, row=4)
        
        get_new_recordings_from_server_button = ttk.Button(self, text="Get New Recordings For specified Device from Server",
                            command=lambda: functions.get_recordings_from_server(device_name.get(), device_super_name.get()))
        get_new_recordings_from_server_button.grid(column=0, columnspan=1, row=5)
        
        get_new_recordings_from_server_instructions = "This will get the recordings for the device in the device name box. It will also assign a super name from the Super Name box"


        msg2 = tk.Message(self, text = get_new_recordings_from_server_instructions)
        msg2.config(width=600)
        msg2.grid(column=1, columnspan=2, row=5)   
        
        get_new_recordings_from_server_button = ttk.Button(self, text="Get Recordings For all devices already in local database from Server",
                            command=lambda: functions.get_recordings_from_server_for_all_devices())
        get_new_recordings_from_server_button.grid(column=0, columnspan=1, row=6)
        
        get_new_recordings_from_server_instructions = "This will see what devices have already been used and the recordings for all of them, and will used the device_super_name already in the local database (will not use the text in the boxes above)."


        msg3 = tk.Message(self, text = get_new_recordings_from_server_instructions)
        msg3.config(width=600)
        msg3.grid(column=1, columnspan=2, row=6) 
        
        retrive_any_missing_recordings_info_from_server_button = ttk.Button(self, text="Retrieve any missing recordings info from server",
                            command=lambda: functions.retrieve_missing_recording_information()())
        retrive_any_missing_recordings_info_from_server_button.grid(column=0, columnspan=1, row=10)
        
        retrive_any_missing_recordings_info_from_server_instructions = "You shouldn't have to use this, but if the previous process was interrupted, you may need to run this to get the missing recording information (there will be nulls in the recordingDateTime etc database field)."


        msg3 = tk.Message(self, text = retrive_any_missing_recordings_info_from_server_instructions)
        msg3.config(width=600)
        msg3.grid(column=1, columnspan=2, row=10)   
        
#         scan_local_folder_for_recordings_not_in_local_db_and_update_button = ttk.Button(self, text="Scan recordings folder for recordings not in local db and update",
#                             command=lambda: functions.scan_local_folder_for_recordings_not_in_local_db_and_update(device_name.get(), device_super_name.get()))
#         scan_local_folder_for_recordings_not_in_local_db_and_update_button.grid(column=0, columnspan=1, row=6)
#        
#         scan_recordings_folder_instructions = "If you do NOT know the device name or super name enter unknown in the fields. The device name will be updated automatically"
# 
#         msg3 = tk.Message(self, text = scan_recordings_folder_instructions)
#         msg3.config(width=600)
#         msg3.grid(column=1, columnspan=1, row=6)               
        
        back_to_home_button = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        back_to_home_button.grid(column=0, columnspan=1, row=20)               

class CreateWekaModelPage(tk.Frame):    
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        title_label = ttk.Label(self, text="Create a Weka model - using Weka https://www.cs.waikato.ac.nz/ml/weka/downloading.html", font=LARGE_FONT)
        title_label.grid(column=0, columnspan=10, row=10)  
        
        instructions1_text = """
        
    Before we can use Weka to create a model, you first need to create an input arff file that uses 
    the model_run_results confirmed sounds. 
    
    Any model you create should be evaluated against test data.  Pick start and end dates to exclude recordings made between those dates (inclusive).
    
    This will also create a csv file that can be used to keep track of which confirmed onsets where used to create the model.
    
    This csv will be used by the Model Accuracy Analysis page.
        
    """    
        instructions1_text_label = ttk.Label(self, text=instructions1_text)                                                    
        instructions1_text_label.grid(column=0, columnspan=10, row=20)  
        
        
        # Couldn't get a date picker to work !!!!! so had to created separate input fields for day/month/year
        first_date_to_exclude_label = ttk.Label(self, text="First date to exclude")
        first_date_to_exclude_label.grid(column=0, columnspan=2, row=21)           
        
        first_date_to_exclude_day_label = ttk.Label(self, text="DAY")
        first_date_to_exclude_day_label.grid(column=0, columnspan=1, row=22)
        
        first_date_to_exclude_day = StringVar(value='1')
        first_date_to_exclude_day_entry = tk.Entry(self,  textvariable=first_date_to_exclude_day, width=5)
        first_date_to_exclude_day_entry.grid(column=1, columnspan=1, row=22)
        
        first_date_to_exclude_month_label = ttk.Label(self, text="MONTH")
        first_date_to_exclude_month_label.grid(column=0, columnspan=1, row=23)
        
        first_date_to_exclude_month = StringVar(value='3')
        first_date_to_exclude_month_entry = tk.Entry(self,  textvariable=first_date_to_exclude_month, width=5)
        first_date_to_exclude_month_entry.grid(column=1, columnspan=1, row=23)
        
        first_date_to_exclude_year_label = ttk.Label(self, text="YEAR")
        first_date_to_exclude_year_label.grid(column=0, columnspan=1, row=24)
        
        first_date_to_exclude_year = StringVar(value='2020')
        first_date_to_exclude_year_entry = tk.Entry(self,  textvariable=first_date_to_exclude_year, width=5)
        first_date_to_exclude_year_entry.grid(column=1, columnspan=1, row=24)
        
        
        last_date_to_exclude_label = ttk.Label(self, text="Last date to exclude")
        last_date_to_exclude_label.grid(column=2, columnspan=2, row=21)
        
        last_date_to_exclude_day_label = ttk.Label(self, text="DAY")
        last_date_to_exclude_day_label.grid(column=2, columnspan=1, row=22)
        
        last_date_to_exclude_day = StringVar(value='31')
        last_date_to_exclude_day_entry = tk.Entry(self,  textvariable=last_date_to_exclude_day, width=5)
        last_date_to_exclude_day_entry.grid(column=3, columnspan=1, row=22)
        
        last_date_to_exclude_month_label = ttk.Label(self, text="MONTH")
        last_date_to_exclude_month_label.grid(column=2, columnspan=1, row=23)
        
        last_date_to_exclude_month = StringVar(value='3')
        last_date_to_exclude_month_entry = tk.Entry(self,  textvariable=last_date_to_exclude_month, width=5)
        last_date_to_exclude_month_entry.grid(column=3, columnspan=1, row=23)
        
        last_date_to_exclude_year_label = ttk.Label(self, text="YEAR")
        last_date_to_exclude_year_label.grid(column=2, columnspan=1, row=24)
        
        last_date_to_exclude_year = StringVar(value='2020')
        last_date_to_exclude_year_entry = tk.Entry(self,  textvariable=last_date_to_exclude_year, width=5)
        last_date_to_exclude_year_entry.grid(column=3, columnspan=1, row=24)
        

#         create_arff_file_for_weka_button = ttk.Button(self, text="Create Arff file for Weka input", command=lambda: functions.create_arff_file_for_weka(False))  
        create_arff_file_for_weka_button = ttk.Button(self, text="Create Arff file for Weka input", command=lambda: create_arff_and_csv_files())      
        create_arff_file_for_weka_button.grid(column=6, columnspan=1, row=25)
        
        instructions2_text = """
BEFORE pressing the 'Create folders for next run' button, update the model_run_name parameter in the 
parameters file with a new name AND exit/close this program and restart to refresh - check it has.  
It is currently set to " + model_run_name + " which is most likely the previous model run folder that 
you used - you don't want to use the same folder - it will end in tears!! (Once pressed, check that 
the folders have been created in the file system).  This will give you a place to save your next Weka 
model.model file. You can now press the Create folders for next run button to create all the necessary 
folders for the next iteration/run."""    
        instructions2_text_label = ttk.Label(self, text=instructions2_text)                                                    
        instructions2_text_label.grid(column=0, columnspan=5, row=30)  
        
        create_folders_button = ttk.Button(self, text="Create folders for next run",command=lambda: functions.create_folders_for_next_run())
        create_folders_button.grid(column=6, columnspan=1, row=30)  
        

        
        instructions3_text = """
You are now ready to use Weka. BUT, if you are going to use AutoWeka it needs to use Java 1.8 
(unlike Weka or Eclipse/Audio Manager which can use openjdk 11 - so at a terminal type 
'sudo update-alternatives --config java' without the quotes and choose option (5 on my computer) 
for jdk1.8 Once the java version has been changed, from a terminal command prompt, cd into the 
directory where Weka has been installed (e.g. ~/weka-3-8-4b (on my computer) and launch Weka 
using the command: java -Xmx16384m -jar weka.jar
    
These instructions are from the video: https://www.futurelearn.com/courses/advanced-data-
mining-with-weka/0/steps/29486\ You will need to have installed the Image Filters Package 
into Weka."""    
        instructions3_text_label = ttk.Label(self, text=instructions3_text)                                                    
        instructions3_text_label.grid(column=0, columnspan=5, row=40)  

        
        instructions5_text = """
        
    In Weka, Press the Explorer button and then the Open file.. button to open the previously created .arff file.
        
    """    
        instructions5_text_label = ttk.Label(self, text=instructions5_text)                                                    
        instructions5_text_label.grid(column=0, columnspan=10, row=50) 

        
        instructions7_text = """
        
    If you want to use AutoWeka follow A instructions next otherwise follow B instructions. 
    
    A) Select the Auto-Weka tab (in Weka) then right click on AUTOWEKAClassifier | Show properties and change timeLimit 
    to something suitable say 4320 (ie 3 days), or first test with 10 minutes :-), press OK, check that (Nom) class is 
    selected and then press start. The weka icon does its dance.  Make sure computer Power Saving is Off, and come back 
    in 3 days! 
    
    B) If don't want to use AutoWeka try this - it will create the same model type (CostSensitiveClassifier) that was being 
    used when these instructions where written.  Note: the ClassifyOnsets code will need to use the same model type as you 
    create here - change it in that code if you create a different model type.
    
    1) Select the Classify tab (at the top). Press the Choose button and navigate to  Weka|classifiers|meta|CostSensitiveClassifier
    
    2) Then left click in text box that has the text CostSensitiveClassifier..... to open another dialog.
    
    3) Next to word classifier, Press Choose and navigate to weka|classifiers|meta|RandomCommittee. 
    
    4) In your computers file system, find the file 'penalties 16x16 10 penalty.cost' and copy it to the current model_run\model folder
    
    5) Press on the box next to costMatrix, press Open and find the 'penalties 16x16 10 penalty.cost', and close the CostMatrixEditor 
    window.
    
    6) Next to the word classifer, press the Choose button and navigate to weka|classifiers|meta|RandomForest, press OK, OK
    
    7) Back in the Classify tab, in Test Options, select 'Cross-validation Folds 10' and press the 'Start' button.
    
    The weka in the bottom right corner does it's dance.
    
    8) When the weka has finished dancing the results are displayed - take a look.
    
    9) Right click on the just finished 'Result list' listing, and save save the result buffer in weka_model foler for this run.
    
    10) Also export the model, to the same location so it is available for future classifications.        
        
    """    
        instructions7_text_label = ttk.Label(self, text=instructions7_text)                                                    
        instructions7_text_label.grid(column=0, columnspan=10, row=60) 
        
              
        
        back_to_home_button = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        back_to_home_button.grid(column=0, columnspan=1, row=80)    
        
        def create_arff_and_csv_files(): 
            # https://www.w3schools.com/python/python_datetime.asp
            firstDate = datetime.datetime((int)(first_date_to_exclude_year.get()), (int)(first_date_to_exclude_month.get()), (int)(first_date_to_exclude_day.get()))
            lastDate = datetime.datetime((int)(last_date_to_exclude_year.get()), (int)(last_date_to_exclude_month.get()), (int)(last_date_to_exclude_day.get()))
#             print(firstDate.strftime("%c"))           
            functions.create_arff_file_for_weka(False, firstDate,lastDate)             
        
class ClassifyOnsetsUsingWekaModelPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.clip_folder = StringVar(value='')
          
        title_label = ttk.Label(self, text="Classify Onsets Using Weka Model", font=LARGE_FONT)
        title_label.grid(column=0, columnspan=1, row=0)    
        
        instructions1_text = """\n\n
        
    1) Onsets can only be classified if you have already created the Edge Histogram features - see 'Create Onsets' page.
    
    2) To classify onsets, you will first need to have created a Weka Model - the Create Weka Model page for instructions 
    on how to do this.
    
    3) Copy the weka model.model file into the current audio_classifier_runs model folder - which is currently set to:
    """ + parameters.run_folder + "/" + parameters.weka_model_folder + """
     
    4) Also copy the 'dummy' input.arff file into the same weka_model folder, from the previous weka_model folder.  
    This file is needed for weka to determine the location of the image file to use.
    
    5) Now open the ClassifyOnsets.java file and change the value of modelRunName variable to the same as this model Run folder name.
    
    6) Still in Eclipse, check that ClassifyOnsets.java code variables deviceSuperNameLabels and classLabels are up-to-date and then run the code.
    
    \n\n"""
                
        instructions1_text_label = ttk.Label(self, text=instructions1_text)                                                    
        instructions1_text_label.grid(column=0, columnspan=1, row=5) 
  
 
        back_to_home_button = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(HomePage))  
        back_to_home_button.grid(column=0, columnspan=1, row=45) 
                            
class CreateOnsetsPage(tk.Frame):    
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.clip_folder = StringVar(value='')
             
        title_label = ttk.Label(self, text="Create Onsets", font=LARGE_FONT)
        title_label.grid(column=0, columnspan=1, row=0)    
        
        
        instructions1_text = """
        
    1) Once you have downloaded new recordings, you need to find locations of interest - called onsets.
    
    2) Press the Run button to create these onsets.    
   
    """
                
        instructions1_text_label = ttk.Label(self, text=instructions1_text)                                                    
        instructions1_text_label.grid(column=0, columnspan=1, row=5) 
               

        
        run_button = ttk.Button(self, text="Run", command=lambda: functions.create_onsets_in_local_db_using_recordings_folder())        
        run_button.grid(column=0, columnspan=1, row=20) 
        
        instructions2_text = """
        
    3) After the onsets have been created, you will need to create 'features' for each onset location.  Later these features will 
    be used to train models and classify sounds.
        a) Press the 'Update Onsets with Edge Histogram Features' button to create the features - they will be stored in the database.
        
    """
    
        instructions2_text_label = ttk.Label(self, text=instructions2_text)                                                    
        instructions2_text_label.grid(column=0, columnspan=1, row=25) 
        
        update_button = ttk.Button(self, text="Update Onsets with Edge Histogram Features", command=lambda: functions.update_onsets_with_edge_histogram_features()())        
        update_button.grid(column=0, columnspan=1, row=30)        

        back_to_home_button = ttk.Button(self, text="Back to Home",command=lambda: controller.show_frame(HomePage))                            
        back_to_home_button.grid(column=0, columnspan=1, row=40)                  

# class CreateSpectrogramsPage(tk.Frame):    
#     
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.clip_folder = StringVar(value='')       
#              
#         title_label = ttk.Label(self, text="Create Spectrograms using ONSETs", font=LARGE_FONT)
#         title_label.grid(column=0, columnspan=1, row=0)    
#         
#         onset_instructions = "Use this page to run the create spectrogram function that will create spectrograms in the spectrogram folder"
#         msg = tk.Message(self, text = onset_instructions)
#         msg.config(bg='lightgreen', font=('times', 17), width=1000)
#         msg.grid(column=0, columnspan=2, row=1)  
#                 
#         run_button = ttk.Button(self, text="Run", command=lambda: functions.create_focused_mel_spectrogram_jps_using_onset_pairs())
#         run_button.grid(column=0, columnspan=1, row=2) 
#         
#         spectrogram_folder_instructions = "The spectrograms will be created in the folder: " + base_folder + '/' + run_folder + " This can be changed in the python parameters file"
#         folder_msg = tk.Message(self, text = spectrogram_folder_instructions)
#         folder_msg.config(width=600)
#         folder_msg.grid(column=1, columnspan=1, row=2)    
# 
#         back_to_home_button = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(HomePage))
#         back_to_home_button.grid(column=0, columnspan=1, row=3)                  

# class CreateTagsFromOnsetsPage(tk.Frame):  
#     
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.current_onset_array_pos = 0
#                      
#         title_label = ttk.Label(self, text="Create Tags From Onsets", font=LARGE_FONT)
#         title_label.grid(column=0, columnspan=1, row=0)    
#         
#         onset_instructions = "Use this page to create Tags from onsets"
#         
#         msg = tk.Message(self, text = onset_instructions)
#         msg.config(bg='lightgreen', font=('times', 16), width=1200)
#         msg.grid(column=0, columnspan=6, row=1)   
#         
#         onset_version_label = ttk.Label(self, text="The version of the onset (field in onset table") 
#         onset_version_label.grid(column=0, columnspan=1, row=2)       
#         onset_version = StringVar(value='5')
#         onset_version_entry = tk.Entry(self,  textvariable=onset_version, width=30)
#         onset_version_entry.grid(column=1, columnspan=1,row=2)
#         
#         recording_id_label = ttk.Label(self, text="Recording Id") 
#         recording_id_label.grid(column=0, columnspan=1, row=3)            
#         self.recording_id = StringVar(value='0000000')
#         self.recording_id_entry = tk.Entry(self,  textvariable=self.recording_id, width=30).grid(column=1, columnspan=1, row=3)
#         
#         start_time_label = ttk.Label(self, text="Start Time")
#         start_time_label.grid(column=2, columnspan=1, row=3)        
#         self.start_time = StringVar(value='0.0')
#         self.start_time_entry = tk.Entry(self,  textvariable=self.start_time, width=30).grid(column=3, columnspan=1,row=3)
#         
#         load_onsets_button = ttk.Button(self, text="Load Onsets",command=lambda: get_onsets())
#         load_onsets_button.grid(column=0, columnspan=1, row=4)                        
# 
#         self.spectrogram_label = ttk.Label(self, image=None)
#         self.spectrogram_label.grid(column=0, columnspan=1, row=5)
#         
#         self.waveform_label = ttk.Label(self, image=None)
#         self.waveform_label.grid(column=1, columnspan=1, row=5)
#         
#         previous_button = ttk.Button(self, text="Previous", command=lambda: previous_onset())
#         previous_button.grid(column=0, columnspan=1, row=6)
#                             
#         play_button = ttk.Button(self, text="Play", command=lambda: functions.play_clip(str(self.current_onset_recording_id), float(self.current_onset_start_time),self.current_onset_duration))
#         play_button.grid(column=1, columnspan=1, row=6)
#                             
#         next_button = ttk.Button(self, text="Next", command=lambda: next_onset())
#         next_button.grid(column=2, columnspan=1, row=6)                           
#                              
#         back_to_home_button = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(HomePage))
#         back_to_home_button.grid(column=0, columnspan=1, row=7)    
#                             
#         def get_onsets():            
#             self.onsets = functions.get_onsets_stored_locally(onset_version.get())            
#             load_current_onset() 
#             
#         def next_onset():
#             if self.current_onset_array_pos < (len(self.onsets)) -1:                        
#                 self.current_onset_array_pos +=1
#                 load_current_onset()
#                
#         def previous_onset():
#             if self.current_onset_array_pos > 0:
#                 self.current_onset_array_pos -=1
#                 load_current_onset()
#                 
#         def play_clip():
#             functions.play_clip(str(self.current_onset_recording_id), float(self.current_onset_start_time),self.current_onset_duration)
#                      
#         def display_images():
#             self.spectrogram_image = functions.get_single_create_focused_mel_spectrogram(self.current_onset_recording_id, self.current_onset_start_time, self.current_onset_duration)
#             self.waveform_image = functions.get_single_waveform_image(self.current_onset_recording_id, self.current_onset_start_time, self.current_onset_duration)            
#             
#             self.spectrogram_label.config(image=self.spectrogram_image)
#             self.waveform_label.config(image=self.waveform_image)
#             
#         def load_current_onset():
#             
#             current_onset = self.onsets[self.current_onset_array_pos]
#              
#             self.current_onset_recording_id = current_onset[1]      
#             self.recording_id.set(self.current_onset_recording_id)
#              
#             self.current_onset_start_time = current_onset[2]
#             self.start_time.set(self.current_onset_start_time)
#             
#             self.current_onset_duration = current_onset[3] 
#                         
#             threading.Thread(target=play_clip(), args=(1,)).start()
#             threading.Thread(target=display_images(), args=(1,)).start()      
            
class EvaluateWekaModelRunResultPage(tk.Frame):    
    
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.current_model_run_result_array_pos = 0
        self.current_model_run_name_ID = 0        
        
        self.unique_model_run_names = functions.get_unique_model_run_names()  
        self.unique_locations = functions.get_unique_locations('recordings')            
                    
        title_label = ttk.Label(self, text="Evaluate Model Run Results", font=LARGE_FONT)
        title_label.grid(column=0, columnspan=1, row=0)           
                
        refresh_model_run_names_button = ttk.Button(self, text="Refresh Unique Model Run Names",command=lambda: refresh_unique_model_run_names())
        refresh_model_run_names_button.grid(column=0, columnspan=1, row=3) 
        
        run_names_label = ttk.Label(self, text="Run Names")
        run_names_label.grid(column=1, columnspan=1, row=2)      
                                    
        self.run_name = StringVar()
        self.run_names_combo = ttk.Combobox(self, textvariable=self.run_name, values=self.unique_model_run_names)
        
        if len(self.unique_model_run_names) > 0:
            self.run_names_combo.current(0)
            self.run_names_combo.grid(column=1, columnspan=1,row=3) 
            self.run_names_combo.current(len(self.unique_model_run_names) - 1)       
            
        location_filter_label = ttk.Label(self, text="Location Filter")
        location_filter_label.grid(column=2, columnspan=1, row=2)      
                                    
        self.location_filter = StringVar()
        self.location_filter_combo = ttk.Combobox(self, textvariable=self.location_filter, values=self.unique_locations)        
                                    
        self.recording_id_filter = StringVar()
#         self.recording_id_filter_combo = ttk.Combobox(self, textvariable=self.recording_id_filter, values=self.unique_locations)
        
        if len(self.unique_locations) > 0:
            self.location_filter_combo.current(0)
            self.location_filter_combo.grid(column=2, columnspan=1,row=3) 
            
        recording_id_filter_label = ttk.Label(self, text="Recording ID Filter (leave blank if not used)")
        recording_id_filter_label.grid(column=3, columnspan=1, row=2)   
        
        self.recording_id_filter_value = StringVar(value='')
        self.recording_id_filter_entry = tk.Entry(self,  textvariable=self.recording_id_filter_value, width=10).grid(column=3, columnspan=1,row=3)   
   
        actual_confirmed_filter_label = ttk.Label(self, text="Filter - Current Actual Confirmed", font=LARGE_FONT)
        actual_confirmed_filter_label.grid(column=0, columnspan=1, row=4)   
        
        # http://effbot.org/tkinterbook/checkbutton.htm
        self.actual_confirmed_other = StringVar() 
        actual_confirmed_other_than_checkbox = ttk.Checkbutton(self,text='Everything OTHER than selected', variable=self.actual_confirmed_other, onvalue="on", offvalue="off")
        actual_confirmed_other_than_checkbox.grid(column=1, columnspan=1, row=4)
        self.actual_confirmed_other.set('off')
             
        self.actual_confirmed_filter = tk.StringVar()
        actual_confirmed_filter_radio_button_none = ttk.Radiobutton(self,text='Not Used', variable=self.actual_confirmed_filter, value='not_used')
        actual_confirmed_filter_radio_button_none.grid(column=0, columnspan=1, row=13)        
        actual_confirmed_filter_radio_button_null = ttk.Radiobutton(self,text='Null Filter (ie nothing in DB table)', variable=self.actual_confirmed_filter, value='IS NULL')
        actual_confirmed_filter_radio_button_null.grid(column=0, columnspan=1, row=14)        
        actual_confirmed_filter_radio_button_morepork_classic = ttk.Radiobutton(self,text='morepork_more-pork', variable=self.actual_confirmed_filter, value='morepork_more-pork')
        actual_confirmed_filter_radio_button_morepork_classic.grid(column=0, columnspan=1, row=15)
        actual_confirmed_filter_radio_button_unknown = ttk.Radiobutton(self,text='Unknown', variable=self.actual_confirmed_filter, value='unknown')
        actual_confirmed_filter_radio_button_unknown.grid(column=0, columnspan=1, row=16) 
        actual_confirmed_filter_radio_button_dove = ttk.Radiobutton(self,text='Dove', variable=self.actual_confirmed_filter, value='dove')
        actual_confirmed_filter_radio_button_dove.grid(column=0, columnspan=1, row=17) 
        actual_confirmed_filter_radio_button_duck = ttk.Radiobutton(self,text='Duck', variable=self.actual_confirmed_filter, value='duck')
        actual_confirmed_filter_radio_button_duck.grid(column=0, columnspan=1, row=18) 
        actual_confirmed_filter_radio_button_dog = ttk.Radiobutton(self,text='Dog', variable=self.actual_confirmed_filter, value='dog')
        actual_confirmed_filter_radio_button_dog.grid(column=0, columnspan=1, row=19) 
        actual_confirmed_filter_radio_button_human = ttk.Radiobutton(self,text='Human', variable=self.actual_confirmed_filter, value='human')
        actual_confirmed_filter_radio_button_human.grid(column=0, columnspan=1, row=20) 
        actual_confirmed_filter_radio_button_siren = ttk.Radiobutton(self,text='Siren', variable=self.actual_confirmed_filter, value='siren')
        actual_confirmed_filter_radio_button_siren.grid(column=0, columnspan=1, row=21) 
        actual_confirmed_filter_radio_button_bird = ttk.Radiobutton(self,text='Bird', variable=self.actual_confirmed_filter, value='bird')
        actual_confirmed_filter_radio_button_bird.grid(column=0, columnspan=1, row=22) 
        actual_confirmed_filter_radio_button_car = ttk.Radiobutton(self,text='Car', variable=self.actual_confirmed_filter, value='car')
        actual_confirmed_filter_radio_button_car.grid(column=0, columnspan=1, row=23) 
        actual_confirmed_filter_radio_button_rumble = ttk.Radiobutton(self,text='Rumble', variable=self.actual_confirmed_filter, value='rumble')
        actual_confirmed_filter_radio_button_rumble.grid(column=0, columnspan=1, row=24)
        actual_confirmed_filter_radio_button_water = ttk.Radiobutton(self,text='Water', variable=self.actual_confirmed_filter, value='water')
        actual_confirmed_filter_radio_button_water.grid(column=0, columnspan=1, row=25)
        actual_confirmed_filter_radio_button_hand_saw = ttk.Radiobutton(self,text='Hand saw', variable=self.actual_confirmed_filter, value='hand_saw')
        actual_confirmed_filter_radio_button_hand_saw.grid(column=0, columnspan=1, row=26)
        
        
        actual_confirmed_filter_radio_button_white_noise = ttk.Radiobutton(self,text='White noise', variable=self.actual_confirmed_filter, value='white_noise')
        actual_confirmed_filter_radio_button_white_noise.grid(column=1, columnspan=1, row=13)
        actual_confirmed_filter_radio_button_plane = ttk.Radiobutton(self,text='Plane', variable=self.actual_confirmed_filter, value='plane')
        actual_confirmed_filter_radio_button_plane.grid(column=1, columnspan=1, row=14)
        actual_confirmed_filter_radio_button_cow = ttk.Radiobutton(self,text='Cow', variable=self.actual_confirmed_filter, value='cow')
        actual_confirmed_filter_radio_button_cow.grid(column=1, columnspan=1, row=15)
        actual_confirmed_filter_radio_button_buzzy_insect = ttk.Radiobutton(self,text='Buzzy_insect', variable=self.actual_confirmed_filter, value='buzzy_insect')
        actual_confirmed_filter_radio_button_buzzy_insect.grid(column=1, columnspan=1, row=16)
        actual_confirmed_filter_radio_button_morepork_more_pork_part = ttk.Radiobutton(self,text='Morepork more-pork Part', variable=self.actual_confirmed_filter, value='morepork_more-pork_part')
        actual_confirmed_filter_radio_button_morepork_more_pork_part.grid(column=1, columnspan=1, row=17)
        actual_confirmed_filter_radio_button_hammering = ttk.Radiobutton(self,text='Hammering', variable=self.actual_confirmed_filter, value='hammering')
        actual_confirmed_filter_radio_button_hammering.grid(column=1, columnspan=1, row=18)
        actual_confirmed_filter_radio_button_frog = ttk.Radiobutton(self,text='Frog', variable=self.actual_confirmed_filter, value='frog')
        actual_confirmed_filter_radio_button_frog.grid(column=1, columnspan=1, row=19)
        actual_confirmed_filter_radio_button_chainsaw = ttk.Radiobutton(self,text='Chainsaw', variable=self.actual_confirmed_filter, value='chainsaw')
        actual_confirmed_filter_radio_button_chainsaw.grid(column=1, columnspan=1, row=20)
        actual_confirmed_filter_radio_button_crackle = ttk.Radiobutton(self,text='Crackle', variable=self.actual_confirmed_filter, value='crackle')
        actual_confirmed_filter_radio_button_crackle.grid(column=1, columnspan=1, row=21)
        actual_confirmed_filter_radio_button_car_horn = ttk.Radiobutton(self,text='Car horn', variable=self.actual_confirmed_filter, value='car_horn')
        actual_confirmed_filter_radio_button_car_horn.grid(column=1, columnspan=1, row=22)
        actual_confirmed_filter_radio_button_fire_work = ttk.Radiobutton(self,text='Fire work', variable=self.actual_confirmed_filter, value='fire_work')
        actual_confirmed_filter_radio_button_fire_work.grid(column=1, columnspan=1, row=23)
        actual_confirmed_filter_radio_button_maybe_morepork_more_pork = ttk.Radiobutton(self,text='Maybe Morepork more-pork', variable=self.actual_confirmed_filter, value='maybe_morepork_more-pork')
        actual_confirmed_filter_radio_button_maybe_morepork_more_pork.grid(column=1, columnspan=1, row=24)
        actual_confirmed_filter_radio_button_music = ttk.Radiobutton(self,text='Music', variable=self.actual_confirmed_filter, value='music')
        actual_confirmed_filter_radio_button_music.grid(column=1, columnspan=1, row=25)
        
        self.actual_confirmed_filter.set('not_used')
        
        predicted_filter_label = ttk.Label(self, text="Filter - Predicted", font=LARGE_FONT)
        predicted_filter_label.grid(column=2, columnspan=1, row=4)  
        
        self.predicted_other = StringVar()
        predicted_other_than_checkbox = ttk.Checkbutton(self,text='Everything OTHER than selected', variable=self.predicted_other, onvalue="on", offvalue="off")
        predicted_other_than_checkbox.grid(column=3, columnspan=1, row=4)
        self.predicted_other.set('off')
             
        self.predicted_filter = tk.StringVar()        
        predicted_filter_radio_button_none = ttk.Radiobutton(self,text='Not Used', variable=self.predicted_filter, value='not_used')
        predicted_filter_radio_button_none.grid(column=2, columnspan=1, row=13)
        predicted_filter_radio_button_morepork_classic = ttk.Radiobutton(self,text='Morepork more-pork', variable=self.predicted_filter, value='morepork_more-pork')
        predicted_filter_radio_button_morepork_classic.grid(column=2, columnspan=1, row=14)
        predicted_filter_radio_button_unknown = ttk.Radiobutton(self,text='Unknown', variable=self.predicted_filter, value='unknown')
        predicted_filter_radio_button_unknown.grid(column=2, columnspan=1, row=15) 
        predicted_filter_radio_button_dove = ttk.Radiobutton(self,text='Dove', variable=self.predicted_filter, value='dove')
        predicted_filter_radio_button_dove.grid(column=2, columnspan=1, row=16) 
        predicted_filter_radio_button_duck = ttk.Radiobutton(self,text='Duck', variable=self.predicted_filter, value='duck')
        predicted_filter_radio_button_duck.grid(column=2, columnspan=1, row=17) 
        predicted_filter_radio_button_dog = ttk.Radiobutton(self,text='Dog', variable=self.predicted_filter, value='dog')
        predicted_filter_radio_button_dog.grid(column=2, columnspan=1, row=18) 
        predicted_filter_radio_button_human = ttk.Radiobutton(self,text='Human', variable=self.predicted_filter, value='human')
        predicted_filter_radio_button_human.grid(column=2, columnspan=1, row=19) 
        predicted_filter_radio_button_siren = ttk.Radiobutton(self,text='Siren', variable=self.predicted_filter, value='siren')
        predicted_filter_radio_button_siren.grid(column=2, columnspan=1, row=20) 
        predicted_filter_radio_button_bird = ttk.Radiobutton(self,text='Bird', variable=self.predicted_filter, value='bird')
        predicted_filter_radio_button_bird.grid(column=2, columnspan=1, row=21) 
        predicted_filter_radio_button_car = ttk.Radiobutton(self,text='Car', variable=self.predicted_filter, value='car')
        predicted_filter_radio_button_car.grid(column=2, columnspan=1, row=22)
        predicted_filter_radio_button_rumble = ttk.Radiobutton(self,text='Rumble', variable=self.predicted_filter, value='rumble')
        predicted_filter_radio_button_rumble.grid(column=2, columnspan=1, row=23)
        predicted_filter_radio_button_water = ttk.Radiobutton(self,text='Water', variable=self.predicted_filter, value='water')
        predicted_filter_radio_button_water.grid(column=2, columnspan=1, row=24)
        predicted_filter_radio_button_hand_saw = ttk.Radiobutton(self,text='Hand saw', variable=self.predicted_filter, value='hand_saw')
        predicted_filter_radio_button_hand_saw.grid(column=2, columnspan=1, row=25) 
        
        
        predicted_filter_radio_button_white_noise = ttk.Radiobutton(self,text='White noise', variable=self.predicted_filter, value='white_noise')
        predicted_filter_radio_button_white_noise.grid(column=3, columnspan=1, row=13)  
        predicted_filter_radio_button_plane = ttk.Radiobutton(self,text='Plane', variable=self.predicted_filter, value='plane')
        predicted_filter_radio_button_plane.grid(column=3, columnspan=1, row=14)
        predicted_filter_radio_button_cow = ttk.Radiobutton(self,text='Cow', variable=self.predicted_filter, value='cow')
        predicted_filter_radio_button_cow.grid(column=3, columnspan=1, row=15)  
        predicted_filter_radio_button_buzzy_insect = ttk.Radiobutton(self,text='Buzzy insect', variable=self.predicted_filter, value='buzzy_insect')
        predicted_filter_radio_button_buzzy_insect.grid(column=3, columnspan=1, row=16)
        predicted_filter_radio_button_morepork_more_pork_part = ttk.Radiobutton(self,text='Morepork more-pork Part', variable=self.predicted_filter, value='morepork_more-pork_part')
        predicted_filter_radio_button_morepork_more_pork_part.grid(column=3, columnspan=1, row=17) 
        predicted_filter_radio_button_hammering = ttk.Radiobutton(self,text='Hammering', variable=self.predicted_filter, value='hammering')
        predicted_filter_radio_button_hammering.grid(column=3, columnspan=1, row=18)
        predicted_filter_radio_button_frog = ttk.Radiobutton(self,text='Frog', variable=self.predicted_filter, value='frog')
        predicted_filter_radio_button_frog.grid(column=3, columnspan=1, row=19)  
        predicted_filter_radio_button_chainsaw = ttk.Radiobutton(self,text='Chainsaw', variable=self.predicted_filter, value='chainsaw')
        predicted_filter_radio_button_chainsaw.grid(column=3, columnspan=1, row=20) 
        predicted_filter_radio_button_crackle = ttk.Radiobutton(self,text='Crackle', variable=self.predicted_filter, value='crackle')
        predicted_filter_radio_button_crackle.grid(column=3, columnspan=1, row=21)  
        predicted_filter_radio_button_car_horn = ttk.Radiobutton(self,text='Car horn', variable=self.predicted_filter, value='car_horn')
        predicted_filter_radio_button_car_horn.grid(column=3, columnspan=1, row=22)
        predicted_filter_radio_button_fire_work = ttk.Radiobutton(self,text='Fire work', variable=self.predicted_filter, value='fire_work')
        predicted_filter_radio_button_fire_work.grid(column=3, columnspan=1, row=23) 
        predicted_filter_radio_button_maybe_morepork_more_pork = ttk.Radiobutton(self,text='Maybe Morepork more-pork', variable=self.predicted_filter, value='maybe_morepork_more-pork')
        predicted_filter_radio_button_maybe_morepork_more_pork.grid(column=3, columnspan=1, row=24)  
        predicted_filter_radio_button_music = ttk.Radiobutton(self,text='Music', variable=self.predicted_filter, value='music')
        predicted_filter_radio_button_music.grid(column=3, columnspan=1, row=25) 
        
        self.predicted_filter.set('not_used') 
        
        used_to_create_model_label = ttk.Label(self, text="Used to create Model")
        used_to_create_model_label.grid(column=0, columnspan=1, row=125)  
        
        self.used_to_create_model_filter = tk.StringVar()
        used_to_create_model_filter_radio_button_greater_than = ttk.Radiobutton(self,text='Yes', variable=self.used_to_create_model_filter, value='yes')
        used_to_create_model_filter_radio_button_greater_than.grid(column=0, columnspan=1, row=126)
        used_to_create_model_filter_radio_button_less_than = ttk.Radiobutton(self,text='No', variable=self.used_to_create_model_filter, value='no')
        used_to_create_model_filter_radio_button_less_than.grid(column=1, columnspan=1, row=126) 
        used_to_create_model_filter_radio_button_not_used = ttk.Radiobutton(self,text='Not used', variable=self.used_to_create_model_filter, value='not_used',command=lambda: self.predicted_probability_filter_value.set(''))
        used_to_create_model_filter_radio_button_not_used.grid(column=1, columnspan=1, row=127)
        self.used_to_create_model_filter.set('not_used')
                 
        
        run_probability_label = ttk.Label(self, text="Probability")
        run_probability_label.grid(column=2, columnspan=1, row=125)  
        
        self.predicted_probability_filter = tk.StringVar()
        predicted_probability_filter_radio_button_greater_than = ttk.Radiobutton(self,text='Greater than', variable=self.predicted_probability_filter, value='greater_than')
        predicted_probability_filter_radio_button_greater_than.grid(column=2, columnspan=1, row=126)
        predicted_probability_filter_radio_button_less_than = ttk.Radiobutton(self,text='Less than', variable=self.predicted_probability_filter, value='less_than')
        predicted_probability_filter_radio_button_less_than.grid(column=3, columnspan=1, row=126)
        self.predicted_probability_filter_value = StringVar(value='')
        self.predicted_probability_filter_entry = tk.Entry(self,  textvariable=self.predicted_probability_filter_value, width=10).grid(column=2, columnspan=1,row=127)    
        predicted_probability_filter_radio_button_not_used = ttk.Radiobutton(self,text='Not used', variable=self.predicted_probability_filter, value='not_used',command=lambda: self.predicted_probability_filter_value.set(''))
        predicted_probability_filter_radio_button_not_used.grid(column=3, columnspan=1, row=127)
       
        self.predicted_probability_filter.set('not_used')        
        
        load_run_results_button = ttk.Button(self, text="Load Run Results using Filters",command=lambda: get_run_results())
        load_run_results_button.grid(column=0, columnspan=1, row=133) 
        
        self.number_of_results_label_value = tk.StringVar()
        number_of_results_label_for_value = ttk.Label(self, textvariable=self.number_of_results_label_value)
        number_of_results_label_for_value.grid(column=0, columnspan=1, row=134)   
        
        self.recording_id_and_result_place_value = tk.StringVar()
        recording_id_label = ttk.Label(self, textvariable=self.recording_id_and_result_place_value) 
        recording_id_label.grid(column=0, columnspan=1, row=135) 
        self.recording_id_and_result_place_value.set("Recording Id")
                   
        start_time_label = ttk.Label(self, text="Start Time")
        start_time_label.grid(column=1, columnspan=1, row=134)        
        self.start_time = StringVar(value='0.0')
        self.start_time_entry = tk.Entry(self,  textvariable=self.start_time, width=30).grid(column=1, columnspan=1,row=135)
        
        self.location_recorded_value = tk.StringVar()
        location_recorded_label = ttk.Label(self, textvariable=self.location_recorded_value) 
        location_recorded_label.grid(column=2, columnspan=1, row=134) 
        self.location_recorded_value.set("Location: ")   
        
        self.when_recorded_value = tk.StringVar()
        when_recorded_label = ttk.Label(self, textvariable=self.when_recorded_value) 
        when_recorded_label.grid(column=2, columnspan=1, row=135) 
        self.when_recorded_value.set("When: ")     
        
        self.spectrogram_label = ttk.Label(self, image=None)
        self.spectrogram_label.grid(column=0, columnspan=1, row=136)
        
        self.waveform_label = ttk.Label(self, image=None)
        self.waveform_label.grid(column=1, columnspan=1, row=136)
        
       
        actual_label_confirmed = ttk.Label(self, text="SET New Actual Confirmed", font=LARGE_FONT)
        actual_label_confirmed.grid(column=0, columnspan=2, row=240)
              
        self.actual_confirmed = tk.StringVar()

        actual_confirmed_radio_button_morepork_classic = ttk.Radiobutton(self,text='Morepork more-pork', variable=self.actual_confirmed, value='morepork_more-pork',command=lambda: confirm_actual())
        actual_confirmed_radio_button_morepork_classic.grid(column=0, columnspan=1, row=242) 
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Unknown', variable=self.actual_confirmed, value='unknown',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=0, columnspan=1, row=243)
        actual_confirmed_radio_button_dove = ttk.Radiobutton(self,text='Dove', variable=self.actual_confirmed, value='dove',command=lambda: confirm_actual())
        actual_confirmed_radio_button_dove.grid(column=0, columnspan=1, row=244)   
        actual_confirmed_radio_button_duck = ttk.Radiobutton(self,text='Duck', variable=self.actual_confirmed, value='duck',command=lambda: confirm_actual())
        actual_confirmed_radio_button_duck.grid(column=0, columnspan=1, row=245) 
        actual_confirmed_radio_button_dog = ttk.Radiobutton(self,text='Dog', variable=self.actual_confirmed, value='dog',command=lambda: confirm_actual())
        actual_confirmed_radio_button_dog.grid(column=0, columnspan=1, row=246) 
        actual_confirmed_radio_button_human = ttk.Radiobutton(self,text='Human', variable=self.actual_confirmed, value='human',command=lambda: confirm_actual())
        actual_confirmed_radio_button_human.grid(column=0, columnspan=1, row=247)   
        actual_confirmed_radio_button_siren = ttk.Radiobutton(self,text='Siren', variable=self.actual_confirmed, value='siren',command=lambda: confirm_actual())
        actual_confirmed_radio_button_siren.grid(column=0, columnspan=1, row=248)
        actual_confirmed_radio_button_bird = ttk.Radiobutton(self,text='Bird', variable=self.actual_confirmed, value='bird',command=lambda: confirm_actual())
        actual_confirmed_radio_button_bird.grid(column=0, columnspan=1, row=249) 
        actual_confirmed_radio_button_car = ttk.Radiobutton(self,text='Car', variable=self.actual_confirmed, value='car',command=lambda: confirm_actual())
        actual_confirmed_radio_button_car.grid(column=0, columnspan=1, row=250)
        actual_confirmed_radio_button_rumble = ttk.Radiobutton(self,text='Rumble', variable=self.actual_confirmed, value='rumble',command=lambda: confirm_actual())
        actual_confirmed_radio_button_rumble.grid(column=0, columnspan=1, row=251)
        actual_confirmed_radio_button_water = ttk.Radiobutton(self,text='Water', variable=self.actual_confirmed, value='water',command=lambda: confirm_actual())
        actual_confirmed_radio_button_water.grid(column=0, columnspan=1, row=252)
        actual_confirmed_radio_button_hand_saw = ttk.Radiobutton(self,text='Hand saw', variable=self.actual_confirmed, value='hand_saw',command=lambda: confirm_actual())
        actual_confirmed_radio_button_hand_saw.grid(column=0, columnspan=1, row=253)
        
        
        actual_confirmed_radio_button_white_noise = ttk.Radiobutton(self,text='White noise', variable=self.actual_confirmed, value='white_noise',command=lambda: confirm_actual())
        actual_confirmed_radio_button_white_noise.grid(column=1, columnspan=1, row=242)
        actual_confirmed_radio_button_plane = ttk.Radiobutton(self,text='Plane', variable=self.actual_confirmed, value='plane',command=lambda: confirm_actual())
        actual_confirmed_radio_button_plane.grid(column=1, columnspan=1, row=243)
        actual_confirmed_radio_button_cow = ttk.Radiobutton(self,text='Cow', variable=self.actual_confirmed, value='cow',command=lambda: confirm_actual())
        actual_confirmed_radio_button_cow.grid(column=1, columnspan=1, row=244) 
        actual_confirmed_radio_button_buzzy_insect = ttk.Radiobutton(self,text='Buzzy insect', variable=self.actual_confirmed, value='buzzy_insect',command=lambda: confirm_actual())
        actual_confirmed_radio_button_buzzy_insect.grid(column=1, columnspan=1, row=245) 
        actual_confirmed_radio_morepork_more_pork_part = ttk.Radiobutton(self,text='Morepork more-pork Part', variable=self.actual_confirmed, value='morepork_more-pork_part',command=lambda: confirm_actual())
        actual_confirmed_radio_morepork_more_pork_part.grid(column=1, columnspan=1, row=246) 
        actual_confirmed_radio_button_hammering = ttk.Radiobutton(self,text='Hammering', variable=self.actual_confirmed, value='hammering',command=lambda: confirm_actual())
        actual_confirmed_radio_button_hammering.grid(column=1, columnspan=1, row=247)  
        actual_confirmed_radio_button_frog = ttk.Radiobutton(self,text='Frog', variable=self.actual_confirmed, value='frog',command=lambda: confirm_actual())
        actual_confirmed_radio_button_frog.grid(column=1, columnspan=1, row=248)
        actual_confirmed_radio_button_chainsaw = ttk.Radiobutton(self,text='Chainsaw', variable=self.actual_confirmed, value='chainsaw',command=lambda: confirm_actual())
        actual_confirmed_radio_button_chainsaw.grid(column=1, columnspan=1, row=249) 
        actual_confirmed_radio_button_crackle = ttk.Radiobutton(self,text='Crackle', variable=self.actual_confirmed, value='crackle',command=lambda: confirm_actual())
        actual_confirmed_radio_button_crackle.grid(column=1, columnspan=1, row=250)  
        actual_confirmed_radio_button_car_horn = ttk.Radiobutton(self,text='Car horn', variable=self.actual_confirmed, value='car_horn',command=lambda: confirm_actual())
        actual_confirmed_radio_button_car_horn.grid(column=1, columnspan=1, row=251)
        actual_confirmed_radio_button_fire_work = ttk.Radiobutton(self,text='Fire work', variable=self.actual_confirmed, value='fire_work',command=lambda: confirm_actual())
        actual_confirmed_radio_button_fire_work.grid(column=1, columnspan=1, row=252)
        actual_confirmed_radio_button_maybe_morepork_more_pork = ttk.Radiobutton(self,text='Maybe Morepork more-pork', variable=self.actual_confirmed, value='maybe_morepork_more-pork',command=lambda: confirm_actual())
        actual_confirmed_radio_button_maybe_morepork_more_pork.grid(column=1, columnspan=1, row=253)
        actual_confirmed_radio_button_music = ttk.Radiobutton(self,text='Music', variable=self.actual_confirmed, value='music',command=lambda: confirm_actual())
        actual_confirmed_radio_button_music.grid(column=1, columnspan=1, row=254)       
       
        predicted_label = ttk.Label(self, text="Predicted (by last model run)", font=LARGE_FONT)
        predicted_label.grid(column=2, columnspan=1, row=240)       
        
        self.predicted_label_value = tk.StringVar()
        predicted_label_value_for_value = ttk.Label(self, textvariable=self.predicted_label_value)
        predicted_label_value_for_value.grid(column=2, columnspan=1, row=241) 
        
        previous_button = ttk.Button(self, text="Previous", command=lambda: previous_run_result())
        previous_button.grid(column=0, columnspan=1, row=260)
                            
        play_button = ttk.Button(self, text="Play Again", command=lambda: functions.play_clip(str(self.current_model_run_name_recording_id), float(self.current_model_run_name_start_time),self.current_model_run_name_duration, True))
        play_button.grid(column=1, columnspan=1, row=260)
        play_button = ttk.Button(self, text="Play Unfiltered", command=lambda: functions.play_clip(str(self.current_model_run_name_recording_id), float(self.current_model_run_name_start_time),self.current_model_run_name_duration, False))
        play_button.grid(column=1, columnspan=1, row=261)
                            
        confirm_next_button = ttk.Button(self, text="Next", command=lambda: next_run_result())
        confirm_next_button.grid(column=2, columnspan=1, row=260)
        
        next_button = ttk.Button(self, text="Unselect", command=lambda: unselect_actual_confirmed())
        next_button.grid(column=2, columnspan=1, row=261)
        
        back_to_home_button = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(HomePage))
        back_to_home_button.grid(column=0, columnspan=1, row=261) 
        
        def create_spectrograms():
            functions.create_spectrogram_jpg_files_for_next_model_run_or_model_test(False)

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
             
            # Need to check that the user didn't enter a probability without selecting the greater or lessor filter
            if (self.predicted_probability_filter.get() == 'not_used'):
                print('self.predicted_probability_filter_value.get() ', self.predicted_probability_filter_value.get())
                if self.predicted_probability_filter_value.get():
                    showinfo("Select Probability Sign", "Either clear the probability value, or select a probability radio button")
                    return
    
            print('self.actual_confirmed_other ', self.actual_confirmed_other.get())
            print('self.predicted_other ', self.predicted_other.get())
            
            self.run_results = functions.get_model_run_results(self.run_names_combo.get(), self.actual_confirmed_filter.get(), self.predicted_filter.get(), self.predicted_probability_filter.get(), self.predicted_probability_filter_value.get(), self.location_filter_combo.get(), self.actual_confirmed_other.get(), self.predicted_other.get(), self.used_to_create_model_filter.get(), self.recording_id_filter_value.get())
                                       
            number_of_results_returned = len(self.run_results)
            print('number_of_results_returned ', number_of_results_returned)
            self.number_of_results_label_value.set("Number of results: " + str(number_of_results_returned))
            if number_of_results_returned > 0:
                first_result = self.run_results[0]
                self.current_model_run_name_ID = first_result[0]
                print('self.current_model_run_name_ID ', self.current_model_run_name_ID) 
                self.current_model_run_result_array_pos = 0                    
                load_current_model_run_result()

        def next_run_result():
          
            if self.current_model_run_result_array_pos < (len(self.run_results)) -1:
                self.current_model_run_result_array_pos +=1
                print('current_model_run_result_array_pos ', self.current_model_run_result_array_pos)
                self.current_model_run_name_ID = self.run_results[self.current_model_run_result_array_pos][0]
                load_current_model_run_result()
             
        def previous_run_result():
            if self.current_model_run_result_array_pos > 0:
                self.current_model_run_result_array_pos -=1
                print('current_model_run_result_array_pos ', self.current_model_run_result_array_pos)
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
            
            self.current_model_run_name_start_time = self.run_result[2]
            self.start_time.set(self.current_model_run_name_start_time)
            
            self.current_model_run_name_duration = self.run_result[3]
            self.current_model_run_name_duration = 0.7 # The original length of 1.5 is too long for a morepork  
        
            self.current_model_run_name_predicted = self.run_result[5]             
            self.current_model_run_name_actual_confirmed = self.run_result[6] 

            if self.run_result[7]:
                self.current_model_run_name_probability = "{0:.2f}".format(self.run_result[7])
            else:
                self.current_model_run_name_probability = '?'
            
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
            elif self.current_model_run_name_actual_confirmed == 'water':
                self.actual_confirmed.set('water')
                
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
            elif self.current_model_run_name_actual_confirmed == 'frog':
                self.actual_confirmed.set('frog') 
            elif self.current_model_run_name_actual_confirmed == 'chainsaw':
                self.actual_confirmed.set('chainsaw') 
            elif self.current_model_run_name_actual_confirmed == 'crackle':
                self.actual_confirmed.set('crackle')
            elif self.current_model_run_name_actual_confirmed == 'car_horn':
                self.actual_confirmed.set('car_horn')
            elif self.current_model_run_name_actual_confirmed == 'fire_work':
                self.actual_confirmed.set('fire_work')
            elif self.current_model_run_name_actual_confirmed == 'maybe_morepork_more-pork':
                self.actual_confirmed.set('maybe_morepork_more-pork')
            elif self.current_model_run_name_actual_confirmed == 'music':
                self.actual_confirmed.set('music')
            else:
                self.actual_confirmed.set('not_set')   

            self.predicted_label_value.set(self.current_model_run_name_predicted + ' with ' + self.current_model_run_name_probability + ' probability')
            
            threading.Thread(target=play_clip(), args=(1,)).start()
            threading.Thread(target=display_images(), args=(1,)).start()
            
class ModelAccuracyAnalysisPage(tk.Frame):    
    
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.current_model_run_result_array_pos = 0
        self.current_model_run_name_ID = 0        
        
        self.unique_model_run_names = functions.get_unique_model_run_names()  
        self.unique_locations = functions.get_unique_locations('recordings')            
                    
        title_label = ttk.Label(self, text="Analyse Model Accuracy", font=LARGE_FONT)
        title_label.grid(column=0, columnspan=1, row=5)
        
        refresh_model_run_names_button = ttk.Button(self, text="Refresh Unique Model Run Names",command=lambda: refresh_unique_model_run_names())
        refresh_model_run_names_button.grid(column=0, columnspan=1, row=10) 
        
        run_names_label = ttk.Label(self, text="Model Run Names")
        run_names_label.grid(column=1, columnspan=1, row=10)      
                                    
        self.run_name = StringVar()
        self.run_names_combo = ttk.Combobox(self, textvariable=self.run_name, values=self.unique_model_run_names)
        
        
        if len(self.unique_model_run_names) > 0:
            self.run_names_combo.current(0)
            self.run_names_combo.grid(column=1, columnspan=1,row=11) 
            self.run_names_combo.current(len(self.unique_model_run_names) - 1)   
            
#         select_arff_file_label = ttk.Label(self, text="Select the arff file that was used to create this model.")
#         select_arff_file_label.grid(column=0, columnspan=1, row=15)   
#         
#         select_arff_file_label = ttk.Label(self, text="Important - the arff file is probably in the previous model run folder to the model run result that you are updating!")
#         select_arff_file_label.grid(column=0, columnspan=1, row=16)      
        
        select_csv_instructions_text = """
        In order to assess if the model is correctly predicting onsets/sounds that were NOT used to create the model,
        import the csv file that was created at the same time that the arff file for the model was created.
        
        This csv file should be called csv_file_for_keeping_track_of_onsets_used_to_create_model.csv and is probably in 
        the previous model run folder to the model run result that you are updating!
        
       """        
        
        select_csv_instructions_text_label = ttk.Label(self, text=select_csv_instructions_text)                                                   
        select_csv_instructions_text_label.grid(column=0, columnspan=1, row=15)  
            
        select_csvf_file_used_to_create_model_button = ttk.Button(self, text="Select csv file",command=lambda: select_csv_file_used_to_create_model())
        select_csvf_file_used_to_create_model_button.grid(column=0, columnspan=1, row=17)   
                    
        update_model_run_results_with_was_used_to_create_model_button = ttk.Button(self, text="Update model run results with onsets used to create model",command=lambda: update_model_run_results_with_onsets_used_to_create_model())
        update_model_run_results_with_was_used_to_create_model_button.grid(column=0, columnspan=1, row=20) 
        
        select_arff_file_label = ttk.Label(self, text="After you have used the Evaluate Model Run Results page to confirm (or otherwise) a few hundred predictions, \nyou can use them to perform an independent test of the model.\nFirst press the \'Create Spectrograms for testing model\' button then the \'Create arff file for testing model\' button.  \nThe images will be created in the  " + parameters.spectrograms_for_model_testing_folder + " folder of this model run, and the arff file will \nbe created as " + spectrograms_for_model_testing_folder)
        select_arff_file_label.grid(column=0, columnspan=1, row=25) 
        
        create_spectrograms_button = ttk.Button(self, text="Create Spectrograms for testing model", command=lambda: functions.create_spectrogram_jpg_files_for_next_model_run_or_model_test(True))
        create_spectrograms_button.grid(column=0, columnspan=1, row=26)
        
        create_test_arff_file_button = ttk.Button(self, text="Create arff file for testing model",command=lambda: functions.create_arff_file_for_weka_image_filter_input(True))
        create_test_arff_file_button.grid(column=0, columnspan=1, row=27)
        
        weka_testing_instructions_text = """\n
        We need two separate arff files to do the testing: 1) The arff file (that has was saved as \n
        arff_file_for_weka_model_creation_image_filtered_no_filename.arff that you used to create the model \n
        and 2) the arff_file_for_weka_model_testing.arff file for the test data.  First, in the Weka Preprocess \n
        tab, you will need to process this arff file by applying the image EdgeHistogramFilter and also remove the \n
        filename attribute (just like you did for the training arff file). Save the test arff file as \n
        arff_file_for_weka_model_testing_image_filtered_no_filename.arff. \n\n
        
        Still in the Preprocess tab, repeat the steps that you previously did to train the model \n
        (you should have saved the result buffer from when you created the model, which will have the details) \n
        - we need to create the model again - but this time, \n
        in the Classify tab, do not use Cross-validation, but use the \'Supplied test set option\', and choose the newly created \n
        \'arff_file_for_weka_model_testing_image_filtered_no_filename.arff\' file. \n          
        Press Close and then press the \'Start\' button.\n\n
        See the video Data Mining with Weka (2.2: Training and testing) for help.\n\n"""
        
        
        weka_testing_instructions_label = ttk.Label(self, text=weka_testing_instructions_text)
                                                   
        weka_testing_instructions_label.grid(column=0, columnspan=1, row=30) 
        
        back_to_home_button = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(HomePage))
        back_to_home_button.grid(column=0, columnspan=1, row=35) 
            
        def refresh_unique_model_run_names():
                self.unique_model_run_names = functions.get_unique_model_run_names()
                self.run_names_combo['values'] = self.unique_model_run_names  
                
        def select_csv_file_used_to_create_model():
#             print(initial_locatation_for_choosing_arff_file_dialog)            
            self.arff_filename = filedialog.askopenfilename(initialdir = initial_locatation_for_choosing_arff_file_dialog,title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
            
                
        def update_model_run_results_with_onsets_used_to_create_model():               
                functions.update_model_run_results_with_onsets_used_to_create_model(self.run_names_combo.get(), self.arff_filename)
                 
        
class CreateTagsOnCacophonyServerFromModelRunPage(tk.Frame):  
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.unique_locations = functions.get_unique_locations('tags')
        self.current_onset_array_pos = 0
                     
        title_label = ttk.Label(self, text="Create Tags On Cacophony Server using the latest model_run_result predictions.", font=LARGE_FONT)
        title_label.grid(column=0, columnspan=1, row=0) 
        
        msg1_instructions = "The Model version is currently set to: " + str(parameters.model_version) + " Before you continue, you should change this in the parameters file, so that it is the same as the actual model version that created the model_run_results. "
        msg1 = tk.Message(self, text = msg1_instructions)
        msg1.config(width=600)
        msg1.grid(column=0, columnspan=1, row=1) 
        
        msg2_instructions = "The model_run_result is currently set to: " + parameters.model_run_name + " Before you continue, you should change this in the parameters file, so that it uses the correct (latest?) model_run_results. "
        msg2 = tk.Message(self, text = msg2_instructions)
        msg2.config(width=600)
        msg2.grid(column=0, columnspan=1, row=2)
        
        msg3_instructions = "The probability / confidence level cutoff (probability_cutoff_for_tag_creation in the parameters file) is currently set to: " + str(parameters.probability_cutoff_for_tag_creation) + " Only tags that have a confidence equal or greater than this will be created.  Also, if the predicted tag (onset) location has been confirmed by a human to NOT be a morepork, then no tag will be created.  This means that for locations that have had a lot of checking the quality of the tags will be higher than the model predicts - and better than for locations that haven't been checked as much."
        msg3 = tk.Message(self, text = msg3_instructions)
        msg3.config(width=600)
        msg3.grid(column=0, columnspan=1, row=3)
                
        msg4_instructions = "You will need to close and reopen this program to refresh those parameters."
        msg4 = tk.Message(self, text = msg4_instructions)
        msg4.config(width=600)
        msg4.grid(column=0, columnspan=1, row=4)
        
        msg5_instructions = "Press the 'Create Local Tags' button to create tags in the local database only."
        msg5 = tk.Message(self, text = msg5_instructions)
        msg5.config(width=600)
        msg5.grid(column=0, columnspan=1, row=5) 
        
        create_local_tags_button = ttk.Button(self, text="Create Local Tags",command=lambda: functions.create_local_tags_from_model_run_result())
        create_local_tags_button.grid(column=1, columnspan=1, row=6)   
        
        msg6_instructions = "Check that the tags have been created in the tags table of the local database.  You can filter on version column using the model version of " + str(parameters.model_version)
        msg6 = tk.Message(self, text = msg6_instructions)
        msg6.config(width=600)
        msg6.grid(column=0, columnspan=1, row=7)
        
        msg7_instructions = "When you are sure that these are DEFINATELY the tags you want to create on the Cacophony Server press the 'Upload Tags To Cacophony Server' button."
        msg7 = tk.Message(self, text = msg7_instructions)
        msg7.config(width=600)
        msg7.grid(column=0, columnspan=1, row=50)
        
        location_filter_label = ttk.Label(self, text="Location Filter")
        location_filter_label.grid(column=1, columnspan=1, row=50)      
                                    
        self.location_filter = StringVar()
        self.location_filter_combo = ttk.Combobox(self, textvariable=self.location_filter, values=self.unique_locations)
        
        if len(self.unique_locations) > 0:
            self.location_filter_combo.current(0)
            self.location_filter_combo.grid(column=1, columnspan=1,row=51) 
        
        upload_tags_button = ttk.Button(self, text="Upload Tags To Cacophony Server",command=lambda: functions.upload_tags_to_cacophony_server(self.location_filter_combo.get()))
        upload_tags_button.grid(column=2, columnspan=1, row=51)
        
        msg7_instructions = "Or you can upload all the tags in one go i.e. all tags for all locations."
        msg7 = tk.Message(self, text = msg7_instructions)
        msg7.config(width=600)
        msg7.grid(column=0, columnspan=1, row=60)
        
        upload_All_tags_button = ttk.Button(self, text="Upload Tags For ALL locations To Cacophony Server",command=lambda: functions.upload_tags_for_all_locations_to_cacophony_server())
        upload_All_tags_button.grid(column=1, columnspan=1, row=60)
        
        back_to_home_button = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(HomePage))
        back_to_home_button.grid(column=0, columnspan=1, row=70) 
        
        
class CreateTestDataPage(tk.Frame):   
   
        
    def leftMousePressedcallback(self, event):
    
        self.x_scroll_bar_minimum = self.scroll_x.get()[0]   
        self.x_scroll_bar_maximum = self.scroll_x.get()[1]                     

        self.x_rectangle_start_position_percent = functions.spectrogram_clicked_at_x_percent(event.x, self.x_scroll_bar_minimum, self.x_scroll_bar_maximum, int(self.canvas.cget("width")))        
        self.y_rectangle_start_position_percent = functions.get_spectrogram_clicked_at_y_percent(event.y, self.spectrogram_image.height())  
            
        duration = self.recordings[self.current_recordings_index][3]
       
        self.x_rectangle_start_position_seconds = functions.get_recording_position_in_seconds(event.x, self.x_scroll_bar_minimum, self.x_scroll_bar_maximum, int(self.canvas.cget("width")), duration)        

        self.y_rectangle_start_position_hertz = functions.get_recording_position_in_hertz(event.y, self.spectrogram_image.height(), int(self.min_freq.get()), int(self.max_freq.get()))  
   

    def on_move_press(self, event):
        if self.temp_rectangle is not None:
            self.canvas.delete(self.temp_rectangle)
        
        self.x_rectangle_finish_position_percent = functions.spectrogram_clicked_at_x_percent(event.x, self.x_scroll_bar_minimum, self.x_scroll_bar_maximum, int(self.canvas.cget("width")))
        self.y_rectangle_finish_position_percent = functions.get_spectrogram_clicked_at_y_percent(event.y, self.spectrogram_image.height())     
        
        
        if not self.actual_confirmed.get():
            # The 'what' radio button hasn't been selected 
            return         

        rectangle_bbox_x1 = functions.convert_x_or_y_postion_percent_to_x_or_y_spectrogram_image_postion(self.spectrogram_image.width(), self.x_rectangle_start_position_percent)
        rectangle_bbox_y1 = functions.convert_x_or_y_postion_percent_to_x_or_y_spectrogram_image_postion(self.spectrogram_image.height(), self.y_rectangle_start_position_percent)
        
        rectangle_bbox_x2 = functions.convert_x_or_y_postion_percent_to_x_or_y_spectrogram_image_postion(self.spectrogram_image.width(), self.x_rectangle_finish_position_percent)
        rectangle_bbox_y2 = functions.convert_x_or_y_postion_percent_to_x_or_y_spectrogram_image_postion(self.spectrogram_image.height(), self.y_rectangle_finish_position_percent)

        self.temp_rectangle = self.canvas.create_rectangle(rectangle_bbox_x1, rectangle_bbox_y1, rectangle_bbox_x2, rectangle_bbox_y2 )
        
        
        
    def leftMouseReleasedcallback(self, event):
        duration = self.recordings[self.current_recordings_index][3]

        self.x_rectangle_finish_position_seconds = functions.get_recording_position_in_seconds(event.x, self.x_scroll_bar_minimum, self.x_scroll_bar_maximum, int(self.canvas.cget("width")), duration)
        self.y_rectangle_finish_position_hertz = functions.get_recording_position_in_hertz(event.y, self.spectrogram_image.height(), int(self.min_freq.get()), int(self.max_freq.get()))
                  
        if self.y_rectangle_start_position_hertz > self.y_rectangle_finish_position_hertz:
            upper_freq_hertz = self.y_rectangle_start_position_hertz
            lower_freq_hertz = self.y_rectangle_finish_position_hertz
        else:
            upper_freq_hertz = self.y_rectangle_finish_position_hertz
            lower_freq_hertz = self.y_rectangle_start_position_hertz
            
        if self.x_rectangle_start_position_seconds <  self.x_rectangle_finish_position_seconds:
            start_position_seconds = self.x_rectangle_start_position_seconds
            finish_position_seconds = self.x_rectangle_finish_position_seconds
        else:
            finish_position_seconds = self.x_rectangle_start_position_seconds
            start_position_seconds = self.x_rectangle_finish_position_seconds    
        
        if abs(finish_position_seconds - start_position_seconds) < 0.1:
            self.play_clip(start_position_seconds)
            return
        
        if not self.actual_confirmed.get():
            # The 'what' radio button hasn't been selected               
            messagebox.showinfo("Oops", "You haven't selected an Actual Confirmed radio button")
            return 
              
        # Create another rectangle and delete the temp_rectangle.  Had to do this to stop on_move_mouse deleting the previous finished rectangle
        if self.temp_rectangle is not None:           

            recording_id = self.recordings[self.current_recordings_index][0]           

            rectangle_bbox_x1 = functions.convert_x_or_y_postion_percent_to_x_or_y_spectrogram_image_postion(self.spectrogram_image.width(), self.x_rectangle_start_position_percent)
            rectangle_bbox_y1 = functions.convert_x_or_y_postion_percent_to_x_or_y_spectrogram_image_postion(self.spectrogram_image.height(), self.y_rectangle_start_position_percent)
            
            rectangle_bbox_x2 = functions.convert_x_or_y_postion_percent_to_x_or_y_spectrogram_image_postion(self.spectrogram_image.width(), self.x_rectangle_finish_position_percent)
            rectangle_bbox_y2 = functions.convert_x_or_y_postion_percent_to_x_or_y_spectrogram_image_postion(self.spectrogram_image.height(), self.y_rectangle_finish_position_percent)
            
            what = self.actual_confirmed.get()
            
            fill_colour = functions.get_spectrogram_rectangle_selection_colour(what)
            
            aRectangle_id = self.canvas.create_rectangle(rectangle_bbox_x1, rectangle_bbox_y1,rectangle_bbox_x2, rectangle_bbox_y2, fill=fill_colour, stipple="gray12" )
        
            self.canvas.delete(self.temp_rectangle) 
            self.canvas.itemconfig(aRectangle_id, tags=(str(recording_id), str(start_position_seconds), str(finish_position_seconds), str(lower_freq_hertz), str(upper_freq_hertz) , self.actual_confirmed.get()))
                                  
            result = functions.insert_test_data_into_database(recording_id, start_position_seconds, finish_position_seconds, lower_freq_hertz, upper_freq_hertz, self.actual_confirmed.get())
            if not result:                
                messagebox.showinfo("Oops", "Could not update database - is it locked?")   
                self.canvas.delete(aRectangle_id) 

    def rightMousePressedcallback(self, event):        
      
        selected_item_id = event.widget.find_withtag('current')[0]        

        item_type = self.canvas.type(CURRENT) # https://stackoverflow.com/questions/38982313/python-tkinter-identify-object-on-click
        if item_type != "image":
            # Deleted it from the database
                       
            tags_from_item = self.canvas.gettags(selected_item_id)
                
            recording_id = tags_from_item[0]
            start_time_seconds = tags_from_item[1]
            finish_time_seconds = tags_from_item[2]
            lower_freq_hertz = tags_from_item[3]
            upper_freq_hertz = tags_from_item[4]
            what = tags_from_item[5]                      

            functions.delete_test_data_row(recording_id, start_time_seconds, finish_time_seconds, lower_freq_hertz, upper_freq_hertz, what)
                            
            # Now delete it from the canvas
            self.canvas.delete(selected_item_id)       
        

    def retrieve_test_data_from_database_and_add_rectangles_to_image(self):  
              
        recording_id = self.recordings[self.current_recordings_index][0]
        duration = self.recordings[self.current_recordings_index][3]
        test_data_rectangles = functions.retrieve_test_data_from_database(recording_id)     
                          
        for test_data_rectangle in test_data_rectangles:
            recording_id = test_data_rectangle[0]
            start_time_seconds = test_data_rectangle[1]
            finish_time_seconds = test_data_rectangle[2]
            lower_freq_hertz = test_data_rectangle[3]
            upper_freq_hertz = test_data_rectangle[4]
            what = test_data_rectangle[5]            

            rectangle_bbox_x1 = functions.convert_time_in_seconds_to_x_value_for_canvas_create_method(start_time_seconds, duration, self.spectrogram_image.width())
            rectangle_bbox_y1 = functions.convert_frequency_to_y_value_for_canvas_create_method(int(self.min_freq.get()), int(self.max_freq.get()), lower_freq_hertz, self.spectrogram_image.height())  
            rectangle_bbox_x2 = functions.convert_time_in_seconds_to_x_value_for_canvas_create_method(finish_time_seconds, duration, self.spectrogram_image.width())
            rectangle_bbox_y2 = functions.convert_frequency_to_y_value_for_canvas_create_method(int(self.min_freq.get()), int(self.max_freq.get()), upper_freq_hertz, self.spectrogram_image.height())
            
            fill_colour = functions.get_spectrogram_rectangle_selection_colour(what)
           
            aRectangle_id = self.canvas.create_rectangle(rectangle_bbox_x1,rectangle_bbox_y1,rectangle_bbox_x2, rectangle_bbox_y2,fill=fill_colour, stipple="gray12")         
            
            # Attach details of test_data to the rectangles (so can 'look' at it one day - with mouse hover?)
            self.canvas.itemconfig(aRectangle_id, tags=(str(recording_id), str(start_time_seconds), str(finish_time_seconds), str(lower_freq_hertz), str(upper_freq_hertz) , what))
            
    def draw_horizontal_frequency_reference_line(self):
        ref_line_canvas_value = functions.convert_frequency_to_y_value_for_canvas_create_method(int(self.min_freq.get()), int(self.max_freq.get()), int(self.horizonal_ref_line_freq.get()), self.spectrogram_image.height())  
        ref_line_id = self.canvas.create_line(0,ref_line_canvas_value,self.spectrogram_image.width(),ref_line_canvas_value, fill='blue')
    
    
    def retrieve_recordings_for_creating_test_data(self,what_filter):
        if what_filter is None:
            self.config(bg="red")
        else:
            self.config(bg="light grey")
        
        self.recordings = functions.retrieve_recordings_for_creating_test_data(what_filter)  


    def reload_recordings_for_creating_test_data(self,what_filter):
        self.retrieve_recordings_for_creating_test_data(what_filter)
        self.change_spectrogram()        
        
        
    def display_spectrogram(self):
        recording_id = self.recordings[self.current_recordings_index][0]
        recording_device_super_name = self.recordings[self.current_recordings_index][4]

        self.spectrogram_image = functions.get_single_create_focused_mel_spectrogram_for_creating_test_data(str(recording_id), int(self.min_freq.get()), int(self.max_freq.get()))
        
        self.image = self.canvas.create_image(0, 0, image=self.spectrogram_image, anchor=NW)   
        self.canvas.configure(height=self.spectrogram_image.height())             
       
        self.canvas.grid(row=20, rowspan = 50, columnspan=20, column=0)
        
        self.scroll_x = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.scroll_x.grid(row=71, columnspan=20, column=0, sticky="ew")        
      
        self.canvas.configure(xscrollcommand=self.scroll_x.set)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
              
        self.canvas.bind("<Button-1>", self.leftMousePressedcallback)        
        self.canvas.bind("<ButtonRelease-1>", self.leftMouseReleasedcallback) 
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        
        self.canvas.bind("<Button-3>", self.rightMousePressedcallback) 
        
        self.retrieve_test_data_from_database_and_add_rectangles_to_image()    
        
        self.draw_horizontal_frequency_reference_line()   
        
        self.recording_id_and_result_place_value2.set("Recording Id: " + str(recording_id) + " at location " + recording_device_super_name) 
        self.recording_index_out_of_total_of_recordings_value.set("Result " + str(self.current_recordings_index) + " of "   + str(len(self.recordings)) + " recordings")                           
            
    def previous_recording(self):
        if self.current_recordings_index > 0:
            self.current_recordings_index = self.current_recordings_index -1
            self.change_spectrogram()        
           
    def next_recording(self):
        if self.current_recordings_index < (len(self.recordings) - 2): 
            self.current_recordings_index = self.current_recordings_index + 1
            self.change_spectrogram() 
            
    def next_recording_and_mark_as_analysed(self):
        recording_id = self.recordings[self.current_recordings_index][0]
        what = self.marked_as_what.get()
        result = functions.mark_recording_as_analysed(recording_id, what)
        if result:
            self.next_recording()
        else:
            messagebox.showinfo("Oops", "Could not update database - is it locked?")
                    
        
    def change_spectrogram(self):
        self.stop_clip()
        recording_id = self.recordings[self.current_recordings_index][0]
        recording_device_super_name = self.recordings[self.current_recordings_index][4]
#         self.spectrogram_image = functions.get_single_create_focused_mel_spectrogram_for_creating_test_data(str(recording_id)) 
        self.spectrogram_image = functions.get_single_create_focused_mel_spectrogram_for_creating_test_data(str(recording_id), int(self.min_freq.get()), int(self.max_freq.get()))  
        self.canvas.configure(height=self.spectrogram_image.height())  
        self.image = self.canvas.create_image(0, 0, image=self.spectrogram_image, anchor=NW)  
                             

        self.retrieve_test_data_from_database_and_add_rectangles_to_image()  
        self.draw_horizontal_frequency_reference_line()   
                
#         self.recording_id_and_result_place_value2.set("Recording Id: " + str(recording_id))
        self.recording_id_and_result_place_value2.set("Recording Id: " + str(recording_id) + " at location " + recording_device_super_name)  
        self.recording_index_out_of_total_of_recordings_value.set("Result " + str(self.current_recordings_index) + " of "   + str(len(self.recordings)) + " recordings")
        
        if self.auto_play.get():
            self.play_clip(0)           
                
    def confirm_actual(self):  
       
        print('self.actual_confirmed.get() ', self.actual_confirmed.get()) 
        # Set the what box - used to enter row in test_data_recording_analysis table     
        self.marked_as_what.set(self.actual_confirmed.get())
            
        
    def play_clip(self,start_position_seconds):
        
        # Stop any clip that is currently playing
        functions.stop_clip()        
               
        self.canvas.delete("audio_position_line") # otherwise can have multiple lines on the spectrogram
        
        duration = self.recordings[self.current_recordings_index][3]
 
        x_canvas_pos = functions.convert_pos_in_seconds_to_canvas_position(self.spectrogram_image.width(), start_position_seconds, duration)  
       
        self.aLine_id = self.canvas.create_line(x_canvas_pos, 0,x_canvas_pos, self.spectrogram_image.height(), fill='red', tags = "audio_position_line")
        # Now play the clip
       
        functions.play_clip(str(self.recordings[self.current_recordings_index][0]), start_position_seconds,duration, self.play_filtered.get())
        
        # https://www.youtube.com/watch?v=f8sKAot-15w
        # Need to calculate the speed to move the line, how many pixels per second
        speed = self.spectrogram_image.width()/duration/20 #  # Will update every 0.1 seconds

        self.playing = True 
        while self.playing:
            self.canvas.move(self.aLine_id,speed,0)
            self.update()
#             time.sleep(0.05)
#             time.sleep(0.0499) # line was moving fractionally slow
#             time.sleep(0.049) # line was moving fractionally slow
            time.sleep(0.0495) # line was moving fractionally slow
        
    def stop_clip(self):
        self.playing = False 
        functions.stop_clip()    
        
    def load_specific_recording_from_creating_test_data(self):
        recording_to_load_id = int(self.specific_recording_id.get())
        print(recording_to_load_id)
        
        # find the index of the recording with this recording_id
        length = len(self.recordings)
        for i in range(length):
            recording_id = int(self.recordings[i][0])
            if recording_id == recording_to_load_id:
                self.current_recordings_index = i
                # Now load this recording
                self.change_spectrogram()
                return
            
        # If it gets here then it didn't find the recording so display a message
        messagebox.showinfo("Oops", "That recording id is not in the available test recordings")
        
        
                
    def load_specific_recording_by_result_index(self):  
        self.current_recordings_index = int(self.specific_recording_index.get())
        self.change_spectrogram()
        # Now change 
        
    
    def __init__(self, parent, controller):
        # https://stackoverflow.com/questions/7727804/tkinter-using-scrollbars-on-a-canvas
        # https://stackoverflow.com/questions/43731784/tkinter-canvas-scrollbar-with-grid
        # https://riptutorial.com/tkinter/example/27784/scrolling-a-canvas-widget-horizontally-and-vertically
                              
        tk.Frame.__init__(self, parent)    
        
        self.playing = False
            
        self.temp_rectangle = None
        self.current_recordings_index = 0
        
        title_label = ttk.Label(self, text="Create Test Data", font=LARGE_FONT)
        title_label.grid(column=0, columnspan=1, row=0) 
        
        msg1_instructions = "Use this page to create test data."
        msg1 = tk.Message(self, text = msg1_instructions)
        msg1.config(width=600)
        msg1.grid(column=0, columnspan=1, row=1)     
        
        min_freq_label = ttk.Label(self, text="Enter the minimum frequency (Hz)")
        min_freq_label.grid(column=1, columnspan=1, row=0)
             
        self.min_freq = StringVar(value='700')
        min_freq_entry = tk.Entry(self,  textvariable=self.min_freq, width=30)
        min_freq_entry.grid(column=1, columnspan=1, row=1)        
        
        max_freq_label = ttk.Label(self, text="Enter the maximum frequency (Hz)")
        max_freq_label.grid(column=2, columnspan=1, row=0)
             
        self.max_freq = StringVar(value='1100')
        max_freq_entry = tk.Entry(self,  textvariable=self.max_freq, width=30)
        max_freq_entry.grid(column=2, columnspan=1, row=1)
        
        horizonal_ref_line_freq_label = ttk.Label(self, text="Enter the frequency (Hz) of the horizontal reference line")
        horizonal_ref_line_freq_label.grid(column=3, columnspan=1, row=0)
        
        self.horizonal_ref_line_freq = StringVar(value='900')      
        horizonal_ref_line_freq_entry = tk.Entry(self,  textvariable=self.horizonal_ref_line_freq, width=30)
        horizonal_ref_line_freq_entry.grid(column=3, columnspan=1, row=1)  
        
        self.canvas = tk.Canvas(self, width=10, height=10)
#         self.canvas = tk.Canvas(self, width=20, height=10)    

#         self.canvas.config(height=test_data_canvas_width)
#         self.canvas.config(width=test_data_canvas_height)
        
        self.canvas.config(height=test_data_canvas_height)
        self.canvas.config(width=test_data_canvas_width)
        
        self.specific_recording_id = StringVar(value='544235')   
        specific_recording_id_entry = tk.Entry(self,  textvariable=self.specific_recording_id, width=30)
        specific_recording_id_entry.grid(column=4, columnspan=1, row=0)        
        
        retrieve_specific_recording_id_button = ttk.Button(self, text="Retrieve this recording (has to be in test_data)", command=lambda: self.load_specific_recording_from_creating_test_data())
        retrieve_specific_recording_id_button.grid(column=4, columnspan=1, row=1)          

        self.specific_recording_index = StringVar(value='0')      
        specific_recording_index_entry = tk.Entry(self,  textvariable=self.specific_recording_index, width=30)
        specific_recording_index_entry.grid(column=5, columnspan=1, row=0)        
        
        retrieve_specific_recording_index_button = ttk.Button(self, text="Retrieve this recording (result index)", command=lambda: self.load_specific_recording_by_result_index())
        retrieve_specific_recording_index_button.grid(column=5, columnspan=1, row=1, rowspan=1)   
        
        self.recording_id_and_result_place_value2 = tk.StringVar()
        recording_id_label = ttk.Label(self, textvariable=self.recording_id_and_result_place_value2) 
        recording_id_label.grid(column=6, columnspan=1, row=0) 
        self.recording_id_and_result_place_value2.set("Recording Id") 
       
        self.retrieve_recordings_for_creating_test_data("morepork_more-pork")


       
        first_not_yet_analysed_recording_button = ttk.Button(self, text="First Recording - not yet analysed", command=lambda: self.reload_recordings_for_creating_test_data(self.marked_as_what.get())) # https://effbot.org/tkinterbook/canvas.htm))
        first_not_yet_analysed_recording_button.grid(column=0, columnspan=1, row=100) 
        
        first_recording_button = ttk.Button(self, text="First Recording (includes already analysed)", command=lambda: self.reload_recordings_for_creating_test_data(None)) # https://effbot.org/tkinterbook/canvas.htm))
        first_recording_button.grid(column=0, columnspan=1, row=110) 
                       
        previous_recording_button = ttk.Button(self, text="Previous Recording", command=lambda: self.previous_recording()) # https://effbot.org/tkinterbook/canvas.htm))
        previous_recording_button.grid(column=1, columnspan=1, row=100) 
        
        play_button = ttk.Button(self, text="Play Recording", command=lambda: self.play_clip(0))
        play_button.grid(column=2, columnspan=1, row=100)        
        
        # https://effbot.org/tkinterbook/checkbutton.htm
        self.play_filtered = BooleanVar()
        play_filtered_Checkbuttton = Checkbutton(self, text="Apply Filter to Playback", variable=self.play_filtered)
        play_filtered_Checkbuttton.grid(column=2, columnspan=1, row=110)
        
        play_button = ttk.Button(self, text="Stop Playing", command=lambda: self.stop_clip())
        play_button.grid(column=3, columnspan=1, row=100)
        
        self.recording_index_out_of_total_of_recordings_value = tk.StringVar()
        recording_index_label = ttk.Label(self, textvariable=self.recording_index_out_of_total_of_recordings_value) 
        recording_index_label.grid(column=3, columnspan=1, row=110) 
        self.recording_index_out_of_total_of_recordings_value.set("Result ") 
                 
        next_recording_button = ttk.Button(self, text="Next Recording (Do NOT mark as Analysed)", command=lambda: self.next_recording()) # https://effbot.org/tkinterbook/canvas.htm))
        next_recording_button.grid(column=4, columnspan=1, row=100)   
        
        self.marked_as_what = StringVar(value='morepork_more-pork')      
        marked_as_what_entry = tk.Entry(self,  textvariable=self.marked_as_what, width=30)
        marked_as_what_entry.grid(column=5, columnspan=1, row=100)   
        
        # Note I used a different button type for this button so I could change the background colour
        next_recording_button = tk.Button(self, text="Next Recording (Mark as Analysed)", bg='green', command=lambda: self.next_recording_and_mark_as_analysed()) # https://effbot.org/tkinterbook/canvas.htm))
        next_recording_button.grid(column=5, columnspan=1, row=110)  
        
        self.auto_play = BooleanVar()
        auto_play_Checkbuttton = Checkbutton(self, text="Automatically play", variable=self.auto_play)
        auto_play_Checkbuttton.grid(column=6, columnspan=1, row=100)  
        
#         self.recording_id_and_result_place_value2 = tk.StringVar()
#         recording_id_label = ttk.Label(self, textvariable=self.recording_id_and_result_place_value2) 
#         recording_id_label.grid(column=0, columnspan=1, row=200) 
#         self.recording_id_and_result_place_value2.set("Recording Id") 
                
        # Add the radio buttons for selecting what the noise is
        
        actual_label_confirmed = ttk.Label(self, text="SET Actual Confirmed", font=LARGE_FONT)
        actual_label_confirmed.grid(column=0, columnspan=1, row=201)
              
        self.actual_confirmed = tk.StringVar()

        actual_confirmed_radio_button_morepork_classic = ttk.Radiobutton(self,text='Morepork more-pork', variable=self.actual_confirmed, value='morepork_more-pork',command=lambda: self.confirm_actual())
        actual_confirmed_radio_button_morepork_classic.grid(column=0, columnspan=1, row=202)               
        
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Unknown', variable=self.actual_confirmed, value='unknown',command=lambda: self.confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=1, columnspan=1, row=202)
        actual_confirmed_radio_button_dove = ttk.Radiobutton(self,text='Dove', variable=self.actual_confirmed, value='dove',command=lambda: self.confirm_actual())
        actual_confirmed_radio_button_dove.grid(column=2, columnspan=1, row=202)   
        actual_confirmed_radio_button_duck = ttk.Radiobutton(self,text='Duck', variable=self.actual_confirmed, value='duck',command=lambda: self.confirm_actual())
        actual_confirmed_radio_button_duck.grid(column=3, columnspan=1, row=202) 
        actual_confirmed_radio_button_dog = ttk.Radiobutton(self,text='Dog', variable=self.actual_confirmed, value='dog',command=lambda: self.confirm_actual())
        actual_confirmed_radio_button_dog.grid(column=4, columnspan=1, row=202) 
        actual_confirmed_radio_button_human = ttk.Radiobutton(self,text='Human', variable=self.actual_confirmed, value='human',command=lambda: self.confirm_actual())
        actual_confirmed_radio_button_human.grid(column=5, columnspan=1, row=202)   
        actual_confirmed_radio_button_siren = ttk.Radiobutton(self,text='Siren', variable=self.actual_confirmed, value='siren',command=lambda: self.confirm_actual())
        actual_confirmed_radio_button_siren.grid(column=6, columnspan=1, row=202)
        
        actual_confirmed_radio_button_bird = ttk.Radiobutton(self,text='Bird', variable=self.actual_confirmed, value='bird',command=lambda: self.confirm_actual())
        actual_confirmed_radio_button_bird.grid(column=0, columnspan=1, row=203) 
        actual_confirmed_radio_button_car = ttk.Radiobutton(self,text='Car', variable=self.actual_confirmed, value='car',command=lambda: self.confirm_actual())
        actual_confirmed_radio_button_car.grid(column=1, columnspan=1, row=203)
        actual_confirmed_radio_button_rumble = ttk.Radiobutton(self,text='Rumble', variable=self.actual_confirmed, value='rumble',command=lambda: self.confirm_actual())
        actual_confirmed_radio_button_rumble.grid(column=2, columnspan=1, row=203)
        actual_confirmed_radio_button_water = ttk.Radiobutton(self,text='Water', variable=self.actual_confirmed, value='water',command=lambda: self.confirm_actual())
        actual_confirmed_radio_button_water.grid(column=3, columnspan=1, row=203)
        actual_confirmed_radio_button_hand_saw = ttk.Radiobutton(self,text='Hand saw', variable=self.actual_confirmed, value='hand_saw',command=lambda: self.confirm_actual())
        actual_confirmed_radio_button_hand_saw.grid(column=4, columnspan=1, row=203) 
        actual_confirmed_radio_button_white_noise = ttk.Radiobutton(self,text='White noise', variable=self.actual_confirmed, value='white_noise',command=lambda: self.confirm_actual())
        actual_confirmed_radio_button_white_noise.grid(column=5, columnspan=1, row=203)
        actual_confirmed_radio_button_plane = ttk.Radiobutton(self,text='Plane', variable=self.actual_confirmed, value='plane',command=lambda: self.confirm_actual())
        actual_confirmed_radio_button_plane.grid(column=6, columnspan=1, row=203)
        
        actual_confirmed_radio_button_cow = ttk.Radiobutton(self,text='Cow', variable=self.actual_confirmed, value='cow',command=lambda: self.confirm_actual())
        actual_confirmed_radio_button_cow.grid(column=0, columnspan=1, row=204) 
        actual_confirmed_radio_button_buzzy_insect = ttk.Radiobutton(self,text='Buzzy insect', variable=self.actual_confirmed, value='buzzy_insect',command=lambda: self.confirm_actual())
        actual_confirmed_radio_button_buzzy_insect.grid(column=1, columnspan=1, row=204) 
        actual_confirmed_radio_morepork_more_pork_part = ttk.Radiobutton(self,text='Morepork more-pork Part', variable=self.actual_confirmed, value='morepork_more-pork_part',command=lambda: self.confirm_actual())
        actual_confirmed_radio_morepork_more_pork_part.grid(column=2, columnspan=1, row=204) 
        actual_confirmed_radio_button_hammering = ttk.Radiobutton(self,text='Hammering', variable=self.actual_confirmed, value='hammering',command=lambda: self.confirm_actual())
        actual_confirmed_radio_button_hammering.grid(column=3, columnspan=1, row=204)  
        actual_confirmed_radio_button_frog = ttk.Radiobutton(self,text='Frog', variable=self.actual_confirmed, value='frog',command=lambda: self.confirm_actual())
        actual_confirmed_radio_button_frog.grid(column=4, columnspan=1, row=204)
        actual_confirmed_radio_button_chainsaw = ttk.Radiobutton(self,text='Chainsaw', variable=self.actual_confirmed, value='chainsaw',command=lambda: self.confirm_actual())
        actual_confirmed_radio_button_chainsaw.grid(column=5, columnspan=1, row=204) 
        actual_confirmed_radio_button_crackle = ttk.Radiobutton(self,text='Crackle', variable=self.actual_confirmed, value='crackle',command=lambda: self.confirm_actual())
        actual_confirmed_radio_button_crackle.grid(column=6, columnspan=1, row=204)  
        
        actual_confirmed_radio_button_car_horn = ttk.Radiobutton(self,text='Car horn', variable=self.actual_confirmed, value='car_horn',command=lambda: self.confirm_actual())
        actual_confirmed_radio_button_car_horn.grid(column=0, columnspan=1, row=205)
        actual_confirmed_radio_button_fire_work = ttk.Radiobutton(self,text='Fire work', variable=self.actual_confirmed, value='fire_work',command=lambda: self.confirm_actual())
        actual_confirmed_radio_button_fire_work.grid(column=1, columnspan=1, row=205)
        actual_confirmed_radio_button_maybe_morepork_more_pork = ttk.Radiobutton(self,text='Maybe Morepork more-pork', variable=self.actual_confirmed, value='maybe_morepork_more-pork',command=lambda: self.confirm_actual())
        actual_confirmed_radio_button_maybe_morepork_more_pork.grid(column=2, columnspan=1, row=205)
        actual_confirmed_radio_button_music = ttk.Radiobutton(self,text='Music', variable=self.actual_confirmed, value='music',command=lambda: self.confirm_actual())
        actual_confirmed_radio_button_music.grid(column=3, columnspan=1, row=205)     
                                 
        back_to_home_button = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(HomePage))
        back_to_home_button.grid(column=0, columnspan=1, row=300) 
        
        self.display_spectrogram()

        
app = Main_GUI()
app.mainloop() 