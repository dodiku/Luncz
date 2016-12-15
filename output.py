from __future__ import print_function
import librosa
import numpy as np
import csv
import ctcsound
# import glob
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
print (old_files)
for file in old_files:
	if not file == ".DS_Store":
		file_path = source + file
		shutil.move(file_path, destination) 


# STARTING CSOUND
cs = ctcsound.Csound()

ret = cs.compile_("csound", "-o", "dac", "/Users/drorayalon/Documents/code/#itp/Csound/05-Luncz/Luncz.csd") # new laptop
# ret = cs.compile_("csound", "-o", "dac", "/Users/dodik/Documents/code/#ITP/Csound/05-Luncz/Luncz.csd") # old laptop

if ret == ctcsound.CSOUND_SUCCESS:
	cs.start()
	pt = ctcsound.CsoundPerformanceThread(cs.csound())
	pt.play()
	# pt.scoreEvent(False, 'i', (102, 1, 1, 0.2, 0))
	while not cs.performBuffer():

		# SEARCHING FOR NEW CSV FILES ON THE '_RECORDINGS' DIRECTORY
		new_files = os.listdir(source)
		beat_list = []
		original_beat_times = []
		tempo_beat_times = []
		recording_tempo = 1
		data = []

		print ("-=-=-=-=-=-BEGIN-=-=-=-=-=-")

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

					# print ('tempo line:', line)
					# print (data)
					# data.append(9)
				recording_tempo = data[0]
				print ('tempo float (recording_tempo):', recording_tempo)
    			print ('data:', data)
		for file in new_files:
			if file.endswith(".csv"):

				# pt.scoreEvent(False, 'i', (100, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3))
				version = version + 1
				pt.scoreEvent(False, 'i', (101, 0, 0.0001, version))

				# GETTING DATA FROM CSV FILE
				print ('csv file:', file)
				
				file_path = source + file
				print (file_path)
				open_file = open(file_path)
				csv_file = csv.reader(open_file)
				for row in csv_file:
					beat_list.append(row[0])
				open_file.close()
				print ('beat list:', beat_list)

				for beat in beat_list:
					# original_beat_times.append(float(beat)*60/recording_tempo)
					original_beat_times.append(float(beat))


				print ('original beat onset times:', original_beat_times)

				# CALCULATE NOTE DURATION
				# note_duration = 10*60/recording_tempo
				# print ('note durations:', note_duration)

    			# CALCULATE NOTES ONSET TIMES
    			# last_beat_ends = 0
    			# next_beat_starts = 0
    			# for beat in range(len(original_beat_times)):
    			# 	print ('aaa')
    			# 	if beat == 0:
    			# 		last_beat_ends = original_beat_times[beat] + note_duration
    			# 		tempo_beat_times.append(original_beat_times[beat])
    			# 		continue
    			# 	else:
    			# 		print ('bbb')
    			# 		# last_beat_ends = original_beat_times[beat-1] 
    			# 		next_beat_starts = original_beat_times[beat]
    			# 		previous_beat_starts = original_beat_times[beat-1]
    			# 		delta = next_beat_starts - previous_beat_starts
    			# 		run = True
    			# 		while run == True:
    			# 			if (next_beat_starts - tempo_beat_times[beat-1]) < note_duration:
    			# 				next_beat_starts = next_beat_starts + delta
    			# 			else:
    			# 				next_beat_starts = next_beat_starts - delta
    			# 				tempo_beat_times.append(next_beat_starts)
    			# 				run = False
    			# 				print('while ended')

    					# while note_duration >= (next_beat_starts - last_beat_ends):
    					# 	print (next_beat_starts, original_beat_times[beat], original_beat_times[beat-1], last_beat_ends)
    					# 	next_beat_starts = next_beat_starts + (original_beat_times[beat] - original_beat_times[beat-1])
    					# print('while ended')
    					# next_beat_starts = next_beat_starts - (original_beat_times[beat] - original_beat_times[beat-1])
    					# tempo_beat_times.append(next_beat_starts)
    					# last_beat_ends = next_beat_starts
					# print ('new beat onset times:', tempo_beat_times)				

				# ADDING SCORE EVENTS
				# delay_time = recording_tempo/60*5
				
				# last_beat = original_beat_times[len(original_beat_times)-1]
				# first_beat = original_beat_times[0]
				# next_first_beat = 5 - last_beat + first_beat
				# repeat = 1
				# number_of_notes = 0
				n = 1
				print ('====== sending =======')
				# pt.scoreEvent(False, 'i', (100, 0, 1, 0.2, cpspch_array[data[n]], version, 1, recording_tempo))
				# print (100, 0, 1, 0.2, cpspch_array[data[n]], version, 1, recording_tempo)
				for time in original_beat_times:
					# pt.scoreEvent(False, 'i', (100, time, 1, 0.2, time+5, number_of_notes, next_first_beat))

					# pt.scoreEvent(False, 'i', (p1, p2, p3, p4, p5, p6))
					# 90*2/60

					# s_per_beat = 60 / recording_tempo
					# s_per_measure = s_per_beat * number_of_beats
					# loop_length = s_per_measure * loop_measures

					s_per_beat = 60 / recording_tempo
					s_per_measure = s_per_beat * len(beat_list)
					loop_length = s_per_measure * 1

					modified_time = recording_tempo*time/60

					if (loop_length <= 6) and (time == original_beat_times[len(original_beat_times)-1]):
						continue

					if (loop_length - modified_time) < 0:
						continue

					# pt.scoreEvent(False, 'i', (100, modified_time, 1, 0.2, cpspch_array[data[n]], version, 1, recording_tempo, loop_length))
					# print (100, modified_time, 1, 0.2, cpspch_array[data[n]], version, 1, recording_tempo, loop_length)
					if 6 - modified_time < 0.8:
						pt.scoreEvent(False, 'i', (100, modified_time, 1, 0, cpspch_array[data[n]], version, 1, recording_tempo, loop_length))
					else:
						pt.scoreEvent(False, 'i', (100, modified_time, 1, 0.2, cpspch_array[data[n]], version, 1, recording_tempo, loop_length))
						print (100, modified_time, 1, 0.2, cpspch_array[data[n]], version, 1, recording_tempo, loop_length)
					n = n+1
				print ('====== end =======')



				# note_number = 0
				# time = 0
				# freq = 0
				# delta = 0
				# try:
				# 	original_beat_times[0]
				# 	time1 = original_beat_times[0]
				# 	freq1 = cpspch_array[data[1]-1]
				# 	# freq1 = 220
				# 	# print (data[1]-1, cpspch_array[data[1]-1])
				# 	note_number = 1
				# 	delta = 5 - original_beat_times[0]
				# except:
				# 	time1 = 0
				# 	freq1 = 0

				# try:
				# 	original_beat_times[1]
				# 	time2 = original_beat_times[1]
				# 	# freq2 = 220
				# 	freq2 = cpspch_array[data[2]-1]
				# 	# print (data[2]-1, cpspch_array[data[2]-1])
				# 	note_number = 2
				# 	delta = 5 - original_beat_times[1]
				# except:
				# 	time2 = 0
				# 	freq2 = 0

				# try:
				# 	original_beat_times[2]
				# 	time3 = original_beat_times[2]
				# 	freq3 = cpspch_array[data[3]-1]
				# 	# freq3 = 220
				# 	# print (data[3]-1, cpspch_array[data[3]-1])
				# 	note_number = 3
				# 	delta = 5 - original_beat_times[2]
				# except:
				# 	time3 = 0
				# 	freq3 = 0

				# try:
				# 	original_beat_times[3]
				# 	time4 = original_beat_times[3]
				# 	freq4 = cpspch_array[data[4]-1]
				# 	# freq4 = 220
				# 	# print (data[4]-1, cpspch_array[data[4]-1])
				# 	note_number = 4
				# 	delta = 5 - original_beat_times[3]
				# except:
				# 	time4 = 0
				# 	freq4 = 0

					
				# version = version + 1
				# # print ('====== clearing score (that will take 5 seconds) =======')
				# # sleep(0.5)
				# if recording_tempo == 0:
				# 	recording_tempo = 60
				# print ('====== sending =======')
				# print (100, 0, 1, time, freq, time1, freq1, time2, freq2, time3, freq3, time4, freq4, delta, note_number, 1, version, recording_tempo)
				# print ('====== end =======')
				# pt.scoreEvent(False, 'i', (100, 0, 1, time, freq, time1, freq1, time2, freq2, time3, freq3, time4, freq4, delta, note_number, 1, version, recording_tempo))

					# number_of_notes = number_of_notes + 1
					# print ('number_of_notes:', number_of_notes)
					# print ('next first beat:', next_first_beat)
    				# beat_time = previous_beat_time + note_duration + beat
    				# previous_beat_time = beat_time
    				# beat_in_tempo = beat 
    				
    				# previous_beat_time = beat_time
				# pt.scoreEvent(False, 'i', (100, (original_beat_times[len(original_beat_times)-1]+1), 5, 0))
				# pt.scoreEvent(False, 'i', (100, (tempo_beat_times[len(tempo_beat_times)-1]+note_duration), 5, 0.20))
		

				# MOVING ALL EXISTING FILES TO A BACKUP DIRECTORY
				old_files = os.listdir(source)
				print (old_files)
				for file in old_files:
					if not file == ".DS_Store":
						file_path = source + file
						shutil.move(file_path, destination) 

				print ("-=-=-=-=-=-END-=-=-=-=-=-")

				

		

		# CLEARING THE DIRECTORY

		# 

		### look for a new file....


		cs.sleep(5000)

	pt.stop()
	pt.join()


del cs

# ret = cs.compileCsdText(csd)
# if ret == ctcsound.CSOUND_SUCCESS:
# 	cs.start()
# 	# cs.perform()
# 	# cs.reset()

# 	pt = ctcsound.CsoundPerformanceThread(cs.csound())
# 	pt.play()

# 	pt.scoreEvent(False, 'i', (1, 0, 2, 0.5, 8.06, 0.05, 0.3, 0.5))

# 	cs.sleep(2000)

# 	pt.stop()
# 	pt.join()


# del cs