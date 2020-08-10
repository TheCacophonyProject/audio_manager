'''
Created on 9 Aug. 2020
based/copied from https://keras.io/examples/audio/speaker_recognition_using_cnn/
@author: tim
'''

import functions
import parameters
import scipy
import sqlite3
from sqlite3 import Error
import requests
import json
from pathlib import Path
import os
from scipy import signal
import numpy as np
from scipy.signal import butter, lfilter
import librosa
import matplotlib.pyplot as plt
# import librosa.display
import matplotlib.colors as mcolors
import soundfile as sf
from subprocess import PIPE, run
from librosa import onset
from PIL import ImageTk,Image 
# from datetime import datetime
import datetime
from pytz import timezone
import sys
from tkinter import filedialog
from pathlib import Path
import tensorflow as tf
from tensorflow import keras 
from keras import metrics
import shutil

BASE_FOLDER = '/home/tim/Work/Cacophony'
TENSORFLOW_RUN_NAME = 'practice'
TENSORFLOW_RUN_FOLDER = BASE_FOLDER + '/Audio_Analysis/audio_classifier_runs/tensorflow_runs' + '/' + TENSORFLOW_RUN_NAME

CHECKPOINT_PATH = TENSORFLOW_RUN_FOLDER + "/checkpoints/" + "training_1/cp.ckpt"
CHECKPOINT_DIRECTORY = os.path.dirname(CHECKPOINT_PATH)

SAVED_MODELS_DIRECTORY = TENSORFLOW_RUN_FOLDER + "/saved_model"
SAVE_MODEL_NAME = SAVED_MODELS_DIRECTORY + "/model-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
# CHECKPOINT_FILEPATH = TENSORFLOW_RUN_FOLDER + '/tmp/checkpoint'
TENSORBOARD_LOGS_DIR = TENSORFLOW_RUN_FOLDER + "/logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    

DATASET_ROOT = os.path.join(os.path.expanduser("~"), "Work/Cacophony/Audio_Analysis/audio_clips")
    
# The folders in which we will put the audio samples and the noise samples
AUDIO_SUBFOLDER = "audio"
NOISE_SUBFOLDER = "noise"

DATASET_AUDIO_PATH = os.path.join(DATASET_ROOT, AUDIO_SUBFOLDER)
DATASET_NOISE_PATH = os.path.join(DATASET_ROOT, NOISE_SUBFOLDER)

# Percentage of samples to use for validation
VALID_SPLIT = 0.1

# Seed to use when shuffling the dataset and the noise
SHUFFLE_SEED = 43

# The sampling rate to use.
# This is the one used in all of the audio samples.
# We will resample all of the noise to this sampling rate.
# This will also be the output size of the audio wave samples
# (since all samples are of 1 second long)
SAMPLING_RATE = 16000

# The factor to multiply the noise with according to:
#   noisy_sample = sample + noise * prop * scale
#      where prop = sample_amplitude / noise_amplitude
SCALE = 0.5

BATCH_SIZE = 128
EPOCHS = 500
# EPOCHS = 2

def get_onsets_from_non_test_march_2020_recordings():
    
    cur = functions.get_database_connection().cursor()
#     cur.execute("SELECT ID, recording_id, start_time_seconds, duration_seconds, device_super_name, device_name, recordingDateTime, recordingDateTimeNZ  from onsets WHERE version = 7 AND (recording_id > ? AND recording_id < ?)", (first_test_data_recording_id, last_test_data_recording_id))
    cur.execute("SELECT ID, recording_id, start_time_seconds, duration_seconds, actual_confirmed, recordingDateTimeNZ, version from onsets WHERE actual_confirmed IS NOT NULL AND version = 5 AND recordingDateTimeNZ NOT BETWEEN ? AND ? ORDER BY recordingDateTimeNZ", ("2020-03-01 00:00", "2020-03-31 23:59"))
    confirmed_onsets = cur.fetchall() 
    
    return confirmed_onsets    
    

