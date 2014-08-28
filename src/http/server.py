'''
Created on Aug 28, 2014

@author: ben
'''
from __future__ import with_statement
import cherrypy
import threading

class HTTPServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sync = threading.Condition()

    def run(self):
        with self.sync:
            cherrypy.server.socket_port = 8080
            #cherrypy.server.socket_host = optional hostname
            cherrypy.tree.mount(HelloWorld(), "/", None)
            cherrypy.engine.start()
        cherrypy.engine.block()

    def stop(self):
        with self.sync:
            cherrypy.engine.exit()
            cherrypy.server.stop()

class HelloWorld(object):
    def index(self):
        return "Hello World!"
    index.exposed = True