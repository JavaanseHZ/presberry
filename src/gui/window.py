'''
Created on Aug 28, 2014

@author: ben
'''

from wx.lib.pubsub import pub
import gtk
import qrencode
import threading
import util.config as PRES_CONFIG

gtk.threads_init()

class PresPresentationPanel(gtk.HBox):
    def __init__(self):
        gtk.HBox.__init__(self)
        self.fileUploaded = False;
    
    def loadPresentation(self, pdfDocument):
        old = self.get_children()
        for i in old:
            self.remove(i)
        presDrawingArea = PresDrawingArea()
        presDrawingArea.loadPdfDocument(pdfDocument)
        presDrawingArea.set_size_request(int(pdfDocument.doc_width * pdfDocument.scaleFactor) , int(pdfDocument.doc_height * pdfDocument.scaleFactor))
        presDrawingArea.fileUploaded = True;
        alignment = gtk.Alignment(0.5, 0.5, 0, 0)
        alignment.add(presDrawingArea)
        self.pack_start(alignment)              

class PresDrawingArea(gtk.DrawingArea):
    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.connect('expose-event', self.expose)
        pub.Publisher.subscribe(self.presSetPage, 'presSetPage')

    def loadPdfDocument(self, pdfDocument):
        self.pdfDocument = pdfDocument
       
    def expose(self, widget, event):
        if self.fileUploaded:
            cr = widget.window.cairo_create()
            cr.set_source_rgb(0, 0, 0)
            cr.scale(self.pdfDocument.scaleFactor, self.pdfDocument.scaleFactor)
            self.pdfDocument.curr_pg_disp.render(cr)
     
    def presSetPage(self, msg):
        self.pdfDocument.curr_pg = int(msg.data)%self.pdfDocument.n_pgs
        self.pdfDocument.curr_pg_disp = self.pdfDocument.doc.get_page(self.pdfDocument.curr_pg)
        self.hide_all()
        self.show_all()
        
class PresStartPanel(gtk.Table):
    def __init__(self, h, w, rows=3, columns=4, homogenous=False):
        gtk.Table.__init__(self, rows, columns, homogenous)
        
        titlesvg = PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_MEDIA_GUI) + '/labeltitle.svg'
        titlepixbuf = gtk.gdk.pixbuf_new_from_file_at_size(titlesvg, width= int(w), height=-1)
        titleImage = gtk.Image()
        titleImage.set_from_pixbuf(titlepixbuf) 
        titleAlign = gtk.Alignment(0.5, 0, 0, 0)
        titleAlign.add(titleImage)
        
        wifisvg = PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_MEDIA_GUI) + '/labelwifi.svg'
        wifipixbuf = gtk.gdk.pixbuf_new_from_file_at_size(wifisvg, width= int(w/4), height=-1)
        wifiImage = gtk.Image()
        wifiImage.set_from_pixbuf(wifipixbuf) 
        wifiAlign = gtk.Alignment(0.5, 1, 0, 0)
        wifiAlign.add(wifiImage)
         
        connectsvg = PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_MEDIA_GUI) + '/labelconnect.svg'
        connectpixbuf = gtk.gdk.pixbuf_new_from_file_at_size(connectsvg, width= int(w/4), height=-1)
        connectImage = gtk.Image()
        connectImage.set_from_pixbuf(connectpixbuf) 
        connectAlign = gtk.Alignment(0.5, 1, 0, 0)
        connectAlign.add(connectImage)
         
        uploadsvg = PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_MEDIA_GUI) + '/labelupload.svg'
        uploadpixbuf = gtk.gdk.pixbuf_new_from_file_at_size(uploadsvg, width= int(w/4), height=-1)
        uploadImage = gtk.Image()
        uploadImage.set_from_pixbuf(uploadpixbuf) 
        uploadAlign = gtk.Alignment(0.5, 1, 0, 0)
        uploadAlign.add(uploadImage)
         
        startsvg = PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_MEDIA_GUI) + '/labelstart.svg'
        startpixbuf = gtk.gdk.pixbuf_new_from_file_at_size(startsvg, width= int(w/4), height=-1)
        startImage = gtk.Image()
        startImage.set_from_pixbuf(startpixbuf) 
        startAlign = gtk.Alignment(0.5, 1, 0, 0)
        startAlign.add(startImage)
         
        wifiQR = qrencode.encode_scaled('WIFI:T:WPA;S:' + PRES_CONFIG.NW_AP + ';P:' + PRES_CONFIG.NW_PW + ';;', int(w/4)-80)
        wifiQR[2].save(PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_MEDIA_GUI) + '/wifiQR.png')
        wifiQRImage = gtk.Image()
        wifiQRImage.set_from_file(PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_MEDIA_GUI) + '/wifiQR.png')
        wifiQRAlign = gtk.Alignment(0.5, 0.5, 0, 0)
        wifiQRAlign.add(wifiQRImage)        
         
        connectQR = qrencode.encode_scaled('http://' + PRES_CONFIG.NW_IP + ':' + PRES_CONFIG.NW_PORT, int(w/4)-80)
        connectQR[2].save(PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_MEDIA_GUI) + '/httpQR.png')
        connectQRImage = gtk.Image()
        connectQRImage.set_from_file(PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_MEDIA_GUI) + '/httpQR.png')
        connectQRAlign = gtk.Alignment(0.5, 0.5, 0, 0)
        connectQRAlign.add(connectQRImage)
         
        uploadimagesvg = PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_MEDIA_GUI) + '/imageupload.svg'
        uploadimagepixbuf = gtk.gdk.pixbuf_new_from_file_at_size(uploadimagesvg, width= int(w/4)-80, height=-1)
        uploadimageImage = gtk.Image()
        uploadimageImage.set_from_pixbuf(uploadimagepixbuf) 
        uploadimageAlign = gtk.Alignment(0.5, 0.5, 0, 0)
        uploadimageAlign.add(uploadimageImage)
         
        startimagesvg = PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_MEDIA_GUI) + '/imagestart.svg'
        startimagepixbuf = gtk.gdk.pixbuf_new_from_file_at_size(startimagesvg, width= int(w/4)-80, height=-1)
        startimageImage = gtk.Image()
        startimageImage.set_from_pixbuf(startimagepixbuf) 
        startimageAlign = gtk.Alignment(0.5, 0.5, 0, 0)
        startimageAlign.add(startimageImage) 
         
        self.attach(titleAlign, 0, 4, 0, 1)
         
        self.attach(wifiAlign, 0, 1, 2, 3)
        self.attach(connectAlign, 1, 2, 2, 3)
        self.attach(uploadAlign, 2, 3, 2, 3)
        self.attach(startAlign, 3, 4, 2, 3)
         
        self.attach(wifiQRAlign, 0, 1, 1, 2)
        self.attach(connectQRAlign, 1, 2, 1, 2)
        self.attach(uploadimageAlign, 2, 3, 1, 2)
        self.attach(startimageAlign, 3, 4, 1, 2)

