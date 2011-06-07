'''
Created on Jun 1, 2011

@author: hinko
'''

from PyQt4 import QtCore
from iPVList import iPVList

class iIOC(QtCore.QObject):

    def __init__(self,
                 parent = None,
                 iocName = None
                 ):

        QtCore.QObject.__init__(self, parent)
        self.iocName = None
        self.pvList = None

        print "iIOC.init: type(iocName)=", type(iocName)

        self.iocName = iocName
        if not self.iocName:
            print 'iIOC.init: IOC name not set!'
            raise ValueError('iIOC.init: IOC name not set!')

        self.pvList = iPVList(self.iocName)
        self.pvList.generate()
        self.pvList.dump()

    def pvObject(self, pvName):
        if not pvName:
            print 'iIOC.pvObject: IOC=', self.iocName, ', pvName not specified!'
            return None
        if not len(pvName):
            print 'iIOC.pvObject: IOC=', self.iocName, ', pvName len==0!'
            return None

        return self.pvList.find(pvName)

    def pvExists(self, pvName):
        return self.pvObject(pvName) != None

    def pvGet(self, pvName, pvSlot):
        print 'iIOC.pvGet: IOC=', self.iocName, 'PV=', pvName

        try:
            iPV = self.pvObject(pvName)
        except ValueError as ex:
            print 'iIOC.pvGet: Handling exception:', ex
        finally:
            iPV.get(pvSlot)

    def pvPut(self, pvName, pvValue, pvSlot):
        print 'iIOC.pvPut: PV=', pvName

        try:
            iPV = self.pvObject(pvName)
        except ValueError as ex:
            print 'iIOC.pvPut: Handling exception:', ex
        finally:
            iPV.put(pvValue, pvSlot)

    def pvMonitorStart(self, pvName, pvSlot):
        print 'iIOC.pvMonitorStart: PV=', pvName

        try:
            iPV = self.pvObject(pvName)
        except ValueError as ex:
            print 'iIOC.pvMonitorStart: Handling exception:', ex
        finally:
            iPV.monitorStart(pvSlot)

    def pvMonitorStop(self, pvName, pvSlot):
        print 'iIOC.pvMonitorStop: PV=', pvName

        try:
            iPV = self.pvObject(pvName)
        except ValueError as ex:
            print 'iIOC.pvMonitorStop: Handling exception:', ex
        finally:
            iPV.monitorStop(pvSlot)

    def pvSubscribeConnect(self, pvName, pvSlot):
        print 'iIOC.pvSubscribeConnect: IOC=', self.iocName, 'PV=', pvName

        try:
            iPV = self.pvObject(pvName)
        except ValueError as ex:
            print 'iIOC.pvSubscribeConnect: Handling exception:', ex
        finally:
            iPV.subscribe(pvSlot, 'sigConnect')

    def pvUnsubscribeConnect(self, pvName, pvSlot):
        print 'iIOC.pvUnsubscribeConnect: IOC=', self.iocName, 'PV=', pvName

        try:
            iPV = self.pvObject(pvName)
        except ValueError as ex:
            print 'iIOC.pvUnsubscribeConnect: Handling exception:', ex
        finally:
            iPV.unsubscribe(pvSlot, 'sigConnect')

    def pvUnsubscribeGet(self, pvName, pvSlot):
        print 'iIOC.pvUnsubscribeGet: IOC=', self.iocName, 'PV=', pvName

        try:
            iPV = self.pvObject(pvName)
        except ValueError as ex:
            print 'iIOC.pvUnsubscribeGet: Handling exception:', ex
        finally:
            iPV.unsubscribe(pvSlot, 'sigGet')

    def pvUnsubscribePut(self, pvName, pvSlot):
        print 'iIOC.pvUnsubscribePut: IOC=', self.iocName, 'PV=', pvName

        try:
            iPV = self.pvObject(pvName)
        except ValueError as ex:
            print 'iIOC.pvUnsubscribePut: Handling exception:', ex
        finally:
            iPV.unsubscribe(pvSlot, 'sigPut')

    def pvUnsubscribeMonitor(self, pvName, pvSlot):
        print 'iIOC.pvUnsubscribeMonitor: IOC=', self.iocName, 'PV=', pvName

        try:
            iPV = self.pvObject(pvName)
        except ValueError as ex:
            print 'iIOC.pvUnsubscribeMonitor: Handling exception:', ex
        finally:
            iPV.unsubscribe(pvSlot, 'sigMonitor')

#===============================================================================
# Close
#===============================================================================
    def close(self):
        print 'iIOC.close: IOC=', self.iocName
        self.pvList.close()
