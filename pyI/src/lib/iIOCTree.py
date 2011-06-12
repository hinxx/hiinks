'''
Created on Jun 12, 2011

@author: hinko
'''

from iConf import iLog, iDefaultIOCTreeXMLFile

from PyQt4 import QtCore
from iXMLTree import iXMLTree

class iIOCTree(iXMLTree):
    def __init__(self, parent, xmlFile = None, tag = 'ioc'):
        if not xmlFile:
            xmlFile = iDefaultIOCTreeXMLFile
        iXMLTree.__init__(self, parent, xmlFile, tag)
        iLog.info("enter")

if __name__ == '__main__':
    print "PVs:"

    def test1():
        ttt = iIOCTree(None, "../conf/iIOClist.xml", "ioc")
        ttt.iNameGet('hinkoHost')
        ttt.iEnabledGet('hinkoHost')
        ttt.iDump('hinkoHost')
        ttt.tDump()

        print "1 ----------------------------"
        ttt.iNameGet('hinkoHost')
        print "2 ----------------------------"
        ttt.iNameSet('hinkoHost', 'foobar')
        print "3 ----------------------------"
        ttt.iNameGet('hinkoHost')
        print "4 ----------------------------"
        ttt.iNameGet('foobar')
        print "5 ----------------------------"
        ttt.iEnabledGet('hinkoHost1')
        print "6 ----------------------------"
        ttt.iEnabledSet('hinkoHost1', "False")
        print "7 ----------------------------"
        ttt.iEnabledGet('hinkoHost1')
        print "8 ----------------------------"
        #ttt.tDump()
        ttt.iDump('hinkoHost')
        ttt.iDump('foobar')
        ttt.iDump('hinkoHost1')

    test1()
    #test2()
