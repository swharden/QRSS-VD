import sys
import gtk
from PIL import ImageTk
from PIL import Image
import numpy
import Tkinter
import threading
import time
import Image
import pyaudio
import numpy

from QRSS_VD_misc import *

config=config_default()
config_show(config)
data=numpy.array(numpy.random.random((config["data_height"],config["data_width"]))*50,dtype=int) #actual FFT data
data=[]
FFT_last=[] #pixel data
update=False #whether or not view window should be redrawn
dienow=False #if die, restart
pcms=[] #series of PCM segments from record()
stats={}
palette=[]#RGB values for spectrum
#raw_input("ENTER to start")


def stats_set(name,val,debug=False):
	global config
	config[name]=val
	if debug:
		print "STATS",name,"=",val

def config_set(name,val,debug=False):
	global config
	config[name]=val
	if debug:
		print "setting",name,"=",val

def newData(newdata):
	global data
	#print "DATA:",len(data),"GOT:",len(newdata)
	data=numpy.roll(data,-1,1)
	data[:,-1]=newdata

fftmins=[]
fftmaxs=[]
fftmeds=[]
def seeWhatToDo():
	"""check to see if anything needs to be done (run every update)."""
	global update, pcms, fftmins, fftmaxs, fftavgs,FFT_last
	if len(pcms)>1:
		lin=pcms.pop(0)
		lin=numpy.append(lin,pcms[0])
		for x in range(config["overlap"]):
			start=(config["binsize"]/config["overlap"])*x
			pcm=lin[start:start+config["binsize"]]
			ffty=pcm2fft(shapeTriangle(pcm))
			logger=numpy.log10(ffty+1.0)*20
			ffty=logger
			FFT_last.append(logger-config["noiseFloorDB"])
			while len(FFT_last)>config["overlap"]:FFT_last.pop(0)
			fftmins.append(numpy.min(ffty));fftmaxs.append(numpy.max(ffty));fftmeds.append(numpy.median(ffty))
			ffty=fft2pix(ffty,config["img_min"],config["img_mult"],\
				config["img_gain"],config["img_auto"],
				numpy.average(fftmins),numpy.average(fftmeds))
			if len(fftmins)>config["img_seek"]:fftmins.pop(0);fftmaxs.pop(0);fftmeds.pop(0)
			newData(ffty)
		update=True
		
recordLive=True #set to False to cause shutdown

def record():
	global pcms,dienow,recordLive
	p = pyaudio.PyAudio() 
	inStream = p.open(format=pyaudio.paInt16,\
				channels=1,rate=config["rate"],\
				input_device_index=config["soundcard"],input=True)
	pcms=[] #holds linear unprocessed data
	while True:
		if recordLive==False: 
			recordLive=True
			return
		pcm=[]
		for i in range(config["binsize"]/512):
			pcm=numpy.append(pcm,numpy.fromstring(inStream.read(512),dtype=numpy.int16))
		#print "PCM:",pcm,len(pcm)
		pcms.append(pcm)

def updatePalette():
	global palette
	palette=genPalette()
	return
		
def totalReset(*args):
	fast=False #this prevents crashes
	global t_rec,recordLive,config
	config=config_recalc(config)
	if fast==False:
		try: t_rec
		except NameError: 
			pass
		else:
			recordLive=False
			while recordLive==False:
				time.sleep(.1)
				print "waiting for RECORDER to die..."
			del t_rec
	
	t_rec=threading.Thread(target=record) 
	t_rec.daemon=True
	t_rec.start()
	
	global pcms,data
	pcms=[]
	data=numpy.array(numpy.random.random((config["data_height"],config["data_width"]))*50,dtype=int) #actual FFT data
	if fast==True: 
		return
	while len(pcms)==0: 
		time.sleep(.1)
		print "waiting for RECORDER to come alive..."
	pcms=[]
	
	

