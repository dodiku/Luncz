from __future__ import print_function
import pyaudio
import wave
import datetime
import librosa
import numpy as np
import csv
import os
import shutil
from time import sleep

source = './_recordings/'
destination = './_recordings/backup/'

# RECORDING A SOUND USING PYAUDIO
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10
AUDIO_OUTPUT_TYPE = ".wav"
WAVE_OUTPUT_FILENAME_NO_EXTENSION = "_recordings/" + datetime.datetime.now().isoformat()
WAVE_OUTPUT_FILENAME = "_recordings/" + datetime.datetime.now().isoformat() + AUDIO_OUTPUT_TYPE

audio = pyaudio.PyAudio()

print ('* * * * * * * * * * * * * * * * * * * * * *')
print ('1...')
print ('* * * * * * * * * * * * * * * * * * * * * *')
sleep(1)

print ('* * * * * * * * * * * * * * * * * * * * * *')
print ('2...')
print ('* * * * * * * * * * * * * * * * * * * * * *')
sleep(1)

print ('* * * * * * * * * * * * * * * * * * * * * *')
print ('3...')
print ('* * * * * * * * * * * * * * * * * * * * * *')
sleep(1)

print ('* * * * * * * * * * * * * * * * * * * * * *')
print ('RECORDING...')
print ('* * * * * * * * * * * * * * * * * * * * * *')

stream = audio.open(format=FORMAT,
                	channels=CHANNELS,
                	rate=RATE,
                	input=True,
                	frames_per_buffer=CHUNK)

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
print ('* * * * * * * * * * * * * * * * * * * * * *')
print('Estimated tempo: {:.2f} beats per minute'.format(tempo))
print ('* * * * * * * * * * * * * * * * * * * * * *')

# generate csv files with beat times
CSV_FILENAME = WAVE_OUTPUT_FILENAME_NO_EXTENSION + ".csv"

beat_times = librosa.frames_to_time(beat_frames, sr=sr)
librosa.output.times_csv(CSV_FILENAME, beat_times)

# WRITING A FILE WITH THE TEMPO
TEXT_FILENAME = WAVE_OUTPUT_FILENAME_NO_EXTENSION + ".txt"
bpm_value = open(TEXT_FILENAME, 'w')
tempo_text = str(tempo) + '\n'
bpm_value.write(tempo_text)


"""""""""""""""""""""""""""""""""""""""
3 - get notes
"""""""""""""""""""""""""""""""""""""""
hz = librosa.feature.chroma_cqt(y=y, sr=sr)

## GET STRONGEST OCTAVE
strongest_octave = 0
strongest_octave_sum = 0
for octave in range(len(hz)):
	sum = 0
	for frame in hz[octave]:
		sum = sum + frame
	if sum > strongest_octave_sum:
		strongest_octave_sum = sum
		strongest_octave = octave

## GET HEIGHEST HZ FOR EACH TIME FRAME
strongest_hz = []
for i in range(len(hz[0])):
	strongest_hz.append(0)

notes = []
for i in range(len(hz[0])):
	notes.append(0)

for frame_i in range(len(hz[0])):
	strongest_temp = 0
	for octave_i in range(len(hz)):

		if hz[octave_i][frame_i] > strongest_temp:
			strongest_temp = hz[octave_i][frame_i]
			strongest_hz[frame_i] = octave_i + 1
			notes[frame_i] = librosa.hz_to_note(hz[octave_i][frame_i])

# C C# D D# E F F# G G# A  A# B
# 1 2  3 4  5 6 7  8 9  10 11 12
strongest_hz_sum = [0,0,0,0,0,0,0,0,0,0,0,0]
for note in strongest_hz:
	strongest_hz_sum[note-1] = strongest_hz_sum[note-1] + 1

for i in range(len(strongest_hz_sum)):
	strongest_hz_sum[i] = float(strongest_hz_sum[i]) / len(strongest_hz)

notes_sorted = [0,0,0,0,0,0,0,0,0,0,0,0]
for num in range(len(notes_sorted)):
	 biggest = strongest_hz_sum.index(max(strongest_hz_sum))
	 notes_sorted[num] = biggest+1
	 strongest_hz_sum[biggest] = strongest_hz_sum[biggest] - 0.25

for note in notes_sorted:
	note_string = str(note) + '\n'
	bpm_value.write(note_string)

bpm_value.close()

print ('* * * * * * * * * * * * * * * * * * * * * *')
print ('RECORDING ANALYSIS COMPLETED SUCCESSFULLY :)')
print ('* * * * * * * * * * * * * * * * * * * * * *')
