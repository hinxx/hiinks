'''
Created on Jun 13, 2011

@author: hinko
'''

from iGLobals import iRaise, iLog, iGlobalHandle, iPVActionValGet, \
    iPVActionValPut, iPVActionMonAdd, iPVActionMonRem, iPVActionStatus, \
    iPVActionInfo

from epics import ca, dbr
from PyQt4 import QtCore
import time

class iPVObj(QtCore.QObject):
    # Local signals
    localOneShot = QtCore.pyqtSignal()
    localPeriodic = QtCore.pyqtSignal()
    # Emit when some properties of this object change
    sigOneShot = QtCore.pyqtSignal('QObject*')
    sigPeriodic = QtCore.pyqtSignal('QObject*')

    def __init__(self, parent = None):
        QtCore.QObject.__init__(self, parent)
        iLog.debug("enter")

        # Properties found in XML
        self.name = None
        self.text = None
        self.enabled = None
        self.group = None
        self.getSuffix = None
        self.putSuffix = None
        self.cmdSuffix = None
        self.mode = None
        self.access = None
        self.format = None
        self.widget = None
        self.strings = None
        self.enums = None
        self.enumInt = None
        self.enumStr = None
        self.comment = None
        self.value = None

        # Other properties
        self.iocName = None
        self.userValue = None
        self.connected = False
        self.success = False
        self.doMonitor = False
        self.getChid = None
        self.putChid = None
        self.monitorID = None
        self.slots = []

        self.localOneShot.connect(self.localSlotOneShot)
        self.localPeriodic.connect(self.localSlotPeriodic)

    def nameIOC(self):
        iLog.debug("enter")

        if not self.iocName:
            iLog.error("IOC name not set for PV %s" % (self.name))
            iRaise(self, "IOC name not set for PV %s" % (self.name))

        name = self.iocName + self.name
        return name

    def nameGetSuffix(self):
        iLog.debug("enter")

        name = self.name
        if self.getSuffix:
            name += self.getSuffix
        return name

    def nameGetFull(self):
        iLog.debug("enter")

        if not self.iocName:
            iLog.error("IOC name not set for PV %s" % (self.name))
            iRaise(self, "IOC name not set for PV %s" % (self.name))

        return self.iocName + self.nameGetSuffix()

    def namePutSuffix(self):
        iLog.debug("enter")

        name = self.name
        if self.putSuffix:
            name += self.putSuffix
        return name

    def namePutFull(self):
        iLog.debug("enter")

        if not self.iocName:
            iLog.error("IOC name not set for PV %s" % (self.name))
            iRaise(self, "IOC name not set for PV %s" % (self.name))

        return self.iocName + self.namePutSuffix()

    def scheduleGet(self):
        iLog.debug("enter")

        iLog.info("Scheduling PV %s" % (self.nameGetFull()))
        handler = iGlobalHandle()
        handler.processList(iPVActionValGet, [self])

    def schedulePut(self):
        iLog.debug("enter")

        iLog.info("Scheduling PV %s" % (self.namePutFull()))
        handler = iGlobalHandle()
        handler.processList(iPVActionValPut, [self])

    def scheduleMonitor(self, state = True):
        iLog.debug("enter")

        self.doMonitor = state

        iLog.info("Scheduling PV %s, doMonitor %s" % (self.nameGetFull(), str(self.doMonitor)))
        handler = iGlobalHandle()
        if self.doMonitor:
            handler.processList(iPVActionMonAdd, [self])
        else:
            handler.processList(iPVActionMonRem, [self])

    def connectNotify(self, signal):
        iLog.debug("enter")
        iLog.debug("Signal '%s'" % (signal))

        if signal == QtCore.SIGNAL('sigOneShot(QObject*)'):
            iLog.info("slot on '%s'" % (signal))
            c = self.receivers(signal)
            iLog.info("New receiver count on '%s' = %d" % (signal, c))

        if signal == QtCore.SIGNAL('sigPeriodic(QObject*)'):
            iLog.info("slot on '%s'" % (signal))
            c = self.receivers(signal)
            iLog.info("New receiver count on '%s' = %d" % (signal, c))


    def disconnectNotify(self, signal):
        iLog.debug("enter")
        iLog.debug("Signal '%s'" % (signal))

        if signal == QtCore.SIGNAL('sigOneShot(QObject*)'):
            iLog.info("slot on '%s'" % (signal))
            c = self.receivers(signal)
            iLog.info("New receiver count on '%s' = %d" % (signal, c))

        if signal == QtCore.SIGNAL('sigPeriodic(QObject*)'):
            iLog.info("slot on '%s'" % (signal))
            c = self.receivers(signal)
            iLog.info("New receiver count on '%s' = %d" % (signal, c))

            if c == 0 and self.doMonitor:
                iLog.info("Stopping monitor '%s'" % (self.nameGetFull()))
                self.scheduleMonitor(False)

    def connectOneShotSignal(self, slot):
        iLog.debug("enter")
        iLog.debug("PV %s, want to connect slot '%s'" % (self.nameIOC(), slot))

        iLog.info("PV %s, slot '%s' connecting now" % (self.nameIOC(), slot))
        try:
            self.sigOneShot.connect(slot, QtCore.Qt.UniqueConnection)
        except TypeError as uniq:
            iLog.warning("Only unique connections allowed on sigOneShot(), PV %s" % (self.nameIOC()))

    def disconnectOneShotSignal(self, slot = None):
        iLog.debug("enter")
        iLog.debug("PV %s, want to disconnect slot '%s'" % (self.nameIOC(), slot))

        iLog.info("PV %s, slot '%s' disconnecting now" % (self.nameIOC(), slot))
        if slot:
            self.sigOneShot.disconnect(slot)
        else:
            self.sigOneShot.disconnect()

    def connectPeriodicSignal(self, slot):
        iLog.debug("enter")
        iLog.debug("PV %s, want to connect slot '%s'" % (self.nameIOC(), slot))

        iLog.info("PV %s, slot '%s' connecting now" % (self.nameIOC(), slot))
        try:
            self.sigPeriodic.connect(slot, QtCore.Qt.UniqueConnection)
        except TypeError as uniq:
            iLog.warning("Only unique connections allowed on sigOneShot(), PV %s" % (self.nameIOC()))

    def disconnectPeriodicSignal(self, slot = None):
        iLog.debug("enter")
        iLog.debug("PV %s, want to disconnect slot '%s'" % (self.nameIOC(), slot))

        iLog.info("PV %s, slot '%s' disconnecting now" % (self.nameIOC(), slot))
        if slot:
            self.sigPeriodic.disconnect(slot)
        else:
            self.sigPeriodic.disconnect()

