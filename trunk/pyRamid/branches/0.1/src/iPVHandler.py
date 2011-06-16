'''
Created on Jun 13, 2011

@author: hinko
'''

from iHelper import iRaise, iLog, iPVActions

from PyQt4 import QtCore
import Queue
import time

from iPVJobs import iPVJobs

class iPVHandler(QtCore.QThread):

    def __init__(self, parent):
        QtCore.QThread.__init__(self, parent)
        iLog.debug("enter")

        self.exiting = False
        self.Q = Queue.Queue()
        self.pvObjList = dict()
        self.pvJobs = iPVJobs(self)

        # Start the thread now
        self.start()

    def enqeue(self, pvAction, pvNameList):
        iLog.debug("enter")

        if not pvAction in iPVActions:
            iRaise (self, "Invalid CA action argument '%s'" % (str(pvAction)))

        if not isinstance(pvNameList, list):
            if pvNameList != None:
                iRaise("Invalid pvNameList argument '%s'" % (type(pvNameList)))

        iLog.debug("Enqueueing PV list %s" % (str(pvNameList)))

        # Enqueue the PV job
        self.Q.put((pvAction, pvNameList))

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
                pvAction, pvNameList = pvData
                self.pvJobs.initData(pvAction, pvNameList)

                # Run the job, specifying the number of threads to spawn
                # FIXME: Should number of threads be different?
                self.pvJobs.run(len(pvNameList))

        iLog.debug("leave")


    def close(self):
        iLog.debug("enter")

        self.exiting = True
        self.Q.put(None)
        self.wait()

# This is called after the main app is closed, and causes errors, since close()
# does all the work already..
#    def __del__(self):
#        iLog.debug("enter")
#
#        self.exiting = True
#        self.Q.put(None)
#        self.wait()
