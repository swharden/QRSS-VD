
# from Tkinter import *
# import os
# import time
import tkFileDialog

# import tkMessageBox
# import ImageTk, Tkinter
# import datetime
# from PIL import ImageDraw
# from PIL import ImageOps
# import scipy
# import os
# import webbrowser
# import tkSimpleDialog



import JpegImagePlugin
import TgaImagePlugin
import PngImagePlugin
import GifImagePlugin
import PcxImagePlugin
import PpmImagePlugin
import BmpImagePlugin
import FliImagePlugin
import EpsImagePlugin
import DcxImagePlugin
import FpxImagePlugin
import ArgImagePlugin
import CurImagePlugin
import GbrImagePlugin
import IcoImagePlugin
import ImImagePlugin
import ImtImagePlugin
import IptcImagePlugin
import McIdasImagePlugin
import MicImagePlugin
import MspImagePlugin
import PcdImagePlugin
import PdfImagePlugin
import PixarImagePlugin
import PsdImagePlugin
import SgiImagePlugin
import SunImagePlugin
import TgaImagePlugin
import TiffImagePlugin
import WmfImagePlugin
import XVThumbImagePlugin
import XbmImagePlugin
import XpmImagePlugin

import os
import pyaudio
import scipy
from scipy import stats
import struct
import scipy.fftpack
from Tkinter import *
import threading
import time, datetime
import math
#import Image
import ImageTk
from PIL import Image
from PIL import ImageOps
from PIL import ImageChops
from PIL import ImageDraw
from PIL import ImageFilter
import random
import webbrowser
import tkMessageBox
import string

basedir='./output/'
files=[]
if not os.path.exists(basedir):
	os.makedirs(basedir)

############################

def commaize( valstr ) :
	ilist = list( valstr )
	ilist.reverse()
	olist = []
	for i in range( len( ilist )) :
		if i % 3 == 0 and i > 2 :
			olist.append( "," )
		olist.append( ilist[i] )
	olist.reverse()
	return string.join(olist, "")

def drawVertScale(height,vertres,freqLow):
	"""draws a scale given height and vertRes in hz/pixel."""
	#ONLY KNOWS UPSIDE DOWN RIGHT NOW
	#height=config["vertSize"]
	#vertres=config["vertRes"]
	#freqLow=config["lowFreq"]
	freqHigh=vertres*height+freqLow
	im=Image.new("L",(100,height),255)
	draw = ImageDraw.Draw(im)
	freq=freqLow #config["lowFreq"])
	txtwidth=0

	if vertres>2:
		tickevery=10
		labelEvery=100
	elif vertres>.5:
		tickevery=5
		labelEvery=25
	else:
		tickevery=1
		labelEvery=10

	freqs=scipy.arange(freqLow,freqHigh,vertres)
	lasthz=int(freqLow+height*vertres)/tickevery
	lastlab=int(freqLow+height*vertres)/labelEvery

	for y in range(height):
		freq=freqs[-(y+1)]
		if int(freq)/tickevery <> lasthz:
			draw.line([(0, y),(5, y)],150)
			lasthz=int(freq)/tickevery
		if int(freq)/labelEvery <> lastlab:
			draw.line([(0, y),(10, y)],0)
			lab=commaize(str(int(labelEvery+int(freq)/labelEvery*labelEvery)))+" Hz"
			labwidth,labheight=draw.textsize(lab)
			if labwidth>txtwidth:
				txtwidth=labwidth
			draw.text((12, y-labheight/2),lab)
			lastlab=int(freq)/labelEvery
	im=im.crop((0,0,12+txtwidth+2,height))
	del draw
	#im.save("scale_vert.bmp","BMP")	
	return im
	
