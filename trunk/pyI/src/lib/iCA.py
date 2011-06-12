'''
Created on Jun 8, 2011

@author: hinko
'''

#===============================================================================
# COMMENTS
#===============================================================================
# TODO: implement synchronized PV groups (for interlock setting)  
# TODO: implement progress report on number of processed, running, successful,
#       etc.. CA operations (statusbar?)  
#===============================================================================

from iConf import iLog

from PyQt4 import QtCore

from iCAWork import iCADispatcher

class iCA(QtCore.QObject):
    sigGet = QtCore.pyqtSignal(dict)
    sigPut = QtCore.pyqtSignal(dict)
    sigMonitor = QtCore.pyqtSignal(dict)
    sigConnected = QtCore.pyqtSignal(dict)
    sigDone = QtCore.pyqtSignal(dict)

    def __init__(self, parent = None):
        QtCore.QObject.__init__(self, parent)
        iLog.info("enter")

        self.dispatcher = iCADispatcher(True)
        self.dispatcher.start()

    def get(self, pvList):
        iLog.info("enter")

        workList = []
        for pvName in pvList:
            workList.append((pvName, None))

        # Create and schedule GET work
        seqId = self.dispatcher.newGetter(workList,
                                          self.doneCallback,
                                          self.getCallback,
                                          self.connectedCallback)
        self.dispatcher.schedule(seqId)

        return seqId

    def put(self, pvList):
        iLog.info("enter")

        workList = []
        for pvName, pvValue in pvList:
            workList.append((pvName, pvValue))

        # Create and schedule PUT work
        seqId = self.dispatcher.newPutter(workList,
                                          self.doneCallback,
                                          self.putCallback,
                                          self.connectedCallback)
        self.dispatcher.schedule(seqId)

        return seqId

    def monitor(self, pvList):
        iLog.info("enter")

        workList = []
        for pvName in pvList:
            workList.append((pvName, None))

        # Create and schedule MONITOR work
        seqId = self.dispatcher.newMonitor(workList,
                                           self.doneCallback,
                                           self.monitorCallback,
                                           self.connectedCallback)
        self.dispatcher.schedule(seqId)

        return seqId

    def monitorStop(self, seqId, pvName = None):
        iLog.info("enter")

        iLog.info("pvName=%s" % (str(pvName)))
        self.dispatcher.stopMonitor(seqId, pvName)

    def connectedCallback(self, pvData):
        iLog.info("enter")
        iLog.info("Emit signal for pvData=%s" % (repr(pvData)))

        self.sigConnected.emit(pvData)

    def getCallback(self, pvData):
        iLog.info("enter")
        iLog.info("Emit signal for pvData=%s" % (repr(pvData)))

        self.sigGet.emit(pvData)

    def putCallback(self, pvData):
        iLog.info("enter")
        iLog.info("Emit signal for pvData=%s" % (repr(pvData)))

        self.sigPut.emit(pvData)

    def monitorCallback(self, pvData):
        iLog.info("enter")
        iLog.info("Emit signal for pvData=%s" % (repr(pvData)))

        self.sigMonitor.emit(pvData)

    def doneCallback(self, pvList):
        iLog.info("enter")
        iLog.info("For pvList=%s" % (repr(pvList)))

        self.sigDone.emit(pvList)

    def close(self):
        iLog.debug("enter")

        iLog.debug("Disconnecting pyqt slots")
        self.sigConnected.disconnect()
        self.sigGet.disconnect()
        self.sigPut.disconnect()
        self.sigMonitor.disconnect()
        self.sigDone.disconnect()

        iLog.debug("closing CA thread ..")
        self.dispatcher.close()
        #self.dispatcher.schedule(None)
        #self.iCAThr.join(1.0)
        self.dispatcher.join()
        self.dispatcher = None
