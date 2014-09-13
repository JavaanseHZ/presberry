from gui.window import PresGUI
from http.server import HTTPServer

class Controller():

    def __init__(self):
        p = PresGUI()
        p.start()
        s = HTTPServer()
        s.start()
    
