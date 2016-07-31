version=1.1

print "IMPORTING LIBRARIES..."
import gtk
import StringIO
import Image, ImageOps
import webbrowser
import os
import time
print "DONE"


def checkUpdates():
    try:
        print "\n\nchecking for updates..."
        import urllib
        f=urllib.urlopen("http://www.swharden.com/vdlabs/version/stitch.txt")
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







class QRSS_STITCHER:

    def stat(self,msg):
        print "STATUS:",msg
        self.lbl_status2.set_text(msg)
        while gtk.events_pending():gtk.main_iteration()

    def on_getfolder(self,*args):
        dialog = gtk.FileChooserDialog("SELECT FIRST IMAGE",None,gtk.FILE_CHOOSER_ACTION_OPEN,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            self.imfilename = dialog.get_filename()
            self.folder=os.path.dirname(self.imfilename)+"/"
            dialog.destroy()
            self.stat("selected new folder of source images")
            self.im_source=Image.open(self.imfilename)
            #self.adj_x1.value,self.adj_y1.value=0,0
            if self.adj_x2.value==0: self.adj_x2.value=self.im_source.size[0]
            if self.adj_y2.value==0: self.adj_y2.value=self.im_source.size[1]
            #self.adj_x2.value,self.adj_y2.value=self.im_source.size
            self.update_preview()
        else:
            self.stat("no folder selected")
            dialog.destroy()
  
    def update_preview(self,*args):

        self.im_cropped = self.im_source.crop((self.adj_x1.value,self.adj_y1.value,\
                                               self.adj_x2.value,self.adj_y2.value))
        prev = self.im_cropped
        prev = ImageOps.expand(prev, border=10, fill=(208,32,144))
        self.image2.set_from_pixbuf(Image_to_GdkPixbuf(prev))

    def on_setmin(self,*args):
        self.stat("set (X1,Y1) to top left corner)")
        self.adj_x1.value,self.adj_y1.value=0,0
        
    def on_setmax(self,*args):
        self.stat("set (X2,Y2) bottom right corner")
        self.adj_x2.value,self.adj_y2.value=self.im_source.size
            
    def on_goto_site(self,*args):
        self.stat("hitting http://www.SWHarden.com/")
        webbrowser.open_new_tab('http://www.SWHarden.com/')

    def on_set_fname(self, *args):
        self.fname=self.entry3.get_text()+".jpg"        
        #self.stat("setting new output filename to "+self.entry3.get_text())
    
    def on_preview(self,*args):
        if self.togglebutton3.get_active()==True:
            self.stat("showing preview window")
            self.window2.show()
        else:
            self.stat("hiding preview window")
            self.window2.hide()
        print "ACTION"

    def on_var_change(self,*args):
        print "ACTION"
    
    def on_stitch(self,*args):
        self.stat("Generating stitched image...")
        x1,y1,x2,y2=[self.adj_x1.value,self.adj_y1.value,\
                     self.adj_x2.value,self.adj_y2.value]
        squish=self.adj_squish.value
        workwith=[]
        for fname in os.listdir(self.folder):
            if ".jpg" in fname or ".bmp" in fname \
                   or ".png" in fname or ".tif" in fname:
                if not "stitched" in fname and \
                   not self.fname in fname:
                    workwith.append(fname)
                    print "I SEE:",self.folder,fname
        workwith.sort()
        im=Image.new("RGB",((x2-x1)*len(workwith),y2-y1))
        try:os.mkdir(self.folder+"/stitched/")
        except:pass #folder there already
        for i in range(len(workwith)):
            print "Loading",workwith[i]
            im2=Image.open(self.folder+workwith[i])
            im2=im2.crop((x1,y1,x2,y2))
            if self.togglebutton2.get_active()==True:
                self.stat("saving %03d_"%i+self.fname+"...")
                im2.save(self.folder+"/stitched/%03d_"%i+self.fname,quality=90)
            im.paste(im2,(i*(x2-x1),0))
        self.stat("saving large image...")
        im.save(self.folder+"/stitched/"+self.fname,quality=90)
        im=im.resize((im.size[0]/squish,im.size[1]),Image.ANTIALIAS)
        im.save(self.folder+"/stitched/squished_"+self.fname,quality=90)
        f=open("stitchlog.txt",'w')
        f.write(str([x1,y1,x2,y2,self.imfilename]))
        f.close()
        print "DONE"             
        self.stat("COMPLETE!!! Launching folder containing stitched images...")   
        os.startfile(self.folder+"/stitched/")

    def on_window_destroy(self, widget, data=None):
        self.window2.hide()
        self.dienow=True
        return
        
    def __init__(self):

        ## CHECK UPDATES ##
        #update=checkUpdates("stitch.txt",version)
        #if update==False: msg="(newest)"
        #else: msg="-- UPDATE AVAILABLE!!!"
        
        self.dienow=False
        self.builder = gtk.Builder()
        self.builder.add_from_file("qrss_stitch.glade") 
        self.builder.connect_signals(self)
        self.lbl_status = self.builder.get_object("lbl_status")
        self.adj_x1 = self.builder.get_object("X1")
        self.adj_x2 = self.builder.get_object("X2")
        self.adj_y1 = self.builder.get_object("Y1")
        self.adj_y2 = self.builder.get_object("Y2")
        self.window2 = self.builder.get_object("window2")
        self.togglebutton3 = self.builder.get_object("togglebutton3")
        self.togglebutton2 = self.builder.get_object("togglebutton2")
        self.lbl_status = self.builder.get_object("lbl_status")
        self.lbl_status2 = self.builder.get_object("lbl_status2")
        self.image2 = self.builder.get_object("image2")
        self.entry3 = self.builder.get_object("entry3")
        self.entry3.set_text("stitched")
        self.adj_squish = self.builder.get_object("adj_squish")
        self.adj_squish.value=10
        self.on_set_fname()
        self.stat("current version: %s"%(str(version)))
             
        try:
            f=open("stitchlog.txt")
            self.adj_x1.value,self.adj_y1.value,\
                self.adj_x2.value,self.adj_y2.value,\
                self.imfilename=eval(f.read())
            f.close()
        except: pass
        
          
        while True:
            if self.dienow: return
            while gtk.events_pending(): gtk.main_iteration()

if __name__ == '__main__':
    x=QRSS_STITCHER()
    checkUpdates()
    time.sleep(1)
    print "EXITING"
    time.sleep(1)
