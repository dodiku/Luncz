from __future__ import print_function
import pyaudio
import wave
import datetime
import librosa
import numpy as np
import csv

# RECORDING A SOUND USING PYAUDIO
CHUNK = 1024
FORMAT = pyaudio.paInt32
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
AUDIO_OUTPUT_TYPE = ".wav"
WAVE_OUTPUT_FILENAME_NO_EXTENSION = "_recordings/" + datetime.datetime.now().isoformat()
WAVE_OUTPUT_FILENAME = "_recordings/" + datetime.datetime.now().isoformat() + AUDIO_OUTPUT_TYPE

audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT,
                	channels=CHANNELS,
                	rate=RATE,
                	input=True,
                	frames_per_buffer=CHUNK)

print ('* * * * * * * * * * * * * * * * * * * * * *')		
print ('RECORDING...')
print ('* * * * * * * * * * * * * * * * * * * * * *')    

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print ('* * * * * * * * * * * * * * * * * * * * * *')		
print ('DONE RECORDING')
print ('* * * * * * * * * * * * * * * * * * * * * *')

stream.stop_stream()
stream.close()
audio.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

"""""""""""""""""""""""""""""""""""""""
1 - loading a file
"""""""""""""""""""""""""""""""""""""""
filename = WAVE_OUTPUT_FILENAME
y, sr = librosa.load(filename)

"""""""""""""""""""""""""""""""""""""""
2 - get tempo == bpm
"""""""""""""""""""""""""""""""""""""""
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
print('Estimated tempo: {:.2f} beats per minute'.format(tempo))

# generate csv files with beat times
CSV_FILENAME = WAVE_OUTPUT_FILENAME_NO_EXTENSION + ".csv"

beat_times = librosa.frames_to_time(beat_frames, sr=sr)
librosa.output.times_csv(CSV_FILENAME, beat_times)
print ('beat_times.csv done')

# # converting csv to json
# with open('beat_times.csv') as f:
#     reader = csv.DictReader(f, fieldnames=['beat'])
#     rows = list(reader)
# with open('beat_times.json', 'w') as f:
#     json.dump(rows, f)
# print ('beat_times.json done')
"""""""""""""""""""""""""""""""""""""""
3 - get notes
"""""""""""""""""""""""""""""""""""""""

"""""""""""""""""""""""""""""""""""""""
3 - get timbre
"""""""""""""""""""""""""""""""""""""""

print ("done :)")