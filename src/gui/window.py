'''
Created on Aug 28, 2014

@author: ben
'''

from wx.lib.pubsub import pub

import cairo
import poppler
import gtk
#import gobject
#from qrtools import QR
import qrencode
import threading

import util.state

 
# class PDFWindow(wx.Window):
#     """ This example class implements a PDF Viewer Window, handling Zoom and Scrolling """
# 
#     #MAX_SCALE = 2
#     #MIN_SCALE = 1
#     #SCROLLBAR_UNITS = 20  # pixels per scrollbar unit
#     
# 
#     def __init__(self, parent):
#         wx.Window.__init__(self, parent, wx.ID_ANY)
#         # Wrap a panel inside
#         self.panel = wx.Panel(self)
#         # Connect panel events
#         self.panel.Bind(wx.EVT_PAINT, self.OnPaint)
#         self.panel.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
#         self.fileUploaded = False;
#         #self.panel.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
#         #self.panel.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
#         pub.Publisher.subscribe(self.updateDisplay, 'updateDisplay')
#         pub.Publisher.subscribe(self.uploadedPDF, 'uploadedPDF')
# 
#     def load_pdf(self, uri):
#         self.doc = poppler.document_new_from_file(uri, None)
#         # the number of pages in the pdf
#         self.n_pgs = self.doc.get_n_pages()
#         # the current page of the pdf
#         self.curr_pg = 0
#         # the current page being displayed
#         self.curr_pg_disp = self.doc.get_page(self.curr_pg)        
#         # the scale of the page
#         self.scale = 1
#         # the document width and height
#         self.doc_width, self.doc_height = self.curr_pg_disp.get_size()
#         self.panel.SetSize((self.doc_width*self.scale, self.doc_height*self.scale))
#         self.Refresh()
#         self.writeSVG()
#  
#  
#     def render_pdf(self):
#         dc = wx.PaintDC(self.panel)
#         cr = wxcairo.ContextFromDC(dc)
#         cr.set_source_rgb(1, 1, 1)
#         #if self.scale != 1:
#         #    cr.scale(self.scale, self.scale)
#         cr.rectangle(0, 0, self.doc_width, self.doc_height)
#         cr.fill()
#         self.curr_pg_disp.render(cr)
#         
#         
# 
#     def OnPaint(self, event):
#         if self.fileUploaded:
#             self.render_pdf()
# 
# #     def OnLeftDown(self, event):
# #         self._UpdateScale(self.scale + 0.2)
# # 
# #     def OnRightDown(self, event):
# #         self._UpdateScale(self.scale - 0.2)
# #         self.writeSVG()
# 
# #     def _UpdateScale(self, new_scale):
# #         if new_scale >= PDFWindow.MIN_SCALE and new_scale <= PDFWindow.MAX_SCALE:
# #             self.scale = new_scale
# #             # Obtain the current scroll position
# #             prev_position = self.GetViewStart() 
# #             # Scroll to the beginning because I'm going to redraw all the panel
# #             self.Scroll(0, 0) 
# #             # Redraw (calls OnPaint and such)
# #             self.Refresh() 
# #             # Update panel Size and scrollbar config
# #             self._UpdateSize()
# #             # Get to the previous scroll position
# #             self.Scroll(prev_position[0], prev_position[1]) 
# # 
# #     def _UpdateSize(self):
# #         u = PDFWindow.SCROLLBAR_UNITS
# #         self.panel.SetSize((self.width*self.scale, self.height*self.scale))
# #         self.SetScrollbars(u, u, (self.width*self.scale)/u, (self.height*self.scale)/u)
# 
#     def OnKeyDown(self, event):
#         # More keycodes in http://docs.wxwidgets.org/stable/wx_keycodes.html#keycodes
#         keycode = event.GetKeyCode() 
#         if keycode == wx.WXK_PAGEDOWN:
#             if self.curr_pg < (self.n_pgs-1):
#                 self.curr_pg = self.curr_pg + 1
#                 self.curr_pg_disp = self.doc.get_page(self.curr_pg)
#                 self.Refresh()
#         elif keycode == wx.WXK_PAGEUP:
#             if self.curr_pg > 0:
#                 self.curr_pg = self.curr_pg - 1
#                 self.curr_pg_disp = self.doc.get_page(self.curr_pg)
#                 self.Refresh()
#         elif keycode == wx.WXK_SPACE:
#             self.writeSVG()
#             self.writePNG()
#     
#     def updateDisplay(self, msg):
#         if self.curr_pg < (self.n_pgs-1):
#             self.curr_pg = self.curr_pg + 1
#             self.curr_pg_disp = self.doc.get_page(self.curr_pg)
#             self.Refresh()
#             self.writeSVG()
#         else:
#             self.curr_pg = 0
#             self.curr_pg_disp = self.doc.get_page(self.curr_pg)
#             self.Refresh()
#             self.writeSVG()
#             
#     
#     def uploadedPDF(self, data):
#         self.fileUploaded = True;
#         print data
#         uri = 'file://' + os.path.abspath('../res/') + '/vortrag.pdf'; #'file://' + data#'
#         self.load_pdf(uri)
#         self.SetFocus()
#     
#     def writeSVG(self):
#     
#         fo = file('../res/vortrag.svg', 'w')
#         
#         WIDTH = 240
#         page = self.curr_pg_disp
#         page_width, page_height = page.get_size()
#         ratio = page_height/page_width
#         HEIGHT = round(ratio*WIDTH)
#         surface = cairo.SVGSurface (fo, WIDTH, HEIGHT)
#         cr = cairo.Context(surface) 
#         cr.translate(0, 0)
#         cr.scale(WIDTH/page_width, HEIGHT/page_height)
#         page.render(cr)
#         cr.set_operator(cairo.OPERATOR_DEST_OVER)
#         cr.set_source_rgb(1, 1, 1)
#         cr.paint()
#         surface.finish()
# 
#     def writePNG(self):
#         WIDTH = 1600
#         page = self.curr_pg_disp
#         page_width, page_height = page.get_size()
#         ratio = page_height/page_width
#         HEIGHT = int(round(ratio*WIDTH))
#         surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
#         cr = cairo.Context(surface)
#         cr.translate(0, 0)
#         cr.scale(WIDTH/page_width, HEIGHT/page_height)
#         page.render(cr)
#         cr.set_operator(cairo.OPERATOR_DEST_OVER)
#         cr.set_source_rgb(1, 1, 1)
#         cr.paint()
#         surface.write_to_png('../../res/vortrag.png')
        

