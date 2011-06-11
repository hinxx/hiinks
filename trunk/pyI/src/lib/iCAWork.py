'''
Created on Jun 8, 2011

@author: hinko
'''
from iConf import *

import sys
import time
import threading, Queue
from epics import ca, dbr

from iThreader import iThreader
from iCAobj import iCAobj

class iCAget(iThreader):
    def __init__(self, parent, workList, numthreads = 1, workDoneCB = None, monitorCB = None):
        iThreader.__init__(self, parent, numthreads, workDoneCB)
        iLog.debug("enter")

        self.workList = workList
        if callable(monitorCB):
            self.monitorCB = monitorCB

    def get_data(self):
        iLog.debug("enter")

        return self.workList

    def handle_data(self, pvData):
        iLog.debug("enter")

        if not isinstance(pvData, iCAobj):
            print "iCAget.handle_data: Invalid data! data=", pvData
            return

        ca.use_initial_context()
        #print "iCAget.handle_data: ca.current_context():", ca.current_context()

        # Try to connect CA channel, but don't wait for completion
        chid = ca.create_channel(pvData.pvName)

        pvData.success = False
        if not ca.isConnected(chid):
            #print "iCAget.handle_data: PV not connected! PV=", pvName
            ca.connect_channel(chid, timeout = 2.0)

        if not ca.isConnected(chid):
            #print "iCAget.handle_data: PV still not connected! PV=", pvData.pvName
            pvData.connected = False
            return pvData.success

        pvData.connected = True

        #print "iCAget.handle_data: PV is connected, PV=", pvName

        pvData.pvGetValue = ca.get(chid)
        #print "iCAget.handle_data: GET value: ", pvData.pvName, "=", pvData.pvGetValue

        pvData.success = True
        return pvData.success

    def handle_result(self, data, result):
        iLog.debug("enter")

        self.res.append((data, result))
        if hasattr(self, "monitorCB"):
            self.monitorCB(data)

    def prerun(self):
        iLog.debug("enter")

        self.res = []

    def postrun(self):
        iLog.debug("enter")

        return self.res


class iCAput(iThreader):
    def __init__(self, parent, workList, numthreads, workDoneCB, monitorCB):
        iThreader.__init__(self, parent, numthreads, workDoneCB)
        iLog.debug("enter")

        self.workList = workList
        if callable(monitorCB):
            self.monitorCB = monitorCB

    def get_data(self):
        iLog.debug("enter")

        return self.workList

    def handle_data(self, pvData):
        iLog.debug("enter")

        if not isinstance(pvData, iCAobj):
            print "iCAput.handle_data: Invalid data! data=", pvData
            return

        ca.use_initial_context()
        #print "iCAput.handle_data: ca.current_context():", ca.current_context()

        # Try to connect CA channel, but don't wait for completion
        chid = ca.create_channel(pvData.pvName)

        pvData.success = False
        if not ca.isConnected(chid):
            #print "iCAput.handle_data: PV not connected! PV=", pvName
            ca.connect_channel(chid, timeout = 2.0)

        if not ca.isConnected(chid):
            #print "iCAput.handle_data: PV still not connected! PV=", pvData.pvName
            pvData.connected = False
            return pvData.success

        pvData.connected = True

        #print "iCAput.handle_data: PV is connected, PV=", pvName

        ret = ca.put(chid, pvData.pvPutValue, wait = True)
        if ret == 1:
            pvData.success = True
            #print "iCAput.handle_data: PUT value: ", pvData.pvName, "=", pvData.pvPutValue
            pvData.pvGetValue = ca.get(chid)
            #print "iCAput.handle_data: GET value: ", pvData.pvName, "=", pvData.pvGetValue

        return pvData.success

    def handle_result(self, data, result):
        iLog.debug("enter")

        self.res.append((data, result))
        if hasattr(self, "monitorCB"):
            self.monitorCB(data)

    def prerun(self):
        iLog.debug("enter")

        self.res = []

    def postrun(self):
        iLog.debug("enter")

        return self.res


