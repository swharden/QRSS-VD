version=1.1

print "IMPORTING LIBRARIES..."
import os
import gtk
import time
import scipy
import numpy
import Image
import datetime
import StringIO
import ImageDraw
import webbrowser
import scipy.misc
import Image, ImageOps
print "DONE"

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


def checkUpdates():
    try:
        print "\n\nchecking for updates..."
        import urllib
        f=urllib.urlopen("http://www.swharden.com/vdlabs/version/stack.txt")
        raw=f.read();f.close()              
        print "RAW:",raw
        data = eval(raw)
        if data==version:
            # site worked, no update
            print "you have the most current version"
            return False
        else:
            # site worked, update available
            print "contacted site, UPDATE AVAILABLE!!!"
            message="A newer version is available!\n\n"
            message+="You are running version: "+str(version)+"\n"
            message+="The newer version is: "+str(data)+"\n\n"
            message+="Do you want to update now?"
            dialog = gtk.MessageDialog(None, 0, gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, message)
            response = dialog.run()
            dialog.destroy()
            if response==-8:
                webbrowser.open_new_tab('http://www.swharden.com/blog/vd-labs-software-by-aj4vd/')
            return True
    except:
        # site didn't work!
        print "couldn't connect to site..."
        return False


class STACKVD:

    def stat(self,msg):
        d=datetime.datetime.now()
        stamp="[%02d:%02d:%02d] "%(d.hour,d.minute,d.second)
        msg=stamp+msg
        print "STATUS:",msg
        self.lbl_status2.set_text(msg)
        self.lbl_status3.set_text(msg)
        self.updateGraphics()


    def on_getfolder(self,*args):
        self.stat("launching file chooser")
        dialog = gtk.FileChooserDialog("SELECT FIRST IMAGE",None,gtk.FILE_CHOOSER_ACTION_OPEN,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            self.fname = dialog.get_filename()
            self.folder,self.fnameonly=os.path.split(self.fname)
            dialog.destroy()
            self.load()
        else:
            self.stat("no folder selected")
            dialog.destroy()

    def load(self, *arg):
        if self.fname==None:
            self.stat("no image loaded!")
            return
        self.stat("LOADING "+self.fname+"...")
        self.im=scipy.misc.imread(self.fname)
        if self.im.shape[1]<2000:
            msg = "!!! SERIOUS PROBLEM !!!\n\n"
            msg+= "Your selected image is less than 2000 pixels wide!\n\n"
            
            msg+= "You must select a very wide, stitched image spanning"
            msg+= " a lot of captures for the stacker to be useful.\n\n"
            
            msg+= "Please use the QRSS Stitcher to create a wide, stitched"
            msg+= " image from the collection of small captures you have. Then"
            msg+= " try the QRSS Stacker again."
            
            dialog = gtk.MessageDialog(None, 0, gtk.DIALOG_MODAL, gtk.BUTTONS_OK, msg)
            response = dialog.run()
            dialog.destroy()
        self.im=self.im.astype(float)
        self.win_main = self.builder.get_object("window1")
        self.win_original.show()
        self.win_preview.show()
        self.stat("LOADING "+self.fname+"... COMPLETE")

        im=Image.open(self.fname)
        self.im_spec2.set_from_pixbuf(Image_to_GdkPixbuf(im))

        self.project()

    def on_saveproj(self,*args):
        self.project(True)

    def project(self,saveit=False):
        if self.working==True:
            print "NOT READY YET"
            return
        if self.lim_from.get_value()>self.lim_to.get_value():
            self.lim_from.set_value(self.lim_to.get_value())
        
        if self.fname==None:
            self.stat("no image loaded!")
            return
        self.stat("projecting image...")
        if saveit==True:
            try:os.mkdir(self.folder+"/stacked/")
            except:pass #folder there already
        self.proj,x,imagesUsed,verts=None,0,0,[]

        ### PER SLICE ########################### 
        while x*self.repeat+self.offset<self.im.shape[1]-self.repeat:
            if x+1<self.lim_from.get_value() \
               or x+1>self.lim_to.get_value() \
               and self.adj_togglefirst1.get_active()==True:
                    self.stat("ignoring slice #%02d"%x)
            else:
                self.stat("processing slice #%02d"%x)
                startx=int(x*self.repeat+self.offset)
                im2=self.im[:,startx:startx+int(self.repeat)]
                if self.stackvert.get_active():
                    verts.append(Image.fromarray(numpy.uint8(im2)))
                if x>0 and self.vertshift<>0:
                    im2=numpy.roll(im2,int(-self.vertshift*x),axis=0)
                if self.proj==None:
                    self.proj=im2
                else:
                    if self.method=="avg":
                        self.proj=self.proj+im2
                    if self.method=="max":
                        self.proj=numpy.maximum(self.proj,im2)
                    if self.method=="med":
                        self.proj=scipy.minimum(self.proj,im2)
                if saveit==True and self.toggle_saveslices.get_active()==True:
                    self.stat("saving slice #%02d"%x)
                    scipy.misc.imsave(self.folder+"/stacked/%02d_"%x+self.fnameonly,im2)
                imagesUsed+=1
            x+=1
        ##########################################
        if self.lim_to.get_value()>x:
            self.lim_to.set_value(x)
        if imagesUsed==0:
            print "BLANK"
            return
        self.lbl_totimgs.set_text("total images: %d (%d used)"%(x,imagesUsed))
        if self.method=="avg":
            self.proj=self.proj/imagesUsed 
        self.proj=self.proj.astype(int)
        im = Image.fromarray(numpy.uint8(self.proj))
        if self.adj_toggleAutoContrast.get_active()==True:      
            im = ImageOps.autocontrast(im, cutoff=0)
        if self.stackvert.get_active():
            imstack=Image.new("RGB",(im.size[0],im.size[1]*(len(verts)+1)))
            draw = ImageDraw.Draw(imstack)
            for i in range(len(verts)):
                imstack.paste(verts[i],(0,im.size[1]*i))
                draw.line((0, im.size[1]*(i+1)-1, im.size[0], im.size[1]*(i+1)-1), fill=(255,255,0))
            imstack.paste(im,(0,im.size[1]*(i+1)))
            im=imstack
        msg1="VD Labs - QRSS Stacker"
        msg="average projection of %d images "%imagesUsed
        msg+="(repeat=%.01fpx, drift=%.01fpx)"%(self.repeat,self.vertshift)
        draw = ImageDraw.Draw(im)
        tw,th=draw.textsize(msg)
        ty=im.size[1]-th
        for sx in [-1,0,1]:
            for sy in [-1,0,1]:
                draw.text((3+sx,3+sy), msg1, (0,0,0));
                draw.text((3+sx,ty-3+sy), msg, (0,0,0))               
        draw.text((3,3), msg1, (255,255,255))
        draw.text((3,ty-3), msg, (255,255,255))

        if saveit==True:
            self.stat("saving projected stack...")
            im.save(self.folder+"/stacked/stacked_"+self.fnameonly,quality=90)
            os.startfile(self.folder+"/stacked/")
        self.im_spec.set_from_pixbuf(Image_to_GdkPixbuf(im))
        #time.sleep(.1)
        self.stat("waiting for commands...")
        self.working==False
        print "PROJECTED"

    def on_window_destroy(self, widget, data=None):
        self.dienow=True

    def jumpup(self, *arg):
        print "JUMPING UP";self.adj_repeat.value += 1;
    def jumpup2(self, *arg):
        print "JUMPING UP";self.adj_repeat.value += 5;
    def jumpup3(self, *arg):
        print "JUMPING UP";self.adj_repeat.value += 25;
        
    def jumpdown(self, *args):
        print "JUMPING DOWN";self.adj_repeat.value -= 1;
    def jumpdown2(self, *args):
        print "JUMPING DOWN";self.adj_repeat.value -= 5;
    def jumpdown3(self, *args):
        print "JUMPING DOWN";self.adj_repeat.value -= 25;

    def tog_max(self,*args):
        self.lbl_method.set_text("maximum")
        self.stat("set stacking method to maximum")
        self.method="max"
        self.project()

    def tog_avg(self,*args):
        self.lbl_method.set_text("average")
        self.stat("set stacking method to average")
        self.method="avg"
        self.project()

    def tog_med(self,*args):
        self.lbl_method.set_text("median")
        self.stat("set stacking method to median")
        self.method="med"
        self.project()  
        
    def newvals(self, junk):
        print "NEW VALUES"
        #time.sleep(.1)
        self.repeat = self.adj_repeat.value
        self.vertshift = self.adj_vertshift.value
        self.offset = self.adj_offset.value
        #if junk=="noproj": return
        self.project()

    def on_orig_click(self,what,where):
        self.lbl_status1.set_text("CLICKED (%d,%d)"%(where.x,where.y))
        self.lastx,self.lasty=where.x,where.y

    def on_orig_move(self,what,where):
        msg="last click: (%d,%d)   "%(self.lastx,self.lasty)
        msg+="current position: (%d,%d)   "%(where.x,where.y)
        msg+="difference: (%d,%d)"%(where.x-self.lastx,where.y-self.lasty)
        self.lbl_status1.set_text(msg)

    def hitsite(self,*args):
        self.stat("launching http://www.SWHarden.com/")
        webbrowser.open_new_tab('http://www.SWHarden.com/')

    def updateGraphics(self):
        while gtk.events_pending():
            gtk.main_iteration()
        
 
    def __init__(self):

        self.fname=None
        self.repeat=1066
        self.vertshift=0
        self.offset=0
        self.dienow=False
        self.builder = gtk.Builder()
        self.builder.add_from_file("vd_stacker.glade") 
        self.builder.connect_signals(self)
        self.adj_repeat = self.builder.get_object("adj_repeat")
        self.adj_vertshift = self.builder.get_object("adj_vertshift")
        self.adj_offset = self.builder.get_object("adj_offset")
        self.adj_offset = self.builder.get_object("adj_offset")
        #self.adj_togglefirst = self.builder.get_object("adj_togglefirst")
        self.im_spec = self.builder.get_object("im_spec")
        self.im_spec2 = self.builder.get_object("im_spec2")
        self.lbl_status1=self.builder.get_object("lbl_status1")
        self.lbl_status2=self.builder.get_object("lbl_status2")
        self.lbl_status3=self.builder.get_object("lbl_status3")
        self.win_main = self.builder.get_object("window1")
        self.win_preview = self.builder.get_object("preview")
        self.win_original = self.builder.get_object("original")
        self.toggle_saveslices = self.builder.get_object("togglebutton3")
        self.adj_togglefirst1=self.builder.get_object("adj_togglefirst1")
        self.lbl_totimgs=self.builder.get_object("lbl_totimgs")
        self.lim_from=self.builder.get_object("adjustment5")
        self.lim_to=self.builder.get_object("adjustment6")
        self.adj_toggleAutoContrast=self.builder.get_object("togglebutton2")
        self.stackvert=self.builder.get_object("togglebutton1")
        self.lbl_version=self.builder.get_object("lbl_version")
        self.lbl_version.set_text("version "+str(version))
        self.lbl_method=self.builder.get_object("lbl_method")
        
        self.method="avg"
        self.lbl_method.set_text("average")
        self.working=False
        self.lim_from.value=1
        self.lim_to.value=3
        self.adj_repeat.value = 500
        self.lastx=0
        self.lasty=0
        
        self.load(self)
        self.newvals(self)
        
        while True:
            if self.dienow==True: return
            self.updateGraphics()

if __name__ == '__main__':
    x=STACKVD()
    checkUpdates()
    time.sleep(1)
    print "EXITING"
    time.sleep(1)