def drawHorizScale(width,horizres):
	"""returns a horizontal scale given width and resolution."""
	im=Image.new("L",(width,100),255)
	draw = ImageDraw.Draw(im)
	maxsec=int(width*horizres)
	lab=" "
	for sec in range(maxsec):
		x=int(float(sec)/horizres)
		if horizres<.3:
			draw.line([(width-x, 0),(width-x, 5)],200)
		if sec%10==0:
			if horizres<.3:
				draw.line([(width-x, 0),(width-x, 10)],0)
				lab=str(int(sec/10)*10)+"s"
				labw=draw.textsize(lab)[0]
				if sec>0:
					draw.text((width-x-labw/2, 12),lab)
			else:
				draw.line([(width-x, 0),(width-x, 10)],200)
		if sec%60==0:
			if horizres>.3:
				draw.line([(width-x, 0),(width-x, 10)],0)
				lab=str(int(sec/60))+"m"
				labw=draw.textsize(lab)[0]
				if sec>0:
					draw.text((width-x-labw/2, 12),lab)
	txtheight=draw.textsize(lab)[1]
	im=im.crop((0,0,width,12+txtheight+2))
	del draw
	#im.save("scale_horiz.bmp","BMP")
	return im

def genLogo(scaleby=15,rotate=50):
	"""create QRSS VD text as an image."""
	b="1111011110111101111000100101110210010100101000010000001001010012"
	b+="1001011110111101111000100101001210110101000001000010001010010012"
	b+="1111010110111101111000010001110"
	b=b.split("2")
	im=Image.new("L",(33,7))
	data=im.load()
	for y in range(len(b)):
		for x in range(len(b[y])):
			data[x+1,y+1]=int(b[y][x])*255
	im=im.resize((im.size[0]*scaleby,im.size[1]*scaleby))
	data=im.load()
	def drawSin(width,height,vertoffset,horizoffset,thickness,darkness):
		for x in range(im.size[0]):
			y=scipy.sin((x-horizoffset)/float(width))*height+vertoffset
			for i in range(thickness):
				if 0<=y+i<im.size[1] and 0<=x<im.size[0]:
					data[x,y+i]=data[x,y+i]+darkness
	if rotate>0:
		canv=Image.new("L",(1000,1000))
		canv.paste(im,(400,450))
		im=canv.rotate(rotate)
		im=im.crop(im.getbbox())
	return im
		
def cornerLogo(width,height):
	imq=ImageOps.invert(genLogo(1,0))
	x,y=imq.size
	im=Image.new("L",(width,height),255)
	im.paste(imq,(width/2-x/2,height/2-y/2))
	#im.save("scale_corner.bmp","BMP")
	return im
	
def addScales(im,yoffset=0,xleft=None,message="",startTime=0):
	f=open(basedir+"scale_info.txt")
	raw=f.read()
	f.close()
	vertRes,lowFreq,horizRes,offset=eval(raw)
	lowFreq=lowFreq+offset
	im1=im
	imr=drawVertScale(im1.size[1],vertRes,lowFreq+yoffset)
	imb=drawHorizScale(im1.size[0],horizRes)
	imc=cornerLogo(imr.size[0],imb.size[1])
	im=Image.new("RGB",(10+im1.size[0]+imr.size[0],10+im1.size[1]+imb.size[1]),(255,255,255))
	im.paste(im1,(0,0))
	im.paste(imb,(0,im1.size[1]+0))
	im.paste(imr,(im1.size[0]+0,0))
	im.paste(imc,(im1.size[0]+0,im1.size[1]+0))
	draw = ImageDraw.Draw(im)
	if xleft==None: msg=""
	else:
		timestamp = horizRes*xleft+startTime
		t = time.localtime(int(timestamp))
		msg="%d/%d/%d %d:%02d:%02d"%(t[0],t[1],t[2],t[3],t[4],t[5])
	if len(message)>0:
		message="  -  "+message
	labwidth,labheight=draw.textsize(msg+message)
	#draw.rectangle((0,0,labwidth+4,labheight+4),0)
	draw.text((2,im.size[1]-labheight-2),msg+message,fill=(0,0,0))
	return im
	
