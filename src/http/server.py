'''
Created on Aug 28, 2014

@author: ben
'''

from wx.lib.pubsub import pub
import cherrypy
import threading
import os
import mimetypes
import simplejson
from util.svggenerator import SVGGenerator
from document.pdfdocument import PDFdocument
from http import HTMLGenerator


#import time
#import Queue
#import webbrowser

MEDIA_DIR = os.path.join(os.path.abspath("../"), u"media")
RES_DIR = os.path.join(os.path.abspath("../"), u"res")
conf = {
    '/media':
        {'tools.staticdir.on': True,
         'tools.staticdir.dir': MEDIA_DIR
        },          
    '/res':
        {'tools.staticdir.on': True,
         'tools.staticdir.dir': RES_DIR
        }
    }


class HTTPServer(threading.Thread):
#     def __init__(self, serverQueue, guiQueue):
#         threading.Thread.__init__(self)
#         self.serverQueue = serverQueue
#         self.guiQueue = guiQueue
    
    def __init__(self):
        threading.Thread.__init__(self)
        

    def run(self):
        cherrypy.server.socket_port = 8080
        #server.socket_host': '0.0.0.0'}
        cherrypy.server.socket_host = '0.0.0.0'
        #cherrypy.engine.subscribe('start', open_page)
        pub.Publisher.subscribe(self.presExit, 'presExit')
        if not mimetypes.inited:
            mimetypes.init()
        mimetypes.add_type('image/svg+xml', '.svg', True)
        
        cherrypy.tree.mount(PresWebsite(), '/', config=conf)
        cherrypy.engine.start()
        cherrypy.engine.block()
        
    def stop(self):
        cherrypy.engine.exit()
        cherrypy.server.stop()
        
    def presExit(self, msg):
        cherrypy.engine.exit()
        cherrypy.server.stop()
    
#def open_page():
#    webbrowser.open("http://127.0.0.1:8080/")

class PresWebsite(object):
    
    def __init__(self):
        object.__init__(self)
        self.windwowWidth = 0
        self.windwowHeight = 0
        #self.serverQueue = Queue.Queue()
        #self.svgReady = False
        #pub.Publisher.subscribe(self.presSVGReady, 'presSVGReady')
        
    #def presSVGReady(self, msg):
    #    self.svgReady = True
        #self.serverQueue.put('ready')
        
    
    @cherrypy.expose
    def index(self):
        pub.Publisher.sendMessage('presConnect')
        return open(os.path.join(MEDIA_DIR, u'index.html'))
        

    @cherrypy.expose
    def upload(self, presFile, width, height):
        self.windwowWidth = width
        self.windwowHeight = height
        print 'filename:' + presFile.filename
        uload_path = RES_DIR
        file_name = 'vortrag.pdf'
    
        uload_path = uload_path + os.path.sep + file_name                
     
        size = 0
        all_data = ''
        while True:
            data = presFile.file.read(8192)
            all_data += data
            if not data:
                break
            size += len(data)
     
        try:
            saved_file=open(uload_path, 'wb')
            saved_file.write(all_data) 
            saved_file.close()
            self.pdfDocument = PDFdocument('file://' + uload_path)
            svgGenerator = SVGGenerator(self.pdfDocument)
            svgGenerator.start()
            pub.Publisher.sendMessage('presUpload', data=self.pdfDocument)
        except ValueError:
            raise cherrypy.HTTPError(400, 'SOME ERROR')       
        return open(os.path.join(MEDIA_DIR, u'startpresentation.html'))
    
    @cherrypy.expose
    def quitPresentation(self):
        pub.Publisher.sendMessage('presQuit')
        return open(os.path.join(MEDIA_DIR, u'finished.html'))
    
    @cherrypy.expose
    def startPresentation(self):
        pub.Publisher.sendMessage('presStart')
        jinjaVars = {'numPages' : self.pdfDocument.n_pgs, 'width' : self.pdfDocument.doc_width, 'height' :self.pdfDocument.doc_height}
        presHTMLTemplate = HTMLGenerator.generateHTML("presentation.html", jinjaVars)
        return open(os.path.join(MEDIA_DIR, u'presentation.html'))
      
    @cherrypy.expose
    def setPage(self, pageNr):
        pub.Publisher.sendMessage('presSetPage', pageNr)
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return simplejson.dumps(dict(page=pageNr))
        #return body#open(os.path.join(MEDIA_DIR, u'presentation.html'))    
        
        

#     @cherrypy.expose
#     def submit(self, name):
#         pub.Publisher.sendMessage('updateDisplay')
#         cherrypy.response.headers['Content-Type'] = 'application/json'
#         return simplejson.dumps(dict(title="Hello, %s" % name))
    
#     @cherrypy.expose
#     def upload(self, filename):
#         
#         pub.Publisher.sendMessage('uploadedPDF', data=filename)
#         cherrypy.response.headers['Content-Type'] = 'application/json'
#         return simplejson.dumps(dict(filename="/res/vortrag.svg"))
    
    

