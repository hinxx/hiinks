'''
Created on Jun 8, 2011

@author: hinko
'''

from lib.iConf import iLog

import sys
import time
from PyQt4 import QtCore

from iCAobj import iCAobj
from iCAWork import iCAget, iCAmonitor, iCAput, iCAThread

class iCA(QtCore.QObject):
    sigGet = QtCore.pyqtSignal('QObject*')
    sigPut = QtCore.pyqtSignal('QObject*')
    sigMonitor = QtCore.pyqtSignal('QObject*')
    sigConnect = QtCore.pyqtSignal('QObject*')
    sigDone = QtCore.pyqtSignal('QObject*')

    iCAThr = None

    def __init__(self, parent = None):
        QtCore.QObject.__init__(self, parent)
        iLog.debug("enter")

        self.iCAThr = iCAThread(True)
        self.iCAThr.start()

    def get(self, pvList):
        iLog.debug("enter")

        #print "iCA.get: pvList=", pvList

        workList = []
        for pvName, pvValue in pvList:
            workList.append(iCAobj(self, pvName))

        #print "iCA.get: workList=", workList

        # Create and schedule GET work
        caWork = iCAget(self, workList, len(workList), self.workDoneCallback, self.getCallback)
        self.iCAThr.schedule(caWork)

        return caWork

    def put(self, pvList):
        iLog.debug("enter")

        #print "iCA.put: pvList=", pvList

        workList = []
        for pvName, pvValue in pvList:
            workList.append(iCAobj(self, pvName, pvValue))

        #print "iCA.put: workList=", workList

        # Create and schedule PUT work
        caWork = iCAput(self, workList, len(workList), self.workDoneCallback, self.putCallback)
        self.iCAThr.schedule(caWork)

        return caWork

    def monitor(self, pvList):
        iLog.debug("enter")

        #print "iCA.monitor: pvList=", pvList

        workList = []
        for pvName, pvValue in pvList:
            workList.append(iCAobj(self, pvName))

        #print "iCA.monitor: workList=", workList

        # Create and schedule MONITOR work
        caWork = iCAmonitor(self, workList, len(workList), self.workDoneCallback, self.monitorCallback)
        self.iCAThr.schedule(caWork)

        return caWork

    def monitorStop(self, caWork):
        #print "iCA.monitorStop: caWork=", caWork
        caWork.stopMonitor()

    def getCallback(self, caJob):
        iLog.debug("enter")

        #print "iCA.getCallback: PV=", caJob.pvName, "=", caJob.pvGetValue, "SUCCESS=", caJob.success
        #print "iCA.getCallback: Emit sigGett(QObject*) for ", caJob.pvName
        self.sigGet.emit(caJob)

    def putCallback(self, caJob):
        iLog.debug("enter")

        #print "iCA.putCallback: PV=", caJob.pvName, "=", caJob.pvGetValue, "SUCCESS=", caJob.success
        #print "iCA.putCallback: Emit sigPut(QObject*) for ", caJob.pvName
        self.sigPut.emit(caJob)

    def monitorCallback(self, caJob):
        iLog.debug("enter")

        #print "iCA.monitorCallback: PV=", caJob.pvName, "=", caJob.pvGetValue, "SUCCESS=", caJob.success
        #print "iCA.monitortCallback: Emit sigPut(QObject*) for ", caJob.pvName
        self.sigMonitor.emit(caJob)

    def workDoneCallback(self, caWork):
        iLog.debug("enter")

        #print "iCA.workDoneCallback: caWork=", caWork
        #for caJob, caResult in caWork.res:
        #    #print "iCA.workDoneCallback: caJob, caResult", caJob, caResult
        #    print "iCA.workDoneCallback: PV=", caJob.pvName, "=", caJob.pvGetValue, "SUCCESS=", caJob.success

        #print "iCA.workDoneCallback: Emit sigDone(QObject*) for ", caWork
        self.sigDone.emit(caWork)

    def close(self):
        iLog.debug("enter")

        iLog.debug("closing CA thread ..")
        self.iCAThr.close()
        self.iCAThr.schedule(None)
        #self.iCAThr.join(1.0)
        self.iCAThr.join()
        self.iCAThr = None

        nrRecievers = self.receivers(QtCore.SIGNAL('sigConnect(QObject*)'))
        #print "iCA.close; sigConnect disconnected, left receivers count=", nrRecievers
        if nrRecievers > 0:
            self.sigConnect.disconnect()
        nrRecievers = self.receivers(QtCore.SIGNAL('sigConnect(QObject*)'))
        #print "iCA.close; sigConnect disconnected, left receivers count=", nrRecievers

        nrRecievers = self.receivers(QtCore.SIGNAL('sigGet(QObject*)'))
        #print "iCA.close; sigGet disconnected, left receivers count=", nrRecievers
        if nrRecievers > 0:
            self.sigGet.disconnect()
        nrRecievers = self.receivers(QtCore.SIGNAL('sigGet(QObject*)'))
        #print "iCA.close; sigGet disconnected, left receivers count=", nrRecievers

        nrRecievers = self.receivers(QtCore.SIGNAL('sigPut(QObject*)'))
        #print "iCA.close; sigPut disconnected, left receivers count=", nrRecievers
        if nrRecievers > 0:
            self.sigPut.disconnect()
        nrRecievers = self.receivers(QtCore.SIGNAL('sigPut(QObject*)'))
        #print "iCA.close; sigPut disconnected, left receivers count=", nrRecievers

        nrRecievers = self.receivers(QtCore.SIGNAL('sigMonitor(QObject*)'))
        #print "iCA.close; sigMonitor disconnected, left receivers count=", nrRecievers
        if nrRecievers > 0:
            self.sigMonitor.disconnect()
        nrRecievers = self.receivers(QtCore.SIGNAL('sigMonitor(QObject*)'))
        #print "iCA.close; sigMonitor disconnected, left receivers count=", nrRecievers

        nrRecievers = self.receivers(QtCore.SIGNAL('sigDone(QObject*)'))
        #print "iCA.close; sigDone disconnected, left receivers count=", nrRecievers
        if nrRecievers > 0:
            self.sigDone.disconnect()
        nrRecievers = self.receivers(QtCore.SIGNAL('sigDone(QObject*)'))
        #print "iCA.close; sigDone disconnected, left receivers count=", nrRecievers


