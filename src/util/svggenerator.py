'''
Created on Sep 12, 2014

@author: ben
'''
import threading
import cairo
import util.config as PRES_CONFIG
import os
import poppler

class SVGGenerator(threading.Thread):
    def __init__(self, pdfDocument, width=200):
        threading.Thread.__init__(self)
        self.pdfDocument = pdfDocument
        self.path = PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_MEDIA_TEMP) + os.path.sep + self.pdfDocument.timestamp + self.pdfDocument.filename
        self.width = width
    
    def run(self):
        for i in range (0, self.pdfDocument.n_pgs):
            fo = file(self.path + str(i) + '.svg', 'w')            
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

class SVGGeneratorPreview(threading.Thread):
    def __init__(self, filePath, width=80):
        threading.Thread.__init__(self)
        self.filePath=filePath
        self.doc = poppler.document_new_from_file('file://' + self.filePath, None)
        self.indexPage = self.doc.get_page(0)
        self.width = width
    
    def run(self):
            fo = file(self.filePath + '0.svg', 'w')            
            page_width, page_height = self.indexPage.get_size()
            ratio = page_height/page_width
            HEIGHT = round(ratio*self.width)
            surface = cairo.SVGSurface (fo, self.width, HEIGHT)
            cr = cairo.Context(surface) 
            cr.translate(0, 0)
            cr.scale(self.width/page_width, HEIGHT/page_height)
            self.indexPage.render(cr)
            cr.set_operator(cairo.OPERATOR_DEST_OVER)
            cr.set_source_rgb(1, 1, 1)
            cr.paint()
            surface.finish()