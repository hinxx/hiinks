'''
Created on Jun 7, 2011

@author: hinko
'''

#===============================================================================
# COMMENTS
#===============================================================================
# TODO: provide combo boxes for known iocs and pvs, along with lineedit input 
#===============================================================================

from iGLobals import iRaise, iLog, iGlobalHandle, iGlobalPVs, iGlobalIOCs

from PyQt4 import QtCore, QtGui

from ui.uiPanelMultiIOCParam import Ui_PanelMultiIOCParam
from lib.iWidgets import iQTreeWidgetItem

class iPanelMultiIOCParam(QtGui.QWidget):

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        iLog.debug("enter")

        self.iocName = None
        self.pvName = None

        self.pvs = iGlobalPVs()
        self.iocs = iGlobalIOCs()

        self.ui = Ui_PanelMultiIOCParam()
        self.ui.setupUi(self)

        self.ui.pushButton_apply.clicked.connect(self.pvApply)
        self.ui.pushButton_refresh.clicked.connect(self.pvRefresh)
        self.ui.lineEdit_pvName.textChanged.connect(self.pvTextChanged)
        self.connect(self.ui.comboBox_pvName, QtCore.SIGNAL('activated(QString)'), self.pvComboChanged)

        pvName = str(self.ui.lineEdit_pvName.text())

        self.ui.comboBox_pvName.addItem('-- unknown --')
        self.ui.comboBox_pvName.addItems(self.pvs['__myid__'])

        self.pvTextChanged(pvName)

    def show(self):
        iLog.debug("enter")

    def hide(self):
        iLog.debug("enter")

    def close(self):
        iLog.debug("enter")

    def pvComboChanged(self, txt):
        iLog.debug("enter")
        iLog.debug("New PV text '%s'" % (txt))
        self.ui.lineEdit_pvName.setText(txt)

    def pvTextChanged(self, txt):
        iLog.debug("enter")
        iLog.debug("New PV text '%s'" % (txt))

        for x in range(1, self.ui.comboBox_pvName.count()):
            comboTxt = str(self.ui.comboBox_pvName.itemText(x))
            if comboTxt.startswith(txt):
                iLog.info("Selecting PV combo '%s' -> '%s'," % (txt, comboTxt))
                self.ui.comboBox_pvName.setCurrentIndex(x)
                return

        self.ui.comboBox_pvName.setCurrentIndex(0)

    def pvChange(self):
        iLog.debug("enter")

        iLog.debug("current pvName=%s" % self.pvName)
        pvName = str(self.ui.lineEdit_pvName.text())
        iLog.debug("have pvName=%s" % pvName)

        if not len(pvName):
            iLog.error("invalid/empty pvName=%s" % pvName)
            return

        if self.pvName == pvName:
            iLog.debug("already showing pvName=%s" % pvName)
            return

        self.pvName = pvName

        iLog.debug("new pvName=%s" % self.pvName)

    def pvPopulate(self):
        iLog.info("enter")

        if self.ui.treeWidget.topLevelItemCount() != 0:
            iLog.warning("Tree widget is already populated")
            return

        for iocName in self.iocs['__myid__']:
            ioc = self.iocs[iocName]
            iLog.info("iocName=%s, ioc=%s" % (iocName, ioc))

            pv = ioc.pv(self.pvName)

            item = iQTreeWidgetItem([iocName, pv.text], pv.widget)
            item.setText(4, pv.name)
            self.ui.treeWidget.addTopLevelItem(item)
            if pv.widget:
                item.setCheckState(3, QtCore.Qt.Unchecked)
                self.ui.treeWidget.setItemWidget(item, 2, item._widget)
            else:
                item.setText(2, "UDF")

    def pvRefresh(self):
        iLog.info("enter")

        self.pvChange()
        self.pvPopulate()

        if len(self.pvName) == 0:
            iLog.error("Invalid iocName argument length")
            return

        iLog.info("self.pvName=%s" % self.pvName)

        for x in range(0, self.ui.treeWidget.topLevelItemCount()):
            item = self.ui.treeWidget.topLevelItem(x)

            ioc = self.iocs[str(item.text(0))]
            pv = ioc.pv(self.pvName)

            item.connectPVObj(pv)

            iLog.debug("Handing over PV '%s' to handler" % pv.nameGetFull())
            pv.scheduleGet()

    def pvApply(self):
        iLog.info("enter")

        if len(self.pvName) == 0:
            iLog.error("Invalid pvName argument length")
            return

        iLog.info("self.pvName=%s" % self.pvName)

        for x in range(0, self.ui.treeWidget.topLevelItemCount()):
            item = self.ui.treeWidget.topLevelItem(x)

            ioc = self.iocs[str(item.text(0))]
            pv = ioc.pv(self.pvName)

            if item.checkState(3) != QtCore.Qt.Checked:
                continue

            pv.userValue = item.iValueGet()

            item.connectPVObj(pv)

            iLog.debug("Handing over PV '%s' to handler" % pv.namePutFull())
            pv.schedulePut()

            item.setCheckState(3, QtCore.Qt.Unchecked)
