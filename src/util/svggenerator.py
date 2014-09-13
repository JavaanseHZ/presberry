'''
Created on Sep 12, 2014

@author: ben
'''
import threading
import cairo

class SVGGenerator(threading.Thread):
    def __init__(self, pdfDocument, width=200):
        threading.Thread.__init__(self)
        self.pdfDocument = pdfDocument
        self.width = width
    
    def run(self):
        for i in range (0, self.pdfDocument.n_pgs):
            fo = file('../res/vortrag_' + str(i) + '.svg', 'w')            
            page = self.pdfDocument.doc.get_page(i)
            page_width, page_height = page.get_size()
            ratio = page_height/page_width
            HEIGHT = round(ratio*self.width)
            surface = cairo.SVGSurface (fo, self.width, HEIGHT)
            cr = cairo.Context(surface) 
            cr.translate(0, 0)
            cr.scale(self.width/page_width, HEIGHT/page_height)
            page.render(cr)
            cr.set_operator(cairo.OPERATOR_DEST_OVER)
            cr.set_source_rgb(1, 1, 1)
            cr.paint()
            surface.finish()