# class PresFrame(wx.Frame):
#  
#     def __init__(self):
#         wx.Frame.__init__(self, None, -1, "wxPdf Viewer", size=(800,600))
#         self.pdfwindow = PDFWindow(self)
#         #uri = 'file://' + os.path.abspath('../../res/') + '/vortrag.pdf'
#         #self.pdfwindow.load_pdf(uri)
#         #self.pdfwindow.SetFocus() # To capture keyboard events
#         #super(Win, self).__init__(None, wx.ID_ANY)
#         #self.p = wx.Panel(self, wx.ID_ANY)
#         #self.p.SetSizer(wx.BoxSizer())
#         #droidfont = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, u'Roboto')
#         # set the minimum size when creating the custom window so that the sizer doesn't "squash" it to 0,0
#         #self.InitUI()
#         
#     def InitUI(self):
#     
#         panel = wx.Panel(self)
# 
#         hbox = wx.BoxSizer(wx.HORIZONTAL)
# 
#         fgs = wx.FlexGridSizer(3, 2, 9, 25)
# 
#         title = wx.StaticText(panel, label="Title")
#         author = wx.StaticText(panel, label="Author")
#         review = wx.StaticText(panel, label="Review")
# 
#         tc1 = wx.TextCtrl(panel)
#         tc2 = wx.TextCtrl(panel)
#         tc3 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
# 
#         fgs.AddMany([(title), (tc1, 1, wx.EXPAND), (author), 
#             (tc2, 1, wx.EXPAND), (review, 1, wx.EXPAND), (tc3, 1, wx.EXPAND)])
# 
#         fgs.AddGrowableRow(2, 1)
#         fgs.AddGrowableCol(1, 1)
# 
#         hbox.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
#         panel.SetSizer(hbox)

gtk.threads_init()

class PDFdocument():
#    def __init__(self):
#         self.doc
#         self.n_pgs
#         self.curr_pg
#         self.curr_pg_disp
#         self.doc_width
#         self.doc_height
       
    def loadPDF(self, uri, windowWidth, windowHeight):
        self.doc = poppler.document_new_from_file(uri, None)
        # the number of pages in the pdf
        self.n_pgs = self.doc.get_n_pages()
        # the current page of the pdf
        self.curr_pg = 0
        # the current page being displayed
        self.curr_pg_disp = self.doc.get_page(self.curr_pg)        
        # the scale of the page
        #self.scale = 1
        # the document width and height
        self.doc_width, self.doc_height = self.curr_pg_disp.get_size()
        print windowWidth,windowHeight, (self.doc_width/self.doc_height)
        if (windowWidth/windowHeight > self.doc_width/self.doc_height):
            self.scaleFactor = windowHeight/self.doc_height          
        else:            
            self.scaleFactor = windowWidth/self.doc_width  

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
        #print int(self.pdfDocument.doc_width * self.pdfDocument.scaleFactor)
        
        #self.canvas.set_size_request(int(self.pdfDocument.doc_width), int(self.pdfDocument.doc_height))
        presDrawingArea.fileUploaded = True;
        alignment = gtk.Alignment(0.5, 0.5, 0, 0)
        alignment.add(presDrawingArea)
        self.pack_start(alignment)
              

