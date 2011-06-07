'''
Created on May 31, 2011

@author: hinko
'''
import sys
import time
from PyQt4 import QtCore
import threading
from epics import ca, dbr


class iPV(QtCore.QObject):
    sigGet = QtCore.pyqtSignal('QObject*')
    sigPut = QtCore.pyqtSignal('QObject*')
    sigMonitor = QtCore.pyqtSignal('QObject*')
    sigConnect = QtCore.pyqtSignal('QObject*')

    def __init__(self, parent = None,
                 iocName = None,
                 portName = None,
                 pvName = None):

        QtCore.QObject.__init__(self, parent)

        self.iocName = None
        self.portName = None
        self.name = None
        self.pvName = None
        self.fullName = None
        self.value = None

        self.chid = None
        self.connected = False
        self.monitored = False

        self.iocName = iocName
        self.port = portName
        self.name = pvName

        self.pvName = ":" + self.port + ":" + self.name
        self.fullName = self.iocName + self.pvName

        ca.use_initial_context()
        print "uCA: ca.current_context():", ca.current_context()

        # Try to connect CA channel, but don't wait for completion
        self.chid = ca.create_channel(self.fullName,
                                      connect = False,
                                      callback = self.caOnConnectionChange)

        print "iPV.init: Created new PV: ", self.fullName

    def subscribe(self, pvSlot, sigName):
        print "iPV.subscribe;"

        # Note: Must use this form for connect! Otherwise unique connection
        #       is not made?!
        try:
            if sigName == 'sigConnect':
                self.sigConnect.connect(pvSlot, QtCore.Qt.UniqueConnection)
            elif sigName == 'sigGet':
                self.sigGet.connect(pvSlot, QtCore.Qt.UniqueConnection)
            elif sigName == 'sigPut':
                self.sigPut.connect(pvSlot, QtCore.Qt.UniqueConnection)
            elif sigName == 'sigMonitor':
                self.sigMonitor.connect(pvSlot, QtCore.Qt.UniqueConnection)
            else:
                print "iPV.subscribe: invalid signal name! ", self.fullName, "sigName=", sigName
        except TypeError as ex:
            print "iPV.subscribe; Caught exception:", ex
            print "iPV.subscribe; Caught double ", sigName, "signal connect, PV=", self.fullName
        print "iPV.subscribe: signal connected", self.fullName, "sigName=", sigName

    def unsubscribe(self, pvSlot, sigName):
        print "iPV.unsubscribe;"

        #try:
        if sigName == 'sigConnect':
            self.sigConnect.disconnect(pvSlot)
        elif sigName == 'sigGet':
            self.sigGet.disconnect(pvSlot)
        elif sigName == 'sigPut':
            self.sigPut.disconnect(pvSlot)
        elif sigName == 'sigMonitor':
            self.sigMonitor.disconnect(pvSlot)
        else:
            print "iPV.unsubscribe: invalid signal name! sigName=", sigName
        #except TypeError as ex:
        #    print "iPV.unsubscribe; Caught exception:", ex
        #    print "iPV.unsubscribe; Caught double ", sigName, "signal connect, PV=", self.fullName

    def get(self, pvSlot):
        print "iPV.get;"

        if callable(pvSlot):
            self.subscribe(pvSlot, "sigGet")

        thr = threading.Thread(target = self.caGethread)
        thr.start()
        print "iPV.get; thread started"
#        thr.join()
#        print "iPV.get; thread joined"

    def put(self, value):
        print "iPV.put;"

        thr = threading.Thread(target = self.caPuthread)
        thr.start()
        print "iPV.put; thread started"
        thr.join()
        print "iPV.put; thread joined"

    def monitorStart(self, pvSlot):
        print "iPV.monitorStart;"

        if callable(pvSlot):
            self.subscribe(pvSlot, "sigMonitor")

        thr = threading.Thread(target = self.caMonitorThread)
        thr.start()
        print "iPV.monitorStart; thread started"
#        thr.join()
#        print "iPV.monitorStart; thread joined"

    def monitorStop(self, pvSlot):
        print "iPV.monitorStop;"
        self.monitored = False

        if callable(pvSlot):
            self.unsubscribe(pvSlot, "sigMonitor")

        nrRecievers = self.receivers(QtCore.SIGNAL('sigConnected(QObject*)'))
        print "iPV.monitorStop; PV=", self.fullName, "sigMonitor disconnected, left receivers count=", nrRecievers

    def isConnected(self):
        print "iPV.isConnected; ", self.connected
        return self.connected

