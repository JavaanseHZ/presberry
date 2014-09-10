'''
Created on Sep 10, 2014

@author: ben
'''

class State():
    def __init__(self, object):
        self.object = object
    
    #def nextState(self):
    #    self.currentState = self.currentState.nextState()

class StartState(State):
    
    def nextState(self):
        print 'StartState'
        self.object.presState = self.object.uploadState
        
class UploadState(State):
    def nextState(self):
        print 'UploadState'
        self.object.presState = self.object.presentationState
        
class PresentationState(State):
    def nextState(self):
        print 'PresentationState'
        self.object.presState = self.object.startState