class PresDrawingArea(gtk.DrawingArea):
    def __init__(self):
        gtk.DrawingArea.__init__(self)
        #self.load_pdf('file://' + os.path.abspath('../res/') + '/vortrag.pdf')
        
        self.connect('expose-event', self.expose)
        pub.Publisher.subscribe(self.presNextPage, 'presNextPage')        
        pub.Publisher.subscribe(self.presPrevPage, 'presPrevPage')

    def loadPdfDocument(self, pdfDocument):
        self.pdfDocument = pdfDocument        
        self.writeSVG()
    #    self.hide_all()
    #    self.show_all()
        
        
    #def redraw(self, widget, event):
    #    self.renderPDF()
    
    def expose(self, widget, event):
        if self.fileUploaded:
            cr = widget.window.cairo_create()
            cr.set_source_rgb(0, 0, 0)
            cr.scale(self.pdfDocument.scaleFactor, self.pdfDocument.scaleFactor)
            self.pdfDocument.curr_pg_disp.render(cr)
            #p_width, p_height = widget.window.get_size()
            #self.panel_width = float(p_width);
            #self.panel_height = float(p_height);
            #self.horIdent = 0;
            #self.verIdent = 0;
            #self.scaleFactor = 0.0
           
            #print self.panel_width, self.panel_height
            #print float(self.panel_width)/float(self.panel_height), self.doc_width/self.doc_height
            
            #if (self.panel_width/self.panel_height > self.pdfDocument.doc_width/self.pdfDocument.doc_height):
            #    self.scaleFactor = self.panel_height/self.pdfDocument.doc_height
                #self.horIdent = (self.panel_width - (self.scaleFactor*self.doc_width))/2
                #self.set_size_request(int(self.scaleFactor*self.pdfDocument.doc_width), p_height)  
            
            #else:
            #    self.scaleFactor = self.panel_width/self.pdfDocument.doc_width
                #self.verIdent = (self.panel_height - (self.scaleFactor*self.doc_height))/2
                #self.set_size_request(p_width, int(self.scaleFactor*self.pdfDocument.doc_width))
                #cr.scale(self.panel_height/self.doc_height, self.panel_height/self.doc_height)
                
#                 #cr.rectangle(self.panel_width-, 0,  self.doc_width, self.doc_height)
#             #print self.panel_width/self.doc_width , self.panel_height/self.doc_height , self.panel_width/self.panel_height , self.doc_width, self.doc_height
            
                #cr.scale(self.panel_width/self.dodoc_widthc_width, self.panel_width/self.doc_width)
            #   # print self.panel_width/self.doc_width , self.panel_height/self.doc_height , self.panel_width/self.panel_height
            
            
            #cr.rectangle(0, 0,  self.scaleFactor*self.doc_width, self.scaleFactor*self.doc_height)
            #cr.rectangle(0, 0,  self.pdfDocument.doc_width, self.pdfDocument.doc_height)
            
            #cr.rectangle(0,0, p_width, p_height)
            #cr.fill()          
            #print cr.region()
            
            
            
            #cr.moveTo()
            #cr.move_to(self.horIdent, self.verIdent)
            
            
