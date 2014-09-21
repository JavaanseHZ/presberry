'''
Created on Sep 16, 2014

@author: ben
'''
import os
import util.config as PRES_CONFIG

def resetTempFolder():
    folder = PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_MEDIA_TEMP)
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            os.unlink(file_path)
        except Exception, e:
            print e

def deletePresFile(presFilename):
    folder = PRES_CONFIG.ABS_PATH(PRES_CONFIG.DIR_MEDIA_PRESENTATION)
    filepath = os.path.join(folder, presFilename)
    try:
        os.unlink(filepath)
        os.unlink(filepath + '0.svg')
        os.unlink(filepath + '0.png')
    except Exception, e:
        print e