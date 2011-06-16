'''
Created on Jun 7, 2011

@author: hinko
'''

#===============================================================================
# COMMENTS
#===============================================================================
#  
#===============================================================================

from iHelper import iRaise, iLog, iPVActionValGet, iPVActionValPut, \
    iPVActionMonAdd, iPVActionMonRem

from PyQt4 import QtCore, QtGui

from iPVTree import iPVTree
from iIOCTree import iIOCTree

from ui.uiPanelDummy import Ui_PanelDummy

class iPanelDummy(QtGui.QWidget):

    def __init__(self, parent, pvHandler):
        QtGui.QWidget.__init__(self, parent)
        iLog.debug("enter")

        self.pvMonitors = dict()
        self.iocName = None
        self.pvName = None
        self.pvTree = iPVTree(self)
        self.iocTree = iIOCTree(self)

        self.pvHandler = pvHandler

        self.ui = Ui_PanelDummy()
        self.ui.setupUi(self)

    def show(self):
        iLog.debug("enter")

    def hide(self):
        iLog.debug("enter")

    def pvGet(self):
        iLog.debug("enter")

        #self.pvHandler.pvJobs.setPVProperty(pvGet, 'slotConnChanged', self.slotConnChanged)
        #self.pvHandler.pvJobs.setPVProperty(pvGet, 'slotValueChanged', self.slotValueChanged)
        #self.pvHandler.pvJobs.setPVProperty(pvGet2, 'slotConnChanged', self.slotConnChanged)
        #self.pvHandler.pvJobs.setPVProperty(pvGet2, 'slotValueChanged', self.slotValueChanged)
        #..
        #self.pvHandler.enqeue(iPVActionValGet, [pvGet, pvGet2, ..])

    def pvPut(self):
        iLog.debug("enter")

        #self.pvHandler.pvJobs.setPVProperty(pvPut, 'userValue', pvValue)
        #self.pvHandler.pvJobs.setPVProperty(pvPut, 'slotConnChanged', self.slotConnChanged)
        #self.pvHandler.pvJobs.setPVProperty(pvPut, 'slotValueChanged', self.slotValueChanged)
        #self.pvHandler.pvJobs.setPVProperty(pvPut2, 'userValue', pvValue)
        #self.pvHandler.pvJobs.setPVProperty(pvPut2, 'slotConnChanged', self.slotConnChanged)
        #self.pvHandler.pvJobs.setPVProperty(pvPut2, 'slotValueChanged', self.slotValueChanged)
        #..
        #self.pvHandler.enqeue(iPVActionValPut, [pvPut, pvPut2, ..])

    def pvMonitor(self):
        iLog.debug("enter")

        #self.pvHandler.pvJobs.setPVProperty(pvName, 'doMonitor', True)
        #self.pvHandler.pvJobs.setPVProperty(pvName, 'slotConnChanged', self.slotConnChanged)
        #self.pvHandler.pvJobs.setPVProperty(pvName, 'slotValueChanged', self.slotValueChanged)
        #self.pvHandler.pvJobs.setPVProperty(pvName2, 'doMonitor', True)
        #self.pvHandler.pvJobs.setPVProperty(pvName2, 'slotConnChanged', self.slotConnChanged)
        #self.pvHandler.pvJobs.setPVProperty(pvName2, 'slotValueChanged', self.slotValueChanged)
        #..
        #self.pvHandler.enqeue(iPVActionMonAdd, [pvName, pvName2, ..])

    def pvUnmonitor(self):
        iLog.debug("enter")

        #self.pvHandler.enqeue(iPVActionMonRem, [pvName, pvName2, ..])
        #self.pvHandler.pvJobs.setPVProperty(pvName, 'doMonitor', False)
        #self.pvHandler.pvJobs.setPVProperty(pvName2, 'doMonitor', False)
        #...

#===============================================================================
# CA callback slots
#===============================================================================

    @QtCore.pyqtSlot('QObject*')
    def slotConnChanged(self, pvObj):
        iLog.debug("enter")
        iLog.debug("Called for pvName=%s, pvValue=%s, pvConnected=%s" %
                   (pvObj.name, pvObj.value, pvObj.connected))

        # Possible use..
        #self.slotValueChanged(pvObj)

    @QtCore.pyqtSlot('QObject*')
    def slotValueChanged(self, pvObj):
        iLog.debug("enter")
        iLog.debug("Called for pvName=%s, pvValue=%s, pvConnected=%s" %
                   (pvObj.name, pvObj.value, pvObj.connected))

        # Update GUI here
