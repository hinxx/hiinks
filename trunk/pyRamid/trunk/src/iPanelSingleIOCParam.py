'''
Created on Jun 7, 2011

@author: hinko
'''

#===============================================================================
# COMMENTS
#===============================================================================
# 
#===============================================================================

from iGLobals import iRaise, iLog, iGlobalHandle, iGlobalPVs, iGlobalIOCs, iPVActionValGet
from iHelper import xmlToDictParser
from PyQt4 import QtCore, QtGui

from ui.uiPanelSingleIOCParam import Ui_PanelSingleIOCParam
from lib.iWidgets import iQTreeWidgetItem

class iPanelSingleIOCParam(QtGui.QWidget):

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        iLog.debug("enter")

        self.iocName = None
        self.pvName = None
        #self.pvs = iGlobalPVs()
        self.iocs = iGlobalIOCs()

        self.config = xmlToDictParser('conf/iSingleIOCPVList.xml')

        self.ui = Ui_PanelSingleIOCParam()
        self.ui.setupUi(self)

        self.ui.pushButton_apply.clicked.connect(self.pvApply)
        self.ui.pushButton_refresh.clicked.connect(self.pvRefresh)
        self.ui.lineEdit_iocName.textChanged.connect(self.iocTextChanged)
        self.connect(self.ui.comboBox_iocName, QtCore.SIGNAL('activated(QString)'), self.iocComboChanged)

        iocName = str(self.ui.lineEdit_iocName.text())

        self.ui.comboBox_iocName.addItem('-- unknown --')
        self.ui.comboBox_iocName.addItems(self.iocs['__myid__'])

        self.iocTextChanged(iocName)

    def show(self):
        iLog.debug("enter")

    def hide(self):
        iLog.debug("enter")

    def close(self):
        iLog.debug("enter")

    def iocComboChanged(self, txt):
        iLog.debug("enter")
        iLog.debug("New IOC text '%s'" % (txt))
        self.ui.lineEdit_iocName.setText(txt)

    def iocTextChanged(self, txt):
        iLog.debug("enter")
        iLog.debug("New IOC text '%s'" % (txt))

        for x in range(1, self.ui.comboBox_iocName.count()):
            comboTxt = str(self.ui.comboBox_iocName.itemText(x))
            if comboTxt.startswith(txt):
                iLog.info("Selecting IOC combo '%s' -> '%s'," % (txt, comboTxt))
                self.ui.comboBox_iocName.setCurrentIndex(x)
                return

        self.ui.comboBox_iocName.setCurrentIndex(0)

    def iocChange(self):
        iLog.debug("enter")

        iLog.debug("current iocName=%s" % self.iocName)
        iocName = str(self.ui.lineEdit_iocName.text())
        iLog.debug("have iocName=%s" % iocName)

        if not len(iocName):
            iLog.error("invalid/empty iocName=%s" % iocName)
            return

        if self.iocName == iocName:
            iLog.debug("already showing iocName=%s" % iocName)
            return

        self.iocName = iocName

        iLog.debug("new iocName=%s" % self.iocName)

    def pvPopulate(self):
        iLog.info("enter")

        if self.ui.treeWidget.topLevelItemCount() != 0:
            iLog.warning("Tree widget is already populated")
            return

        for iKey in self.config['__myid__']:
            iVal = self.config[iKey]
            iLog.info("iKey=%s, iVal=%s" % (iKey, iVal))
            item = QtGui.QTreeWidgetItem([iKey])
            self.ui.treeWidget.addTopLevelItem(item)

            for pKey in iVal['__myid__']:
                pVal = iVal[pKey]
                iLog.info("pKey=%s, pVal=%s" % (pKey, pVal))

                ioc = self.iocs[self.iocName]
                pv = ioc.pv(pKey)

                child = iQTreeWidgetItem([pv.text], pv.widget)
                item.addChild(child)
                child.setText(3, pKey)
                if pv.widget:
                    child.setCheckState(2, QtCore.Qt.Unchecked)
                    self.ui.treeWidget.setItemWidget(child, 1, child._widget)
                else:
                    child.setText(1, "UDF")

        self.ui.treeWidget.expandAll()


    def pvRefresh(self):
        iLog.info("enter")

        self.iocChange()
        self.pvPopulate()

        if len(self.iocName) == 0:
            iLog.error("Invalid iocName argument length")
            return

        iLog.info("self.iocName=%s" % self.iocName)

        for x in range(0, self.ui.treeWidget.topLevelItemCount()):
            item = self.ui.treeWidget.topLevelItem(x)
            for xx in range(0, item.childCount()):
                child = item.child(xx)

                ioc = self.iocs[self.iocName]
                pvName = str(child.text(3))
                pv = ioc.pv(pvName)

                child.connectPVObj(pv)

                iLog.debug("Handing over PV '%s' to handler" % pv.nameGetFull())
                pv.scheduleGet()

    def pvApply(self):
        iLog.info("enter")

        if len(self.iocName) == 0:
            iLog.error("Invalid iocName argument length")
            return

        iLog.info("self.iocName=%s" % self.iocName)

        for x in range(0, self.ui.treeWidget.topLevelItemCount()):
            item = self.ui.treeWidget.topLevelItem(x)
            for xx in range(0, item.childCount()):
                child = item.child(xx)

                ioc = self.iocs[self.iocName]
                pvName = str(child.text(3))
                pv = ioc.pv(pvName)

                if child.checkState(2) != QtCore.Qt.Checked:
                    continue

                pv.userValue = child.iValueGet()

                child.connectPVObj(pv)

                iLog.debug("Handing over PV '%s' to handler" % pv.namePutFull())
                pv.schedulePut()

                child.setCheckState(2, QtCore.Qt.Unchecked)
