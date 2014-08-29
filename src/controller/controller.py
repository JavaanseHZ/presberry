import wx
from gui import window
from http import server

if __name__=="__main__":
    s = server.HTTPServer()
    s.start()
    p = window.PresWindow()
    p.start()
