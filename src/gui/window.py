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
    def __init__(self, rows=2, columns=3, homogenous=False):
        gtk.Table.__init__(self, rows, columns, homogenous)     
        
        titleImage = gtk.Image()
        titleImage.set_from_file("../res/title.png")
        titleAlign = gtk.Alignment(0.5, 0, 0, 0)
        titleAlign.add(titleImage)
        
        wifiImage = gtk.Image()
        wifiImage.set_from_file("../res/sidebar1.png")
         
        wifiQR = qrencode.encode_scaled('WIFI:T:WPA;S:' + PRES_CONFIG.NW_AP + ';P:' + PRES_CONFIG.NW_PW + ';;', 400)
        wifiQR[2].save('../res/wifiQR.png')
        wifiQRImage = gtk.Image()
        wifiQRImage.set_from_file('../res/wifiQR.png')
        
        wifiBox = gtk.HBox()
        wifiBox.pack_start(wifiImage)
        wifiBox.pack_start(wifiQRImage)
        wifiAlign = gtk.Alignment(0, 0.5, 0, 0)
        wifiAlign.add(wifiBox)        
        
        httpImage = gtk.Image()
        httpImage.set_from_file("../res/sidebar2.png")
        httpQR = qrencode.encode_scaled('http://' + PRES_CONFIG.NW_IP + ':' + PRES_CONFIG.NW_PORT, 400)
        httpQR[2].save('../res/httpQR.png')
        
        httpQRImage = gtk.Image()
        httpQRImage.set_from_file('../res/httpQR.png')
          
        httpBox = gtk.HBox()
        httpBox.pack_start(httpQRImage)
        httpBox.pack_start(httpImage)
        httpAlign = gtk.Alignment(1, 0.5, 0, 0)
        httpAlign.add(httpBox)
         
        self.attach(titleAlign, 0, 3, 0, 1)
        self.attach(wifiAlign, 0, 1, 1, 2)
        self.attach(httpAlign, 2, 3, 1, 2)
        
class PresUploadPanel(gtk.Table):
    def __init__(self, rows=2, columns=3, homogenous=False):
        gtk.Table.__init__(self, rows, columns, homogenous)        
        
        titleImage = gtk.Image()
        titleImage.set_from_file("../res/title.png")
        titleAlign = gtk.Alignment(0.5, 0, 0, 0)
        titleAlign.add(titleImage)
        
        uploadImage = gtk.Image()
        uploadImage.set_from_file("../res/sidebar3.png")
        
        uploadIconImage = gtk.Image()
        uploadIconImage.set_from_file("../res/uploadImage.png")
        
        uploadBox = gtk.HBox()
        uploadBox.pack_start(uploadImage)
        uploadBox.pack_start(uploadIconImage)
        uploadAlign = gtk.Alignment(0, 0.5, 0, 0)
        uploadAlign.add(uploadBox)
                
        startImage = gtk.Image()
        startImage.set_from_file("../res/sidebar4.png")
        
        startIconImage = gtk.Image()
        startIconImage.set_from_file("../res/startImage.png")
          
        startBox = gtk.HBox()
        startBox.pack_start(startIconImage)
        startBox.pack_start(startImage)
        startAlign = gtk.Alignment(1, 0.5, 0, 0)
        startAlign.add(startBox)       
        
        self.attach(titleAlign, 0, 3, 0, 1)
        self.attach(uploadAlign, 0, 1, 1, 2)
        self.attach(startAlign, 2, 3, 1, 2)

class PresWindow(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)
        
        pub.Publisher.subscribe(self.presConnect, 'presConnect')
        pub.Publisher.subscribe(self.presUpload, 'presUpload')
        pub.Publisher.subscribe(self.presStart, 'presStart')
        pub.Publisher.subscribe(self.presQuit, 'presQuit')
        self.setWindowSize(PRES_CONFIG.W_FULLSCREEN, PRES_CONFIG.W_WIDTH, PRES_CONFIG.W_HEIGHT)
        self.set_app_paintable(True)
          
        self.startPanel = PresStartPanel()
        self.uploadPanel = PresUploadPanel()
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

    def presUpload(self, msg):
        pdfDocument = msg.data
        pdfDocument.calculateScaleFactor(self.windowWidth, self.windowHeight)
        self.presentationPanel.loadPresentation(pdfDocument)
        
    def presStart(self, msg):
        color = (gtk.gdk).Color(0,0,0)
        self.modify_bg(gtk.STATE_NORMAL, color)        
        self.setPanel(self.presentationPanel)
    
    def presConnect(self, msg):
        self.presentationPanel.fileUploaded = False;
        color = (gtk.gdk).Color(65535, 65535, 65535)
        self.modify_bg(gtk.STATE_NORMAL, color)        
        self.setPanel(self.uploadPanel)
    
    def presQuit(self, msg):
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
# 50#f9fbe7
# 100#f0f4c3
# 200#e6ee9c
# 300#dce775
# 400#d4e157
# 500#cddc39
# 600#c0ca33
# 700#afb42b
# 800#9e9d24
# 900#827717