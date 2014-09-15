'''
Created on Sep 12, 2014

@author: ben
'''
import poppler

class PDFdocument():
    def __init__(self, uri, filename, timestamp):
        self.doc = poppler.document_new_from_file(uri, None)
        self.timestamp = timestamp
        self.n_pgs = self.doc.get_n_pages()
        self.filename = filename
        self.curr_pg = 0
        self.curr_pg_disp = self.doc.get_page(self.curr_pg)
        self.doc_width, self.doc_height = self.curr_pg_disp.get_size()
       
    def calculateScaleFactor(self, windowWidth, windowHeight):
        self.scaleFactor = windowWidth/self.doc_width
        if(windowHeight +1 < (self.doc_height * self.scaleFactor)): #offset for float calculation 
            self.scaleFactor = windowHeight/self.doc_height