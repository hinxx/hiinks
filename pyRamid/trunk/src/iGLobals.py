'''
Created on Jun 16, 2011

@author: hinko
'''
import sys
import logging



#===============================================================================
# Some global variables and methods
#===============================================================================

iIOCList = None
iPVList = None
iHandler = None

iPVActionValGet = 'valGet'
iPVActionValPut = 'valPut'
iPVActionMonAdd = 'monAdd'
iPVActionMonRem = 'monRem'
iPVActionStatus = 'status'
iPVActionInfo = 'info'

iPVActions = (iPVActionValGet, iPVActionValPut, iPVActionMonAdd,
             iPVActionMonRem, iPVActionStatus, iPVActionInfo)


# Make a global logging object.
iLog = logging.getLogger("iLog")
#iLog.setLevel(logging.DEBUG)
iLog.setLevel(logging.INFO)

iLogHandle = logging.StreamHandler(stream = sys.stdout)
iLogFormatter = logging.Formatter("%(levelname)s %(asctime)s %(module)s %(funcName)s %(lineno)d %(message)s")
iLogHandle.setFormatter(iLogFormatter)
iLog.addHandler(iLogHandle)

iDefaultIOCTreeXMLFile = "conf/iIOClist.xml"
iDefaultPVTreeXMLFile = "conf/iPVlist.xml"
iDefaultDataDir = "data"

def iRaise(obj, msg, ex = ValueError):
    if obj:
        txt = "%s.%s: msg = '%s'" % (obj.__class__.__name__, __name__, msg)
    else:
        txt = "%s: msg = '%s'" % (__name__, msg)
    iLog.error("Raising exception %s" % (txt))
    raise ex, txt

def iInitIOCs(ioclist):
    global iIOCList
    iIOCList = ioclist
    iLog.debug("iIOCList obj %s .." % (iIOCList))

def iInitPVs(pvlist):
    global iPVList
    iPVList = pvlist
    iLog.debug("iPVList obj %s .." % (iPVList))

def iInitHandler(handler):
    global iHandler
    iHandler = handler
    iLog.debug("iHandler obj %s .." % (iHandler))

def iGlobalIOCs():
    global iIOCList
    iLog.debug("iIOCList obj %s .." % (iIOCList))
    return iIOCList

def iGlobalPVs():
    global iPVList
    iLog.debug("iPVList obj %s .." % (iPVList))
    return iPVList

def iGlobalHandle():
    global iHandler
    iLog.debug("iHandler obj %s .." % (iHandler))
    return iHandler

