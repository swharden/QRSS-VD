import StringIO
import gtk
import numpy
import string
from PIL import Image, ImageDraw, ImageOps

def config_recalc(config):
	config["binsize"]=2**config["binpower"]
	config["horizres"]=float(config["binsize"])/config["rate"]/config["overlap"] #sec/pixel
	config["vertres"]=1.0/(config["binsize"])*config["rate"] #hz/pixel
	config["data_height"]=config["binsize"]/2 #pixels
	config["maxfreq"]=1.0/(config["binsize"])*config["rate"]*(config["binsize"]/2) #in Hz
	config["window_width"]=config["data_width"] #size of the data viewing window
	return config

def config_default():
	config={}
	
	### MISC ###
	config["version"]=2.0 #current release

	### SIZES ###
	config["data_width"]=500 #should match window_width
	#config["data_height"]=512 #height of the actual spectrograph data
	#config["window_width"]=config["data_width"] #size of the data viewing window
	config["window_height"]=300 #size of the data viewing window
	
	### FFT PROPERTIES ###
	config["soundcard"]=1 #soundcard device ID
	config["rate"]=5000 #samples per second
	config["binpower"]=11 #IMPORTANT! length of PCM analyzed (2^x)
	config["overlap"]=8 #each bin is overlapped how many times?
	config["bandhigh"]=999999999
	config["bandlow"]=0
	config["offset"]=0
	config["noiseFloorDB"]=50 #make noise floor -50dB
	
	### IMAGE PROPERTIES ###
	config["img_cutoff"]=10000
	config["img_min"]=0
	config["img_mult"]=19
	config["img_gain"]=7
	config["img_auto"]=True
	config["img_seek"]=20

	### AUTOCAPTURE ###
	
	### LOCAL SITE ###
	
	### FTP SETTINGS ###
	
	return config_recalc(config)

def shapeTriangle(data):
        triangle=numpy.array(range(len(data)/2)+range(len(data)/2)[::-1])+1
        return (data*triangle)/(len(data)/2)

def pcm2fft(pcm,raw=True):
	#global currentCol, data, pcms, lastfft, fftmin,fftmax, fftyLast
	fft=numpy.fft.fft(pcm)
	ffty=numpy.sqrt(fft.real**2+fft.imag**2)[:len(fft)/2][::-1]
	if raw==True: return ffty
	ffty=20*numpy.log10(ffty)-30
	return ffty

def fft2pix(ffty,min=0,mult=10,gain=7,autoGain=False,avgLow=0,avgMed=999):
	if autoGain==False:
		#ffty=ffty/10000
		ffty=ffty+min/100.0
		ffty=255*ffty/(mult/5)
	else:
		ffty=ffty-avgLow
		ffty=ffty/avgMed*gain
	ffty=numpy.where(ffty>255,255,ffty)
	ffty=numpy.where(ffty<0,0,ffty)
	#print "AGN:",max(ffty)
	return ffty

def config_show(config):
	keys=config.keys()
	keys.sort()
	for key in keys:
		print key,"\t",config[key]

def dataWindow(data,top=0,height=300):
	top=min(len(data)-height,top)
	#print "DATA HEIGHT:",len(data)
	#print "MAX RETURN",top+height
	return data[top:top+height]

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

def drawHorizScale(horizres,width=300):
	"""returns a horizontal scale given width and resolution."""
	im=Image.new("L",(width,100),255)
	draw = ImageDraw.Draw(im)
	maxsec=int(width*horizres)
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
	#im.show()
	return im
	
def drawVertScale(vertres,height=300,freqLow=1000):
	"""draws a scale given height and vertRes in hz/pixel."""
	freqHigh=vertres*height+freqLow
	im=Image.new("L",(100,height),255)
	draw = ImageDraw.Draw(im)
	freq=freqLow
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
	freqs=numpy.arange(freqLow,freqHigh,vertres)
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
	#im.show()
	return im

def commaize(valstr) :
	ilist = list( valstr )
	ilist.reverse()
	olist = []
	for i in range( len( ilist )) :
		if i % 3 == 0 and i > 2 :
			olist.append( "," )
		olist.append( ilist[i] )
	olist.reverse()
	return string.join(olist, "")

def cornerLogo(width,height):
	imq=ImageOps.invert(genLogo(1,0))
	x,y=imq.size
	im=Image.new("L",(width,height),255)
	im.paste(imq,(width/2-x/2,height/2-y/2))
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


