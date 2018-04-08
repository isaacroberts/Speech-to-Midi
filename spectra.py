import pyaudio
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
from scipy.fftpack import fft

import time
import sys
import array as ar

np.set_printoptions(threshold=np.inf)

FREQ_RANGE=(3,6)

TONES=np.array(['A','A#','B','C','C#','D','D#','E','F','F#','G','G#'])

FREQS=np.array([])
NOTES=np.array([])

def setup_constants(low_octave=FREQ_RANGE[0],high_octave=FREQ_RANGE[1]):
	global FREQS
	global NOTES
	global FREQ_RANGE

	FREQ_RANGE=(low_octave,high_octave)

	FREQS=np.exp2(np.arange(FREQ_RANGE[0]-4,FREQ_RANGE[1]-3,1./12.)) * 440.

	FREQS=np.concatenate(
	(np.array([FREQS[0]*.95]), FREQS,np.array([np.inf]))
	)

	nums=np.array(np.arange(FREQ_RANGE[0],FREQ_RANGE[1]+1).astype(str))
	nums=nums.reshape(-1,1)

	NOTES=np.core.defchararray.add(TONES,nums)
	NOTES=NOTES.reshape(-1,)
	NOTES=np.concatenate(
	(np.array(['Lo']),NOTES,np.array(['Hi']))
	)