#===============================================================================
# Slots for local signals
#===============================================================================
    @QtCore.pyqtSlot()
    def localSlotOneShot(self):
        iLog.debug("enter")

        self.sigOneShot.emit(self)

    @QtCore.pyqtSlot()
    def localSlotPeriodic(self):
        iLog.debug("enter")

        self.sigPeriodic.emit(self)

#===============================================================================
# Channel access
#===============================================================================

    def _caRefreshValue(self, value, periodic = False):
        iLog.debug("enter")

        iLog.info("PV old value %s is %s" % (self.name, str(self.value)))
        self.value = value

        iLog.info("PV value changed %s is %s" % (self.name, str(self.value)))
        if periodic:
            self.localPeriodic.emit()
        else:
            self.localOneShot.emit()

    def _caRefreshConn(self, state):
        iLog.debug("enter")

        iLog.info("PV old connect state %s is %s" % (self.name, str(self.connected)))
        self.connected = state
        if not self.connected:
            self.value = 'UDF'

        iLog.info("PV connect state changed %s is %s" % (self.name, str(self.connected)))

        self.localPeriodic.emit()
        self.localOneShot.emit()

    def _caOnConnectionChange(self, pvname = None, conn = None, chid = None):
        iLog.debug("enter")
        #ca.show_cache()

        iLog.debug("pvName=%s, connected=%s, chid=%s" % (pvname, str(conn), str(chid)))

        self._caRefreshConn(conn)

        iLog.debug("leave")

    def _caOnMonitorChange(self, chid = None, status = None, count = None, ftype = None, pvname = None, value = None, **kwds):
        iLog.debug("enter")
        #ca.show_cache()

        self._caRefreshValue(value, True)

        iLog.debug("leave")

    def _caConnectChannel(self, pvAction):
        iLog.debug("enter")

        name = self.nameGetFull()
        if pvAction == iPVActionValPut:
            name = self.namePutFull()

        # Try to connect CA channel, but don't wait for completion
        chid = ca.create_channel(name,
                                callback = self._caOnConnectionChange)
        iLog.debug("PV self.getChid created pvName=%s, getChid=%s" % (name, str(self.getChid)))

        if not self.getChid and (pvAction != iPVActionValPut):
            self.getChid = chid
        if not self.putChid and (pvAction == iPVActionValPut):
            self.putChid = chid

        conn = ca.isConnected(chid)
        if not conn:
            iLog.warning("PV not connected yet calling ca.connect_channel(), pvName=%s" % (name))
            ca.connect_channel(chid, timeout = 1.0)

        conn = ca.isConnected(chid)
        if not conn:
            iLog.error("PV STILL not connected after 1 second.., pvName=%s" % (name))
            self._caRefreshConn(conn)

        return conn

    def _caChannelStatus(self):
        iLog.info("enter")

        iLog.info("TODO ..")

    def _caChannelInfo(self):
        iLog.info("enter")

        iLog.info("TODO ..")


    def _caGet(self):
        iLog.debug("enter")

        name = self.nameGetFull()

        iLog.debug("try pvName=%s, getChid=%s, connected=%s" % (name, self.getChid, ca.isConnected(self.getChid)))
        try:
            value = ca.get(self.getChid)
            conn = ca.isConnected(self.getChid)
        except ca.CASeverityException as caex:
            iLog.error("GET CASeverityException pvName=%s, exception=%s" % (name, caex))
            #ca.show_cache()
        finally:
            iLog.debug("GET pvName=%s, value=%s" % (name, str(value)))

            self._caRefreshValue(value)

    def _caPut(self):
        iLog.debug("enter")

        name = self.namePutFull()

        iLog.debug("try pvName=%s, pvValue=%s, userValue=%s" % (name, str(self.value), str(self.userValue)))
        try:
            ret = ca.put(self.putChid, self.userValue, wait = True)
            if ret == 1:
                self._caGet()
        except ca.CASeverityException as caex:
            iLog.error("CASeverityException pvName=%s, exception=%s" % (name, caex))
            #ca.show_cache()
        finally:
            iLog.debug("put pvName=%s, value=%s" % (name, str(self.value)))

    def _caSubscribeMonitor(self):
        iLog.debug("enter")

        name = self.nameGetFull()

        if not self.doMonitor:
            iLog.warning("PV %s is not enabled for monitoring" % (name))
            return

        if self.monitorID:
            iLog.warning("Monitor already present for pvName=%s" % (name))
            return

        iLog.debug("try pvName=%s, getChid=%s, connected=%s" % (name, self.getChid, ca.isConnected(self.getChid)))
        # Subscribe to events
        try:
            self.monitorID = ca.create_subscription(self.getChid,
                                                       callback = self._caOnMonitorChange)
        except ca.CASeverityException as caex:
            iLog.error("CASeverityException pvName=%s, eventID=%s, exception=%s" % (name, str(self.monitorID), caex))
            #ca.show_cache()
        finally:
            iLog.debug("starting monitor pvName=%s, eventID=%s" % (name, str(self.monitorID)))

    def _caUnsubscribeMonitor(self):
        iLog.debug("enter")

        name = self.nameGetFull()

        if self.doMonitor:
            iLog.warning("PV %s is enabled for monitoring" % (name))
            return

        iLog.debug("try pvName=%s, getChid=%s, connected=%s" % (name, self.getChid, ca.isConnected(self.getChid)))

        if not self.monitorID:
            iLog.warning("No monitor for pvName=%s" % (name))
            return

        iLog.info("stopping monitor pvName=%s" % (name))
        ca.clear_subscription(self.monitorID[2])
        ca.flush_io()
        self.monitorID = None
        ca.flush_io()

    def _caHandler(self, pvAction):
        iLog.debug("enter")

        if not self._caConnectChannel(pvAction):
            return

        if pvAction == iPVActionValGet:

            self._caGet()

        elif pvAction == iPVActionValPut:

            self._caPut()

        elif pvAction == iPVActionMonAdd:

            self._caSubscribeMonitor()

        elif pvAction == iPVActionMonRem:

            self._caUnsubscribeMonitor()

        elif pvAction == iPVActionStatus:

            self._caChannelStatus()

        elif pvAction == iPVActionInfo:

            self._caChannelInfo()
