'''
Created on Sep 12, 2014

@author: ben
'''
import poppler

class PDFdocument():
    def __init__(self, uri):
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
       
    def calculateScaleFactor(self, windowWidth, windowHeight):
        if (windowWidth/windowHeight > self.doc_width/self.doc_height):
            self.scaleFactor = windowWidth/self.doc_width          
        else:
            self.scaleFactor = windowHeight/self.doc_height  