class PitchWitch(object):



	def callback(self,in_data, frame_ct,time_info,status):

		self.update(in_data)
		"""
		self.findPitches(self.bar_freqs)
		l=frame_ct
		for n in range(0,l):
			sin=0
			for ix,amp in self.playing.items():
				sin+=amp*np.sin(self.phase*FREQS[ix])
			for i in range(0,CHANNELS):
				self.outbuffer[n+i*l] =  sin
			self.phase +=2*np.pi/RATE
		return (bytes(self.outbuffer),pyaudio.paContinue)
		"""
		self.t+=1
		return (None,pyaudio.paContinue)



	def __init__(self):

		p=pyaudio.PyAudio()

		output_info=p.get_default_output_device_info()

		self.CHUNK = 1024*1
		self.WIDTH = 4
		self.FORMAT = p.get_format_from_width(self.WIDTH)
		self.CHANNELS=1
		self.RATE = int(output_info['defaultSampleRate'])

		if (self.CHANNELS>output_info['maxOutputChannels']):
			self.CHANNELS=output_info['maxOutputChannels']

		res=26* 2**(FREQ_RANGE[0]-4)
		min_window=self.RATE/res
		min_window=2**np.ceil(np.log2(min_window))
		if self.CHUNK < min_window:
			self.CHUNK=int(min_window)

		self.amp_scale=1

		if self.WIDTH==1:
			self.np_datatype=np.int8
			self.amp_scale=1./127.
		elif self.WIDTH==2:
			self.np_datatype=np.int16
			self.amp_scale=1./32767.
		elif self.WIDTH==4:
			self.np_datatype=np.float32
			self.amp_scale=1
		else:
			print("ERROR: Unrecognized Data Width ",self.WIDTH)
		# For Callback function
		#self.phase=0
		#self.outbuffer=ar.array('f',range(self.CHUNK*self.CHANNELS))

		pg.setConfigOptions(antialias=True)

		#----Graph Stuff------

		self.barx=np.zeros(len(NOTES))
		self.wfx=np.arange(0,self.CHUNK)
		self.wfy=np.zeros(self.CHUNK)

		self.app=QtGui.QApplication(sys.argv)
		self.win=pg.GraphicsWindow(title='Spectra')
		#self.win.setGeometry(5,115,1000,1000)

		wf_xlabels = [(0, '0'), (2048, '2048'), (4096, '4096')]
		wf_xaxis = pg.AxisItem(orientation='bottom')
		wf_xaxis.setTicks([wf_xlabels])

		wf_ylabels = [(-64,'-1'), (0, '0'), (64, '1')]
		wf_yaxis = pg.AxisItem(orientation='left')
		wf_yaxis.setTicks([wf_ylabels])
		self.waveform = self.win.addPlot(
			title='WAVEFORM', row=1, col=1, axisItems={'bottom': wf_xaxis, 'left': wf_yaxis},
		)

		self.wf=self.waveform.plot(pen='c',w=1)
		self.waveform.setYRange(-.05,.05,padding=0)
		self.waveform.setXRange(0,self.CHUNK,padding=.005)

		sp_xaxis = pg.AxisItem(orientation='bottom')
		z=list(zip(np.arange(0,len(NOTES)),NOTES))
		ticks=[z[::2],z]
		sp_xaxis.setTicks(ticks)


		self.barx=np.arange(0,len(NOTES))
		self.bar_freqs=np.zeros(len(NOTES))
		self.play_graph=np.zeros(len(NOTES))
		self.df=np.zeros(len(NOTES))
		self.plot = self.win.addPlot(
            title='SPECTRUM', row=2, col=1,colspan=2, axisItems={'bottom': sp_xaxis},
        )

		SPECTRA_COLOR=QtGui.QColor(255,255,0)
		HAB_COLOR=QtGui.QColor(0,0,0)

		self.spectrum = pg.BarGraphItem(x=self.barx,height=self.bar_freqs,
			width=.4,brush=SPECTRA_COLOR
			)
		self.hab=pg.BarGraphItem(x=self.barx,height=self.play_graph,width=.1,
			brush=HAB_COLOR,pen=HAB_COLOR)
		self.plot.setXRange(0,len(NOTES),padding=.05)
		self.plot.setYRange(0,100,padding=0)

		self.plot.addItem(self.spectrum)
		self.plot.addItem(self.hab)

		#----Chroma Plot-------
		chroma_xlabels=list(zip(np.arange(0,12),TONES))

		chroma_colors=np.array([
			#| A, A#, B
			QtGui.QColor(255,135,0),QtGui.QColor(230,50,50),QtGui.QColor(230,230,230),
			#| C, C#, D
			QtGui.QColor(0,200,250),QtGui.QColor(50,50,135),QtGui.QColor(150,90,25),
			#| D#, E, F
			QtGui.QColor(175,96,112),QtGui.QColor(150,10,150),QtGui.QColor(250,240,0),
			#| F#, G, G#
			QtGui.QColor(0,0,0),QtGui.QColor(40,120,40),QtGui.QColor(50,250,50),
			])
		color_range=[QtGui.QColor(240,240,240)]
		color_range=np.append(color_range,
			np.tile(chroma_colors,FREQ_RANGE[1]-FREQ_RANGE[0]+1),axis=0)
		color_range=np.append(color_range,
			[QtGui.QColor(0,0,0)],axis=0)

		self.spectrum.setOpts(brushes=color_range)
		#self.hab.setOpts(pens=color_range)
		self.hab.setOpts(brushes=color_range)

		chroma_yaxis= pg.AxisItem(orientation='left')

		chroma_xaxis=pg.AxisItem(orientation='bottom')
		chroma_xaxis.setTicks([chroma_xlabels])

		self.chroma_plot=self.win.addPlot(
		title='CHROMA',row=1,col=2,axisItems={'bottom':chroma_xaxis,'left':chroma_yaxis},
		)
		self.chroma_freqs=np.zeros(12)
		self.chroma=pg.BarGraphItem(x=np.arange(0,12),height=self.chroma_freqs,width=.75,brush=HAB_COLOR)
		self.chroma.setOpts(brushes=chroma_colors)

		self.chroma_plot.setXRange(0,12,padding=.075)
		self.chroma_plot.setYRange(0,1,padding=0.1)
		self.chroma_plot.addItem(self.chroma)

		self.updated=False

		#---------FFT Math---------
		fftfreqs=np.fft.fftfreq(self.CHUNK,self.CHUNK/self.RATE)*self.CHUNK
		fftfreqs=np.abs(fftfreqs[0:int(self.CHUNK)])

		#fftfreqs=1./fftfreqs
		#print(fftfreqs)
		freq_boundaries=FREQS*(2**(1./24.))
		self.bins=np.digitize(fftfreqs,bins=freq_boundaries,right=False)
		#print(self.bins)

		#------PyAudio Stuff--------

		self.playing={}

		self.stream = p.open(
			format=self.FORMAT,
			channels=self.CHANNELS,
			rate=self.RATE,
			input=True,
			output=False,
			frames_per_buffer=self.CHUNK,
			stream_callback=(self.callback)
		)
		# QTimer
		SAMPLE_INTERVAL=10
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.draw)
		self.timer.start(SAMPLE_INTERVAL)


	def run(self):
		self.t=0
		tstart=time.time()
		self.app.exec_()
		#print("fps=",((self.t)/(time.time()-tstart)))


	def update(self,data):

		if self.CHANNELS > 1:
			data=data[:self.CHUNK*self.WIDTH]

		data_int=np.fromstring(data,self.np_datatype)
		self.wfy=np.array(data_int,self.np_datatype)

		self.wfy=self.wfy*self.amp_scale

		fy=np.abs(np.fft.fft(self.wfy)[0:self.CHUNK])

		cur_freqs=np.zeros(len(NOTES))
		cur_freqs[self.bins]+=fy

		self.df=cur_freqs-self.bar_freqs

		self.bar_freqs+=self.df*.5

		buckets=self.bar_freqs[1:len(NOTES)-1].reshape((-1,12))

		self.chroma_freqs=np.sum(buckets,axis=0).reshape((-1,))
		self.chroma_freqs-=np.mean(self.chroma_freqs)
		self.chroma_freqs[self.chroma_freqs<0.1]=0
		sum=np.sum(self.chroma_freqs)
		if sum>5:
			self.chroma_freqs/=sum
		else:
			self.chroma_freqs=np.zeros(12)

		#self.play_graph [ self.play_graph < 0 ] =0

	def findPitches(self,freqs):
		for key,val in list(self.playing.items()):
			if val > 1:
				val*=.95
			elif val > .1:
				val-=.01
			else:
				val=0
			if val<=0:
				del self.playing[key]
				self.play_graph[key]=0
			else:
				self.playing[key]=val
				self.play_graph[key]=val*20
		top=np.maximum(freqs,2)
		for n in range(0,len(top)):
			if top[n]>0 and freqs[top[n]] > 5:
				set= max(self.playing.get(top[n],0),n+1)
				self.playing[top[n]] = set
				self.play_graph[top[n]] = set*20

	def barcolors(self):

		colorbins=np.digitize(self.df,[-1e10,-100,-10,-1,0,1,10,100,1e10])


		colors=np.array([ QtGui.QColor(255,255,0),
			QtGui.QColor(0,0,200), QtGui.QColor(100,100,200), QtGui.QColor(150,150,250),
			QtGui.QColor(150,150,150),
			QtGui.QColor(150,250,150), QtGui.QColor(100,200,100), QtGui.QColor(0,200,0),
			QtGui.QColor(255,255,0),QtGui.QColor(255,255,255)])

		return colors[colorbins]

	def draw(self):

		#self.hab.setOpts(height=self.play_graph)
		self.spectrum.setOpts(height=self.bar_freqs)
		self.wf.setData(self.wfx,self.wfy)

		self.chroma.setOpts(height=self.chroma_freqs)



if __name__ =='__main__':
	global pw

	if len(sys.argv)>=2:
		if "h" in sys.argv[1]:
			print(
			"""
Usage: python spectra.py X Y
Where x and y is a range of octaves.
The lower the bottom octave, the choppier the
analyzer will be due to FFT constraints.
Omitting x and y defaults to octaves 3 to 6.

			""")
		exit(0)
	if len(sys.argv)>=3:
		low=int(sys.argv[1])
		high=int(sys.argv[2])
		if high<low:
			temp=low
			low=high
			high=temp
		setup_constants(low,high)
	else:
		setup_constants()
	pw=PitchWitch()
	pw.run()
