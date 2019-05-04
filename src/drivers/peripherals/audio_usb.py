#steps:
# 1. ensure audio outptu is possible, play youtube video
# 2. record --device=hw:1,0 --format S16_LE --rate 44100 -c1 test.wav
# 3. aplay test.wav


#import pyaudio
#sudo apt-get install python3-dev
#sudo apt-get install python-pyaudio
#sudo apt-get install python3-pyaudio
#pip3 install matplotlib #this will take 10's of minutes...
#note: had to uinstall numpy a few times, then reinstall to get matplotlib to work:
#  pip3 uninstall numpy
#  pip3 uninstall numpy
#  pip3 install numpy

#!/usr/bin/env python3
import pyaudio
import wave

CHUNK = 512
FORMAT = pyaudio.paInt16 #paInt8
CHANNELS = 1
RATE = 44100 #sample rate
RECORD_SECONDS = 1.0
WAVE_OUTPUT_FILENAME = "pyaudio-output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK) #buffer

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data) # 2 bytes(16 bits) per channel

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

#windowing...
from scipy.fftpack import fft
import numpy as np
from scipy.io import wavfile as wav
import matplotlib.pyplot as plt
rate, data = wav.read(WAVE_OUTPUT_FILENAME) #rate=44100
data_len=len(data)
window = np.hamming(data_len)
data_windowed=[a*b for a,b in zip(window,data)]
fft_out = np.abs(fft(data_windowed))
#plt.plot(data, np.abs(fft_out))
#half_data_len=int(data_len/2)
deltaF=rate/data_len
x_axis=list(range(data_len))
x_axis=[x*deltaF for x in x_axis]
max_cutoff=1000 #max Hz
num_el=sum(i<max_cutoff for i in x_axis)
data_max=max(fft_out[0:num_el])
data_max_index=list(fft_out).index(data_max)
freq_max=x_axis[data_max_index] #red 438 [A4], green 782 [G5 {261, C4, third harmonic}], blue 391 [G4], white: 440+522+784 [A4+C5+G5], yellow: 522+440 C5+A4, cyan: 391+783 G4+G5, purple: 782+440 A4+G5
print("Frequency: "+str(freq_max)+" Hz")
from math import log
fft_out_log=[20*log(y,10) for y in fft_out]
plt.plot(x_axis[0:num_el], fft_out_log[0:num_el])
plt.show()
