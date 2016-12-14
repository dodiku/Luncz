from __future__ import print_function
import librosa
import numpy as np
import csv
import ctcsound
# import glob
import os
import shutil
import csv

new_files = []
old_files = []

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

ret = cs.compile_("csound", "-o", "dac", "/Users/drorayalon/Documents/code/#itp/Csound/05-Luncz/Luncz2.csd") # new laptop
# ret = cs.compile_("csound", "-o", "dac", "/Users/dodik/Documents/code/#ITP/Csound/05-Luncz/Luncz.csd") # old laptop

if ret == ctcsound.CSOUND_SUCCESS:
	cs.start()
	pt = ctcsound.CsoundPerformanceThread(cs.csound())
	pt.play()
	pt.scoreEvent(False, 'i', (102, 1, 1, 0.2, 0))
	while not cs.performBuffer():

		# SEARCHING FOR NEW CSV FILES ON THE '_RECORDINGS' DIRECTORY
		new_files = os.listdir(source)
		beat_list = []
		original_beat_times = []
		tempo_beat_times = []
		recording_tempo = 1

		print ("-=-=-=-=-=-BEGIN-=-=-=-=-=-")

		# GETTING THE TEMPO
		for file in new_files:
			if file.endswith(".txt"):
				
				file_path = source + file
				open_file = open(file_path)
				text_file = csv.reader(open_file)

				for line in text_file:
					print ('tempo line:', line)
    				recording_tempo = float(line[0])
    				print ('tempo float (recording_tempo):', recording_tempo)

		for file in new_files:
			if file.endswith(".csv"):

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
				
				last_beat = original_beat_times[len(original_beat_times)-1]
				first_beat = original_beat_times[0]
				next_first_beat = 5 - last_beat + first_beat
				repeat = 1
				number_of_notes = 0
				


				# note_number = 0
				# time = 0
				# freq = 220
				# try:
				# 	original_beat_times[0]
				# 	time1 = original_beat_times[0]
				# 	freq1 = 220
				# 	note_number = 1
				# 	delta = 5 - original_beat_times[0]
				# except:
				# 	pass

				# try:
				# 	original_beat_times[1]
				# 	time2 = original_beat_times[1]
				# 	freq2 = 220
				# 	note_number = 2
				# 	delta = 5 - original_beat_times[1]
				# except:
				# 	time2 = 0
				# 	freq2 = 0

				# try:
				# 	original_beat_times[2]
				# 	time3 = original_beat_times[2]
				# 	freq3 = 220
				# 	note_number = 3
				# 	delta = 5 - original_beat_times[2]
				# except:
				# 	time3 = 0
				# 	freq3 = 0

				# try:
				# 	original_beat_times[3]
				# 	time4 = original_beat_times[3]
				# 	freq4 = 220
				# 	note_number = 4
				# 	delta = 5 - original_beat_times[3]
				# except:
				# 	time4 = 0
				# 	freq4 = 0
				note_num = 1
				time_delta = 0
				first_note = original_beat_times[0]
				for time in original_beat_times:
					time_real = time - time_delta
					pt.scoreEvent(False, 'i', (100, time_real, 1, 0.15, 220, note_num, len(original_beat_times), first_note))
					time_delta = time
					note_num = note_num + 1
					print (100, time_real, 1, 0.15, note_num)

					# pt.scoreEvent(False, 'i', (p1, p2, p3, p4, p5, p6))
					# pt.scoreEvent(False, 'i', (100, time, 1, 0.15))
				# pt.scoreEvent(False, 'i', (100, 0, 1, time, freq, time1, freq1, time2, freq2, time3, freq3, time4, freq4, delta, note_number, 1))
				# print (100, 0, 1, time, freq, time1, freq1, time2, freq2, time3, freq3, time4, freq4, delta, note_number, 1)

					# number_of_notes = number_of_notes + 1
					# print ('number_of_notes:', number_of_notes)
					# print ('next first beat:', next_first_beat)
    	# 			beat_time = previous_beat_time + note_duration + beat
    	# 			previous_beat_time = beat_time
    	# 			beat_in_tempo = beat 
    				
    	# 			previous_beat_time = beat_time
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