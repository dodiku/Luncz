from __future__ import print_function
import librosa
import numpy as np
import csv
import ctcsound

cs = ctcsound.Csound()

'''''''''''''''''''''''''''
starting the main thread
'''''''''''''''''''''''''''
ret = cs.compile_("csound", "-o", "dac", "/Users/drorayalon/Documents/code/#itp/Csound/05-Luncz/Luncz.csd")
if ret == ctcsound.CSOUND_SUCCESS:
	cs.start()
	pt = ctcsound.CsoundPerformanceThread(cs.csound())
	pt.play()
	pt.scoreEvent(False, 'i', (102, 1, 1, 0.2, 0))
	print ('yyyy')
	while not cs.performBuffer():
		# pt.scoreEvent(False, 'i', (102, 1, 1, 0.2, 0, 2))

		### look for a new file....
		print ('* * * * * * * * * * * * * * * * * * * * * *')		
		print ('looking for a new recording data...')
		print ('* * * * * * * * * * * * * * * * * * * * * *')

		cs.sleep(5000)
	pt.stop()
	pt.join()


del cs

filename = "/_recordings/1-03 Believe.mp3"
y, sr = librosa.load(filename)

tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
print('Estimated tempo: {:.2f} beats per minute'.format(tempo))

beat_times = librosa.frames_to_time(beat_frames, sr=sr)
librosa.output.times_csv('/_recordings/beats/beat_times.csv', beat_times)
print ('beat_times.csv done')

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