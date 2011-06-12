'''
Created on Jun 7, 2011

@author: hinko
'''

#===============================================================================
# COMMENTS
#===============================================================================
# TODO: provide combo boxes for known iocs and pvs, along with lineedit input 
#===============================================================================

from lib.iConf import iLog
from lib.iPVTree import iPVTree
from lib.iIOCTree import iIOCTree

from PyQt4 import QtCore, QtGui
from ui.uiPVSingle import Ui_PVSingle
from lib.iCAWork import caActionMonitor

class iPVSingle(QtGui.QWidget):

    def __init__(self, parent, caAccess):
        QtGui.QWidget.__init__(self, parent)
        iLog.debug("enter")

        self.pvMonitors = dict()
        self.pvName = None

        self.caAccess = caAccess
        self.caAccess.sigGet.connect(self.caGetSlot)
        self.caAccess.sigPut.connect(self.caPutSlot)
        self.caAccess.sigMonitor.connect(self.caMonitorSlot)
        self.caAccess.sigConnected.connect(self.caConnectedSlot)
        self.caAccess.sigDone.connect(self.caDoneSlot)

        self.ui = Ui_PVSingle()
        self.ui.setupUi(self)

        self.ui.pushButton_get.clicked.connect(self.pvGet)
        self.ui.pushButton_put.clicked.connect(self.pvPut)
        self.ui.pushButton_monitor.clicked.connect(self.pvMonitor)
        self.ui.pushButton_unmonitor.clicked.connect(self.pvUnmonitor)
        self.ui.tableWidget.itemSelectionChanged.connect(self.tableSelect)
        self.ui.pushButton_unmonitor.setDisabled(True)

        iocName = str(self.ui.lineEdit_iocName.text())
        pvName = str(self.ui.lineEdit_pvName.text())
        if len(iocName) and len(pvName):
            self.pvName = iocName + pvName
            self.ui.label_pvName.setText("PV %s : " % (self.pvName))

    def show(self):
        iLog.debug("enter")

    def hide(self):
        iLog.debug("enter")

    def pvGet(self):
        iLog.debug("enter")

        iocName = str(self.ui.lineEdit_iocName.text())
        pvName = str(self.ui.lineEdit_pvName.text())

        if len(iocName) == 0 or len(pvName) == 0:
            return

        self.pvName = iocName + pvName
        self.ui.label_pvName.setText("PV %s : " % (self.pvName))
        iLog.debug("pvName=%s" % self.pvName)

        self.caAccess.get([self.pvName])

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

        self.pvName = iocName + pvName
        self.ui.label_pvName.setText("PV %s " % (self.pvName))
        iLog.debug("pvName=%s, pvValue=%s" % (self.pvName, pvValue))

        # NOTE: Tuple is the argument here!
        self.caAccess.put([(self.pvName, pvValue)])

    def pvMonitor(self):
        iLog.debug("enter")

        iocName = str(self.ui.lineEdit_iocName.text())
        pvName = str(self.ui.lineEdit_pvName.text())

        if len(iocName) == 0 or len(pvName) == 0:
            return

        fullName = iocName + pvName

        if fullName in self.pvMonitors:
            iLog.warning("iocName=%s, pvName=%s is already monitored!" % (iocName, pvName))
            return

        row = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.setRowCount(row + 1)
        item = QtGui.QTableWidgetItem(fullName)
        self.ui.tableWidget.setItem(row, 0, item)
        item = QtGui.QTableWidgetItem("UDF")
        self.ui.tableWidget.setItem(row, 1, item)
        item = QtGui.QTableWidgetItem("UDF")
        self.ui.tableWidget.setItem(row, 2, item)

        self.ui.tableWidget.resizeColumnToContents(0)

        iLog.debug("pvName=%s" % fullName)

        self.pvMonitors[fullName] = self.caAccess.monitor([fullName])

    def pvUnmonitor(self):
        iLog.debug("enter")

        rows = []
        for item in self.ui.tableWidget.selectedItems():
            if item.column() != 0:
                continue

            pvName = str(item.text())
            if pvName in self.pvMonitors:
                iLog.debug("Removing monitor for pvName=%s" % pvName)

                seqId = self.pvMonitors[pvName]
                self.caAccess.monitorStop(seqId, pvName)
                del self.pvMonitors[pvName]

                rows.append(item.row())

        rows.reverse()
        for row in rows:
            self.ui.tableWidget.removeRow(row)
            self.ui.tableWidget.resizeColumnToContents(0)

    def tableSelect(self):
        iLog.debug("enter")

        if self.ui.tableWidget.selectedItems():
            self.ui.pushButton_unmonitor.setEnabled(True)
        else:
            self.ui.pushButton_unmonitor.setDisabled(True)

