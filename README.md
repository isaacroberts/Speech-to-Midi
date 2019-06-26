# Speech To Midi

README

---

This is a spectrum analyzer and MIDI converter designed with the intention of using background conversation to seed music generation.

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


