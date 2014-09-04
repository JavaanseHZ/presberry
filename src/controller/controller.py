import Queue
from gui import window
from http import server

serverQueue = Queue.Queue()
guiQueue = Queue.Queue()

class Controller():

    def __init__(self):
        s = server.HTTPServer(guiQueue, serverQueue)
        s.start()
        p = window.PresWindow(guiQueue, serverQueue)
        p.start()


    
