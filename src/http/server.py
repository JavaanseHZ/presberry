'''
Created on Aug 28, 2014

@author: ben
'''
import cherrypy
import threading
import wx.lib.pubsub as pubsub
import wx
import time

class HTTPServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sync = threading.Condition()

    def run(self):
        time.sleep(5)
        pubsub.Publisher().sendMessage("update", 10)
        cherrypy.server.socket_port = 8080
        #cherrypy.server.socket_host = optional hostname
        cherrypy.tree.mount(HelloWorld(), "/", None)
        cherrypy.engine.start()
        cherrypy.engine.block()
        

    def stop(self):
        cherrypy.engine.exit()
        cherrypy.server.stop()

class HelloWorld(object):
    def index(self):
        return "Hello World!"
    index.exposed = True