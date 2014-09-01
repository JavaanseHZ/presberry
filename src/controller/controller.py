import wx
import Queue
from gui import window
from http import server

serverQueue = Queue.Queue()
guiQueue = Queue.Queue()

if __name__=="__main__":
    s = server.HTTPServer(guiQueue, serverQueue)
    s.start()
    p = window.PresWindow(guiQueue, serverQueue)
    p.start()