class iCAmonitor(iThreader):
    def __init__(self, parent, workList, numthreads, workDoneCB, monitorCB):
        iThreader.__init__(self, parent, numthreads, workDoneCB)
        iLog.debug("enter")

        self.workList = workList
        self.eventID = None
        if callable(monitorCB):
            self.monitorCB = monitorCB

    def _caOnMonitorChange(self, pvname = None, value = None, **kwds):
        iLog.debug("enter")

        #print "iCAmonitor._caOnMonitorChange:", pvname, value, repr(kwds)

        for x, xa in self.res:
            if x.pvName == pvname:
                x.pvGetValue = value
                x.success = True
                if hasattr(self, "monitorCB"):
                    self.monitorCB(x)

    def stopMonitor(self):
        iLog.debug("enter")

        for x, xa in self.res:
            if x.monitor:
                #print "iCAmonitor.stopMonitor: PV=", x.pvName, ", was monitored:", x.monitor
                ca.clear_subscription(x.monitor[2])
                ca.flush_io()
                x.monitor = None
        ca.flush_io()

    def get_data(self):
        iLog.debug("enter")

        return self.workList

    def handle_data(self, pvData):
        iLog.debug("enter")

        if not isinstance(pvData, iCAobj):
            print "iCAmonitor.handle_data: Invalid data! data=", pvData
            return

        ca.use_initial_context()
        #print "iCAmonitor.handle_data: ca.current_context():", ca.current_context()

        # Try to connect CA channel, but don't wait for completion
        chid = ca.create_channel(pvData.pvName)

        pvData.success = False
        if not ca.isConnected(chid):
            #print "iCAmonitor.handle_data: PV not connected! PV=", pvName
            ca.connect_channel(chid, timeout = 2.0)

        if not ca.isConnected(chid):
            #print "iCAmonitor.handle_data: PV still not connected! PV=", pvData.pvName
            pvData.connected = False
            return pvData.success

        pvData.connected = True

        #print "iCAmonitor.handle_data: PV is connected, PV=", pvName

        # FIXME: Do this now, so that first self._caOnMonitorChange call can
        # store the value.
        self.res.append((pvData, False))

        # Subscribe to events
        pvData.monitor = ca.create_subscription(chid, callback = self._caOnMonitorChange)

        # Get first data?
        #pvData.pvGetValue = ca.get(chid)
        #print "iCAmonitor.handle_data: GET value: ", pvData.pvName, "=", pvData.pvGetValue

        pvData.success = True
        return pvData.success

    def handle_result(self, data, result):
        iLog.debug("enter")

        pass
        #self.res.append((data, result))

    def prerun(self):
        iLog.debug("enter")

        self.res = []

    def postrun(self):
        iLog.debug("enter")

        return self.res

class iCAThread(threading.Thread):
    def __init__(self, doRun):
        threading.Thread.__init__(self)
        iLog.debug("enter")

        self.doRun = doRun
        self.Q = Queue.Queue()

        ca.use_initial_context()
        #print "iCAThread.init: ca.current_context():", ca.current_context()

    def close(self):
        iLog.debug("enter")
        self.doRun = False

    def schedule(self, pvWork):
        iLog.debug("enter")

        if not isinstance(pvWork, iThreader):
            if pvWork != None:
                raise ValueError, "iCAThread.schedule: Invalid value! pvWork=" + str(pvWork)
                return

        self.Q.put(pvWork)

    def run(self):
        iLog.debug("enter")

        # Loop until stopped from above
        while self.doRun:
            while 1:
                pvWork = self.Q.get()
                if pvWork is None:
                    break

                # Run the work and signal completion
                pvWork.run()
                if hasattr(pvWork, "workDoneCB"):
                    pvWork.workDoneCB(pvWork)
                    #ca.show_cache()

        ca.finalize_libca()
        #ca.show_cache()
        
        iLog.debug("leave")
