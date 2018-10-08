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

I started this project to see if there was any truth to the old saying that music is a conversation. After converting the pitch bins to MIDI data I found that regular speech is too unemotive and too frequently interrupted while most music is highly emotive and highly continuous. 
For future development I would like to find a data set of background speech and compare it to background music (such as trance or classical).

