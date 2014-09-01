'''
Created on Aug 28, 2014

@author: ben
'''

from wx.lib.pubsub import pub

import cairo
import poppler
import wxPython
import wx
import wx.lib.wxcairo as wxcairo
import sys
import cherrypy
import qrcode
import threading
import rsvg

 
class PDFWindow(wx.ScrolledWindow):
    """ This example class implements a PDF Viewer Window, handling Zoom and Scrolling """

    MAX_SCALE = 2
    MIN_SCALE = 1
    SCROLLBAR_UNITS = 20  # pixels per scrollbar unit

    def __init__(self, parent):
        wx.ScrolledWindow.__init__(self, parent, wx.ID_ANY)
        # Wrap a panel inside
        self.panel = wx.Panel(self)
        # Initialize variables
        self.n_page = 0
        self.scale = 1
        self.document = None
        self.n_pages = None
        self.current_page = None
        self.width = None
        self.height = None
        # Connect panel events
        self.panel.Bind(wx.EVT_PAINT, self.OnPaint)
        self.panel.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.panel.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.panel.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        pub.Publisher.subscribe(self.updateDisplay, 'updateDisplay')

    def LoadDocument(self, file):
        self.document = poppler.document_new_from_file("file://" + file, None)
        self.n_pages = self.document.get_n_pages()
        self.current_page = self.document.get_page(self.n_page)
        self.width, self.height = self.current_page.get_size() 
        self._UpdateSize()

    def OnPaint(self, event):
        dc = wx.PaintDC(self.panel)
        cr = wxcairo.ContextFromDC(dc)
        cr.set_source_rgb(1, 1, 1)  # White background
        if self.scale != 1:
            cr.scale(self.scale, self.scale)
        cr.rectangle(0, 0, self.width, self.height)
        cr.fill()
        self.current_page.render(cr)

    def OnLeftDown(self, event):
        self._UpdateScale(self.scale + 0.2)

    def OnRightDown(self, event):
        self._UpdateScale(self.scale - 0.2)
        self.writeSVG()

    def _UpdateScale(self, new_scale):
        if new_scale >= PDFWindow.MIN_SCALE and new_scale <= PDFWindow.MAX_SCALE:
            self.scale = new_scale
            # Obtain the current scroll position
            prev_position = self.GetViewStart() 
            # Scroll to the beginning because I'm going to redraw all the panel
            self.Scroll(0, 0) 
            # Redraw (calls OnPaint and such)
            self.Refresh() 
            # Update panel Size and scrollbar config
            self._UpdateSize()
            # Get to the previous scroll position
            self.Scroll(prev_position[0], prev_position[1]) 

    def _UpdateSize(self):
        u = PDFWindow.SCROLLBAR_UNITS
        self.panel.SetSize((self.width*self.scale, self.height*self.scale))
        self.SetScrollbars(u, u, (self.width*self.scale)/u, (self.height*self.scale)/u)

    def OnKeyDown(self, event):
        update = True
        # More keycodes in http://docs.wxwidgets.org/stable/wx_keycodes.html#keycodes
        keycode = event.GetKeyCode() 
        if keycode in (wx.WXK_PAGEDOWN, wx.WXK_SPACE):
            next_page = self.n_page + 1
        elif keycode == wx.WXK_PAGEUP:
            next_page = self.n_page - 1
        else:
            update = False
        if update and (next_page >= 0) and (next_page < self.n_pages):
                self.n_page = next_page
                self.current_page = self.document.get_page(next_page)
                self.Refresh()
    
    def updateDisplay(self, msg):
        next_page = self.n_page + 1
        self.n_page = next_page
        self.current_page = self.document.get_page(next_page)
        self.Refresh()
    
    def writeSVG(self):
    
        #fo = file('test.svg', 'w')

        WIDTH, HEIGHT  = 1024, 1024
        
        ## Prepare a destination surface -> out to an SVG file!
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH,HEIGHT)#cairo.SVGSurface (fo, WIDTH, HEIGHT)
        ctx = cairo.Context (surface)
        ctx.set_source_rgb(1, 1, 1)  # White background
        if self.scale != 1:
            ctx.scale(self.scale, self.scale)
        ctx.rectangle(0, 0, self.width, self.height)
        ctx.fill()
        #ctx.set_source_rgb(0.5, 0.5, 0.5)
        #ctx.fill()
        #ctx.scale (WIDTH/1.0, HEIGHT/1.0)
        #self.current_page.render_for_printing(ctx)
        
        self.current_page.render(ctx)
        surface.write_to_png("svg.png")
        
        
        
        ## draw something - this taken from the web.
        # Normalizing the canvas
        '''pat = cairo.LinearGradient (0.0, 0.0, 0.0, 1.0)
        pat.add_color_stop_rgba (1, 0.7, 0, 0, 0.5) # First stop, 50% opacity
        pat.add_color_stop_rgba (0, 0.9, 0.7, 0.2, 1) # Last stop, 100% opacity
        ctx.rectangle (0, 0, 1, 1) # Rectangle(x0, y0, x1, y1)
        ctx.set_source (pat)
        ctx.fill ()
        ctx.translate (0.1, 0.1) # Changing the current transformation matrix
        ctx.move_to (0, 0)
        ctx.arc (0.2, 0.1, 0.1, -math.pi/2, 0) # Arc(cx, cy, radius, start_angle, stop_angle)
        ctx.line_to (0.5, 0.1) # Line to (x,y)
        ctx.curve_to (0.5, 0.2, 0.5, 0.4, 0.2, 0.8) # Curve(x1, y1, x2, y2, x3, y3)
        ctx.close_path ()
        ctx.set_source_rgb (0.3, 0.2, 0.5) # Solid color
        ctx.set_line_width (0.02)
        ctx.stroke ()'''
        
        ## Do the deed.
        #surface.finish()
        #surface.write_to_png()
        

class PresFrame(wx.Frame):
 
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "wxPdf Viewer", size=(800,600))
        self.pdfwindow = PDFWindow(self)
        self.pdfwindow.LoadDocument("/home/ben/git/presberry/res/vortrag.pdf")
        self.pdfwindow.SetFocus() # To capture keyboard events
        
class PresWindow(threading.Thread):
    
    def __init__(self, serverQueue, guiQueue):
        threading.Thread.__init__(self)
        self.serverQueue = serverQueue
        self.guiQueue = guiQueue

    def run(self):

        app = wx.App()
        self.f = PresFrame()   
        self.f.Show()
        app.MainLoop()