
# from Tkinter import *
# import os
# import time
import tkFileDialog
import tkSimpleDialog
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
		#timestamp = horizRes*xleft+startTime
		t = time.localtime(int(time.time()))
		msg="%d/%d/%d %d:%02d:%02d"%(t[0],t[1],t[2],t[3],t[4],t[5])
	if len(message)>0:
		message="  -  "+message
	labwidth,labheight=draw.textsize(msg+message)
	#draw.rectangle((0,0,labwidth+4,labheight+4),0)
	draw.text((2,im.size[1]-labheight-2),msg+message,fill=(0,0,0))
	return im
		


def saveWhole(pics):
	ims=[]
	width=0
	height=0
	places=[]
	for i in range(len(pics)):
		im=Image.open(basedir+pics[i])
		ims.append(im)
		places.append(width)
		width+=im.size[0]
		if im.size[1]>height:
			height=im.size[1]
	im=Image.new("RGB",(width,height))
	for i in range(len(pics)):
		im.paste(ims[i],(places[i],0))
	im=addScales(im,0,width,"",0)
	draw = ImageDraw.Draw(im)
	draw.line((0,0,0,im.size[1]),fill=0)
	draw.line((0,0,im.size[0],0),fill=0)
	draw.line((0,im.size[1]-1,im.size[0]-1,im.size[1]-1),fill=0)
	draw.line((im.size[0]-1,0,im.size[0]-1,im.size[1]-1),fill=0)
	print "SAVING!"
	im.save(basedir+"grabber.jpg","JPEG")
	im=im.resize((im.size[0]/10,im.size[1]/10),Image.BILINEAR)
	im.save(basedir+"grabberThumb.jpg","JPEG")
			
def intToTime(i):
	t = time.localtime(int(i))
	t = "%d/%d/%d %d:%02d:%02d"%(t[0],t[1],t[2],t[3],t[4],t[5])
	return t
	
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
	print str("grabber 1.05")
	print "\n"*5
	time.sleep(1)

	
	
textIntro()
print "This program will continuously watch '%s' and generate web-friendly spectrographs every time a new image is seen."%basedir
print
print "How of the most recent images shold beincluded?"
print "(enter an integer, or leave blank for 3)"
ans=raw_input("answer:")
if ans=="": numPics=3
else: numPics=int(ans)
did=[]
while True:
	files=os.listdir(basedir)
	if not "scale_info.txt" in files:
		print "WHOA!",'I do not see a "scale_info.txt" file\n'+\
		'in that folder.  If you proceed without having one in there, I am\n'+\
		'pretty sure this program will crash when you try to assemble the\n'+\
		'web friendly images.  Come on! I need scale information!\n\n'+\
		'FEED ME!!!!!!!!!!!!!!!!!!!'
	files.sort()
	goodies=[]
	for i in range(len(files)):
		if files[i][-4:] in [".bmp",".png",".jpg"] and "_" in files[i]:
			goodies.append(files[i])
	goodies=goodies[-numPics:]
	if not goodies[-1] in did:
		print "MAKING IMAGE WITH:",goodies[-1]
		saveWhole(goodies)
		did.append(goodies[-1])
	else:
		"NOTHING NEW"
		time.sleep(5)