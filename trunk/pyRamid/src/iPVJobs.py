'''
Created on Jun 13, 2011

@author: hinko
'''

from iHelper import iRaise, iLog, iPVActionValGet, iPVActionValPut, \
    iPVActionMonAdd, iPVActionMonRem, iPVActionStatus, iPVActionInfo, iPVActions

from epics import ca, dbr
from PyQt4 import QtCore
import time

from iThreader import iThreader
from iPVObj import iPVObj

class iPVJobs(iThreader):
    # TODO: Consider using signal to set pvObj properties !?
    sigPVObjChanged = QtCore.pyqtSignal('QObject*')

    def __init__(self, parent):

        iThreader.__init__(self, parent)
        iLog.debug("enter")

        self.pvObjList = dict()
        self.pvJobList = dict()
        self.sigPVObjChanged.connect(self.slotPVObjChanged)

#===============================================================================
# Channel access
#===============================================================================

    def _caOnConnectionChange(self, pvname = None, conn = None, chid = None):
        iLog.debug("enter")
        #ca.show_cache()

        iLog.debug("pvName=%s, connected=%s, chid=%s" % (pvname, str(conn), str(chid)))

        pvObj = self.pvObjList[pvname]

        pvObj.setCAConnected(conn)
        if not conn:
            pvObj.setCAValue(None)

        self.sigPVObjChanged.emit(pvObj)

        iLog.debug("leave")

    def _caOnMonitorChange(self, chid = None, status = None, count = None, ftype = None, pvname = None, value = None, **kwds):
        iLog.debug("enter")
        #ca.show_cache()

        pvObj = self.pvObjList[pvname]

        pvObj.setCAValue(value, force = True)

        iLog.debug("leave")

    def _caConnectChannel(self, pvObj):
        iLog.debug("enter")

        if not isinstance(pvObj, iPVObj):
            iRaise (self, "Invalid PV data object argument '%s'" % (type(pvObj)))

        if not pvObj.chid:
            # Try to connect CA channel, but don't wait for completion
            pvObj.chid = ca.create_channel(pvObj.name,
                                               callback = self._caOnConnectionChange)
            iLog.debug("PV chid created pvName=%s, chid=%s" % (pvObj.name, str(pvObj.chid)))

        conn = ca.isConnected(pvObj.chid)
        if not conn:
            iLog.warning("PV not connected, pvName=%s" % (pvObj.name))
            ca.connect_channel(pvObj.chid, timeout = 1.0)

        conn = ca.isConnected(pvObj.chid)
        if not conn:
            iLog.error("PV still not connected, pvName=%s" % (pvObj.name))
            pvObj.setCAConnected(conn, force = True)

        return conn

    def _caChannelStatus(self, pvObj):
        iLog.debug("enter")

        if not isinstance(pvObj, iPVObj):
            iRaise (self, "Invalid PV data object argument '%s'" % (type(pvObj)))

        iLog.debug("TODO ..")

    def _caChannelInfo(self, pvObj):
        iLog.debug("enter")

        if not isinstance(pvObj, iPVObj):
            iRaise (self, "Invalid PV data object argument '%s'" % (type(pvObj)))

        iLog.debug("TODO ..")


    def _caGet(self, pvObj):
        iLog.debug("enter")

        if not isinstance(pvObj, iPVObj):
            iRaise (self, "Invalid PV data object argument '%s'" % (type(pvObj)))

        iLog.debug("pvName=%s" % pvObj.name)

        try:
            value = ca.get(pvObj.chid)
            conn = ca.isConnected(pvObj.chid)
        except ca.CASeverityException as caex:
            iLog.error("GET CASeverityException pvName=%s, exception=%s" % (pvObj.name, caex))
            #ca.show_cache()
        finally:
            iLog.debug("GET pvName=%s, value=%s" % (pvObj.name, str(value)))

            pvObj.setCAValue(value, force = True)

    def _caPut(self, pvObj):
        iLog.debug("enter")

        if not isinstance(pvObj, iPVObj):
            iRaise (self, "Invalid PV data object argument '%s'" % (type(pvObj)))

        iLog.debug("pvName=%s, pvValue=%s" % (pvObj.name, str(pvObj.value)))

        try:
            ret = ca.put(pvObj.chid, pvObj.userValue, wait = True)
            if ret == 1:
                self._caGet(pvObj)
        except ca.CASeverityException as caex:
            iLog.error("PUT CASeverityException pvName=%s, exception=%s" % (pvObj.name, caex))
            #ca.show_cache()
        finally:
            iLog.debug("PUT pvName=%s" % (pvObj.name))

    def _caSubscribeMonitor(self, pvObj):
        iLog.debug("enter")

        if not isinstance(pvObj, iPVObj):
            iRaise (self, "Invalid PV data object argument '%s'" % (type(pvObj)))

        if pvObj.monitorID:
            iLog.warning("Monitor already present for pvName=%s" % (pvObj.name))
            return

        iLog.debug("MONITOR pvName=%s, chid=%s, connected=%s" % (pvObj.name, pvObj.chid, ca.isConnected(pvObj.chid)))
        # Subscribe to events
        try:
            pvObj.monitorID = ca.create_subscription(pvObj.chid,
                                                       callback = self._caOnMonitorChange)
        except ca.CASeverityException as caex:
            iLog.error("MONITOR CASeverityException pvName=%s, eventID=%s, exception=%s" % (pvObj.name, str(pvObj.monitorID), caex))
            #ca.show_cache()
        finally:
            iLog.debug("MONITOR pvName=%s, eventID=%s" % (pvObj.name, str(pvObj.monitorID)))

    def _caUnsubscribeMonitor(self, pvObj):
        iLog.debug("enter")

        if not isinstance(pvObj, iPVObj):
            iRaise (self, "Invalid PV data object argument '%s'" % (type(pvObj)))

        iLog.debug("pvName=%s" % (pvObj.name))

        if not pvObj.monitorID:
            iLog.warning("No monitor for pvName=%s" % (pvObj.name))
            return

        # FIXME: Handle multiple listeners to qt signal from monitor!!!
        iLog.debug("Stopping monitor for pvName=%s" % (pvObj.name))
        ca.clear_subscription(pvObj.monitorID[2])
        ca.flush_io()
        pvObj.monitorID = None
        ca.flush_io()

