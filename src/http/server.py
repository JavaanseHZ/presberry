'''
Created on Aug 28, 2014

@author: ben
'''

from wx.lib.pubsub import pub
import cherrypy
import threading
import random
import string

class HTTPServer(threading.Thread):
    def __init__(self, serverQueue, guiQueue):
        threading.Thread.__init__(self)
        self.serverQueue = serverQueue
        self.guiQueue = guiQueue

    def run(self):
        cherrypy.server.socket_port = 8080
        #cherrypy.server.socket_host = optional hostname
        cherrypy.tree.mount(StringGenerator(), '/', None)
        cherrypy.engine.start()
        cherrypy.engine.block()

    def stop(self):
        cherrypy.engine.exit()
        cherrypy.server.stop()


class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return """<html>
          <head></head>
          <body>
            <form method="get" action="generate">
              <input type="text" value="8" name="length" />
              <button type="submit">Give it now!</button>
            </form>
          </body>
        </html>"""

    @cherrypy.expose
    def generate(self, length=8):
        pub.Publisher.sendMessage('updateDisplay')
        return ''.join(random.sample(string.hexdigits, int(length)))