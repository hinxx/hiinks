'''
Created on Jun 16, 2011

@author: hinko
'''

from iGLobals import iRaise, iLog

from PyQt4 import QtCore
from iHelper import iGetPV
from iPVHandler import iPVHandler

class iIOCObj(QtCore.QObject):
    sigValueChanged = QtCore.pyqtSignal('QObject*')
    sigConnChanged = QtCore.pyqtSignal('QObject*')

    def __init__(self, parent = None):
        QtCore.QObject.__init__(self, parent)
        iLog.debug("enter")

        # Properties found in XML
        self.name = None
        self.text = None
        self.enabled = None
        self.ip = None
        self.group = None
        self.comment = None

        # Other properties
        self.connected = False
        self.pvs = dict()

    def pv(self, pvName):
        iLog.debug("enter")

        iLog.debug("looking for PV %s" % (pvName))

        pvObj = None
        if pvName in self.pvs.keys():
            iLog.debug("already in the list %s" % (pvName))
            pvObj = self.pvs[pvName]
        else:
            for _pvObj in self.pvs.values():
                if (_pvObj.getSuffix) and (_pvObj.name + _pvObj.getSuffix == pvName):
                    pvObj = _pvObj
                    iLog.debug("found '%s' in the list" % (_pvObj.name))
                    break
                elif (_pvObj.putSuffix) and (_pvObj.name + _pvObj.putSuffix == pvName):
                    pvObj = _pvObj
                    iLog.debug("found '%s' in the list" % (_pvObj.name))
                    break
                elif (_pvObj.cmdSuffix) and (_pvObj.name + _pvObj.cmdSuffix == pvName):
                    pvObj = _pvObj
                    iLog.debug("found '%s' in the list" % (_pvObj.name))
                    break

            if not pvObj:
                iLog.debug("Looking in the XML tree for '%s'" % (pvName))
                pvObj = iGetPV(pvName)
                if pvObj:
                    iLog.debug("XML tree contains '%s'" % (pvName))
                    pvObj.iocName = self.name
                    pvObj.setParent(self)

                    self.pvs[pvName] = pvObj

        iLog.info("PV object %s" % (pvObj))
        return pvObj
