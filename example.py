import ctcsound
cs = ctcsound.Csound()

csd = '''
<CsoundSynthesizer>

<CsOptions>
  -o dac -m0
</CsOptions>

<CsInstruments>
sr     = 48000
ksmps  = 100
nchnls = 2
0dbfs  = 1

          instr 1
idur      =         p3
iamp      =         p4
icps      =         cpspch(p5)
irise     =         p6
idec      =         p7
ipan      =         p8

kenv      linen     iamp, irise, idur, idec
kenv      =         kenv*kenv
asig      poscil    kenv, icps
a1, a2    pan2      asig, ipan
          outs      a1, a2
          endin
</CsInstruments>

<CsScore>
f 0 14400    ; a 4 hours session should be enough

i 1 0 1 0.5 7.06 0.05 0.3 0.5
;e 1.5

</CsScore>
</CsoundSynthesizer>
'''
print csd
ret = cs.compileCsdText(csd)
if ret == ctcsound.CSOUND_SUCCESS:
	cs.start()
	# cs.perform()
	# cs.reset()

	pt = ctcsound.CsoundPerformanceThread(cs.csound())
	pt.play()

	# cs.sleep(8000)

	pt.scoreEvent(False, 'i', (1, 0.5, 2, 0.5, 8.06, 0.05, 0.3, 0.5))

	# cs.sleep(8000)

	cs.sleep(4000)

	pt.stop()
	pt.join()


del cs