'''
Created on Jun 1, 2011

@author: hinko
'''

from PyQt4 import QtCore
from iIOC import iIOC

class iIOCList(QtCore.QObject):

    def __init__(self, parent = None):
        QtCore.QObject.__init__(self, parent)

        # Dictionary containing all known IOCs (IOCname: uIOC object)
        self.iocList = dict()

    def addIOC(self, iocName):
        ioc = iIOC(self, iocName)
        self.iocList[iocName] = ioc

        print 'iIOCList.addIOC: new IOC:', iocName

    def find(self, iocName):
        if not len(self.iocList):
            print 'iIOCList.find: IOC list empty!'
            raise ValueError('iIOCList.find: IOC list empty!')
            return None

        if iocName in self.iocList:
            return self.iocList[iocName]

        print 'iIOCList.find: IOC not found, IOC=', iocName
        raise ValueError('iIOCList.find: IOC not found, IOC=', iocName)
        return None

    def dump(self):
        if not len(self.iocList):
            print 'iIOCList.dump: IOC list empty!'
            return None

        print 'iIOCList.dump: IOC list'
        print ' -----------------------------'
        for ioc in self.iocList.values():
            ioc.pvList.dump()
        print ' -----------------------------'

    def close(self):
        print 'iIOCList.close:'
        for ioc in self.iocList.values():
            ioc.close()
        self.iocList = None