class ScrolledCanvas(Frame):
	def __init__(self, parent=None):
		Frame.__init__(self, parent)
		self.master.title("QRSS VD - Spectrogram Viewer")
		self.pack(expand=YES, fill=BOTH)
		self.canv = Canvas(self, relief=SUNKEN)
		self.canv.config(width=700, height=500)
		self.canv.config(highlightthickness=0)
		sbarV = Scrollbar(self, orient=VERTICAL)
		sbarH = Scrollbar(self, orient=HORIZONTAL)
		sbarV.config(command=self.canv.yview)
		sbarH.config(command=self.canv.xview)
		self.canv.config(yscrollcommand=sbarV.set)
		self.canv.config(xscrollcommand=sbarH.set)
		sbarV.pack(side=RIGHT, fill=Y)
		sbarH.pack(side=BOTTOM, fill=X)
		self.canv.pack(side=LEFT, expand=YES, fill=BOTH)
		self.message=""
		self.startTime=None
		
		self.canv.config(cursor="ul_angle")
		
		def updateImages():
			totx,maxy=0,0
			self.pics=[]
			#files.sort()
			#for item in files:
			for item in files:
				#if "capt" in item and ".bmp" in item:
				fname=item
				v=int(fname.split("_")[1].split('.')[0])
				if self.startTime==None: self.startTime=v
				elif v<self.startTime: self.startTime=v
				t = time.localtime(v)
				stamp="%d/%d/%d %d:%02d:%02d"%\
						(t[0],t[1],t[2],t[3],t[4],t[5])
				print "LOADING",item,stamp
				im=Image.open(basedir+fname)
				imx,imy=im.size
				draw=ImageDraw.Draw(im)
				labwidth,labheight=draw.textsize(stamp)
				draw.rectangle((imx-labwidth-4,4,imx,labheight+4),fill=0)
				draw.text((imx-labwidth-2,5),stamp)
				draw.line((imx-1,0,imx-1,20),255)
				totx+=imx
				if maxy<imy: maxy=imy
				imp=ImageTk.PhotoImage(im)
				imt=self.canv.create_image(totx-imx,0,anchor="nw",image=imp)
				imt=Label(image=imp,cursor="crosshair")
				self.pics.append([im,imp,imt,totx-imx])
				self.canv.config(scrollregion=(0,0,totx,maxy))
				self.maxx=totx
				self.maxy=maxy
				self.master.update()
		
		self.x1,self.y1,self.x2,self.y2=None,None,None,None
		def click(event):
			self.canv.focus_set()
			x = self.canv.canvasx(event.x)
			y = self.canv.canvasy(event.y)
			if self.x1==None:
				self.x1=int(x)
				self.y1=int(y)
				print "UPPER LEFT: (%d,%d)"%(x,y)
				self.canv.config(cursor="lr_angle")
				return
			if self.x2==None:
				self.x2=int(x)
				self.y2=int(y)
				
				if self.x2<self.x1:
					t=self.x2
					self.x2=self.x1
					self.x2=t
				if self.y2<self.y1:
					t=self.y2
					self.y2=self.y1
					self.y2=t
				if self.y1==self.y2: self.y2=self.y1+10
				if self.x1==self.x2: self.x2=self.x1+10
				
				print "LOWER RIGHT: (%d,%d)"%(x,y)
				msg="Do you want to save the region\n"
				msg+="between (%d,%d) and (%d,%d)?\n\n"%(self.x2,self.x1,self.y2,self.y1)
				msg+="It's %dpx by %dpx..."%(self.x2-self.x1,self.y2-self.y1)
				#if tkMessageBox.askyesno("SAVE", msg):
				saveWhole(True)
				self.x1,self.y1,self.x2,self.y2=None,None,None,None
				self.canv.config(cursor="ul_angle")
		
		def saveWhole(crop=False):
			print "SAVING! (may take time)"
			im=Image.new("RGB",(self.maxx,self.maxy))
			for i in range(len(self.pics)):
				print "stitching",i,"of",len(self.pics),"..."
				im.paste(self.pics[i][0],(self.pics[i][3],0))
			if crop==True:
				im=im.crop((self.x1,self.y1,self.x2,self.y2))
				print "CROPPING:",self.x1,self.y1,self.x2,self.y2
				im=addScales(im,self.y2,self.x1,self.message,self.startTime)
			else:
				print "NOT CROPPING, SAVING DIRECTLY!"
				im=addScales(im,im.size[1],im.size[0],self.message,self.startTime)
			draw = ImageDraw.Draw(im)		
			
			if True: #DRAW RECTANGLE?
				draw.line((0,0,0,im.size[1]),fill=0)
				draw.line((0,0,im.size[0],0),fill=0)
				draw.line((0,im.size[1]-1,im.size[0]-1,im.size[1]-1),fill=0)
				draw.line((im.size[0]-1,0,im.size[0]-1,im.size[1]-1),fill=0)
			im.save("TEMP.png")
			os.system("TEMP.png")
			#im.show()
			#fname="cropped_%d.bmp"%time.time()
			#print "saving as",fname
			#print "size:",im.size
			#im.save(fname,"BMP")
			#print "SAVED!"
			
		def setmsg(event=None):
			self.message = tkSimpleDialog.askstring("CUSTOM MESSAGE",\
				"What would you like your message to be?\n(blank for no message)",\
				initialvalue="captured by AJ4VD")
		
		def hitSite(event=None):
			site="http://www.SWHarden.com/QRSS_VD/"
			print "LAUNCHING:",site
			webbrowser.open(site)
		
		def do_rightClickMenu(event):
			try:popup.tk_popup(event.x_root, event.y_root, 0)
			finally:popup.grab_release()
		popup = Menu(self.canv, tearoff=0)
		popup.add_command(label="set custom message",command=setmsg)
		popup.add_command(label="save ENTIRE image",command=saveWhole)
		popup.add_separator()
		popup.add_command(label="QRSS VD Website",command=hitSite)
		self.canv.bind("<Button-3>", do_rightClickMenu)
		self.canv.bind("<1>", click)
		self.master.update()
		updateImages()
		

