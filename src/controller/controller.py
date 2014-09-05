import Queue
from gui.window import *
from http.server import *

serverQueue = Queue.Queue()
guiQueue = Queue.Queue()

class Controller():

    def __init__(self):
        #s = HTTPServer(guiQueue, serverQueue)
        #s.start()
        p = PresWindow(guiQueue, serverQueue)
        p.start()
    
