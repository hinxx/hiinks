'''
Created on Jun 13, 2011

@author: hinko
'''

from iHelper import iRaise, iLog

from PyQt4 import QtCore

class iPVObj(QtCore.QObject):
    sigValueChanged = QtCore.pyqtSignal('QObject*')
    sigConnChanged = QtCore.pyqtSignal('QObject*')

    def __init__(self, parent, name, **kwargs):
        QtCore.QObject.__init__(self, parent)
        iLog.debug("enter")

        self.name = name
        self.value = None
        self.userValue = None
        self.connected = False
        self.doSignals = False
        self.success = False
        self.doMonitor = False
        self.chid = None
        self.monitorID = None

    def setCAValue(self, value, force = False):
        iLog.debug("enter")

        iLog.debug("PV old value %s is %s" % (self.name, str(self.value)))
        if (self.value != value) or (force):
            self.value = value
            iLog.debug("PV value changed %s is %s" % (self.name, str(self.value)))
            self.sigValueChanged.emit(self)

    def setCAConnected(self, state, force = False):
        iLog.debug("enter")

        if (self.connected != state) or (force):
            self.connected = state
            iLog.debug("PV connect state changed %s is %s" % (self.name, str(self.connected)))
            self.sigConnChanged.emit(self)

    def setUserValue(self, value):
        iLog.debug("enter")

        self.userValue = value
        iLog.debug("PV user value changed userValue=%s (%s)" % (str(self.userValue), type(self.userValue)))
