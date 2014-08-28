import wx
from gui import window
from http import server

if __name__=="__main__":
    s = server.HTTPServer()
    s.start()
    app = wx.App()    
    f = window.PresFrame()
    f.Show()
    app.MainLoop()
    
