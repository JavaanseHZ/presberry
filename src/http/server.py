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
from http import htmlGenerator
import util.config as PRES_CONFIG

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

    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        cherrypy.server.socket_port = 8080
        cherrypy.server.socket_host = '0.0.0.0'
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

class PresWebsite(object):
    
    def __init__(self):
        object.__init__(self)
    
    @cherrypy.expose
    def index(self):
        pub.Publisher.sendMessage('presConnect')
        return open(os.path.join(MEDIA_DIR, u'index.html'))

    @cherrypy.expose
    def upload(self, presFile):
        if(presFile.content_type.value == 'application/pdf'):
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
                svgGenerator = SVGGenerator(self.pdfDocument, PRES_CONFIG.SVG_WIDTH)
                svgGenerator.start()
                pub.Publisher.sendMessage('presUpload', data=self.pdfDocument)
            except ValueError:
                raise cherrypy.HTTPError(400, 'SOME ERROR')       
            return open(os.path.join(MEDIA_DIR, u'startpresentation.html'))
        return open(os.path.join(MEDIA_DIR, u'index.html')) 
    
    @cherrypy.expose
    def quitPresentation(self):
        pub.Publisher.sendMessage('presQuit')
        return open(os.path.join(MEDIA_DIR, u'finished.html'))
    
    @cherrypy.expose
    def startPresentation(self, slideMode, slideOrder):
        pub.Publisher.sendMessage('presStart')
        presHTMLTemplate = htmlGenerator.generateHTML("presentation.html",
                                                      numPages=self.pdfDocument.n_pgs,
                                                      width=self.browserWidth,
                                                      height=self.browserHeight,
                                                      mode=slideMode,
                                                      order=slideOrder)
        return presHTMLTemplate
      
    @cherrypy.expose
    def setPage(self, pageNr):
        pub.Publisher.sendMessage('presSetPage', pageNr)
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return simplejson.dumps(dict(page=pageNr))
    
    @cherrypy.expose
    def setSize(self, browserWidth, browserHeight):
        self.browserWidth = int(browserWidth)
        self.browserHeight = int(browserHeight)
        print self.browserHeight
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return simplejson.dumps(dict())