import sys
import gtk
from PIL import ImageTk
from PIL import Image
import numpy
import Tkinter
import threading
import time
import StringIO
import Image

data=numpy.array(numpy.random.random((400,500))*50,dtype=int)
update=False

def Image_to_GdkPixbuf (image):
    file = StringIO.StringIO ()
    image.save (file, 'ppm')
    contents = file.getvalue()
    file.close ()
    loader = gtk.gdk.PixbufLoader ('pnm')
    loader.write (contents, len (contents))
    pixbuf = loader.get_pixbuf ()
    loader.close ()
    return pixbuf

def record():
	global data,update
	while True:
		time.sleep(.1)
		print "RECORD"
		data=numpy.roll(data,-1,1)
		update=True

class TutorialTextEditor:
 
	def on_window_destroy(self, widget, data=None):
		gtk.main_quit()
     
	def __init__(self):
		global update
		self.builder = gtk.Builder()
		self.builder.add_from_file("testing2.glade") 
		self.builder.connect_signals(self)
		self.x = self.builder.get_object("viewbox")
		self.timestart=time.clock()
		self.times=0
		self.t_rec=threading.Thread(target=record) 
		self.t_rec.daemon=True # daemon mode forces thread to quit with program
		self.t_rec.start()
		
		while True:
			while gtk.events_pending():gtk.main_iteration()
			if update==True:self.go()
			
			### TIMER ###
			#self.times+=1
			#if self.times%50==0:
			#	status="%.02f FPS"%(self.times/(time.clock()-self.timestart))
			#	print status
		
	def go(self):
		global update
		print "UPDATING"
		self.im=Image.fromstring('L', (data.shape[1],data.shape[0]), data.astype('b').tostring())
		self.x.set_from_pixbuf(Image_to_GdkPixbuf(self.im))
		update=False

if __name__ == "__main__":
	editor = TutorialTextEditor()
	gtk.main()
	print "OUT"
