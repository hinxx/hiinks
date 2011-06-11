'''
Created on Jun 10, 2011

@author: hinko
'''
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

iDefaultIOClistXmlFile = "conf/iIOClist.xml"
iDefaultPVlistXmlFile = "conf/iPVlist.xml"
