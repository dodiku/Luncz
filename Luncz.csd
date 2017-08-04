<CsoundSynthesizer>
<CsInstruments>
sr     = 44100
kr     = 4410
ksmps  = 10
nchnls = 2
0dbfs = 1.0

gibeats = 0
giversion = 0
gitempo = 60.0
gifreq1 = 0.0
giloop_length = 6


;------------------------------------------------------------------------------
; Instrument: Beats
;------------------------------------------------------------------------------

instr 100

iduration = 2
iamplitude = 0.3
iattack = 0.001
iduration = p3
ifreq = cpspch (p5-1)


if (p7 == 1) then
	gitempo = p8
	giloop_length = p9
endif


aenv linseg 0, iduration * iattack, iamplitude, iduration * ( 1 - iattack ), 0
ares poscil3 aenv, ifreq, 1
ares moogvcf ares, 2000, 0.2
outs ares, ares


if (p6 == giversion) then
	schedule 100, 6, p3, p4, p5, p6, 0, p8, p9
	gifreq1 = p5
endif

endin


;------------------------------------------------------------------------------
; Instrument: Recording version tracker
;------------------------------------------------------------------------------

instr 101

giversion = p4

endin


;------------------------------------------------------------------------------
; Instrument: Background music
;------------------------------------------------------------------------------

instr 102

iduration = p3
iattack = 0.5
icurrentnote = 0
inoteC = cpspch (6.0)
inoteG = cpspch (6.07)
inoteD = cpspch (5.2)
itimbre = p7

kNotesArray[] init 3
kNotesArray[] fillarray inoteC, inoteG, inoteD
alfo = 0

if (gifreq1 == 0) then
	kfreq = kNotesArray[p6]
	iamplitude = 0.1
	itable1 = 2
	itable2 = 2
else
	icurrentnote = gifreq1
	kfreq = cpspch (icurrentnote)
	iamplitude = 0.1
	itable1 = 3
	itable2 = 2
	alfo lfo 2, 8
endif



if (p6 == 0) && (p5 == 1) then
	schedule p1, 12*60/gitempo*0.8, 12*60/gitempo, iamplitude, 1 ,1, itable1
	schedule p1, 12*60/gitempo*0.8, 12*60/gitempo, iamplitude, 0 ,1, itable2

elseif (p6 == 1) && (p5 == 1)  then
	schedule p1, 12*60/gitempo*0.8, 12*60/gitempo, iamplitude, 1 ,2, itable1
	schedule p1, 12*60/gitempo*0.8, 12*60/gitempo, iamplitude, 0 ,2, itable2

elseif (p6 == 2) && (p5 == 1)  then
	schedule p1, 12*60/gitempo*0.8, 12*60/gitempo, iamplitude, 1 ,0, itable1
	schedule p1, 12*60/gitempo*0.8, 12*60/gitempo, iamplitude, 0 ,0, itable2

endif

aenv linseg 0, iduration * iattack, p4, iduration * ( 1 - iattack ), 0


ares poscil3 aenv, kfreq+alfo, itimbre
ares moogvcf ares, 400, 0.8
outs ares, ares

endin

;------------------------------------------------------------------------------
; Instrument: Open instrument to keep the piece going..
;------------------------------------------------------------------------------

instr 103

endin



</CsInstruments>
<CsScore>

f1 0 [2^16] 10 1 1 0.05 0 ; Sine
f2 0 [2^16] 10 1 0.15 6 2 1 ; default background sound
f3 0 [2^14] 10 1 0   0.3 0    0.2 0     0.14 0     .111
f4 0 [2^14] 10 1 1   1   1    0.7 0.5   0.3  0.1

i 102	0	12		0.2		1		0	2
i 103 	0 	99999999999


</CsScore>
</CsoundSynthesizer>
<bsbPanel>
 <label>Widgets</label>
 <objectName/>
 <x>100</x>
 <y>100</y>
 <width>320</width>
 <height>240</height>
 <visible>true</visible>
 <uuid/>
 <bgcolor mode="nobackground">
  <r>255</r>
  <g>255</g>
  <b>255</b>
 </bgcolor>
</bsbPanel>
<bsbPresets>
</bsbPresets>
