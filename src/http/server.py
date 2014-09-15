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

#MEDIA_DIR = os.path.join(os.path.abspath("../"), u"media")
#RES_DIR = os.path.join(os.path.abspath("../"), u"res")
conf = {
     '/' + PRES_CONFIG.DIR_MEDIA_PRESENTATION:
        {'tools.staticdir.on': True,
         'tools.staticdir.dir': PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_MEDIA_PRESENTATION)
        },          
    '/' + PRES_CONFIG.DIR_HTML:
        {'tools.staticdir.on': True,
         'tools.staticdir.dir': PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_HTML)
        },
    '/' + PRES_CONFIG.DIR_JS:
        {'tools.staticdir.on': True,
         'tools.staticdir.dir': PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_JS)
        },
    '/' + PRES_CONFIG.DIR_CSS:
        {'tools.staticdir.on': True,
         'tools.staticdir.dir': PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_CSS)
        },
    '/' + PRES_CONFIG.DIR_CSS + '/fonts':
        {'tools.staticdir.on': True,
         'tools.staticdir.dir': PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_CSS + '/fonts')
        },
    '/' + PRES_CONFIG.DIR_JQUERYMOBILE:
        {'tools.staticdir.on': True,
         'tools.staticdir.dir': PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_JQUERYMOBILE)
        },
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
        self.slideMode = "change";
        self.slideOrder = "normal";
    
    @cherrypy.expose
    def index(self):
        pub.Publisher.sendMessage('presConnect')
        #htmlTemplate = open(os.path.join(PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_HTML), u'index.html'))
        presHTMLTemplate = htmlGenerator.generateHTML('presberry.html',
                                                      html_dir= PRES_CONFIG.DIR_HTML,
                                                      css_dir= PRES_CONFIG.DIR_CSS,
                                                      js_dir= PRES_CONFIG.DIR_JS,
                                                      jquerymobile_dir= PRES_CONFIG.DIR_JQUERYMOBILE,
                                                      pres_dir= PRES_CONFIG.DIR_MEDIA_PRESENTATION)
        return presHTMLTemplate

    @cherrypy.expose
    def upload(self, presFile, upload):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        if(presFile.content_type.value == 'application/pdf'):
            uload_path = PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_MEDIA_PRESENTATION) + os.path.sep + presFile.filename;
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
                self.pdfDocument = PDFdocument('file://' + uload_path, presFile.filename)
                svgGenerator = SVGGenerator(self.pdfDocument, PRES_CONFIG.SVG_WIDTH)
                svgGenerator.start()
                pub.Publisher.sendMessage('presUpload', data=self.pdfDocument)               
                htmlTemplate = htmlGenerator.generateHTML('carousel.html',
                                                      pres_dir= PRES_CONFIG.DIR_MEDIA_PRESENTATION,
                                                      numPages=self.pdfDocument.n_pgs,
                                                      filename=self.pdfDocument.filename,
                                                      width="100%",
                                                      height="100%",
                                                      order=self.slideOrder)
                previewImage =  htmlGenerator.generateHTML('previewElement.html',
                                                      pres_dir= PRES_CONFIG.DIR_MEDIA_PRESENTATION,
                                                      filename=self.pdfDocument.filename,
                                                      width="50%",
                                                      height="50%")
                return simplejson.dumps(dict(html=htmlTemplate, preview=previewImage))
            except ValueError:
                raise cherrypy.HTTPError(400, 'SOME ERROR')                   
        return simplejson.dumps(dict(html=""))     
            #return open(os.path.join(PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_HTML), u'startpresentation.html'))
        #return open(os.path.join(PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_HTML), u'index.html'))
    @cherrypy.expose
    def startPresentation(self, **kwargs):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        pub.Publisher.sendMessage('presStart')
        return simplejson.dumps(dict(mode=self.slideMode, order=self.slideOrder))
    
    @cherrypy.expose
    def quitPresentation(self, **kwargs):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        pub.Publisher.sendMessage('presQuit')
        return simplejson.dumps(dict())
    
    @cherrypy.expose
    def settings(self, slideMode, slideOrder):
        self.slideMode = slideMode;
        self.slideOrder = slideOrder;
        cherrypy.response.headers['Content-Type'] = 'application/json'       
        return simplejson.dumps(dict())
    
    @cherrypy.expose
    def setPage(self, pageNr):
        pub.Publisher.sendMessage('presSetPage', pageNr)
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return simplejson.dumps(dict(page=pageNr))
    
#     @cherrypy.expose
#     def loadPresentation(self):
#         htmlTemplate = htmlGenerator.generateHTML('carousel.html',
#                                                       pres_dir= PRES_CONFIG.DIR_MEDIA_PRESENTATION,
#                                                       numPages=self.pdfDocument.n_pgs,
#                                                       width="100%",
#                                                       height="100%",
#                                                       order=self.slideOrder)
#         return simplejson.dumps(dict(html=htmlTemplate))
#        
#     @cherrypy.expose
#     def quitPresentation(self):
#         pub.Publisher.sendMessage('presQuit')
#         return open(os.path.join(PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_HTML), u'finished.html'))
#     
#     @cherrypy.expose
#     def startPresentation(self, slideMode, slideOrder):
#         pub.Publisher.sendMessage('presStart')
#         presHTMLTemplate = htmlGenerator.generateHTML('presentation.html',
#                                                       html_dir= PRES_CONFIG.DIR_HTML,
#                                                       css_dir= PRES_CONFIG.DIR_CSS,
#                                                       js_dir= PRES_CONFIG.DIR_JS,
#                                                       jquerymobile_dir= PRES_CONFIG.DIR_JQUERYMOBILE,
#                                                       pres_dir= PRES_CONFIG.DIR_MEDIA_PRESENTATION,
#                                                       numPages=self.pdfDocument.n_pgs,
#                                                       width=self.browserWidth,
#                                                       height=self.browserHeight,
#                                                       mode=slideMode,
#                                                       order=slideOrder)
#         return presHTMLTemplate
    
    
        
      
   
    
#     @cherrypy.expose
#     def setSize(self, browserWidth, browserHeight):
#         self.browserWidth = int(browserWidth)
#         self.browserHeight = int(browserHeight)
#         print self.browserHeight
#         cherrypy.response.headers['Content-Type'] = 'application/json'
#         return simplejson.dumps(dict())