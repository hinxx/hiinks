'''
Created on Jun 1, 2011

@author: hinko
'''

import os
import sys
from PyQt4 import QtCore
from iPV import iPV

class iPVList(QtCore.QObject):

    def __init__(self,
                 iocName,
                 parent = None):

        QtCore.QObject.__init__(self, parent)
        # List of known IOC PVs in format:
        # :<port>:<record>
        self.pvFile = "PVs"
        # Dictionary containing all known PVs (PVname: uPV object)
        self.pvList = dict()
        self.iocName = None

        self.iocName = iocName
        if not self.iocName:
            print 'iPVList.init: IOC name not set!'
            raise ValueError('iPVList.init: IOC name not set!')

    def generate(self, pvFile = None):

        if not self.iocName:
            print "iPVList.generate: IOC name missing!"
            return None

        print "iPVList.generate: IOC=", self.iocName

        if not pvFile:
            pvFile = self.pvFile

        if not os.path.exists(pvFile):
            print 'iPVList.generate: PV list file not found!,', pvFile
            raise ValueError('iPVList.generate: PV list file not found!,', pvFile)

        f = open(pvFile)
        for line in f:
            fullName = line.strip("\n")
            dummy, port, name = fullName.split(":")
            #print "iPVList.generate: PV ==", name

#            filter = ["ENV_MAX_ADC_MONITOR", "SA_X_MONITOR", "SA_Y_MONITOR", "SA_SUM_MONITOR" ]
#            if not name in filter:
#                continue

            obj = iPV(self, self.iocName, port, name)

            # Set PV access
            if name.endswith("_SP"):
                obj.access = "write-only"
            elif name.endswith("_MONITOR"):
                obj.access = "read-only"
            elif name.endswith("_CMD"):
                obj.access = "write-only"
            else:
                obj.access = "read-only"

            # Add enum strings to the PV if any
            if name == 'ENV_AGC_MONITOR' or name == 'ENV_AGC_SP':
                obj.enums = ["Manual", "Auto"]
            elif name == 'ENV_DSC_MONITOR' or name == 'ENV_DSC_SP':
                obj.enums = ["Off", "Unity", "Auto", "Lastgood"]
            elif name == 'ENV_ILK_MODE_MONITOR' or name == 'ENV_ILK_MODE_SP':
                obj.enums = ["Disable", "Enable", "Gain dep."]
            elif name == 'ENV_MC_PLL_MONITOR' or name == 'ENV_SC_PLL_MONITOR':
                obj.enums = ["Unlocked", "Locked"]
            elif name == 'ENV_PM_MODE_MONITOR' or name == 'ENV_PM_MODE_SP':
                obj.enums = ["External", "Internal", "Position"]
            elif  name == 'ENV_PMDEC_MONITOR' or name == 'ENV_PMDEC_SP' or \
                name == 'ENV_STATS_DDDEC_MONITOR' or name == 'ENV_STATS_DDDEC_SP':
                obj.enums = ["1", "64"]

            # Add to list
            self.pvList[fullName] = obj

        f.close()

    def find(self, pvName):
        if not len(self.pvList):
            print "iPVList.find: PVList empty, IOC=", self.iocName
            raise ValueError("iPVList.find: PVList empty, IOC=", self.iocName)
            return None

        if pvName in self.pvList:
            return self.pvList[pvName]

        print "iPVList.find: PV not found, PV=", pvName, ",IOC=", self.iocName
        raise ValueError("iPVList.find: PV not found, PV=", pvName, ",IOC=", self.iocName)
        return None

    def dump(self):
        if not len(self.pvList):
            print "iPVList.dump: PVList empty, IOC=", self.iocName
            return None

        print "iPVList.dump: PV list, IOC=", self.iocName
        for pv in self.pvList.values():
            print pv.fullName

    def close(self):
        print "iPVList.close: IOC=", self.iocName
        for v in self.pvList.values():
            v.close()
        self.pvList = None