def create_and_save_clip_as_wav(recording_id, start_time, duration, applyBandPassFilter, what):
    audio_in_path = functions.getRecordingsFolder() + '/' + str(recording_id) + '.m4a'
    print('audio_in_path ', audio_in_path)
    print('start_time ', start_time)
    print('duration ', duration)

    audio_out_folder = '/home/tim/Work/Cacophony/Audio_Analysis/audio_clips/' + what + '/'    
       
    Path(audio_out_folder).mkdir(parents=True, exist_ok=True)
    
    audio_out_folder_filename = audio_out_folder  + str(recording_id) + '_' + what + '_' + str(start_time) + '.wav'
    
#     audio_in_path = '/home/tim/Work/Cacophony/downloaded_recordings/all_recordings/' + recording_id + '.m4a'

    
    print('audio_out_folder_filename ', audio_out_folder_filename)
    
    y, sr = librosa.load(audio_in_path, sr=None) 
    y_start = sr * start_time
    y_end = (sr * start_time) + (sr * duration)
    y_time_clipped = y[int(y_start):int(y_end)]
    
#     y_time_clipped_amplified = np.int16(y_time_clipped/np.max(np.abs(y_time_clipped)) * 32767) # can't remember where 32767 came from :-(
    
    
    
    y_time_clipped_amplified_filtered = functions.butter_bandpass_filter(y_time_clipped, parameters.morepork_min_freq, parameters.morepork_max_freq, sr)    
  

    sf.write(audio_out_folder_filename, y_time_clipped_amplified_filtered, sr)
    
    

def create_audio_clips_for_speaker_recogntion_not_march_test_data():
    confirmed_onsets = get_onsets_from_non_test_march_2020_recordings()
   
    count = 0
    count_of_confirmed_onsets = len(confirmed_onsets)
    print("count_of_confirmed_onsets ", count_of_confirmed_onsets)
    for confired_onset in confirmed_onsets:
        count+=1
        print(count, ' of ', count_of_confirmed_onsets)
        recording_id = confired_onset[1]
        start_time_seconds = confired_onset[2]
#         duration_seconds = confired_onset[3]
        duration_seconds = 1 # For now use 1 second so it is the same as the speaker recognition example code
        what = confired_onset[4]
        recordingDateTimeNZ = confired_onset[5]
        version = confired_onset[6]
        
        # Create filtered clip
        create_and_save_clip_as_wav(recording_id, start_time_seconds, duration_seconds, True, what)
        
def check_tensorflow_setup():
    print('tensorflow version is ',tf.__version__)
    print('python version is ',sys.version)
    print(tf.config.list_physical_devices('GPU'))
    
    # https://www.tensorflow.org/api_docs/python/tf/config/experimental/set_memory_growth
    physical_devices = tf.config.list_physical_devices('GPU')
    try:
        tf.config.experimental.set_memory_growth(physical_devices[0], True)
    except:
        # Invalid device or cannot modify virtual devices once initialized.
        pass
    
    

    if not os.path.exists(TENSORFLOW_RUN_FOLDER):
        os.makedirs(TENSORFLOW_RUN_FOLDER)
        
    if not os.path.exists(CHECKPOINT_DIRECTORY):
        os.makedirs(CHECKPOINT_DIRECTORY)
        
    if not os.path.exists(SAVED_MODELS_DIRECTORY):
        os.makedirs(SAVED_MODELS_DIRECTORY)
        
    
    print('tensorflow version is ',tf.__version__)
    physical_devices = tf.config.list_physical_devices('GPU')
    print(physical_devices)
    print(DATASET_ROOT)
    print("TENSORBOARD_LOGS_DIR: ", TENSORBOARD_LOGS_DIR)
    
    
def prepare_audio_files():
    # If folder `audio`, does not exist, create it, otherwise do nothing
    if os.path.exists(DATASET_AUDIO_PATH) is False:
        os.makedirs(DATASET_AUDIO_PATH)

    # If folder `noise`, does not exist, create it, otherwise do nothing
    if os.path.exists(DATASET_NOISE_PATH) is False:
        os.makedirs(DATASET_NOISE_PATH)
    
    for folder in os.listdir(DATASET_ROOT):
        if os.path.isdir(os.path.join(DATASET_ROOT, folder)):
            if folder in [AUDIO_SUBFOLDER, NOISE_SUBFOLDER]:
                # If folder is `audio` or `noise`, do nothing
                continue
    #         elif folder in ["other", "_background_noise_"]:
            elif folder in ["car","car_horn","chainsaw", "cow", "crackle", "dog", "fire_work", "hammering", "hand_saw", "music", "plane", "rumble", "siren", "unknown" , "water", "white_noise"]:
                # If folder is one of the folders that contains noise samples,
                # move it to the `noise` folder
                shutil.move(
                    os.path.join(DATASET_ROOT, folder),
                    os.path.join(DATASET_NOISE_PATH, folder),
                )
            else:
                # Otherwise, it should be a speaker folder, then move it to
                # `audio` folder
                shutil.move(
                    os.path.join(DATASET_ROOT, folder),
                    os.path.join(DATASET_AUDIO_PATH, folder),
                )

