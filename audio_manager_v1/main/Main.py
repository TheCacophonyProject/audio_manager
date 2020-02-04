'''
Created on 5 Sep 2019
Modified 17 12 2019a

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
from tkinter import filedialog


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
        
        for F in (HomePage, RecordingsPage, TaggingPage, CreateWekaModelPage, ClassifyOnsetsUsingWekaModelPage, CreateOnsetsPage, CreateSpectrogramsPage, CreateTagsFromOnsetsPage, EvaluateWekaModelRunResultPage, CreateTagsOnCacophonyServerFromModelRunPage, ModelAccuracyAnalysisPage):
      
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
        
        device_super_name_label = ttk.Label(self, text="Device Super name (e.g. Hammond_Park)")
        device_super_name_label.grid(column=0, columnspan=1, row=2)
        
        device_super_name = StringVar(value='Hammond_Park')
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
        msg1.grid(column=0, columnspan=1, row=1)  
        
        create_spectrograms_instructions = "Press the Create Spectrograms for Next Run button to create the spectrograms (from confirmed onsets) that will be used to train the next version/iteration of the model"
        create_spectrograms_msg = tk.Message(self, text = create_spectrograms_instructions)
        create_spectrograms_msg.config(width=600)
        create_spectrograms_msg.grid(column=0, columnspan=1, row=2)  
        
        create_spectrograms_button = ttk.Button(self, text="Create Spectrograms for Next Run", command=lambda: functions.create_spectrogram_jpg_files_for_next_model_run_or_model_test(False))
        create_spectrograms_button.grid(column=1, columnspan=1, row=2)
        
        create_arff_instructions = "Pressing the Create Arff file for Weka input button will put the names of the previously created spectrograms into an .arff file, that Weka will then use. You can find the file called " + arff_file_for_weka_model_creation + " in the " + model_run_name + " folder."
        create_arff_file_msg = tk.Message(self, text = create_arff_instructions)
        create_arff_file_msg.config(width=600)
        create_arff_file_msg.grid(column=0, columnspan=1, row=3)  
        
        create_arff_file_for_weka_button = ttk.Button(self, text="Create Arff file for Weka input", command=lambda: functions.create_arff_file_for_weka_image_filter_input(False))
        create_arff_file_for_weka_button.grid(column=1, columnspan=1, row=3)
        
        create_folders_instructions = "BEFORE pressing the next button, update the model_run_name parameter in the parameters file with a new name AND exit/close this program and restart to refresh - check it has.  It is currently set to " + model_run_name + " which is most likely the previous model run folder that you used - you don't want to use the same folder - it will end in tears!! (Once pressed, check that the folders have been created in the file system).  This will give you a place to save your next Weka model.model file. You can now press the Create folders for next run button to create all the necessary folders for the next iteration/run. "
        create_folders_msg = tk.Message(self, text = create_folders_instructions)
        create_folders_msg.config(width=600)
        create_folders_msg.grid(column=0, columnspan=1, row=4) 
        
        create_folders_button = ttk.Button(self, text="Create folders for next run",command=lambda: functions.create_folders_for_next_run())
        create_folders_button.grid(column=1, columnspan=1, row=4)  
        
        using_weka_instructions1 = "You are now ready to use Weka. BUT, if you are going to use AutoWeka it needs to use Java 1.8 (unlike Weka or Eclipse/Audio Manager which can use openjdk 11 - so at a terminal type 'sudo update-alternatives --config java' without the quotes and choose option (5 on my computer) for jdk1.8 Once the java version has been changed, from a terminal command prompt, cd into the directory where Weka has been installed (e.g. ~/weka-3-8-4b (on my computer) and launch Weka using the command: java -Xmx16384m -jar weka.jar"
        using_weka_msg1 = tk.Message(self, text = using_weka_instructions1)
        using_weka_msg1.config(width=600)
        using_weka_msg1.grid(column=0, columnspan=1, row=5)  
        
        using_weka_instructions2 = "These instructions are from the video: https://www.futurelearn.com/courses/advanced-data-mining-with-weka/0/steps/29486\ You will need to have installed the Image Filters Package into Weka."
        using_weka_msg2 = tk.Message(self, text = using_weka_instructions2)
        using_weka_msg2.config(width=600)
        using_weka_msg2.grid(column=0, columnspan=1, row=6)  
        
        using_weka_instructions3 = "In Weka, Press the Explorer button and then the Open file.. button to open the previously created .arff file. Now Press the Choose button below the Filter label and navigate to weka|filters|unsupervised|instance|imagefilter|EdgeHistogramFilter \
Then click on the Box with the name of the Filter (EdgeHistogramFilter) and paste in the path to image directory where all the spectrograms were created and press OK - it doesn't appear to have the ability to navigate to the directory.  Now press the Apply button to apply the filter."
        using_weka_msg3 = tk.Message(self, text = using_weka_instructions3)
        using_weka_msg3.config(width=600)
        using_weka_msg3.grid(column=0, columnspan=1, row=7)  
        
        using_weka_instructions4 = "The Weka image in the bottom right corner will do a dance while it is processing and when finished you should see a list of Attiributes (with the first being filename) and then MPEG-7 etc. Save the file with the name: device_names_added_arff_file_for_weka_model_creation_image_filtered.arff"
        using_weka_msg4 = tk.Message(self, text = using_weka_instructions4)
        using_weka_msg4.config(width=600)
        using_weka_msg4.grid(column=0, columnspan=1, row=8) 
        
#         using_weka_instructions5 = "In Weka, save the arff file, in the same location, with the name: arff_file_for_weka_model_creation_image_filtered.arff. Now, back in this GUI, press the Add Device Names button on the right to add the device names to the arff file."
#         using_weka_msg5 = tk.Message(self, text = using_weka_instructions5)
#         using_weka_msg5.config(width=600)
#         using_weka_msg5.grid(column=0, columnspan=1, row=9) 
#         
#         add_device_names_to_arff_button = ttk.Button(self, text="Add Device names to arff file",command=lambda: functions.add_device_names_to_arff())
#         add_device_names_to_arff_button.grid(column=1, columnspan=1, row=9) 
        
        using_weka_instructions6 = "Open this new arff file."
        using_weka_msg6 = tk.Message(self, text = using_weka_instructions6)
        using_weka_msg6.config(width=600)
        using_weka_msg6.grid(column=0, columnspan=1, row=10) 
         
        
        using_weka_instructions7 = "Now you need to remove the filename attribute by selecting the box and press the Remove button.  Save this as device_names_added_arff_file_for_weka_model_creation_image_filtered_filename_removed.arff  \n\nIf you want to use AutoWeka follow A instructions next otherwise follow B instructions. \n\nA) Select the Auto-Weka tab (in Weka) then right click on AUTOWEKAClassifier | Show properties and change timeLimit to something suitable say 4320 (ie 3 days), or first test with 10 minutes :-), press OK, check that (Nom) class is selected and then press start. The weka icon does its dance.  Make sure computer Power Saving is Off, and come back in 3 days!  \n\nB) If don't want to use AutoWeka try this - select the Classify tab (at the top). Press the Choose button and navigate to  Weka|classifiers|Trees|LMT (or you may have another model - and had saved the result buffer, if so in there you can copy the Scheme e.g. weka.classifiers.functions.SMO -C 1.0322930159130057 -L 0.001 -P 1.0E-12 -N 0 -M -V -1 -W 1 -K \"weka.classifiers.functions.supportVector.RBFKernel -C 250007 -G 0.4733376743447805\" -calibrator \"weka.classifiers.functions.Logistic -R 1.0E-8 -M -1 -num-decimal-places 4\" - and paste it here.  Use Cross-validation Folds 10 and press start. The weka image does it's dance and then the results displayed"
        using_weka_msg7 = tk.Message(self, text = using_weka_instructions7)
        using_weka_msg7.config(width=600)
        using_weka_msg7.grid(column=0, columnspan=1, row=11) 
        
        using_weka_instructions8 = "To export the model, in the Result list, right mouse click and Choose Save model and save as model.model in the weka_model directory for this run (Create the directory if you did not follow the instructions above). It is also worth saving the result buffer in a text file with this run."
        using_weka_msg8 = tk.Message(self, text = using_weka_instructions8)
        using_weka_msg8.config(width=600)
        using_weka_msg8.grid(column=0, columnspan=1, row=12) 
        
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
        
        run_button = ttk.Button(self, text="Run", command=lambda: functions.create_onsets_in_local_db_using_recordings_folder())        
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
        actual_confirmed_filter_radio_button_unknown = ttk.Radiobutton(self,text='Water', variable=self.actual_confirmed_filter, value='water')
        actual_confirmed_filter_radio_button_unknown.grid(column=0, columnspan=1, row=25)
        
        
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
        actual_confirmed_filter_radio_button_unknown = ttk.Radiobutton(self,text='Frog', variable=self.actual_confirmed_filter, value='frog')
        actual_confirmed_filter_radio_button_unknown.grid(column=1, columnspan=1, row=19)
        actual_confirmed_filter_radio_button_unknown = ttk.Radiobutton(self,text='Chainsaw', variable=self.actual_confirmed_filter, value='chainsaw')
        actual_confirmed_filter_radio_button_unknown.grid(column=1, columnspan=1, row=20)
        actual_confirmed_filter_radio_button_unknown = ttk.Radiobutton(self,text='Crackle', variable=self.actual_confirmed_filter, value='crackle')
        actual_confirmed_filter_radio_button_unknown.grid(column=1, columnspan=1, row=21)
        actual_confirmed_filter_radio_button_unknown = ttk.Radiobutton(self,text='Car horn', variable=self.actual_confirmed_filter, value='car_horn')
        actual_confirmed_filter_radio_button_unknown.grid(column=1, columnspan=1, row=22)
        actual_confirmed_filter_radio_button_unknown = ttk.Radiobutton(self,text='Fire work', variable=self.actual_confirmed_filter, value='fire_work')
        actual_confirmed_filter_radio_button_unknown.grid(column=1, columnspan=1, row=23)
        actual_confirmed_filter_radio_button_unknown = ttk.Radiobutton(self,text='Maybe Morepork more-pork', variable=self.actual_confirmed_filter, value='maybe_morepork_more-pork')
        actual_confirmed_filter_radio_button_unknown.grid(column=1, columnspan=1, row=24)
        actual_confirmed_filter_radio_button_unknown = ttk.Radiobutton(self,text='Music', variable=self.actual_confirmed_filter, value='music')
        actual_confirmed_filter_radio_button_unknown.grid(column=1, columnspan=1, row=25)
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
        predicted_filter_radio_button_unknown = ttk.Radiobutton(self,text='Water', variable=self.predicted_filter, value='water')
        predicted_filter_radio_button_unknown.grid(column=2, columnspan=1, row=24)
        
        
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
        predicted_filter_radio_button_unknown = ttk.Radiobutton(self,text='Frog', variable=self.predicted_filter, value='frog')
        predicted_filter_radio_button_unknown.grid(column=3, columnspan=1, row=19)  
        predicted_filter_radio_button_unknown = ttk.Radiobutton(self,text='Chainsaw', variable=self.predicted_filter, value='chainsaw')
        predicted_filter_radio_button_unknown.grid(column=3, columnspan=1, row=20) 
        predicted_filter_radio_button_unknown = ttk.Radiobutton(self,text='Crackle', variable=self.predicted_filter, value='crackle')
        predicted_filter_radio_button_unknown.grid(column=3, columnspan=1, row=21)  
        predicted_filter_radio_button_unknown = ttk.Radiobutton(self,text='Car horn', variable=self.predicted_filter, value='car_horn')
        predicted_filter_radio_button_unknown.grid(column=3, columnspan=1, row=22)
        predicted_filter_radio_button_unknown = ttk.Radiobutton(self,text='Fire work', variable=self.predicted_filter, value='fire_work')
        predicted_filter_radio_button_unknown.grid(column=3, columnspan=1, row=23) 
        predicted_filter_radio_button_unknown = ttk.Radiobutton(self,text='Maybe Morepork more-pork', variable=self.predicted_filter, value='maybe_morepork_more-pork')
        predicted_filter_radio_button_unknown.grid(column=3, columnspan=1, row=24)  
        predicted_filter_radio_button_unknown = ttk.Radiobutton(self,text='Music', variable=self.predicted_filter, value='music')
        predicted_filter_radio_button_unknown.grid(column=3, columnspan=1, row=25) 
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
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Dove', variable=self.actual_confirmed, value='dove',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=0, columnspan=1, row=244)   
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Duck', variable=self.actual_confirmed, value='duck',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=0, columnspan=1, row=245) 
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Dog', variable=self.actual_confirmed, value='dog',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=0, columnspan=1, row=246) 
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Human', variable=self.actual_confirmed, value='human',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=0, columnspan=1, row=247)   
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Siren', variable=self.actual_confirmed, value='siren',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=0, columnspan=1, row=248)
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Bird', variable=self.actual_confirmed, value='bird',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=0, columnspan=1, row=249) 
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Car', variable=self.actual_confirmed, value='car',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=0, columnspan=1, row=250)
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Rumble', variable=self.actual_confirmed, value='rumble',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=0, columnspan=1, row=251)
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Water', variable=self.actual_confirmed, value='water',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=0, columnspan=1, row=252)
        
        
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='White noise', variable=self.actual_confirmed, value='white_noise',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=1, columnspan=1, row=242)
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Plane', variable=self.actual_confirmed, value='plane',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=1, columnspan=1, row=243)
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Cow', variable=self.actual_confirmed, value='cow',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=1, columnspan=1, row=244) 
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Buzzy insect', variable=self.actual_confirmed, value='buzzy_insect',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=1, columnspan=1, row=245) 
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Morepork more-pork Part', variable=self.actual_confirmed, value='morepork_more-pork_part',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=1, columnspan=1, row=246) 
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Hammering', variable=self.actual_confirmed, value='hammering',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=1, columnspan=1, row=247)  
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Frog', variable=self.actual_confirmed, value='frog',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=1, columnspan=1, row=248)
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Chainsaw', variable=self.actual_confirmed, value='chainsaw',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=1, columnspan=1, row=249) 
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Crackle', variable=self.actual_confirmed, value='crackle',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=1, columnspan=1, row=250)  
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Car horn', variable=self.actual_confirmed, value='car_horn',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=1, columnspan=1, row=251)
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Fire work', variable=self.actual_confirmed, value='fire_work',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=1, columnspan=1, row=252)
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Maybe Morepork more-pork', variable=self.actual_confirmed, value='maybe_morepork_more-pork',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=1, columnspan=1, row=253)
        actual_confirmed_radio_button_unknown = ttk.Radiobutton(self,text='Music', variable=self.actual_confirmed, value='music',command=lambda: confirm_actual())
        actual_confirmed_radio_button_unknown.grid(column=1, columnspan=1, row=254)       
       
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
            
        select_arff_file_label = ttk.Label(self, text="Select the arff file that was used to create this model.")
        select_arff_file_label.grid(column=0, columnspan=1, row=15)   
        
        select_arff_file_label = ttk.Label(self, text="Important - the arff file is probably in the previous model run folder to the model run result that you are updating!")
        select_arff_file_label.grid(column=0, columnspan=1, row=16)       
            
        select_arff_file_used_to_create_model_button = ttk.Button(self, text="Select arff file",command=lambda: select_arff_file_used_to_create_model())
        select_arff_file_used_to_create_model_button.grid(column=0, columnspan=1, row=17)    
            
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
                
        def select_arff_file_used_to_create_model():
#             print(initial_locatation_for_choosing_arff_file_dialog)            
            self.arff_filename = filedialog.askopenfilename(initialdir = initial_locatation_for_choosing_arff_file_dialog,title = "Select file",filetypes = (("arff files","*.arff"),("all files","*.*")))
            
                
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
        msg7.grid(column=0, columnspan=1, row=10)
        
        location_filter_label = ttk.Label(self, text="Location Filter")
        location_filter_label.grid(column=1, columnspan=1, row=10)      
                                    
        self.location_filter = StringVar()
        self.location_filter_combo = ttk.Combobox(self, textvariable=self.location_filter, values=self.unique_locations)
        
        if len(self.unique_locations) > 0:
            self.location_filter_combo.current(0)
            self.location_filter_combo.grid(column=1, columnspan=1,row=11) 
        
        upload_tags_button = ttk.Button(self, text="Upload Tags To Cacophony Server",command=lambda: functions.upload_tags_to_cacophony_server(self.location_filter_combo.get()))
        upload_tags_button.grid(column=2, columnspan=1, row=11)
        
        back_to_home_button = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(HomePage))
        back_to_home_button.grid(column=0, columnspan=1, row=61) 
                                                                               
        
app = Main_GUI()
app.mainloop() 