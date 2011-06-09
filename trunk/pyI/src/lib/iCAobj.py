'''
Created on Jun 8, 2011

@author: hinko
'''

from PyQt4 import QtCore

class iCAobj(QtCore.QObject):
    def __init__(self, parent, pvName, pvPutValue = None):
        QtCore.QObject.__init__(self, parent)

        self.pvName = pvName
        self.pvGetValue = None
        self.pvPutValue = pvPutValue
        self.success = False
        self.monitor = False
        self.connected = False
