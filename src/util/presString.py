'''
Created on Sep 16, 2014

@author: benni
'''
def getTimestampHTML(timestamp):
    i = timestamp.replace("-", "/", 2)
    i = i.replace("-", ":", 2)
    i = i.replace("_", "")
    i = i.replace("T", "&#32;&#32;&#32;", 2)
    return i;

def reduceFolderList(folderList):
    reducedFolderList = [i.partition('_') + (getTimestampHTML(i.partition('_')[0]),) for i in folderList if 'pdf' in i.lower()[-3:]]
    
    return reducedFolderList 