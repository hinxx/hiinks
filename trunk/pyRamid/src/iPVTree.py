'''
Created on Jun 12, 2011

@author: hinko
'''

from iHelper import iLog, iDefaultPVTreeXMLFile

from iXMLTree import iXMLTree

class iPVTree(iXMLTree):
    def __init__(self, parent, xmlFile = None, tag = 'pv'):
        if not xmlFile:
            xmlFile = iDefaultPVTreeXMLFile
        iXMLTree.__init__(self, parent, xmlFile, tag)
        iLog.debug("enter")

    def pvGetName(self, iName):
        iLog.debug("enter")

        iValue = self.iGet(iName, 'getSuffix')
        if iValue:
            iLog.debug("Using suffix with PV name %s" % (iName + iValue))
            return iName + iValue

        iLog.debug("Using default PV name %s" % (iName))
        return iName

    def pvPutName(self, iName):
        iLog.debug("enter")

        iValue = self.iGet(iName, 'putSuffix')
        if iValue:
            iLog.debug("Using suffix with PV name %s" % (iName + iValue))
            return iName + iValue

        iLog.debug("Using default PV name %s" % (iName))
        return iName

    def pvIsModeValue(self, iName):
        iLog.debug("enter")

        iValue = self.iGet(iName, 'mode')
        if iValue:
            iLog.debug("Got MODE value %s=%s" % (iName, iValue))
            return (iValue == 'value')

        iLog.debug("Not found MODE value for %s" % (iName))
        return False