# Split noise into chunks of 16000 each
def load_noise_sample(path):
    sample, sampling_rate = tf.audio.decode_wav(
        tf.io.read_file(path), desired_channels=1
    )
    if sampling_rate == SAMPLING_RATE:
        # Number of slices of 16000 each that can be generated from the noise sample
        slices = int(sample.shape[0] / SAMPLING_RATE)
        sample = tf.split(sample[: slices * SAMPLING_RATE], slices)
        return sample
    else:
        print("Sampling rate for {} is incorrect. Ignoring it".format(path))
        return None

def setup_noise():
    # Get the list of all noise files
    noise_paths = []
    for subdir in os.listdir(DATASET_NOISE_PATH):
        subdir_path = Path(DATASET_NOISE_PATH) / subdir
        if os.path.isdir(subdir_path):
            noise_paths += [
                os.path.join(subdir_path, filepath)
                for filepath in os.listdir(subdir_path)
                if filepath.endswith(".wav")
            ]   

    print(
        "Found {} files belonging to {} directories".format(
            len(noise_paths), len(os.listdir(DATASET_NOISE_PATH))
        )
    )
    
    command = (
        "for dir in `ls -1 " + DATASET_NOISE_PATH + "`; do "
        "for file in `ls -1 " + DATASET_NOISE_PATH + "/$dir/*.wav`; do "
        "sample_rate=`ffprobe -hide_banner -loglevel panic -show_streams "
        "$file | grep sample_rate | cut -f2 -d=`; "
        "if [ $sample_rate -ne 16000 ]; then "
        "ffmpeg -hide_banner -loglevel panic -y "
        "-i $file -ar 16000 temp.wav; "
        "mv temp.wav $file; "
        "fi; done; done"
    )

    os.system(command)
    
    noises = []
    for path in noise_paths:
        sample = load_noise_sample(path)
        if sample:
            noises.extend(sample)
    noises = tf.stack(noises)
    
    print(
        "{} noise files were split into {} noise samples where each is {} sec. long".format(
            len(noise_paths), noises.shape[0], noises.shape[1] // SAMPLING_RATE
        )
    )
    
    return noises
    
def paths_and_labels_to_dataset(audio_paths, labels):
    """Constructs a dataset of audios and labels."""
    path_ds = tf.data.Dataset.from_tensor_slices(audio_paths)
    audio_ds = path_ds.map(lambda x: path_to_audio(x))
    label_ds = tf.data.Dataset.from_tensor_slices(labels)
    return tf.data.Dataset.zip((audio_ds, label_ds))


def path_to_audio(path):
    """Reads and decodes an audio file."""
    audio = tf.io.read_file(path)
    audio, _ = tf.audio.decode_wav(audio, 1, SAMPLING_RATE)
    return audio


def add_noise(audio, noises=None, scale=0.5):
    if noises is not None:
        # Create a random tensor of the same size as audio ranging from
        # 0 to the number of noise stream samples that we have.
        tf_rnd = tf.random.uniform(
            (tf.shape(audio)[0],), 0, noises.shape[0], dtype=tf.int32
        )
        noise = tf.gather(noises, tf_rnd, axis=0)

        # Get the amplitude proportion between the audio and the noise
        prop = tf.math.reduce_max(audio, axis=1) / tf.math.reduce_max(noise, axis=1)
        prop = tf.repeat(tf.expand_dims(prop, axis=1), tf.shape(audio)[1], axis=1)

        # Adding the rescaled noise to audio
        audio = audio + noise * prop * scale

    return audio