class spectrograph:
			
	def on_window_destroy2(self, *args):
		"""We clicked the X button."""
		print "IM EXITING NOW"
		time.sleep(1)
		sys.exit(0)
    
	def destroy(self,object,event=None):
		"""instead of destroying something, hide it."""
		print "HIDING",object,event
		object.hide()
		return True #MUST DO THIS!
	
	def set_viewXY(self,*args):
		config_set("window_height",int(self.in_viewY.get_text()))
		totalReset()
		self.drawScaleBars()
    
	def updateStats(self):
		stats_set("avg_max",numpy.average(fftmaxs))
		stats_set("avg_min",numpy.average(fftmins))
		stats_set("avg_med",numpy.average(fftmeds))
		imgstats="### INSTANT VALUES ###"
		imgstats+="\nMAX:\t%d"%fftmaxs[-1]
		imgstats+="\nMIN:\t%d"%fftmins[-1]
		imgstats+="\nMED:\t%d"%fftmeds[-1]
		imgstats+="\n\n### AVERAGE FOR %.02f SEC ###"%(config["img_seek"]*config["horizres"])
		imgstats+="\nMAX:\t%d"%numpy.average(fftmaxs)
		imgstats+="\nMIN:\t%d"%numpy.average(fftmins)
		imgstats+="\nMED:\t%d"%numpy.average(fftmeds)
		imgstats+="\n\n### RECENT PIXEL ROW VALUES ###"
		#hist,bins=numpy.histogram(data[:,-1],range(256))
		#print hist
		#imgstats+="\nMAX:\t%d\t(%.02f%%)"%(1,1)
		#imgstats+="\nMIN:\t%d\t(%.02f%%)"%(1,1)
		#imgstats+="\nMED:\t%d"%numpy.median(data[:,-1])
		#imgstats+="\n\n### SUGGESTED VALUES ###"
		#imgstats+="\nCONTRAST:\t%d"%(numpy.average(fftmeds)/255)
		#imgstats+="\nBRIGHTNESS:\t%d"%(numpy.average(fftmins)*-1)
		self.lbl_imgstats = self.builder.get_object("lbl_imgstats")
		self.lbl_imgstats.set_text(imgstats)
		
    
	def set_view_size(self,*args):
		self.sizer = self.builder.get_object("win_setViewerSize")
		self.in_viewX = self.builder.get_object("in_viewX")
		self.in_viewY = self.builder.get_object("in_viewY")
		self.in_viewX.set_text(str(config["window_width"]))
		self.in_viewY.set_text(str(config["window_height"]))
		self.sizer.show()
		
	def open_win_image(self,*args):
		self.win_image = self.builder.get_object("win_image")
		#self.win_image.connect("destroy", self.destroy)
		#self.win_image.connect("delete_event", self.destroy)
		self.in_absCutoff = self.builder.get_object("in_absCutoff")
		self.in_absCutoff.set_text(str(config["img_cutoff"]))
		self.adj_pixMin = self.builder.get_object("adj_pixMin")
		self.adj_pixMin.set_value(config["img_min"])
		self.adj_pixMult = self.builder.get_object("adj_pixMult")
		self.adj_pixMult.set_value(config["img_mult"])
		self.adj_pixGain = self.builder.get_object("adj_pixGain")
		self.adj_pixGain.set_value(config["img_gain"])
		self.adj_pixSeek = self.builder.get_object("adj_pixSeek")
		self.adj_pixSeek.set_value(config["img_seek"])
		self.win_image.show()
		#raw_input()
	
	def set_image_stats(self,*args):
		print "SETTING STATS"
		self.in_absCutoff = self.builder.get_object("in_absCutoff")
		self.adj_pixMin = self.builder.get_object("adj_pixMin")
		self.adj_pixMult = self.builder.get_object("adj_pixMult")
		self.adj_pixGain = self.builder.get_object("adj_pixGain")
		self.adj_pixSeek = self.builder.get_object("adj_pixSeek")
		config_set("img_cutoff",int(self.in_absCutoff.get_text()))
		config_set("img_min",self.adj_pixMin.get_value())
		config_set("img_mult",self.adj_pixMult.get_value())
		config_set("img_gain",self.adj_pixGain.get_value())
		config_set("img_seek",self.adj_pixSeek.get_value())
	
	def open_win_preview(self,*args):
		self.win_image = self.builder.get_object("win_preview")
		self.in_rate = self.builder.get_object("in_rate")
		self.in_rate.set_text(str(config["rate"]))
		self.in_binpwr = self.builder.get_object("in_binpwr")
		self.in_binpwr.set_text(str(config["binpower"]))
		self.in_overlap = self.builder.get_object("in_overlap")
		self.in_overlap.set_text(str(config["overlap"]))
		self.in_base = self.builder.get_object("in_base")
		self.in_base.set_text(str(config["overlap"]))
		self.in_width = self.builder.get_object("in_width")
		self.in_width.set_text(str(config["data_width"]))
		self.in_bandlow = self.builder.get_object("in_bandlow")
		self.in_bandlow.set_text(str(config["bandlow"]))
		self.in_bandhigh = self.builder.get_object("in_bandhigh")
		self.in_bandhigh.set_text(str(config["bandhigh"]))
		self.update_fft_preview()
		self.win_image.show()
	
	def update_fft_preview(self,*args):
		overlap=int(self.in_overlap.get_text())
		bandlow=int(self.in_overlap.get_text())
		bandhigh=int(self.in_bandhigh.get_text())
		rate=int(self.in_rate.get_text())
		binpower=int(self.in_binpwr.get_text())
		binsize=2**binpower
		print "CRAP:",float(binsize),rate,overlap
		horizres=(float(binsize)/rate)/overlap
		fftheight=binsize/2
		maxfreq=1.0/(binsize)*rate*(binsize/2)
		maxfreq=min([maxfreq,bandhigh])
		minfreq=max([0,bandlow])
		vertres=1.0/(binsize)*rate #hz/pixel
		vertsize=(maxfreq-minfreq)/vertres
		prev="\nRATE: %d"%rate
		prev+="\nBIN SIZE: 2^%d=%d"%(binpower,binsize)
		prev+="\nPCM OVERLAP: %d"%(overlap)
		prev+="\nVERTICAL CALCULATION SIZE: %d pixels"%(fftheight)
		prev+="\nVERTICAL SIZE AFTER BANDPASS: %d pixels"%(vertsize)
		prev+="\nVERTICAL RESOLUTION: %.05f Hz/pixel"%(vertres)
		prev+="\nLOWEST FREQUENCY: %d Hz"%(minfreq)
		prev+="\nHIGHEST FREQUENCY: %d Hz"%(maxfreq)
		prev+="\nHORIZONTAL SIZE: %d pixels"%(config["data_width"])
		prev+="\nHORIZONTAL RESOLUTION: %.02f sec/pixel"%(horizres)
		self.lbl_preview = self.builder.get_object("lbl_preview")
		self.lbl_preview.set_text(prev)
		self.img_preview = self.builder.get_object("img_preview")
		self.img_preview.set_from_pixbuf(Image_to_GdkPixbuf(FFTpredict(rate,binsize,overlap,400)))
		return
     
	def set_fft_values(self,*args):
		config_set("rate",int(self.in_rate.get_text()))
		config_set("binpower",int(self.in_binpwr.get_text()))
		config_set("overlap",int(self.in_overlap.get_text()))
		#config_set("data_width",int(self.in_width.get_text()))
		config_set("bandlow",int(self.in_bandlow.get_text()))
		config_set("bandhigh",int(self.in_bandhigh.get_text()))
		totalReset(self)
     
	def on_vscrollbar1_change_value(self,*args):
		"""After the vertical scrollbar value is changed."""
		global update
		update=True
		self.drawScaleBars()

		
	def drawScaleBars(self):
		self.toppixel=self.adj.get_value()/90.0*(config["data_height"])
		self.toppixel=min(config["data_height"]-config["window_height"],self.toppixel)
		self.botpixel=config["data_height"]-(self.toppixel+config["window_height"])
		self.botfreq=self.botpixel*config["vertres"]
		
		self.im_vertscale=drawVertScale(config["vertres"],config["window_height"],self.botfreq)
		self.viewbox_scaleY.set_from_pixbuf(Image_to_GdkPixbuf(self.im_vertscale))
		
		self.im_horizscale=drawHorizScale(config["horizres"],config["data_width"])
		self.viewbox_scaleX.set_from_pixbuf(Image_to_GdkPixbuf(self.im_horizscale))
     
		self.logo=cornerLogo(self.im_vertscale.size[0],self.im_horizscale.size[1])
		self.viewbox_logo.set_from_pixbuf(Image_to_GdkPixbuf(self.logo))
		
		self.linescale=graphFFTlineScale(self.im_horizscale.size[1])
		self.viewbox_graphScale.set_from_pixbuf(Image_to_GdkPixbuf(self.linescale))
		
		
     
	def __init__(self):
		"""When launching the spectrograph."""
		self.builder = gtk.Builder()
		self.builder.add_from_file("testing2.glade") 
		self.builder.connect_signals(self)
		self.viewbox = self.builder.get_object("viewbox")
		self.viewbox_scaleX = self.builder.get_object("viewbox_scaleX")
		self.viewbox_scaleY = self.builder.get_object("viewbox_scaleY")
		self.viewbox_graph = self.builder.get_object("viewbox_graph")
		self.viewbox_graphScale = self.builder.get_object("viewbox_graphScale")
		self.viewbox_graph = self.builder.get_object("viewbox_graph")
		self.viewbox_logo = self.builder.get_object("viewbox_logo")
		self.img_histogram = self.builder.get_object("img_histogram")
		self.win_spectrograph = self.builder.get_object("win_spectrograph")
		self.adj = self.builder.get_object("adj_vertScroll")
		self.toppixel=0
		self.timestart=time.clock()
		totalReset(self)
		self.drawScaleBars()
		updatePalette()
		while True: #infinite loop
			if dienow==True: return
			while gtk.events_pending():gtk.main_iteration()
			seeWhatToDo()
			if update==True:
				self.drawSpec()
				self.updateStats()
			#else:
				#print "FREE TIME!"
		
	def drawSpec(self):
		"""Update the data viewer window."""
		global update
		#print "UPDATING",time.time()
		
		# DRAW MAIN DATA WINDOW
		dataw=dataWindow(data,self.toppixel,config["window_height"])
		self.im=Image.fromstring('L', (dataw.shape[1],dataw.shape[0]), dataw.astype('b').tostring())
		self.im=colorize(self.im,palette)
		self.viewbox.set_from_pixbuf(Image_to_GdkPixbuf(self.im))
		
		# DRAW HISTOGRAM
		self.histo=genHistogram(dataw[:,-1])
		self.img_histogram.set_from_pixbuf(Image_to_GdkPixbuf(self.histo))
		
		# DRAW LINE GRAPH
		x=numpy.sum(FFT_last,0)/config["overlap"]
		linedata=x[self.toppixel:self.toppixel+config["window_height"]]
		self.imLine=graphFFTline(linedata)
		self.viewbox_graph.set_from_pixbuf(Image_to_GdkPixbuf(self.imLine))
		
		update=False

if __name__ == "__main__":
	print ">>> LOADING UP <<<"
	s=spectrograph()
	gtk.main()
	del s
	print "OUT"