#     def renderPDF(self):
#         if self.fileUploaded:
#             cr = self.window.cairo_create()
#             cr.set_source_rgb(1, 1, 1)
#             cr.scale(2.0, 2.0)
#             cr.rectangle(0, 0,  self.doc_width, self.doc_height)
#             cr.fill()            
#             self.curr_pg_disp.render(cr)
#             #self.queue_draw()
    
    def writeSVG(self):
     
        fo = file('../res/vortrag.svg', 'w')
         
        WIDTH = 400
        page = self.pdfDocument.curr_pg_disp
        page_width, page_height = page.get_size()
        ratio = page_height/page_width
        HEIGHT = round(ratio*WIDTH)
        surface = cairo.SVGSurface (fo, WIDTH, HEIGHT)
        cr = cairo.Context(surface) 
        cr.translate(0, 0)
        cr.scale(WIDTH/page_width, HEIGHT/page_height)
        page.render(cr)
        cr.set_operator(cairo.OPERATOR_DEST_OVER)
        cr.set_source_rgb(1, 1, 1)
        cr.paint()
        surface.finish()
        print 'svg written'

    
    def presNextPage(self, msg):
        if self.pdfDocument.curr_pg < (self.pdfDocument.n_pgs-1):
            self.pdfDocument.curr_pg = self.pdfDocument.curr_pg + 1
            self.pdfDocument.curr_pg_disp = self.pdfDocument.doc.get_page(self.pdfDocument.curr_pg)
            self.hide_all()
            self.show_all()
        else:
            self.pdfDocument.curr_pg = 0
            self.pdfDocument.curr_pg_disp = self.pdfDocument.doc.get_page(self.pdfDocument.curr_pg)
            self.hide_all()
            self.show_all()
        self.writeSVG()
    
    def presPrevPage(self, msg):
        if self.pdfDocument.curr_pg > 0:
            self.pdfDocument.curr_pg = self.pdfDocument.curr_pg-1
            self.pdfDocument.curr_pg_disp = self.pdfDocument.doc.get_page(self.pdfDocument.curr_pg)
            self.hide_all()
            self.show_all()
        else:
            self.pdfDocument.curr_pg = self.pdfDocument.n_pgs-1
            self.pdfDocument.curr_pg_disp = self.pdfDocument.doc.get_page(self.pdfDocument.curr_pg)
            self.hide_all()
            self.show_all()
        self.writeSVG()
        
class PresStartPanel(gtk.Table):
    def __init__(self, rows=2, columns=3, homogenous=False):
        gtk.Table.__init__(self, rows, columns, homogenous)
        
        
        titleImage = gtk.Image()
        titleImage.set_from_file("../res/title.png")
        titleAlign = gtk.Alignment(0.5, 0, 0, 0)
        titleAlign.add(titleImage)
        
        wifiImage = gtk.Image()
        wifiImage.set_from_file("../res/sidebar1.png")
        
         
        wifiQR = qrencode.encode_scaled('WIFI:T:WPA;S:Pres_AP;P:Pres_AP;;', 400)
        #wifiData=[u"Presberry_AP", u"WPA", u"PresberryIstKlasse" ]
        #wifiQR = QR(data=wifiData, data_type=u"wifi", pixel_size=13, level='L', margin_size=0 )
        #wifiQR.encode()
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
        
        httpQR = qrencode.encode_scaled('http://presberry.org:8080', 400)
        httpQR[2].save('../res/httpQR.png')
        #httpQR = QR(data=u"http://presberry.org:8080", pixel_size=15, level='L', margin_size=0)
        #httpQR.encode()
        httpQRImage = gtk.Image()
        httpQRImage.set_from_file('../res/httpQR.png')
        #httpQRImage.set_from_file(httpQR.filename)
        
        httpBox = gtk.HBox()
        httpBox.pack_start(httpQRImage)
        httpBox.pack_start(httpImage)
        httpAlign = gtk.Alignment(1, 0.5, 0, 0)
        httpAlign.add(httpBox)
        
        arrowImage = gtk.Image()
        arrowImage.set_from_file("../res/arrowImage.png")
        arrowAlign = gtk.Alignment(0.5, 0.5, 0, 0)
        arrowAlign.add(arrowImage)       
        
        self.attach(titleAlign, 0, 3, 0, 1)
        self.attach(wifiAlign, 0, 1, 1, 2)
        self.attach(arrowAlign, 1, 2, 1, 2)
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
        
        uploadQRImage = gtk.Image()
        uploadQRImage.set_from_file("../res/uploadImage.png")
        
        uploadBox = gtk.HBox()
        uploadBox.pack_start(uploadImage)
        uploadBox.pack_start(uploadQRImage)
        uploadAlign = gtk.Alignment(0, 0.5, 0, 0)
        uploadAlign.add(uploadBox)
                
        startImage = gtk.Image()
        startImage.set_from_file("../res/sidebar4.png")
        
        startQRImage = gtk.Image()
        startQRImage.set_from_file("../res/startImage.png")
        
        arrowImage = gtk.Image()
        arrowImage.set_from_file("../res/arrowImage.png")
        arrowAlign = gtk.Alignment(0.5, 0.5, 0, 0)
        arrowAlign.add(arrowImage)
       
        startBox = gtk.HBox()
        startBox.pack_start(startQRImage)
        startBox.pack_start(startImage)
        startAlign = gtk.Alignment(1, 0.5, 0, 0)
        startAlign.add(startBox)       
        
        self.attach(titleAlign, 0, 3, 0, 1)
        self.attach(uploadAlign, 0, 1, 1, 2)
        self.attach(arrowAlign, 1, 2, 1, 2)
        self.attach(startAlign, 2, 3, 1, 2)

