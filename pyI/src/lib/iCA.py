'''
Created on Jun 8, 2011

@author: hinko
'''


import sys
import time
from PyQt4 import QtCore

from iCAobj import iCAobj
from iCAWork import iCAget, iCAmonitor, iCAput, iCAThread

class iCA(QtCore.QObject):

    iCAThr = None

    def __init__(self, parent = None):

        QtCore.QObject.__init__(self, parent)

        self.iCAThr = iCAThread(True)
        self.iCAThr.start()

    def put(self, workList):
        #print "iCA.put: workList=", workList

        # Create and schedule PUT work
        caWork = iCAput(workList, len(workList), self.workDoneCallback, self.monitorCallback)
        self.iCAThr.schedule(caWork)

        return caWork

    def get(self, workList):
        #print "iCA.get: workList=", workList

        # Create and schedule GET work
        caWork = iCAget(workList, len(workList), self.workDoneCallback, self.monitorCallback)
        self.iCAThr.schedule(caWork)

        return caWork

    def monitor(self, workList):
        #print "iCA.monitor: workList=", workList

        # Create and schedule MONITOR work
        caWork = iCAmonitor(workList, len(workList), self.workDoneCallback, self.monitorCallback)
        self.iCAThr.schedule(caWork)

        return caWork

    def monitorStop(self, caWork):
        print "iCA.monitorStop: caWork=", caWork
        caWork.stopMonitor()

    def monitorCallback(self, caJob):
        print "iCA.monitorCallback: PV=", caJob.pvName, "=", caJob.pvGetValue, "SUCCESS=", caJob.success

    def workDoneCallback(self, caWork):
        #print "iCA.workDoneCallback: caWork=", caWork
        for caJob, caResult in caWork.res:
            #print "iCA.workDoneCallback: caJob, caResult", caJob, caResult
            print "iCA.workDoneCallback: PV=", caJob.pvName, "=", caJob.pvGetValue, "SUCCESS=", caJob.success

    def close(self):
        print "iCA.close: Closing main CA thread=", self.iCAThr
        self.iCAThr.close()
        self.iCAThr.schedule(None)
        #self.iCAThr.join(1.0)
        self.iCAThr.join()
        self.iCAThr = None
        #ca.finalize_libca()
        #ca.show_cache()
        print "iCA.close: DONE!"


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
        pv1 = iCAobj("hinkoHost:P:ai1")
        pv2 = iCAobj("hinkoHost:P:ai2")
        pv3 = iCAobj("hinkoHost:P:ai3")
        e.get([pv1, pv2, pv3])
        time.sleep(3)
        #ca.show_cache()

        print
        print "------ round 2 --------"
        print
        e.get([pv1, pv2, pv3])
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
        pv1 = iCAobj("hinkoHost:P:ai1", 11)
        pv2 = iCAobj("hinkoHost:P:ai2", 22)
        pv3 = iCAobj("hinkoHost:P:ai3", 33)
        e.put([pv1, pv2, pv3])
        time.sleep(3)
        #ca.show_cache()

        print
        print "------ END!!! --------"
        print
        e.close()

    def test_put_get():
        e = iCA()

        print
        print "------ PUT round 1 --------"
        print
        pv1 = iCAobj("hinkoHost:P:ai1", 11)
        pv2 = iCAobj("hinkoHost:P:ai2", 22)
        pv3 = iCAobj("hinkoHost:P:ai3", 33)
        e.put([pv1, pv2, pv3])
        time.sleep(3)
        #ca.show_cache()

        print
        print "------ GET round 1 --------"
        print
        e.get([pv1, pv2, pv3])
        time.sleep(3)
        #ca.show_cache()

        print
        print "------ END!!! --------"
        print
        e.close()


    def test_monitor_only():
        e = iCA()

        print
        print "------ round 1 starting monitor --------"
        print
        pv1 = iCAobj("hinkoHost:P:ai1")
        pv2 = iCAobj("hinkoHost:P:ai2")
        pv3 = iCAobj("hinkoHost:P:ai3")
        mon = e.monitor([pv1, pv2, pv3])
        time.sleep(5)
        #ca.show_cache()

        print
        print "------ round 1 stopping monitor  --------"
        print
        e.monitorStop(mon)
        time.sleep(5)
        #ca.show_cache()

        print
        print "------ END!!! --------"
        print
        e.close()

    # run the test
    #test_get_only()
    #test_put_only()
    #test_put_get()
    test_monitor_only()
