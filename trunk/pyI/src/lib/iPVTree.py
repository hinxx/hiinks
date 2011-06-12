'''
Created on Jun 12, 2011

@author: hinko
'''

from iConf import iLog, iDefaultPVTreeXMLFile

from PyQt4 import QtCore
from iXMLTree import iXMLTree

class iPVTree(iXMLTree):
    def __init__(self, parent, xmlFile = None, tag = 'pv'):
        if not xmlFile:
            xmlFile = iDefaultPVTreeXMLFile
        iXMLTree.__init__(self, parent, xmlFile, tag)
        iLog.info("enter")

    def pvGetName(self, iName):
        iLog.info("enter")

        iValue = self.iGet(iName, 'getSuffix')
        if iValue:
            iLog.info("Using suffix with PV name %s" % (iName + iValue))
            return iName + iValue

        iLog.debug("Using default PV name %s" % (iName))
        return iName

    def pvIsModeValue(self, iName):
        iLog.info("enter")

        iValue = self.iGet(iName, 'mode')
        if iValue:
            iLog.info("Got MODE value %s=%s" % (iName, iValue))
            return (iValue == 'value')

        iLog.debug("Not found MODE value for %s" % (iName))
        return False

if __name__ == '__main__':
    print "PVs:"

    def test1():
        ttt = iPVTree(None, "../conf/iPVlist.xml", "pv")
        ttt.iNameGet(':P:ai1')
        ttt.iEnabledGet(':P:ai1')
        ttt.iDump(':P:ai1')
        ttt.tDump()

        print "1 ----------------------------"
        ttt.iNameGet(':P:ai1')
        print "2 ----------------------------"
        ttt.iNameSet(':P:ai1', 'foobar')
        print "3 ----------------------------"
        ttt.iNameGet(':P:ai1')
        print "4 ----------------------------"
        ttt.iNameGet('foobar')
        print "5 ----------------------------"
        ttt.iEnabledGet(':P:ai2')
        print "6 ----------------------------"
        ttt.iEnabledSet(':P:ai2', "False")
        print "7 ----------------------------"
        ttt.iEnabledGet(':P:ai2')
        print "8 ----------------------------"
        #ttt.tDump()
        ttt.iDump(':P:ai1')
        ttt.iDump('foobar')
        ttt.iDump(':P:ai2')

    test1()
    #test2()
