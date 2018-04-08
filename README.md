# PitchWitch

README

---

This is a spectrum analyzer with color-coding and pitch binning to improve comprehension speed.

---

Required Packages: 
	-Numpy
	-Scipy
	-PyAudio
	-PyQtGraph

Usage: 
	python spectra.py 
		or
	python spectra.py X Y
	
Where X is the lower octave and Y is the higher octave. The lower the bottom octave, the choppier the analyzer will be due to FFT constraints. 

Omitting X and Y defaults an octave range of 3 to 6.

Run python spectra.py -help to see this description.


---

I developed it to see if there were any immediately recognizable patterns in peoples' voice pitches. I noticed a few patterns in individuals' voice patterns but it was too chaotic for me to pursue further at this point. 
For future development I would like to use machine learning to match facial expression to voice pitch to see if there's a pattern.

After staring at it for hours I think I'm starting to develop a synesthesia-esque form of perfect pitch. More staring is needed. 


