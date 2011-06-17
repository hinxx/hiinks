'''
Created on Jun 13, 2011

@author: hinko
'''

from iGLobals import iRaise, iLog, iPVActions

from PyQt4 import QtCore
import Queue
import time

from iPVJobs import iPVJobs

class iPVHandler(QtCore.QThread):

    def __init__(self, parent = None):
        QtCore.QThread.__init__(self, parent)
        iLog.debug("enter")

        self.exiting = False
        self.Q = Queue.Queue()
        self.pending = []
        self.pvJobs = iPVJobs(self)

        # Start the thread now
        self.start()

    def enqeueList(self, pvAction, pvObjList):
        iLog.debug("enter")

        if not pvAction in iPVActions:
            iRaise (self, "Invalid CA action argument '%s'" % (str(pvAction)))

        if not isinstance(pvObjList, list):
            iRaise("Invalid pvObjList argument '%s'" % (type(pvObjList)))

        iLog.debug("Enqueueing PV list %s" % (str(pvObjList)))
        self.pending.append((pvAction, pvObjList))

    def processList(self, pvAction = None, pvObjList = None):

        if pvAction and pvObjList:
            self.enqeueList(pvAction, pvObjList)

        while len(self.pending):
            # Enqueue the PV job
            self.Q.put(self.pending.pop())

    def run(self):
        # Note: This is never called directly. It is called by Qt once the
        # thread environment has been set up.
        iLog.debug("enter")

        # Loop until stopped from above
        while not self.exiting:
            while 1:
                pvData = self.Q.get()

                if pvData is None:
                    break

                if not isinstance(pvData, tuple):
                    iRaise("Invalid pvData queue argument '%s'" % (type(pvData)))

                # Set job data
                pvAction, pvObjList = pvData
                self.pvJobs.initData(pvAction, pvObjList)

                # Run the job, specifying the number of threads to spawn
                # FIXME: Should number of threads be different?
                self.pvJobs.run(len(pvObjList))

        iLog.debug("leave")


    def close(self):
        iLog.debug("enter")

        self.exiting = True
        self.Q.put(None)
        self.wait()