#===============================================================================
# CA callback slots
#===============================================================================

    @QtCore.pyqtSlot(dict)
    def caGetSlot(self, pvData):
        iLog.info("enter")
        iLog.info("Called for pvName=%s, pvValue=%s, pvConnected=%s" % (pvData['name'], pvData['value'], pvData['connected']))

        if self.pvName == pvData['name']:
            iLog.info("pvName=%s, value=%s, success=%s" % (pvData['name'], pvData['value'], pvData['success']))

            self.ui.label_pvValue.setText("%s" % (str(pvData['value'])))

            if pvData['connected']:
                self.ui.label_pvConnected.setText("(connected)")
            else:
                self.ui.label_pvConnected.setText("(UN-CONNECTED)")

    @QtCore.pyqtSlot(dict)
    def caPutSlot(self, pvData):
        iLog.info("enter")
        iLog.info("Called for pvName=%s, pvValue=%s, pvConnected=%s" % (pvData['name'], pvData['value'], pvData['connected']))

        if self.pvName == pvData['name']:
            iLog.debug("pvName=%s, value=%s, success=%s" % (pvData['name'], pvData['value'], pvData['success']))

            self.ui.label_pvValue.setText("%s" % (str(pvData['value'])))

            if pvData['connected']:
                self.ui.label_pvConnected.setText("(connected)")
            else:
                self.ui.label_pvConnected.setText("(UN-CONNECTED)")

    @QtCore.pyqtSlot(dict)
    def caMonitorSlot(self, pvData):
        iLog.info("enter")
        iLog.info("Called for pvName=%s, pvValue=%s, pvConnected=%s" % (pvData['name'], pvData['value'], pvData['connected']))

        if not pvData['name'] in self.pvMonitors:
            iLog.warning("No monitor for pvName=%s, pvValue=%s, pvConnected=%s" % (pvData['name'], pvData['value'], pvData['connected']))
            return

        iLog.debug("pvName=%s, value=%s, success=%s" % (pvData['name'], pvData['value'], pvData['success']))
        for nameItem in self.ui.tableWidget.findItems(pvData['name'], QtCore.Qt.MatchExactly):
            item = self.ui.tableWidget.item(nameItem.row(), nameItem.column() + 1)
            item.setText(str(pvData['value']))
            item = self.ui.tableWidget.item(nameItem.row(), nameItem.column() + 2)
            item.setText(str(pvData['connected']))
            if pvData['connected']:
                item.setText(str(pvData['(connected)']))
            else:
                item.setText(str(pvData['(UN-CONNECTED)']))

    @QtCore.pyqtSlot(dict)
    def caConnectedSlot(self, pvData):
        iLog.info("enter")
        iLog.info("Called for pvName=%s, pvValue=%s, pvConnected=%s" % (pvData['name'], pvData['value'], pvData['connected']))

        if not pvData['connected']:
            self.caGetSlot(pvData)
            self.caMonitorSlot(pvData)

    @QtCore.pyqtSlot(dict)
    def caDoneSlot(self, pvList):
        iLog.info("enter")
        iLog.info("Called for pvList=%s" % (repr(pvList)))
