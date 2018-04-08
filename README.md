# PitchWitch

README

---

This is a spectrum analyzer with color-coding and grouping across octaves to improve comprehension speed.

WARNING: This project is giving me synesthesia.

---

Required Packages: 

	-Python3 
	-Numpy	
	-Scipy
	-PyAudio
	-PyQtGraph
	

Usage: 

	python3 spectra.py 
		or
	python3 spectra.py X Y
	
Where X is the lower octave and Y is the higher octave. The lower the bottom octave, the choppier the analyzer will be due to FFT constraints. 

Omitting X and Y defaults an octave range of 3 to 6.

Run with "-help" to see this description.


---

I developed it to see if there were any immediately recognizable patterns in peoples' voice pitches. I noticed a few minor patterns like people repeatedly ending sentences on the same note but it was too chaotic for me to pursue further at this point. 
For future development I would like to turn recorded speech into MIDI data and run it on a machine learning model to see how it compares to music. 

