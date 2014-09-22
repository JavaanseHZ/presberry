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
from datetime import datetime

from http.svggenerator import SVGGenerator, SVGGeneratorPreview
from http.pnggenerator import PNGGenerator, PNGGeneratorPreview
from document.pdfdocument import PDFdocument
from http import htmlGenerator
import util.config as PRES_CONFIG
import util.presString as presString
import util.presFile as presFile

conf = {
     '/' + PRES_CONFIG.DIR_MEDIA_PRESENTATION:
        {'tools.staticdir.on': True,
         'tools.staticdir.dir': PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_MEDIA_PRESENTATION)
        },
    '/' + PRES_CONFIG.DIR_MEDIA_TEMP:
        {'tools.staticdir.on': True,
         'tools.staticdir.dir': PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_MEDIA_TEMP)
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
         'tools.staticdir.dir': PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_CSS + os.path.sep + 'fonts')
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
        self.slideMode = "change"
        self.slideOrder = "normal"
        self.slideTimer = "timerOn"
        self.slideImage = "svg"
        self.presInProgress = "false"
    
    @cherrypy.expose
    def index(self):
        pub.Publisher.sendMessage('presConnect')
        folderList = os.listdir(PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_MEDIA_PRESENTATION));
        presFileData = presString.reduceFolderList(folderList)
        #htmlTemplate = open(os.path.join(PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_HTML), u'index.html'))
        presHTMLTemplate = htmlGenerator.generateHTML('presberry.html',
                                                      html_dir= PRES_CONFIG.DIR_HTML,
                                                      css_dir= PRES_CONFIG.DIR_CSS,
                                                      js_dir= PRES_CONFIG.DIR_JS,
                                                      jquerymobile_dir= PRES_CONFIG.DIR_JQUERYMOBILE,
                                                      filedata= presFileData,
                                                      pres_dir= PRES_CONFIG.DIR_MEDIA_PRESENTATION)
        return presHTMLTemplate

    @cherrypy.expose
    def upload(self, presFile, upload):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        if(presFile.content_type.value == 'application/pdf'):
            timestampID = datetime.now().strftime('%Y-%m-%dT%H-%M-%S_')
            uload_path = PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_MEDIA_PRESENTATION) + os.path.sep + timestampID + presFile.filename;
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
                svgGeneratorPreview = SVGGeneratorPreview(uload_path)
                svgGeneratorPreview.start()
                pngGeneratorPreview = PNGGeneratorPreview(uload_path)
                pngGeneratorPreview.start()
                
                timestampHTML = presString.getTimestampHTML(timestampID)
                fileListItemHTML =  htmlGenerator.generateHTML('previewElement.html',
                                                      pres_dir= PRES_CONFIG.DIR_MEDIA_PRESENTATION,
                                                      filename= presFile.filename,
                                                      timestamp=timestampID,
                                                      pTimestamp = timestampHTML)
                return simplejson.dumps(dict(fileListItem=fileListItemHTML))
            except ValueError:
                raise cherrypy.HTTPError(400, 'SOME ERROR')
        return simplejson.dumps(dict(html=""))     
            #return open(os.path.join(PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_HTML), u'startpresentation.html'))
        #return open(os.path.join(PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_HTML), u'index.html'))
    
    @cherrypy.expose
    def setupPresentation(self, timestampID, filenameHTML):
        presFile.resetTempFolder()
        uload_path = PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_MEDIA_PRESENTATION) + os.path.sep + timestampID + filenameHTML;
        self.pdfDocument = PDFdocument('file://' + uload_path, filenameHTML, timestampID)
        if(self.slideImage == 'svg'):
            svgGenerator = SVGGenerator(self.pdfDocument, PRES_CONFIG.SVG_WIDTH)
            svgGenerator.start()
        else:
            pngGenerator = PNGGenerator(self.pdfDocument, PRES_CONFIG.PNG_WIDTH)
            pngGenerator.start()
        pub.Publisher.sendMessage('presSetup', data=self.pdfDocument)               
        carouselHTML = htmlGenerator.generateHTML('carousel.html',
                                              temp_dir= PRES_CONFIG.DIR_MEDIA_TEMP,
                                              numPages=self.pdfDocument.n_pgs,
                                              filename = filenameHTML,
                                              timestamp = timestampID,
                                              width="100%",
                                              height="100%",
                                              order=self.slideOrder,
                                              imagetype=self.slideImage)
        return simplejson.dumps(dict(carousel=carouselHTML))
    
    @cherrypy.expose
    def startPresentation(self, **kwargs):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        pub.Publisher.sendMessage('presStart')
        return simplejson.dumps(dict(mode=self.slideMode, order=self.slideOrder, timer=self.slideTimer))
    
    @cherrypy.expose
    def quitPresentation(self, **kwargs):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        pub.Publisher.sendMessage('presQuit')
        return simplejson.dumps(dict())
    
    @cherrypy.expose
    def setSettings(self, slideMode, slideOrder, slideTimer, slideImage):
        self.slideMode = slideMode
        self.slideOrder = slideOrder        
        self.slideTimer = slideTimer
        self.slideImage = slideImage
        cherrypy.response.headers['Content-Type'] = 'application/json'       
        return simplejson.dumps(dict())
    
    @cherrypy.expose
    def getSettings(self, **kwargs):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return simplejson.dumps(dict(mode=self.slideMode, order=self.slideOrder, timer=self.slideTimer, image=self.slideImage))
    
    @cherrypy.expose
    def setPage(self, pageNr):
        pub.Publisher.sendMessage('presSetPage', pageNr)
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return simplejson.dumps(dict(page=pageNr))
    
    @cherrypy.expose
    def deletePresentation(self, delTimestampID, filenameHTML):
        #pub.Publisher.sendMessage('presSetPage', pageNr)
        presFile.deletePresFile(delTimestampID[3:] + filenameHTML);
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return simplejson.dumps(dict(delFileID=delTimestampID))