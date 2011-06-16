'''
Created on Jun 9, 2011

@author: hinko
'''
import sys
import logging

#===============================================================================
# COMMENTS
#===============================================================================
# TODO: provide other streams for logging (file, etc)
# TODO: provide other logging logging level to separate (file, etc)
# TODO: provide gui console for log output
#===============================================================================

#===============================================================================
# Some defines
#===============================================================================
iPVActionValGet = 'valGet'
iPVActionValPut = 'valPut'
iPVActionMonAdd = 'monAdd'
iPVActionMonRem = 'monRem'
iPVActionStatus = 'status'
iPVActionInfo = 'info'

iPVActions = (iPVActionValGet, iPVActionValPut, iPVActionMonAdd,
             iPVActionMonRem, iPVActionStatus, iPVActionInfo)


#===============================================================================
# Some methods
#===============================================================================
def iRaise(obj, msg, ex = ValueError):
    raise ex, "%s.%s: msg = '%s'" % (obj.__class__.__name__, __name__, msg)


# Make a global logging object.
iLog = logging.getLogger("iLog")
iLog.setLevel(logging.DEBUG)
#iLog.setLevel(logging.INFO)

iLogHandle = logging.StreamHandler(stream = sys.stdout)
iLogFormatter = logging.Formatter("%(levelname)s %(asctime)s %(module)s %(funcName)s %(lineno)d %(message)s")
iLogHandle.setFormatter(iLogFormatter)
iLog.addHandler(iLogHandle)

iDefaultIOCTreeXMLFile = "conf/iIOClist.xml"
iDefaultPVTreeXMLFile = "conf/iPVlist.xml"
iDefaultPVDataDir = "data"
