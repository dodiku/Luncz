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

# # MOVING ALL EXISTING FILES TO A BACKUP DIRECTORY
# old_files = os.listdir(source)
# print (old_files)
# for file in old_files:
# 	if not file == ".DS_Store":
# 		file_path = source + file
# 		shutil.move(file_path, destination) 


# STARTING CSOUND
cs = ctcsound.Csound()

ret = cs.compile_("csound", "-o", "dac", "/Users/drorayalon/Documents/code/#itp/Csound/05-Luncz/Luncz.csd") # new laptop
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
		for file in new_files:
			if file.endswith(".csv"):
				print ("-=-=-=-=-=-=-=-=-=-=-=-=-=-")
				print (file)

				# GETTING DATA FROM CSV FILE
				file_path = source + file
				print (file_path)
				open_file = open(file_path)
				csv_file = csv.reader(open_file)
				for row in csv_file:
					beat_list.append(row[0])
				open_file.close()
				print (beat_list)
    			print ("-=-=-=-=-=-=-=-=-=-=-=-=-=-")

    			# ADDING SCORE EVENTS
    			for beat in beat_list:
    				pt.scoreEvent(False, 'i', (100, beat, 0.3, 0.2))

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