def FFTpredict(rate=5000,binsize=1024*8,overlap=8,vertsize=300):
	fftheight=binsize/2
	maxfreq=1.0/(binsize)*rate*(binsize/2)
	vertres=1.0/(binsize)*rate #hz/pixel
	horizres=float(binsize)/rate/overlap #sec/pixel
	data=numpy.random.random((vertsize,300))*75
	sec=0
	for x in range(vertsize):
		sec+=horizres
		try:
			if sec%6<3:data[50][x]=255
			else:data[50+(1/(1.0/(binsize)*rate))][x]=255
			if sec%6<3:data[100][x]=255
			else:data[100+(10/(1.0/(binsize)*rate))][x]=255
			if sec%20<10:data[150][x]=255
			else:data[150+(10/(1.0/(binsize)*rate))][x]=255			
		except:
			pass
	im=Image.fromstring('L', (data.shape[1],data.shape[0]), data.astype('b').tostring())
	im=addScales(im,1.0/(binsize)*rate,float(binsize)/rate/overlap)
	draw = ImageDraw.Draw(im)
	draw.text((5, 35),"QRSS 3 with a 1 Hz shift")
	draw.text((5, 85),"QRSS 10 with a 5 Hz shift")
	draw.text((5, 135),"QRSS 10 with a 5 Hz shift")
	draw.text((5, 235),"color scale")
	for x in range(255):
		draw.line([(x+5, 250),(x+5, 275)],(x,x,x))	
	#im.show()
	return im

def genHistogram(dataw):
	#print dataw
	#print dataw.flatten()
	hist,bins=numpy.histogram(dataw,range(256))
	hist=hist*100.0/max(hist)
	im=Image.new("L",(256+30,100+30))
	draw = ImageDraw.Draw(im)
	draw.line([(14,116),(256+14,116)],255)
	draw.line([(14,14),(14,116)],255)
	for x in range(255):
		draw.line([(x+15,100+15),(x+15,15+100-int(hist[x]))],100)
	return im

def addScales(im,vertRes,horizRes,lowFreq=0):
	im1=im
	imr=drawVertScale(vertRes,im1.size[1],lowFreq)
	imb=drawHorizScale(horizRes,im1.size[0])
	imc=cornerLogo(imr.size[0],imb.size[1])
	### ASSEMBLE PARTS INTO FINAL IMAGE ###
	im=Image.new("RGB",(im1.size[0]+imr.size[0],\
		im1.size[1]+imb.size[1]),(255,255,255))
	im.paste(im1,(0,0))
	im.paste(imb,(0,im1.size[1]+0))
	im.paste(imr,(im1.size[0]+0,0))
	im.paste(imc,(im1.size[0]+0,im1.size[1]+0))
	return im
	
	
def normalize(lin,mult):
	lin=lin-min(lin)
	lin=lin/max(lin)
	lin=lin*mult
	return lin

def graphFFTline(lin):
	#lin=normalize(lin,100)
	#print min(lin)
	#lin=lin-min(lin)
	im=Image.new("L",(100,len(lin)),255)
	draw = ImageDraw.Draw(im)
	for x in range(0,11):
		draw.line([(x*10,0),(x*10,len(lin))],200)
	for y in range(1,len(lin)):
		#print (lin[y-1],y-1),(lin[y],y)
		draw.line([(lin[y-1],y-1),(lin[y],y)],0)
	return im

def graphFFTlineScale(height):
	im=Image.new("L",(100,height),255)
	draw = ImageDraw.Draw(im)
	draw.text((10, 10),"10dB/line")
	return im
	#for x in range(10,100,10):
	#	draw.text((x, 2),"-%ddB"%x)
	#return im
	
def genPalette():
	palette = []
	for i in range(256):
		r=max(i*2-256,0)
		g=i
		b=min(i*2,255)
		palette.append((r,g,b))
	return palette
	
def colorize(im,pal):
	im=im.convert("RGB")
	pix=im.load()
	for x in range(im.size[0]):
		for y in range(im.size[1]):
			pix[x,y]=pal[pix[x,y][0]]
	return im
	
if __name__ == "__main__":
	print "THIS SCRIPT ISN'T SUPPOSED TO BE EXECUTED!"
	raw_input("press ENTER to exit")
