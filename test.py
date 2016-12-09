import ctcsound

cs = ctcsound.Csound()

'''''''''''''''''''''''''''
starting the main thread
'''''''''''''''''''''''''''
ret = cs.compile_("csound", "-o", "dac", "/Users/drorayalon/Documents/code/#itp/Csound/05-Luncz/test.csd")
if ret == ctcsound.CSOUND_SUCCESS:
    cs.perform()
    cs.start()
    cs.reset()

'''''''''''''''''''''''''''
starting the main thread
'''''''''''''''''''''''''''
pt = ctcsound.CsoundPerformanceThread(cs.csound())
pt.play()

pt.scoreEvent(False, 'i', (101, 1, 10, 0.2, 0, 2))
print ('yyyy')
pt.stop()
pt.join()


del cs