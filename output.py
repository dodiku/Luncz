'''
Thanks a lot to https://github.com/fggp, who provided supported and assistance
with the 'ctcsound' package throughout the building process.
See the ctcsound package here: https://github.com/fggp/ctcsound
See the help thread here: https://github.com/fggp/ctcsound/issues/2
'''

from __future__ import print_function
import librosa
import numpy as np
import csv
import ctcsound
import os
import shutil
import csv
from time import sleep

new_files = []
old_files = []

version = 0

# C C# D D# E F F# G G# A  A# B
# 1 2  3 4  5 6 7  8 9  10 11 12

cpspch_array = [7.00, 7.01, 7.02, 7.03, 7.04, 7.05, 7.06, 7.07, 7.08, 7.09, 7.10, 7.11, 7.12]

source = './_recordings/'
destination = './_recordings/backup/'

# MOVING ALL EXISTING FILES TO A BACKUP DIRECTORY
old_files = os.listdir(source)
for file in old_files:
	if not (file == ".DS_Store" or file == "README.md"):
		file_path = source + file
		shutil.move(file_path, destination) 


# STARTING CSOUND
cs = ctcsound.Csound()
ret = cs.compile_("csound", "-o", "dac", "Luncz.csd")

if ret == ctcsound.CSOUND_SUCCESS:
	cs.start()
	pt = ctcsound.CsoundPerformanceThread(cs.csound())
	pt.play()
	while not cs.performBuffer():

		# SEARCHING FOR NEW CSV FILES ON THE '_RECORDINGS' DIRECTORY
		new_files = os.listdir(source)
		beat_list = []
		original_beat_times = []
		tempo_beat_times = []
		recording_tempo = 1
		data = []

		# GETTING THE TEMPO
		for file in new_files:
			if file.endswith(".txt"):
				
				file_path = source + file
				open_file = open(file_path)
				text_file = csv.reader(open_file)
				
				i = 0
				for line in text_file:
					if i == 0:
						data.append(float(line[0]))
						i += 1
					else:
						data.append(int(line[0]))

				recording_tempo = data[0]

		for file in new_files:
			if file.endswith(".csv"):

				version = version + 1
				pt.scoreEvent(False, 'i', (101, 0, 0.0001, version))

				# GETTING DATA FROM CSV FILE				
				file_path = source + file
				open_file = open(file_path)
				csv_file = csv.reader(open_file)
				for row in csv_file:
					beat_list.append(row[0])
				open_file.close()

				for beat in beat_list:
					original_beat_times.append(float(beat))

				n = 1
				print ('* * * * * * * * * * * * * * * * * * * * * *')
				print ('SENDING TO CSOUND')
				print ('* * * * * * * * * * * * * * * * * * * * * *')
				print ('Getting data from:', file)
				print ('Beat onset times:', original_beat_times)
				print ('Csound score lines:')
				for time in original_beat_times:

					s_per_beat = 60 / recording_tempo
					s_per_measure = s_per_beat * len(beat_list)
					loop_length = s_per_measure * 1

					modified_time = recording_tempo*time/60

					if (loop_length <= 6) and (time == original_beat_times[len(original_beat_times)-1]):
						continue

					if (loop_length - modified_time) < 0:
						continue

					if 6 - modified_time < 0.8:
						pt.scoreEvent(False, 'i', (100, modified_time, 1, 0, cpspch_array[data[n]], version, 1, recording_tempo, loop_length))
						print (100, modified_time, 1, 0, cpspch_array[data[n]], version, 1, recording_tempo, loop_length)
					else:
						pt.scoreEvent(False, 'i', (100, modified_time, 1, 0.2, cpspch_array[data[n]], version, 1, recording_tempo, loop_length))
						print (100, modified_time, 1, 0.2, cpspch_array[data[n]], version, 1, recording_tempo, loop_length)
					n = n+1
				print ('* * * * * * * * * * * * * * * * * * * * * *')
				print ('END')
				print ('* * * * * * * * * * * * * * * * * * * * * *')

				# MOVING ALL EXISTING FILES TO A BACKUP DIRECTORY
				old_files = os.listdir(source)
				for file in old_files:
					if not (file == ".DS_Store" or file == "README.md"):
						file_path = source + file
						shutil.move(file_path, destination)

		cs.sleep(5000)

	pt.stop()
	pt.join()


del cs