if __name__ == "__main__":

    import os
    # Set EPICS base stuff
    epics_base = '/home/hinko/workspace/base-3.14.12.1'
    print 'exporting EPICS_CA_MAX_ARRAY_BYTES: 16777216'
    path = os.environ.get('PATH', '') + ':' + epics_base + '/bin/linux-x86'
    os.environ['PATH'] = path
    path = os.environ.get('LD_LIBRARY_PATH', '') + ':' + epics_base + '/lib/linux-x86'
    os.environ['LD_LIBRARY_PATH'] = path
    os.environ['EPICS_HOST_ARCH'] = 'linux-x86'

    def test_get_only():
        e = iCA()

        print
        print "------ round 1 --------"
        print
#        pv1 = iCAobj(e, "hinkoHost:P:ai1")
#        pv2 = iCAobj(e, "hinkoHost:P:ai2")
#        pv3 = iCAobj(e, "hinkoHost:P:ai3")
#        e.get([pv1, pv2, pv3])
        l = [("hinkoHost:P:ai1", None), ("hinkoHost:P:ai2", None), ("hinkoHost:P:ai3", None)]
        e.get(l)
        time.sleep(3)
        #ca.show_cache()

        print
        print "------ round 2 --------"
        print
#        e.get([pv1, pv2, pv3])
        e.get(l)
        time.sleep(3)
        #ca.show_cache()

        print
        print "------ END!!! --------"
        print
        e.close()

    def test_put_only():
        e = iCA()

        print
        print "------ round 1 --------"
        print
        pv1 = iCAobj(e, "hinkoHost:P:ai1", 11)
        pv2 = iCAobj(e, "hinkoHost:P:ai2", 22)
        pv3 = iCAobj(e, "hinkoHost:P:ai3", 33)
        e.put([pv1, pv2, pv3])
        time.sleep(3)

        print
        print "------ END!!! --------"
        print
        e.close()

    def test_put_get():
        e = iCA()

        print
        print "------ PUT round 1 --------"
        print
        pv1 = iCAobj(e, "hinkoHost:P:ai1", 11)
        pv2 = iCAobj(e, "hinkoHost:P:ai2", 22)
        pv3 = iCAobj(e, "hinkoHost:P:ai3", 33)
        e.put([pv1, pv2, pv3])
        time.sleep(3)

        print
        print "------ GET round 1 --------"
        print
        e.get([pv1, pv2, pv3])
        time.sleep(3)

        print
        print "------ END!!! --------"
        print
        e.close()


    def test_monitor_only():
        e = iCA()

        print
        print "------ round 1 starting monitor --------"
        print
        pv1 = iCAobj(e, "hinkoHost:P:ai1")
        pv2 = iCAobj(e, "hinkoHost:P:ai2")
        pv3 = iCAobj(e, "hinkoHost:P:ai3")
        mon = e.monitor([pv1, pv2, pv3])
        time.sleep(5)

        print
        print "------ round 1 stopping monitor  --------"
        print
        e.monitorStop(mon)
        time.sleep(5)

        print
        print "------ END!!! --------"
        print
        e.close()

    # run the test
    test_get_only()
    #test_put_only()
    #test_put_get()
    #test_monitor_only()
