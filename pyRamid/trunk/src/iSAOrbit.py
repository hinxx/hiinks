'''
Created on Jun 18, 2011

@author: hinko
'''

#===============================================================================
# COMMENTS
#===============================================================================
#
#===============================================================================

from iGLobals import iRaise, iLog, iGlobalPVs, iGlobalIOCs, iGlobalHandle

from PyQt4 import QtCore, QtGui

from ui.uiPanelSAOrbit import Ui_PanelSAOrbit
from lib.iWidgets import iQGraphicsWidget

class iPanelSAOrbit(QtGui.QWidget):

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        iLog.debug("enter")

        self.iocName = None
        self.pvNames = [':SA:SA_X', ':SA:SA_Y', ':SA:SA_SUM']
        self.pvs = iGlobalPVs()
        self.iocs = iGlobalIOCs()
        self.items = dict()

        self.ui = Ui_PanelSAOrbit()
        self.ui.setupUi(self)

        self.ui.pushButton_refresh.clicked.connect(self.pvRefresh)


    def show(self):
        iLog.debug("enter")

    def hide(self):
        iLog.debug("enter")

    def pvPopulate(self):
        iLog.debug("enter")

        if len(self.items) != 0:
            iLog.warning("items list already present")
            return

        pvName = self.pvNames[0]
        idx = 0
        for iocName in self.iocs['__myid__']:
            ioc = self.iocs[iocName]
            pv = ioc.pv(pvName)
            item = iQGraphicsWidget(self.ui.graphicsView, pv)

            #self.ui.graphicsView.iWidgets[pv.nameGetFull()] = item
            self.ui.graphicsView.addWidget(item)

            self.items[pv.nameGetFull()] = item
            iLog.info("added PV '%s' to view, index %d" % (pv.nameGetFull(), idx))
            idx += 1

    def pvRefresh(self):
        iLog.info("enter")

        self.pvPopulate()

        if len(self.items) == 0:
            iLog.error("invalid items list argument")
            return

        pvName = self.pvNames[0]
        for iocName in self.iocs['__myid__']:
            ioc = self.iocs[iocName]
            pv = ioc.pv(pvName)

            item = self.items[pv.nameGetFull()]

            item.connectPVObj(pv)

            iLog.debug("Handing over PV '%s' to handler" % pv.nameGetFull())
            pv.scheduleGet()
