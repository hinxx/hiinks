'''
Created on Jun 7, 2011

@author: hinko
'''

#===============================================================================
# COMMENTS
#===============================================================================
#
#===============================================================================

from iGLobals import iRaise, iLog, iGlobalPVs, iGlobalIOCs, iGlobalHandle

from PyQt4 import QtCore, QtGui

from ui.uiPanelTest import Ui_PanelTest
from lib.iWidgets import iQTableWidgetItem, iQLabel

class iPanelTest(QtGui.QWidget):

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        iLog.debug("enter")

        self.pvMonitors = dict()
        self.iocName = None
        self.pvName = None
        self.pvs = iGlobalPVs()
        self.iocs = iGlobalIOCs()

        self.pvHandler = iGlobalHandle()

        self.ui = Ui_PanelTest()
        self.ui.setupUi(self)

        self.ui.pushButton_get.clicked.connect(self.pvGet)
        self.ui.pushButton_put.clicked.connect(self.pvPut)
        self.ui.pushButton_monitor.clicked.connect(self.pvMonitor)
        self.ui.tableWidget.itemClicked.connect(self.pvUnmonitor)
        self.ui.lineEdit_iocName.textChanged.connect(self.iocTextChanged)
        self.ui.lineEdit_pvName.textChanged.connect(self.pvTextChanged)
        self.connect(self.ui.comboBox_iocName, QtCore.SIGNAL('activated(QString)'), self.iocComboChanged)
        self.connect(self.ui.comboBox_pvName, QtCore.SIGNAL('activated(QString)'), self.pvComboChanged)

        iocName = str(self.ui.lineEdit_iocName.text())
        pvName = str(self.ui.lineEdit_pvName.text())

        self.ui.comboBox_iocName.addItem('-- unknown --')
        self.ui.comboBox_iocName.addItems([ioc for ioc in self.iocs['__myid__']])
        self.ui.comboBox_pvName.addItem('-- unknown --')
        self.ui.comboBox_pvName.addItems([pv for pv in self.pvs['__myid__']])
        self.iocTextChanged(iocName)
        self.pvTextChanged(pvName)

    def show(self):
        iLog.debug("enter")

    def hide(self):
        iLog.debug("enter")


    def iocComboChanged(self, txt):
        iLog.debug("enter")
        iLog.debug("New IOC text '%s'" % (txt))
        self.ui.lineEdit_iocName.setText(txt)

    def pvComboChanged(self, txt):
        iLog.debug("enter")
        iLog.debug("New PV text '%s'" % (txt))
        self.ui.lineEdit_pvName.setText(txt)

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

    def pvGet(self):
        iLog.debug("enter")

        iocName = str(self.ui.lineEdit_iocName.text())
        pvName = str(self.ui.lineEdit_pvName.text())

        if len(iocName) == 0:
            iLog.error("Invalid iocName argument length")
            return

        if len(pvName) == 0:
            iLog.error("Invalid pvName argument length")
            return

        self.iocName = iocName
        self.pvName = pvName
        iLog.debug("self.iocName=%s, self.pvName=%s" % (self.iocName, self.pvName))

        ioc = self.iocs[self.iocName]
        pv = ioc.pv(self.pvName)
        pv.connectOneShotSignal(self.ui.label_pvValue.slotOneShot)

        self.ui.label_pvName.setText("%s" % (pv.nameGetFull()))

        iLog.debug("Handing over PV '%s' to handler" % pv.nameGetFull())
        pv.scheduleGet()

    def pvPut(self):
        iLog.debug("enter")

        iocName = str(self.ui.lineEdit_iocName.text())
        pvName = str(self.ui.lineEdit_pvName.text())
        pvValue = str(self.ui.lineEdit_pvValue.text())

        if len(iocName) == 0 or len(pvName) == 0:
            iLog.warning("Skipping due to missing iocName=%s and/or pvName=%s" % (iocName, pvName))
            return
        if len(pvValue) == 0:
            iLog.warning("Skipping due to missing pvValue=%s" % (pvValue))
            return

        self.iocName = iocName
        self.pvName = pvName
        iLog.debug("self.pvName=%s, pvValue=%s" % (self.pvName, pvValue))

        ioc = self.iocs[self.iocName]
        pv = ioc.pv(self.pvName)
        pv.userValue = pvValue

        self.ui.label_pvName.setText("PV %s" % (pv.nameGetFull()))

        iLog.debug("Handing over PV '%s' to handler" % pv.namePutFull())
        pv.schedulePut()

    def pvMonitor(self):
        iLog.debug("enter")

        iocName = str(self.ui.lineEdit_iocName.text())
        pvName = str(self.ui.lineEdit_pvName.text())

        if len(iocName) == 0:
            iLog.error("Invalid iocName argument length")
            return

        if len(pvName) == 0:
            iLog.error("Invalid pvName argument length")
            return

        iLog.debug("iocName=%s, pvName=%s" % (iocName, pvName))

        ioc = self.iocs[iocName]
        pv = ioc.pv(pvName)

        row = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.setRowCount(row + 1)

        item = QtGui.QTableWidgetItem(pv.iocName)
        self.ui.tableWidget.setItem(row, 0, item)

        item = QtGui.QTableWidgetItem(pv.nameGetSuffix())
        self.ui.tableWidget.setItem(row, 1, item)

        item = iQTableWidgetItem('')
        self.ui.tableWidget.setCellWidget(row, 2, item._widget)
        pv.connectPeriodicSignal(item.slotPeriodic)
        self.ui.tableWidget.setItem(row, 2, item)

        item = QtGui.QTableWidgetItem("UDF")
        item.setCheckState(QtCore.Qt.Checked)
        self.ui.tableWidget.setItem(row, 3, item)

        self.ui.tableWidget.resizeColumnToContents(0)

        iLog.debug("Handing over MONITOR to pvHandler, PV %s" % pv.nameGetFull())

        pv.scheduleMonitor(True)

    def pvUnmonitor(self, item):
        iLog.debug("enter")
        iLog.info("clicked on item: %s" % (item.text()))

        if item.column() != 3:
            return

        if item.checkState() != QtCore.Qt.Checked:
            row = item.row()

            iocItem = self.ui.tableWidget.item(row, 0)
            pvItem = self.ui.tableWidget.item(row, 1)
            valueItem = self.ui.tableWidget.item(row, 2)

            ioc = self.iocs[str(iocItem.text())]
            pv = ioc.pv(str(pvItem.text()))
            pv.disconnectPeriodicSignal(valueItem.slotPeriodic)

            self.ui.tableWidget.removeRow(row)
            self.ui.tableWidget.resizeColumnToContents(0)

            iLog.info("removing monitor PV %s" % (pv.nameGetFull()))
