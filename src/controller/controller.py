from gui.window import PresGUI
from http.server import HTTPServer

#serverQueue = Queue.Queue()
#guiQueue = Queue.Queue()

class Controller():

    def __init__(self):
        #p = PresWindow(guiQueue, serverQueue)
        p = PresGUI()
        p.start()
        #s = HTTPServer(guiQueue, serverQueue)
        s = HTTPServer()
        s.start()
    
