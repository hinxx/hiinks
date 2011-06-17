'''
Created on Jun 13, 2011

@author: hinko
'''

from iGLobals import iRaise, iLog, iPVActions
from iThreader import iThreader
from iPVObj import iPVObj

from epics import ca, dbr


class iPVJobs(iThreader):

    def __init__(self, parent = None):

        iThreader.__init__(self, parent)
        iLog.debug("enter")

        self.pvObjList = []
        self.pvAction = None

#===============================================================================
# iThreader overloaded methods
#===============================================================================

    def initData(self, pvAction, pvObjList):
        iLog.debug("enter")

        if not pvAction in iPVActions:
            iRaise (self, "Invalid CA action argument '%s'" % (str(pvAction)))

        if not isinstance(pvObjList, list):
            if pvObjList != None:
                iRaise("Invalid pvObjList argument '%s'" % (type(pvObjList)))

        self.pvObjList = pvObjList
        self.pvAction = pvAction
        iLog.debug("PV self.pvObjList action %s" % (str(pvAction)))

    def getData(self):
        iLog.debug("enter")

        iLog.debug("Current self.pvObjList=%s" % (self.pvObjList))
        return self.pvObjList

    def handleData(self, pvObj):
        iLog.debug("enter")

        iLog.debug("pvObj=%s" % str(pvObj))
        if not isinstance(pvObj, iPVObj):
            iRaise (self, "Invalid PV data object argument '%s'" % (type(pvObj)))

        iLog.debug("Handling PV %s, action %s" % (pvObj.name, self.pvAction))

        ca.use_initial_context()

        pvObj._caHandler(self.pvAction)

    def handleResult(self, pvObj, result):
        iLog.debug("enter")
        self.pvObjList.remove(pvObj)

    def prerun(self):
        iLog.debug("enter")

    def postrun(self):
        iLog.debug("enter")
        self.pvObjList = []

#===============================================================================
# Other methods
#===============================================================================
    def close(self):
        iLog.info("done")
