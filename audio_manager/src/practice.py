'''
Created on 28 Jul. 2020

@author: tim
'''

import librosa
import librosa.display
import parameters
import matplotlib.pyplot as plt
import functions
import matplotlib.colors as mcolors

audio_in_path = '/home/tim/Work/Cacophony/downloaded_recordings/all_recordings/537989.m4a'
y, sr = librosa.load(audio_in_path, sr=None) 
print(y)

# y = functions.butter_bandpass_filter(y, 200, 2000, sr, order=3)  
y = functions.butter_bandpass_filter(y, 600, 1200, sr, order=4)    
y = functions.noise_reduce(y, sr)  

image_out_path = '/home/tim/Temp/temp_spectrogram_order_4_powernorm_2.jpg'

# mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, fmin=600,fmax=1200)
# mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, fmin=300,fmax=5000)
# mel_spectrogram = librosa.feature.mfcc(y=y, sr=sr)

plt.axis('off') # no axis
plt.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[]) # Remove the white edge
#         librosa.display.specshow(mel_spectrogram, cmap='binary') #https://matplotlib.org/examples/color/colormaps_reference.html
# librosa.display.specshow(mel_spectrogram, norm=mcolors.PowerNorm(0.3), cmap='binary') 
# librosa.display.specshow(mel_spectrogram, norm=mcolors.PowerNorm(0.3), cmap='Greys') 
librosa.display.specshow(mel_spectrogram, norm=mcolors.PowerNorm(0.2), cmap='binary') 

# librosa.display.waveplot(y, sr)
        
        
#         librosa.display.specshow(mel_spectrogram) #https://matplotlib.org/examples/color/colormaps_reference.html
plt.savefig(image_out_path, bbox_inches=None, pad_inches=0)
plt.close()

print('finished')


