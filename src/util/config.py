'''
Created on Sep 13, 2014

@author: benni
'''
import ConfigParser
import os

configParser = ConfigParser.ConfigParser()
configParser.read('config.ini')

SVG_WIDTH = configParser.getint('SVG', 'width')
PNG_WIDTH = configParser.getint('PNG', 'width')

NW_WIFIMODE = configParser.get('NETWORK', 'wifimode')#not implemented yet
NW_AP = configParser.get('NETWORK', 'ap')
NW_PW = configParser.get('NETWORK', 'pw')
NW_IP = configParser.get('NETWORK', 'ip')
NW_PORT = configParser.get('NETWORK', 'port')

W_FULLSCREEN = configParser.getboolean('WINDOW', 'fullscreen')
W_WIDTH = configParser.getint('WINDOW', 'width')
W_HEIGHT = configParser.getint('WINDOW', 'height')

DIR_MEDIA_GUI =  configParser.get('DIRECTORIES', 'gui')
DIR_MEDIA_PRESENTATION =  configParser.get('DIRECTORIES', 'presentation')
DIR_MEDIA_TEMP =  configParser.get('DIRECTORIES', 'temp')
DIR_HTML = configParser.get('DIRECTORIES', 'html')
DIR_JS =  configParser.get('DIRECTORIES', 'javascript')
DIR_CSS =  configParser.get('DIRECTORIES', 'css')
DIR_JQUERYMOBILE =  configParser.get('DIRECTORIES', 'jquerymobile')

def ABS_PATH(directory):
    return os.path.join(os.path.abspath("../"), directory)