class PresWindow(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)
        
        pub.Publisher.subscribe(self.presConnect, 'presConnect')
        pub.Publisher.subscribe(self.presSetup, 'presSetup')
        pub.Publisher.subscribe(self.presStart, 'presStart')
        pub.Publisher.subscribe(self.presQuit, 'presQuit')
        self.setWindowSize(PRES_CONFIG.W_FULLSCREEN, PRES_CONFIG.W_WIDTH, PRES_CONFIG.W_HEIGHT)
        self.set_app_paintable(True)
          
        self.startPanel = PresStartPanel(h= self.windowHeight, w=self.windowWidth)
        self.presentationPanel = PresPresentationPanel()
        
        color = (gtk.gdk).Color(65535, 65535, 65535)
        self.modify_bg(gtk.STATE_NORMAL, color)
        self.setPanel(self.startPanel)
        
    def setWindowSize(self, isFullscreen=False, width=1280, height=1024):
        if isFullscreen:
            self.fullscreen()
            screen = self.get_screen()
            mg = screen.get_monitor_geometry(screen.get_monitor_at_window(screen.get_active_window()))
            self.windowWidth = mg.width
            self.windowHeight = mg.height
        else:
            self.set_default_size(width, height)
            self.windowWidth = float(width)
            self.windowHeight = float(height)

    def presSetup(self, msg):
        pdfDocument = msg.data
        pdfDocument.calculateScaleFactor(self.windowWidth, self.windowHeight)
        self.presentationPanel.loadPresentation(pdfDocument)
        
    def presStart(self, msg):
        self.presentationPanel.fileUploaded = True;
        color = (gtk.gdk).Color(0,0,0)
        self.modify_bg(gtk.STATE_NORMAL, color)        
        self.setPanel(self.presentationPanel)
    
    def presConnect(self, msg):
        color = (gtk.gdk).Color(65535, 65535, 65535)
        self.modify_bg(gtk.STATE_NORMAL, color)        
        #self.setPanel(self.uploadPanel)
    
    def presQuit(self, msg):
        self.presentationPanel.fileUploaded = False;
        color = (gtk.gdk).Color(65535, 65535, 65535)
        self.modify_bg(gtk.STATE_NORMAL, color)        
        self.setPanel(self.startPanel)        
    
    def setPanel(self, widget):
        old = self.get_children()
        for i in old:
            self.remove(i)
        self.add(widget)
        self.show_all()
        
class PresGUI(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        window = PresWindow()
        window.connect("delete-event", self.presExit)
        window.connect("key_press_event", self.presKeyExit)
        window.show_all()
        gtk.threads_enter()
        gtk.main()
        gtk.threads_leave()
    
    def presExit(self, widget, event):
        gtk.main_quit(self, widget, event)
        pub.Publisher.sendMessage('presExit')
    
    def presKeyExit(self, widget, event):
        if event.keyval == 113:
            gtk.main_quit(self, widget, event)
            pub.Publisher.sendMessage('presExit')
        
# Lime
# 500 #cddc39
# 50#f9fbe7 249 251 231
# 100#f0f4c3 240 244 195
# 200#e6ee9c 230 238 156
# 300#dce775
# 400#d4e157
# 500#cddc39 205 220 57
# 600#c0ca33 192 202 51
# 700#afb42b 175 180 43
# 800#9e9d24 158 157 36
# 900#827717 130 119 23