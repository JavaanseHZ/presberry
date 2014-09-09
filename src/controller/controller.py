import Queue
from gui.window import *
from http.server import *

#serverQueue = Queue.Queue()
#guiQueue = Queue.Queue()

class Controller():

    def __init__(self):
        #p = PresWindow(guiQueue, serverQueue)
        p = PresWindow()
        p.start()
        #s = HTTPServer(guiQueue, serverQueue)
        s = HTTPServer()
        s.start()
    
