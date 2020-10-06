'''
Created on 5 Sep 2019
Modified 17 12 2019a

@author: tim

'''
from tkinter.messagebox import showinfo
from threading import Thread
# from pylint.test import test_self

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

import functions
import parameters


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
        
#         for F in (HomePage, RecordingsPage, TaggingPage, CreateWekaModelPage, ClassifyOnsetsUsingWekaModelPage, CreateOnsetsPage, CreateSpectrogramsPage, CreateTagsFromOnsetsPage, EvaluateModelRunResultPage, CreateTagsOnCacophonyServerFromModelRunPage, ModelAccuracyAnalysisPage, CreateTestDataPage):
        for F in (HomePage,  EvaluateModelRunResultPage ):
          
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
        
                   
          
        evaluateWekaModelRunResultPage_button = ttk.Button(self, text="Step 4: Manually Evaluate model Run Result",
                            command=lambda: controller.show_frame(EvaluateModelRunResultPage))        
        evaluateWekaModelRunResultPage_button.pack()        
        
                     
        
        


     

            
class EvaluateModelRunResultPage(tk.Frame):    
    
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.current_model_run_result_array_pos = 0
        self.current_model_run_name_ID = 0        
        
        self.unique_training_data_runs = functions.get_unique_model_run_names()  
        self.unique_locations = functions.get_unique_locations('recordings')            
                    
        title_label = ttk.Label(self, text="Evaluate Model Run Results", font=LARGE_FONT)
        title_label.grid(column=0, columnspan=1, row=0)           
                
        refresh_model_run_names_button = ttk.Button(self, text="Refresh Unique Model Run Names",command=lambda: refresh_unique_model_run_names())
        refresh_model_run_names_button.grid(column=0, columnspan=1, row=3) 
        
        run_names_label = ttk.Label(self, text="Run Names")
        run_names_label.grid(column=1, columnspan=1, row=2)      
                                    
        self.run_name = StringVar()
        self.run_names_combo = ttk.Combobox(self, textvariable=self.run_name, values=self.unique_training_data_runs)
        
        if len(self.unique_training_data_runs) > 0:
            self.run_names_combo.current(0)
            self.run_names_combo.grid(column=1, columnspan=1,row=3) 
            self.run_names_combo.current(len(self.unique_training_data_runs) - 1)       
            
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
        
       
        def confirm_actual():
            print('self.actual_confirmed.get() ', self.actual_confirmed.get())
            functions.update_model_run_result(self.current_model_run_name_ID, self.actual_confirmed.get())
            functions.update_onset(self.current_model_run_name_recording_id, self.current_model_run_name_start_time, self.actual_confirmed.get())
        
        def unselect_actual_confirmed():
            self.actual_confirmed.set('not_used')
            confirm_actual()
        
        def refresh_unique_model_run_names():
            self.unique_training_data_runs = functions.get_unique_model_run_names()
            self.run_names_combo['values'] = self.unique_training_data_runs  
            
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
            run_folder = parameters.run_folder
            self.spectrogram_image = functions.get_single_create_focused_mel_spectrogram(self.current_model_run_name_recording_id, self.current_model_run_name_start_time, self.current_model_run_name_duration, run_folder)
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
        
            self.current_training_data_predicted = self.run_result[5]             
            self.current_model_run_name_actual_confirmed = self.run_result[6] 

            if self.run_result[7]:
                self.current_training_data_probability = "{0:.2f}".format(self.run_result[7])
            else:
                self.current_training_data_probability = '?'
            
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

            self.predicted_label_value.set(self.current_training_data_predicted + ' with ' + self.current_training_data_probability + ' probability')
            
            threading.Thread(target=self.play_clip(), args=(1,)).start()
            threading.Thread(target=display_images(), args=(1,)).start()
     
        
        
app = Main_GUI()
app.mainloop() 