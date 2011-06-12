'''
Created on Jun 10, 2011

@author: hinko
'''

#===============================================================================
# COMMENTS
#===============================================================================
# TODO: provide other streams for logging (file, etc)
# TODO: provide other logging logging level to separate (file, etc)
# TODO: provide gui console for log output
#===============================================================================

import sys
import logging

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
iDefaultPVDataDir = "data"