#===============================================================================
# CA
#===============================================================================
    def caOnConnectionChange(self, pvname = None, conn = None, chid = None):
        print "iPV.caOnConnectionChange:", pvname, conn, chid

        self.connected = conn

        print "iPV.caOnConnectionChange: Emit sigConnect(QObject*) for ", self.fullName
        self.sigConnect.emit(self)

    def caWaitConnectionChange(self, timeout = 2.5):
        print "iPV.caWaitConnectionChange: waiting", timeout, "seconds"
        t0 = time.time()
        cnt = 0

        while time.time() - t0 < timeout:

            if self.connected:
                sys.stdout.write("OK\n")
                return True

            time.sleep(0.001)
            cnt += 1
            if cnt % 100 == 0:
                sys.stdout.write(".")

        sys.stdout.write("FAIL\n")
        return False

    def caGethread(self, **kwds):
        time.sleep(0.1)
        print "iPV.caGethread: PV=", self.fullName

        ca.use_initial_context()
        print "iPV.caGethread: ca.current_context():", ca.current_context()

        if not self.connected:
            print "iPV.caGethread: PV not connected! PV=", self.fullName
            ca.connect_channel(self.chid, timeout = 2.0)
            self.caWaitConnectionChange()

        if not self.connected:
            print "iPV.caGethread: PV still not connected! PV=", self.fullName
            return

        print "iPV.caGethread: PV is connected, PV=", self.fullName

        self.value = ca.get(self.chid)
        print "iPV.caGethread: PV READ value: ", self.fullName, "=", self.value

        print "iPV.caGethread: Emit sigGet(QObject*) for ", self.fullName
        self.sigGet.emit(self)

    def caPuthread(self, **kwds):
        time.sleep(0.1)
        print "iPV.caPuthread:"

        print "iPV.caPuthread: Emit sigPut(QObject*) for ", self.fullName
        self.sigPut.emit(self)

    def caMonitorThread(self, **kwds):
        time.sleep(0.1)
        print "iPV.caMonitorThread:"
        if self.monitored:
            print "iPV.caMonitorThread: FIXME: This should not happen! PV=", self.fullName
            return

        print "iPV.caMonitorThread: Starting thread PV=", self.fullName

        ca.use_initial_context()
        print "iPV.caMonitorThread: ca.current_context():", ca.current_context()

        if not self.connected:
            print "iPV.caMonitorThread: PV not connected! PV=", self.fullName
            ca.connect_channel(self.chid, timeout = 2.0)
            self.caWaitConnectionChange()

        if not self.connected:
            print "iPV.caMonitorThread: PV still not connected! PV=", self.fullName
            return

        print "iPV.caMonitorThread: PV is connected, PV=", self.fullName

        # Subscribe to events
        self.monitored = True
        self.eventID = ca.create_subscription(self.chid,
                                              callback = self.caOnMonitorChange)

        # Wait until we have received monitored=False
        while self.monitored == True:
            time.sleep(0.05)

        # Un-subscribe to CA monitor
        if self.eventID:
            print "iPV.caMonitorThread: PV=", self.fullName, ", have eventID:", self.eventID
            ca.clear_subscription(self.eventID[2])
            ca.flush_io()
            self.eventID = None

        print "iPV.caMonitorThread: Stopping thread PV= ", self.fullName

#        print "iPV.caMonitorThread: Emit sigMonitor(QObject*) for ", self.fullName
#        self.sigMonitor.emit(self)

    def caOnMonitorChange(self, pvname = None, value = None, **kwds):
        print "iPV.caOnMonitorChange:", pvname, value, repr(kwds)

        self.value = value

        print "iPV.caOnMonitorChange: Emit sigMonitor(QObject*) for ", self.fullName
        self.sigMonitor.emit(self)

#===============================================================================
# Close
#===============================================================================
    def close(self):
        print "iPV.close: PV=", self.fullName , "THREADS=", threading.enumerate()

        print "iPV.close; stopping monitor"
        self.monitored = False

        nrRecievers = self.receivers(QtCore.SIGNAL('sigConnected(QObject*)'))
        print "iPV.close; PV=", self.fullName, "sigConnected disconnected, left receivers count=", nrRecievers
        if nrRecievers > 0:
            self.sigConnected.disconnect()
        nrRecievers = self.receivers(QtCore.SIGNAL('sigConnected(QObject*)'))
        print "iPV.close; PV=", self.fullName, "sigConnected disconnected, left receivers count=", nrRecievers

        nrRecievers = self.receivers(QtCore.SIGNAL('sigGet(QObject*)'))
        print "iPV.close; PV=", self.fullName, "sigGet disconnected, left receivers count=", nrRecievers
        if nrRecievers > 0:
            self.sigGet.disconnect()
        nrRecievers = self.receivers(QtCore.SIGNAL('sigGet(QObject*)'))
        print "iPV.close; PV=", self.fullName, "sigGet disconnected, left receivers count=", nrRecievers

        nrRecievers = self.receivers(QtCore.SIGNAL('sigMonitor(QObject*)'))
        print "iPV.close; PV=", self.fullName, "sigMonitor disconnected, left receivers count=", nrRecievers
        if nrRecievers > 0:
            self.sigMonitor.disconnect()
        nrRecievers = self.receivers(QtCore.SIGNAL('sigMonitor(QObject*)'))
        print "iPV.close; PV=", self.fullName, "sigMonitor disconnected, left receivers count=", nrRecievers
