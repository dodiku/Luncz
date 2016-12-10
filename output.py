from __future__ import print_function
import librosa
import numpy as np
import csv
import ctcsound
import glob
import os
import shutil

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

ret = cs.compile_("csound", "-o", "dac", "/Users/drorayalon/Documents/code/#itp/Csound/05-Luncz/Luncz.csd")
if ret == ctcsound.CSOUND_SUCCESS:
	cs.start()
	pt = ctcsound.CsoundPerformanceThread(cs.csound())
	pt.play()
	pt.scoreEvent(False, 'i', (102, 1, 1, 0.2, 0))
	while not cs.performBuffer():

		# SEARCHING FOR NEW CSV FILES ON THE '_RECORDINGS' DIRECTORY
		# new_files = os.listdir(source)
		# for file in new_files:
		# 	if not file == ".DS_Store":
		# 		#### read the file....

		# GETTING DATA FROM CSV FILE

		# CLEARING THE DIRECTORY

		# pt.scoreEvent(False, 'i', (102, 1, 1, 0.2, 0, 2))

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