#############################


firstImg=None
lastImg=None
imageFiles=[]

def setFirst():
	global firstImg
	if len(listbox.curselection())==0: return
	while imageFiles[int(listbox.curselection()[0])][1]==None:
		print "SELECTED:",listbox.curselection()
		listbox.selection_set(int(listbox.curselection()[0])+1)
		listbox.selection_clear(int(listbox.curselection()[0]))
		print "SELECTED:",listbox.curselection()
	firstImg=int(listbox.curselection()[0])
	doCalcs()
	
def setLast():
	global lastImg
	if len(listbox.curselection())==0: return
	lastImg=int(listbox.curselection()[0])
	doCalcs()
	
def doCalcs():
	if firstImg==None or lastImg==None:
		lbl.config(text="No images are currently selected...")
	else:
		t1=imageFiles[firstImg][1]
		t2=imageFiles[lastImg][1]
		numImgs=0
		for i in range(firstImg,lastImg+1):
			if not imageFiles[i][1]==None:
				numImgs+=1
		msg="%d images have been selected!\n"%(numImgs)
		msg+="First image: %s\n"%imageFiles[firstImg][0]
		msg+="First time: %s\n"%intToTime(t1)
		msg+="Last time: %s\n"%intToTime(t2)
		msg+="Last image: %s\n"%imageFiles[lastImg][0]
		msg+="Span time: about %d minutes\n"%int((t2-t1)/60.0)
		lbl.config(text=msg)

def selectAllImages():
	global firstImg,lastImg
	firstImg=0
	lastImg=listbox.size()-1
	doCalcs()

def intToTime(i):
	t = time.localtime(int(i))
	t = "%d/%d/%d %d:%02d:%02d"%(t[0],t[1],t[2],t[3],t[4],t[5])
	return t
	
