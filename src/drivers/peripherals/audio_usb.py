#steps:
# 1. ensure audio outptu is possible, play youtube video
# 2. record --device=hw:1,0 --format S16_LE --rate 44100 -c1 test.wav
# 3. aplay test.wav


#import pyaudio
# xx pip3 install pyaudio
# xx pip3 install python3-pyaudio
#sudo apt-get install python3-dev
#sudo apt-get install python-pyaudio
#sudo apt-get install python3-pyaudio

#pyaud = pyaudio.PyAudio()

#!/usr/bin/env python3
import pyaudio
import wave

CHUNK = 512
FORMAT = pyaudio.paInt16 #paInt8
CHANNELS = 1
RATE = 44100 #sample rate
RECORD_SECONDS = 5
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