#===============================================================================
# iThreader overloaded methods
#===============================================================================

    def initData(self, pvAction, pvNameList):
        iLog.debug("enter")

        if not pvAction in iPVActions:
            iRaise (self, "Invalid CA action argument '%s'" % (str(pvAction)))

        if not isinstance(pvNameList, list):
            if pvNameList != None:
                iRaise("Invalid pvNameList argument '%s'" % (type(pvNameList)))

        iLog.debug("Init data for PV list %s" % (str(pvNameList)))

        for pvName in pvNameList:
            # Create new PV object if not found in the map
            if not pvName in self.pvObjList:
                self.pvObjList[pvName] = iPVObj(self, pvName)
                iLog.debug("PV added to self.pvObjList %s" % (str(pvName)))

            self.pvJobList[pvName] = pvAction
            iLog.debug("PV added to job self.pvJobList %s (%s), pvAction=%s" % (pvName, self.pvObjList[pvName], pvAction))

    def getData(self):
        iLog.debug("enter")

        iLog.debug("Current self.pvJobList=%s" % (self.pvJobList))
        return self.pvJobList.items()

    def handleData(self, pvData):
        iLog.debug("enter")

        iLog.debug("pvData=%s" % str(pvData))
        if not isinstance(pvData, tuple):
            iRaise (self, "Invalid PV name argument '%s'" % (type(pvData)))

        pvName, pvAction = pvData
        iLog.debug("Handling PV %s, action %s" % (pvName, pvAction))

        pvObj = self.pvObjList[pvName]
        if not isinstance(pvObj, iPVObj):
            iRaise (self, "Invalid PV data object argument '%s'" % (type(pvObj)))

        ca.use_initial_context()

        if not self._caConnectChannel(pvObj):
            return

        if pvAction == iPVActionValGet:

            self._caGet(pvObj)

        elif pvAction == iPVActionValPut:

            self._caPut(pvObj)

        elif pvAction == iPVActionMonAdd:

            self._caSubscribeMonitor(pvObj)

        elif pvAction == iPVActionMonRem:

            self._caUnsubscribeMonitor(pvObj)

        elif pvAction == iPVActionStatus:

            self._caChannelStatus(pvObj)

        elif pvAction == iPVActionInfo:

            self._caChannelInfo(pvObj)

    def handleResult(self, pvName, result):
        iLog.debug("enter")

        self.pvJobList = dict()

    def prerun(self):
        iLog.debug("enter")

    def postrun(self):
        iLog.debug("enter")

#===============================================================================
# Manage pvObj
#===============================================================================

    def setPVProperty(self, pvName, pvKey, pvValue):
        iLog.debug("enter")

        # Create new PV object if not found in the map
        if not pvName in self.pvObjList:
            self.pvObjList[pvName] = iPVObj(self, pvName)
            iLog.debug("PV added to self.pvObjList %s" % (str(pvName)))

        pvObj = self.pvObjList[pvName]

        if hasattr(pvObj, pvKey):
            setattr(pvObj, pvKey, pvValue)
            iLog.debug("pvObj.%s=%s" % (pvKey, getattr(pvObj, pvKey)))
        elif pvKey == 'slotValueChanged':
            try:
                pvObj.sigValueChanged.connect(pvValue, type = QtCore.Qt.UniqueConnection)
            except TypeError as err:
                iLog.error("PV %s, pvObj.sigValueChanged.connect failed: %s" % (pvObj.name, err))
        elif pvKey == 'slotConnChanged':
            try:
                pvObj.sigConnChanged.connect(pvValue, type = QtCore.Qt.UniqueConnection)
            except TypeError as err:
                iLog.error("PV %s, pvObj.sigConnChanged.connect failed: %s" % (pvObj.name, err))

    @QtCore.pyqtSlot('QObject*')
    def slotPVObjChanged(self, pvObj):
        iLog.debug("enter")

        if not isinstance(pvObj, iPVObj):
            iRaise (self, "Invalid PV object argument '%s'" % (type(pvObj)))

        iLog.debug("pvObj PV name=%s" % (pvObj.name))

        if pvObj.connected and pvObj.doMonitor and not pvObj.monitorID:
            iLog.debug("PV %s needs to be monitored" % (pvObj.name))

            self._caSubscribeMonitor(pvObj)



#===============================================================================
# Other methods
#===============================================================================
    def close(self):
        iLog.debug("done")
