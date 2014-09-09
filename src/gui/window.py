'''
Created on Aug 28, 2014

@author: ben
'''

from wx.lib.pubsub import pub

import cairo
import poppler
import gtk
import gobject
#import qrcode
import threading
import rsvg
import os, os.path
import urllib

 
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

class PresCanvas(gtk.DrawingArea):
    def __init__(self):
        super(PresCanvas, self).__init__()
        #self.load_pdf('file://' + os.path.abspath('../res/') + '/vortrag.pdf')
        self.fileUploaded = False;
        self.connect('expose-event', self.expose)
        pub.Publisher.subscribe(self.updateDisplay, 'updateDisplay')
        pub.Publisher.subscribe(self.uploadedPDF, 'uploadedPDF')

    def load_pdf(self, uri):
        self.doc = poppler.document_new_from_file(uri, None)
        # the number of pages in the pdf
        self.n_pgs = self.doc.get_n_pages()
        # the current page of the pdf
        self.curr_pg = 0
        # the current page being displayed
        self.curr_pg_disp = self.doc.get_page(self.curr_pg)        
        # the scale of the page
        self.scale = 1
        # the document width and height
        self.doc_width, self.doc_height = self.curr_pg_disp.get_size()
        
        self.hide_all()
        self.show_all()
        
    #def redraw(self, widget, event):
    #    self.renderPDF()
    
    def expose(self, widget, event):
        if self.fileUploaded:
            cr = widget.window.cairo_create()
            cr.set_source_rgb(1, 1, 1)
            cr.scale(2.0, 2.0)
            cr.rectangle(0, 0,  self.doc_width, self.doc_height)
            cr.fill()            
            self.curr_pg_disp.render(cr)
            
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
         
        WIDTH = 800
        page = self.curr_pg_disp
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

    
    def updateDisplay(self, msg):
        if self.curr_pg < (self.n_pgs-1):
            self.curr_pg = self.curr_pg + 1
            self.curr_pg_disp = self.doc.get_page(self.curr_pg)
            self.hide_all()
            self.show_all()
        else:
            self.curr_pg = 0
            self.curr_pg_disp = self.doc.get_page(self.curr_pg)
            self.hide_all()
            self.show_all()
        self.writeSVG()
    
    def uploadedPDF(self, data):
        self.fileUploaded = True;
        uri = 'file://' + os.path.abspath('../res/') + '/vortrag.pdf'; #'file://' + data#'
        self.load_pdf(uri)
        
class PresWindow(threading.Thread):
    
    def __init__(self, serverQueue, guiQueue):
        threading.Thread.__init__(self)
        self.serverQueue = serverQueue
        self.guiQueue = guiQueue       

    def run(self):
        window = gtk.Window()
        window.set_default_size(800, 600)
        window.connect("delete-event", gtk.main_quit)
        #window.connect("expose-event", draw)
        window.set_app_paintable(True)
        canvas = PresCanvas()
        window.add(canvas)
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