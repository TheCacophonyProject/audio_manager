'''
Created on 5 Aug. 2020

@author: tim
'''
import functions

# functions.create_audio_clips_for_speaker_recogntion_not_march_test_data()

import numpy as np
from keras.utils import to_categorical
### Categorical data to be converted to numeric data
colors = ["red", "green", "yellow", "red", "blue"]

### Universal list of colors
total_colors = ["red", "green", "blue", "black", "yellow"]

### map each color to an integer
mapping = {}
for x in range(len(total_colors)):
  mapping[total_colors[x]] = x

# integer representation
for x in range(len(colors)):
  colors[x] = mapping[colors[x]]

one_hot_encode = to_categorical(colors)

print("one_hot_encode ", one_hot_encode)