def populateImageList(arg=None):
	global basedir, imageFiles
	imageFiles=[]
	if arg==None:
		basedir=tkFileDialog.askdirectory(initialdir=basedir)+"/"
	else:
		basedir=arg
	lFolder.config(text="Images in: "+basedir)
	files=os.listdir(basedir)
	if not "scale_info.txt" in files:
		tkMessageBox.showinfo("WHOA!",'I do not see a "scale_info.txt" file\n'+\
		'in this folder.  If you proceed without having one in there, I am\n'+\
		'pretty sure this program will crash when you try to assemble the\n'+\
		'full size image for browsing.  Come on! I need scale information!\n\n'+\
		'FEED ME!!!!!!!!!!!!!!!!!!!')
	files.sort()
	for i in range(len(files)):
		if files[i][-4:] in [".bmp",".png",".jpg"] and "_" in files[i]:
			fsec=int(files[i].split("_")[1].split(".")[0])
			imageFiles.append([files[i],fsec])
			if len(imageFiles)>0:
				if not imageFiles[i-1][1]==None:
					if imageFiles[i][1]>imageFiles[i-1][1]+60*20: #NUMBER OF SECONDS TO CONSIDER A SPACE
						imageFiles.insert(len(imageFiles)-1,[" -- space -- ",None])
			#print files[i],fsec
	listbox.delete(0,END)
	
	if len(imageFiles)>0:
		for i in range(len(imageFiles)):
			if imageFiles[i][0]==" -- space -- ": 
				s=" -- space -- "
			else:
				s="%s (%s)"%(imageFiles[i][0],intToTime(imageFiles[i][1]))
			listbox.insert(END, s)
		selectAllImages()
	
def letsGo():
	global files
	imgs=[]
	for i in range(firstImg,lastImg+1):
		if not imageFiles[i][1]==None:
			imgs.append(imageFiles[i][0])
	files=imgs
	master.destroy()
	#print "THESE ARE THE IMAGES:"
	#print imgs
	
def textIntro():
	"""cool ascii logo."""
	daText="66964111111884111111166741111118864111111978899784116677411941111111957784112266113611226711641122661194112266117998893711977361137112286115663711790911371188071139116702243811660224779867391199636113711980811576361197391138111111143681111118397111111768886836911949114381166391158939118836113611229611602222891190222297116787677098119114836117939115663911411911381186091164118707116411770711869887990891114663911993911598388111111438116836113871111114399111111476867998807814766391111111456960222261113224973224902222224670222222479868977666024879632222222485668976880224"
	daText=daText.replace("0","\\")
	daText=daText.replace("1","#")
	daText=daText.replace("2","_")
	daText=daText.replace("3","|")
	daText=daText.replace("4","/")
	daText=daText.replace("5","\n")			
	daText=daText.replace("6","8")			
	daText=daText.replace("7","8")			
	daText=daText.replace("8","9")			
	daText=daText.replace("9"," ")			
	print "\n"*20+daText+"by Scott Harden, AJ4VD"," "*19,
	print str("viewer 1.04")
	print "\n"*5
	time.sleep(1)

textIntro()
	
master = Tk()
master.title("QRSS VD - Viewer - Image Selection")
master.config(padx=5, pady=5)
listFrame = Frame(master)
scrollbar = Scrollbar(listFrame, orient=VERTICAL)
listbox = Listbox(listFrame, yscrollcommand=scrollbar.set, width=60)
scrollbar.config(command=listbox.yview)
scrollbar.pack(side=RIGHT, fill=Y)
listbox.pack(side=LEFT, fill=BOTH, expand=1)

lbl=Label(master,text="NO FILES FOUND!",anchor=N+W,justify=LEFT,width=50,padx=10,pady=10)
lFolder = Label(master,text="xxxxxx", justify=LEFT, anchor=W)
bFirst = Button(master, text="Set as First Image", command=setFirst)
bLast = Button(master, text="Set as Last Image", command=setLast)
bAll = Button(master, text="Select All Images", command=selectAllImages)
bRefresh = Button(master, text="Refresh File List", command=lambda: populateImageList(basedir))
bFold = Button(master, text="Select Different Folder", command=populateImageList)
bGo = Button(master, text="BROWSE THESE IMAGES", command=letsGo)

lFolder.grid(row=1,column=1,sticky=S+W)
listFrame.grid(row=2,column=1)
lbl.grid(row=3,column=1,sticky=E+W+N+S)
bFirst.grid(row=4,column=1,sticky=E+W)
bLast.grid(row=5,column=1,sticky=E+W)
bAll.grid(row=6,column=1,sticky=E+W)
bRefresh.grid(row=7,column=1,sticky=E+W)
bFold.grid(row=8,column=1,sticky=E+W)
bGo.grid(row=9,column=1,sticky=E+W)


populateImageList(basedir)
mainloop()
ScrolledCanvas().mainloop()
