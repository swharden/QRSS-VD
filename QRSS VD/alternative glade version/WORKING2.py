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
print data
print len(data)
print len(data[1])
datapix=data #pixel data
update=False #whether or not view window should be redrawn
pcms=[] #series of PCM segments from record()
stats={}
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
	data=numpy.roll(data,-1,1)
	data[:,-1]=newdata

fftmins=[]
fftmaxs=[]
fftmeds=[]
def seeWhatToDo():
	"""check to see if anything needs to be done (run every update)."""
	global update, pcms, fftmins, fftmaxs, fftavgs
	if len(pcms)>1:
		lin=pcms.pop(0)
		lin=numpy.append(lin,pcms[0])
		for x in range(8-1):
			pcm=lin[x*1024/8:x*1024/8+1024]
			ffty=pcm2fft(shapeTriangle(pcm))
			
			fftmins.append(numpy.min(ffty))
			fftmaxs.append(numpy.max(ffty))
			fftmeds.append(numpy.median(ffty))
			
			ffty=fft2pix(ffty,config["img_min"],config["img_mult"],\
							config["img_gain"],config["img_seek"])
			if len(fftmins)>config["img_seek"]:
				fftmins.pop(0)
				fftmaxs.pop(0)
				fftmeds.pop(0)
			newData(ffty)
		update=True
		
recordLive=True #set to False to cause shutdown
def record():
	global pcms
	p = pyaudio.PyAudio() 
	inStream = p.open(format=pyaudio.paInt16,\
				channels=1,rate=config["rate"],\
				input_device_index=config["soundcard"],input=True)
	pcms=[] #holds linear unprocessed data
	while True:
		if recordLive==False: return
		pcms.append(numpy.fromstring(inStream.read(1024),dtype=numpy.int16))		

class spectrograph:
	
	def on_window_destroy(self, widget, data=None):
		"""We clicked the X button."""
		global recordLive
		recordLive=False
		print "IM DONE"
		#time.sleep(1)
		sys.exit(0)
    
	def destroy(self,object,event):
		"""instead of destroying something, hide it."""
		print "HIDING",object,event
		object.hide()
		return True #MUST DO THIS!
	
	def set_viewXY(self,a):
		config_set("window_height",int(self.in_viewY.get_text()))
    
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
		
    
	def set_view_size(self,a):
		self.sizer = self.builder.get_object("win_setViewerSize")
		self.in_viewX = self.builder.get_object("in_viewX")
		self.in_viewY = self.builder.get_object("in_viewY")
		self.in_viewX.set_text(str(config["window_width"]))
		self.in_viewY.set_text(str(config["window_height"]))
		self.sizer.show()
		
	def open_win_image(self,a):
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
	
	def set_image_stats(self,a,b,c):
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
     
	def on_vscrollbar1_change_value(self,a,b,c):
		"""After the vertical scrollbar value is changed."""
		global update
		update=True
     
	def __init__(self):
		"""When launching the spectrograph."""
		self.builder = gtk.Builder()
		self.builder.add_from_file("testing2.glade") 
		self.builder.connect_signals(self)
		self.viewbox = self.builder.get_object("viewbox")
		self.viewbox = self.builder.get_object("img_histogram")
		self.win_spectrograph = self.builder.get_object("win_spectrograph")
		
		self.adj = self.builder.get_object("adj_vertScroll")
		self.timestart=time.clock()
		self.t_rec=threading.Thread(target=record) 
		self.t_rec.daemon=True
		self.t_rec.start()
		while True: #infinite loop
			#print "HEIGHT:",
			while gtk.events_pending():gtk.main_iteration()
			seeWhatToDo()
			if update==True:
				self.drawSpec()
				self.updateStats()
		
	def drawSpec(self):
		"""Update the data viewer window."""
		global update
		print "UPDATING",time.time()
		dataw=dataWindow(data,self.adj.get_value()*int((config["data_height"]-config["window_height"])/100.0),config["window_height"])
		self.im=Image.fromstring('L', (dataw.shape[1],dataw.shape[0]), dataw.astype('b').tostring())
		self.viewbox.set_from_pixbuf(Image_to_GdkPixbuf(self.im))
		
		self.histo=genHistogram(dataw)
		self.viewbox.set_from_pixbuf(Image_to_GdkPixbuf(self.histo))
		
		update=False

if __name__ == "__main__":
	s=spectrograph()
	gtk.main()
	print "OUT"
