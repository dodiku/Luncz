import ctcsound
cs = ctcsound.Csound()

csd = '''
<CsoundSynthesizer>

<CsOptions>
  -d -o dac -m0
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
</CsScore>
</CsoundSynthesizer>
'''
cs.compileCsdText(csd)
cs.start()

pt = ctcsound.CsoundPerformanceThread(cs.csound())
pt.play()

pt.scoreEvent(False, 'i', (1, 2, 10, 0.5, 8.06, 0.05, 0.3, 0.5))
pt.scoreEvent(False, 'i', (1, 0.5, 1, 0.5, 9.06, 0.05, 0.3, 0.5))
pt.scoreEvent(False, 'i', (1, 4.5, 1, 0.5, 9.06, 0.05, 0.3, 0.5))
# pt.record('b.wav', 1000, 1)
pt.stop()
pt.join()