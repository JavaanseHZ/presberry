'''
Created on Sep 13, 2014

@author: benni
'''
import ConfigParser

configParser = ConfigParser.ConfigParser()
configParser.read('config.ini')

SVG_WIDTH = configParser.getint('SVG', 'width')

NW_WIFIMODE = configParser.get('NETWORK', 'wifimode')#not implemented yet
NW_AP = configParser.get('NETWORK', 'ap')
NW_PW = configParser.get('NETWORK', 'pw')
NW_IP = configParser.get('NETWORK', 'ip')
NW_PORT = configParser.get('NETWORK', 'port')

W_FULLSCREEN = configParser.getboolean('WINDOW', 'fullscreen')
W_WIDTH = configParser.getint('WINDOW', 'width')
W_HEIGHT = configParser.getint('WINDOW', 'height')