class PresWindow(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)
        
        pub.Publisher.subscribe(self.presUpload, 'presUpload')
        pub.Publisher.subscribe(self.presConnect, 'presConnect')
        pub.Publisher.subscribe(self.presQuit, 'presQuit')
        #pub.Publisher.subscribe(self.updateDisplay, 'updateDisplay')
        #self.isFullscreen = False
        self.setWindowSize()
        self.set_app_paintable(True)
                
        self.startState = util.state.StartState(self)
        self.presentationState = util.state.PresentationState(self)
        self.uploadState = util.state.UploadState(self)
        
        self.presState = self.startState
        
        self.startPanel = PresStartPanel()
        self.uploadPanel = PresUploadPanel()
        self.presentationPanel = PresPresentationPanel()
        
        color = (gtk.gdk).Color(65535, 65535, 65535)
        self.modify_bg(gtk.STATE_NORMAL, color)
        self.setPanel(self.startPanel)
        #self.add(self.startPanel)
        #self.show_all()
        
        
        #vbox = gtk.VBox()
       
        #screen = self.get_screen()
        #mg = screen.get_monitor_geometry(screen.get_monitor_at_window(screen.get_active_window()))
        #print "monitor: %d x %d" % (mg.width,mg.height)
            # current monitor
        #curmon = screen.get_monitor_at_window(screen.get_active_window())
        #print screen.get_width(), screen.get_height()
        
    def setWindowSize(self, isFullscreen=False, width=1200, height=800):
        if isFullscreen:
            self.fullscreen()
            screen = self.get_screen()
            mg = screen.get_monitor_geometry(screen.get_monitor_at_window(screen.get_active_window()))
            self.windowWidth = mg.width
            self.windowHeight = mg.height
            #print mg.width, mg.height
        else:
            self.set_default_size(width, height)
            self.windowWidth = float(width)
            self.windowHeight = float(height)
            
        

    def presUpload(self, data):
        
        uri = 'file://' + data.data#.tostring() #os.path.abspath('../res/') + '/vortrag.pdf'; #'file://' + data#'
        print data.data
        pdfDocument = PDFdocument()
        pdfDocument.loadPDF(uri, self.windowWidth, self.windowHeight)
        #self.presPanel = PresPresentationPanel()
        self.presentationPanel.loadPresentation(pdfDocument)
        
        
        #self.add(alignment)
        #self.show_all()
        color = (gtk.gdk).Color(0,0,0)
        self.modify_bg(gtk.STATE_NORMAL, color)
        
        self.setPanel(self.presentationPanel)
        self.presState.nextState()
       
        #self.canvas.hide_all()
        #self.canvas.show_all()
        #self.alignment.set(0.5, 0.5, 0, 0)
    #def updateDisplay(self, msg):
        #self.presState.nextState()
    
    def presConnect(self, data):
        self.presentationPanel.fileUploaded = False;
        color = (gtk.gdk).Color(65535, 65535, 65535)
        self.modify_bg(gtk.STATE_NORMAL, color)
        
        self.setPanel(self.uploadPanel)
        self.presState.nextState()
    
    def presQuit(self, data):
        color = (gtk.gdk).Color(65535, 65535, 65535)
        self.modify_bg(gtk.STATE_NORMAL, color)
        
        self.setPanel(self.startPanel)
        self.presState.nextState()
        
    
    def setPanel(self, widget):
        old = self.get_children()
        for i in old:
            self.remove(i)
        self.add(widget)
        self.show_all()
        
        

        
class PresGUI(threading.Thread):
    
#     def __init__(self, serverQueue, guiQueue):
#         threading.Thread.__init__(self)
#         self.serverQueue = serverQueue
#         self.guiQueue = guiQueue
    
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        window = PresWindow()
        window.connect("delete-event", gtk.main_quit)
        window.show_all()
        gtk.threads_enter()
        gtk.main()
        gtk.threads_leave()

#def draw(widget, surface):
#        page.render(surface)

#document = poppler.document_new_from_file('file://' + os.path.abspath('../res/') + '/vortrag.pdf', None)
#page = document.get_page(0)
        
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