def audio_to_fft(audio):
    # Since tf.signal.fft applies FFT on the innermost dimension,
    # we need to squeeze the dimensions and then expand them again
    # after FFT
    audio = tf.squeeze(audio, axis=-1)
    fft = tf.signal.fft(
        tf.cast(tf.complex(real=audio, imag=tf.zeros_like(audio)), tf.complex64)
    )
    fft = tf.expand_dims(fft, axis=-1)

    # Return the absolute value of the first half of the FFT
    # which represents the positive frequencies
    return tf.math.abs(fft[:, : (audio.shape[1] // 2), :])   

def get_list_of_class_names():
    # Get the list of audio file paths along with their corresponding labels

    class_names = os.listdir(DATASET_AUDIO_PATH)
    print("Our class names: {}".format(class_names,))
    
    audio_paths = []
    labels = []
    for label, name in enumerate(class_names):
        print("Processing speaker {}".format(name,))
        dir_path = Path(DATASET_AUDIO_PATH) / name
        speaker_sample_paths = [
            os.path.join(dir_path, filepath)
            for filepath in os.listdir(dir_path)
            if filepath.endswith(".wav")
        ]
        audio_paths += speaker_sample_paths
        labels += [label] * len(speaker_sample_paths)
    
    print(
        "Found {} files belonging to {} classes.".format(len(audio_paths), len(class_names))
    )
    
    return audio_paths, labels, class_names
    
def shuffle(audio_paths, labels):
    # Shuffle
    rng = np.random.RandomState(SHUFFLE_SEED)
    rng.shuffle(audio_paths)
    rng = np.random.RandomState(SHUFFLE_SEED)
    rng.shuffle(labels)
    return audio_paths, labels
    
def split_into_training_and_validation(audio_paths, labels):
    # Split into training and validation
    num_val_samples = int(VALID_SPLIT * len(audio_paths))
    print("Using {} files for training.".format(len(audio_paths) - num_val_samples))
    train_audio_paths = audio_paths[:-num_val_samples]
    train_labels = labels[:-num_val_samples]
    
    print("Using {} files for validation.".format(num_val_samples))
    valid_audio_paths = audio_paths[-num_val_samples:]
    valid_labels = labels[-num_val_samples:]
    
    # Create 2 datasets, one for training and the other for validation
    train_ds = paths_and_labels_to_dataset(train_audio_paths, train_labels)
    train_ds = train_ds.shuffle(buffer_size=BATCH_SIZE * 8, seed=SHUFFLE_SEED).batch(
        BATCH_SIZE
    )
    
    valid_ds = paths_and_labels_to_dataset(valid_audio_paths, valid_labels)
    valid_ds = valid_ds.shuffle(buffer_size=32 * 8, seed=SHUFFLE_SEED).batch(32)
    
    return train_ds, valid_ds, valid_audio_paths, valid_labels
    
def add_noise_to_training_set(train_ds, noises):
    # Add noise to the training set
    train_ds = train_ds.map(
        lambda x, y: (add_noise(x, noises, scale=SCALE), y),
        num_parallel_calls=tf.data.experimental.AUTOTUNE,
    )
    
def transform_audio_wave_to_the_frequency_domain(train_ds, valid_ds):
    # Transform audio wave to the frequency domain using `audio_to_fft`
    train_ds = train_ds.map(
        lambda x, y: (audio_to_fft(x), y), num_parallel_calls=tf.data.experimental.AUTOTUNE
    )
    train_ds = train_ds.prefetch(tf.data.experimental.AUTOTUNE)
    
    valid_ds = valid_ds.map(
        lambda x, y: (audio_to_fft(x), y), num_parallel_calls=tf.data.experimental.AUTOTUNE
    )
    valid_ds = valid_ds.prefetch(tf.data.experimental.AUTOTUNE)
    
    return train_ds, valid_ds

def residual_block(x, filters, conv_num=3, activation="relu"):
    # Shortcut
    s = keras.layers.Conv1D(filters, 1, padding="same")(x)
    for i in range(conv_num - 1):
        x = keras.layers.Conv1D(filters, 3, padding="same")(x)
        x = keras.layers.Activation(activation)(x)
    x = keras.layers.Conv1D(filters, 3, padding="same")(x)
    x = keras.layers.Add()([x, s])
    x = keras.layers.Activation(activation)(x)
    return keras.layers.MaxPool1D(pool_size=2, strides=2)(x)


def build_model(input_shape, num_classes):
    inputs = keras.layers.Input(shape=input_shape, name="input")

    x = residual_block(inputs, 16, 2)
    x = residual_block(x, 32, 2)
    x = residual_block(x, 64, 3)
    x = residual_block(x, 128, 3)
    x = residual_block(x, 128, 3)

    x = keras.layers.AveragePooling1D(pool_size=3, strides=3)(x)
    x = keras.layers.Flatten()(x)
    x = keras.layers.Dense(256, activation="relu")(x)
    x = keras.layers.Dense(128, activation="relu")(x)

    outputs = keras.layers.Dense(num_classes, activation="softmax", name="output")(x)    

    return keras.models.Model(inputs=inputs, outputs=outputs)
    
def get_keras_metrics():
    METRICS = [     
#       keras.metrics.BinaryAccuracy(name='accuracy'),
      "accuracy",      
      tf.keras.metrics.SparseCategoricalCrossentropy(),
    ]
    return METRICS
    
def get_model_check_point_callback():
    # https://www.tensorflow.org/api_docs/python/tf/keras/callbacks/ModelCheckpoint
   
    metric = 'val_accuracy'
    model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
#         filepath=PATH_TO_MODEL_CHECKPOINT + 'model.{epoch:02d}-{val_loss:.2f}.h5',
        filepath=CHECKPOINT_PATH,
        save_weights_only=True,
        monitor=metric,
        mode='max',
        save_best_only=True)
    
    return model_checkpoint_callback

def get_all_callbacks():
    my_callbacks = [
    tf.keras.callbacks.EarlyStopping(patience=50, restore_best_weights=True),
#     tf.keras.callbacks.ModelCheckpoint(filepath=PATH_TO_MODEL_CHECKPOINT + 'model.{epoch:02d}-{val_loss:.2f}.h5'),
    get_model_check_point_callback(),
#     tf.keras.callbacks.TensorBoard(log_dir='./logs'),  TENSORBOARD_LOGS_DIR
#     tf.keras.callbacks.TensorBoard(log_dir=TENSORBOARD_LOGS_DIR),  
    tf.keras.callbacks.TensorBoard(log_dir=TENSORBOARD_LOGS_DIR, profile_batch=0),  # Bug in tensorboard updating- needs , profile_batch=0 - https://github.com/tensorflow/tensorboard/issues/2084#issuecomment-483395808
    ]
    
    return my_callbacks

# def get_early_stopping_callback():
#     earlystopping_cb = keras.callbacks.EarlyStopping(patience=50, restore_best_weights=True)   
#     return earlystopping_cb

def test_model(valid_audio_paths, valid_labels, noises, model, class_names):
    count_of_validation_audio_paths = len(valid_audio_paths)
    print("count_of_validation_audio_paths: ", count_of_validation_audio_paths)
#     SAMPLES_TO_DISPLAY = 10
    SAMPLES_TO_DISPLAY = count_of_validation_audio_paths

    test_ds = paths_and_labels_to_dataset(valid_audio_paths, valid_labels)
    test_ds = test_ds.shuffle(buffer_size=BATCH_SIZE * 8, seed=SHUFFLE_SEED).batch(
        BATCH_SIZE
    )
    
    test_ds = test_ds.map(lambda x, y: (add_noise(x, noises, scale=SCALE), y))
    
    for audios, labels in test_ds.take(1):
        # Get the signal FFT
        ffts = audio_to_fft(audios)
        # Predict
        y_pred = model.predict(ffts)
        # Take random samples
        rnd = np.random.randint(0, BATCH_SIZE, SAMPLES_TO_DISPLAY)
        audios = audios.numpy()[rnd, :, :]
        labels = labels.numpy()[rnd]
        y_pred = np.argmax(y_pred, axis=-1)[rnd]
        
        count_of_TP_morepork = 0
        count_of_TN_morepork = 0
        count_of_FP_morepork = 0
        count_of_FN_morepork = 0
        
    
        for index in range(SAMPLES_TO_DISPLAY):
            # For every sample, print the true and predicted label
            # as well as run the voice with the noise
#             print(
#                 "Speaker: {} - Predicted: {}".format(
#                     class_names[labels[index]],
#                     class_names[y_pred[index]],
#                 )
#             )
            print("Speaker: {} - Predicted: {}".format(class_names[labels[index]], class_names[y_pred[index]],))
            
            actual_class_name = class_names[labels[index]]
            predicted_class_name = class_names[y_pred[index]]
            
            if predicted_class_name == "morepork_more-pork":
                if actual_class_name == "morepork_more-pork":
                    count_of_TP_morepork+=1
                else:
                    count_of_FP_morepork+=1
            else:
                if actual_class_name == "morepork_more-pork":
                    count_of_FN_morepork+=1
                else:
                    count_of_TN_morepork+=1
                                
        print("count_of_TP_morepork: ", count_of_TP_morepork)
        print("count_of_TN_morepork: ", count_of_TN_morepork)
        print("count_of_FP_morepork: ", count_of_FP_morepork)
        print("count_of_FN_morepork: ", count_of_FN_morepork)
        
                 
                 
#             display(Audio(audios[index, :, :].squeeze(), rate=SAMPLING_RATE))
        
def evaluate_model_and_store_in_database(model_name):
    # https://www.tensorflow.org/tutorials/keras/save_and_load
    model_to_load = SAVED_MODELS_DIRECTORY + "/" + model_name
    print("Model to load: ", model_to_load)
    model = tf.keras.models.load_model(model_to_load)

    # Check its architecture
    model.summary()
    
    # Prepare a wav file
    
       

def run(use_saved_checkpoint, train_model, save_model_for_standalone_use, evaluate_model, model_name):
    check_tensorflow_setup()
    prepare_audio_files()
    noises = setup_noise()
    audio_paths, labels, class_names = get_list_of_class_names()
    audio_paths, labels = shuffle(audio_paths, labels)
    train_ds, valid_ds, valid_audio_paths, valid_labels = split_into_training_and_validation(audio_paths, labels)
    add_noise_to_training_set(train_ds, noises)
    train_ds, valid_ds = transform_audio_wave_to_the_frequency_domain(train_ds, valid_ds)
        
    model = build_model((SAMPLING_RATE // 2, 1), len(class_names))
    model.compile(optimizer="Adam", loss="sparse_categorical_crossentropy", metrics=get_keras_metrics())
        
    if use_saved_checkpoint:
#         check_point_to_load = PATH_TO_MODEL_CHECKPOINT + "model.01-0.77.h5"
        check_point_to_load =  CHECKPOINT_PATH
        print("check_point_to_load: ", check_point_to_load)
        model.load_weights(check_point_to_load)
    
    model.summary()
    
    if (train_model):
        history = model.fit(
            train_ds,
            epochs=EPOCHS,
            validation_data=valid_ds,
            callbacks=[get_all_callbacks()],
        )
    
    
    print(model.evaluate(valid_ds))
    
    test_model(valid_audio_paths, valid_labels, noises, model, class_names)
    
    if (save_model_for_standalone_use):
        model.save(filepath=SAVE_MODEL_NAME)
        print("Model saved at: ", SAVE_MODEL_NAME)
        
    if (evaluate_model):
        evaluate_model_and_store_in_database(model_name)


run(use_saved_checkpoint=False, train_model=True, save_model_for_standalone_use=False, evaluate_model=False, model_name=None)  # Normal options
# run(use_saved_checkpoint=True, train_model=True, save_model_for_standalone_use=False, evaluate_model=False, model_name=None)  # Carry on training from previous checkpoint
# run(use_saved_checkpoint=True, train_model=False, save_model_for_standalone_use=True, evaluate_model=False, model_name=None)  # Just load model from checkpoint, and save as standalone model for production use
# run(use_saved_checkpoint=False, train_model=False, save_model_for_standalone_use=False, evaluate_model=True, model_name="model-20200810-163033") # Load latest model and evaluate test data, storing results in database
# run(use_saved_checkpoint=True, train_model=False, save_model_for_standalone_use=False, evaluate_model=False, model_name=None) # Just test_model
    