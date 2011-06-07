'''
Created on Jun 7, 2011

@author: hinko
'''
## Add ui path to library
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from PyQt4 import QtCore, QtGui
from ui.uiPVSingle import Ui_PVSingle


class iPVSingle(QtGui.QWidget):
    iocList = None
    pvMonitors = dict()

    def __init__(self, parent = None, iocList = None):
        QtGui.QWidget.__init__(self, parent)
        print "iPVSingle.init:"

        print "iPVSingle.init iocList: ", iocList
        self.iocList = iocList

        self.ui = Ui_PVSingle()
        self.ui.setupUi(self)

        QtCore.QObject.connect(self.ui.pushButton_get,
                               QtCore.SIGNAL("clicked()"), self.pvGet)
        QtCore.QObject.connect(self.ui.pushButton_put,
                               QtCore.SIGNAL("clicked()"), self.pvPut)
        QtCore.QObject.connect(self.ui.pushButton_monitor,
                               QtCore.SIGNAL("clicked()"), self.pvMonitor)
        QtCore.QObject.connect(self.ui.pushButton_unmonitor,
                               QtCore.SIGNAL("clicked()"), self.pvUnmonitor)
        QtCore.QObject.connect(self.ui.tableWidget,
                               QtCore.SIGNAL("itemSelectionChanged()"), self.tableSelect)
        self.ui.pushButton_unmonitor.setDisabled(True)

    def pvGet(self):
        iocName = str(self.ui.lineEdit_iocName.text())
        pvName = str(self.ui.lineEdit_pvName.text())

        iioc = self.iocList.find(iocName)
        print "iPVSingle.pvGet: IOC=", iioc.iocName, ", PV=", pvName

        self.pvConnectSlot(iioc.pvObject(pvName))
        iioc.pvSubscribeConnect(pvName, self.pvConnectSlot)

        iioc.pvGet(pvName, self.pvGetSlot)

    def pvPut(self):
        print "iPVSingle.pvPut:"

        iocName = str(self.ui.lineEdit_iocName.text())
        pvName = str(self.ui.lineEdit_pvName.text())
        pvValue = str(self.ui.lineEdit_pvValueWrite.text())

        iioc = self.iocList.find(iocName)

        iioc.pvPut(pvName, pvValue)

    def pvMonitor(self):
        print "iPVSingle.pvMonitor:"

        iocName = str(self.ui.lineEdit_iocName.text())
        pvName = str(self.ui.lineEdit_pvName.text())

        iioc = self.iocList.find(iocName)

        fullName = iioc.iocName + pvName
        if fullName in self.pvMonitors:
            print "uPVSingle.pvMonitor: Already monitoring PV:", fullName
            return

        row = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.setRowCount(row + 1)
        print "uPVSingle.pvMonitor: rows: ", row
        item = QtGui.QTableWidgetItem(fullName)
        self.ui.tableWidget.setItem(row, 0, item)
        item = QtGui.QTableWidgetItem("UDF")
        self.ui.tableWidget.setItem(row, 1, item)
        item = QtGui.QTableWidgetItem("UDF")
        self.ui.tableWidget.setItem(row, 2, item)
        item = QtGui.QTableWidgetItem("UDF")
        self.ui.tableWidget.setItem(row, 3, item)

#        self.ui.tableWidget.setColumnWidth(0, 180)
        self.ui.tableWidget.resizeColumnToContents(0)

        print "iPVSingle.pvMonitor: Start monitoring PV=", fullName
        #self.pvMonitors[fullName] = iioc.pvMonitorStart(pvName, self.pvMonitorSlot)
        self.pvMonitors[fullName] = iioc.pvObject(pvName)
        iioc.pvMonitorStart(pvName, self.pvMonitorSlot)

    def pvUnmonitor(self):
        print "iPVSingle.pvUnmonitor:"

        rows = []
        for item in self.ui.tableWidget.selectedItems():
            if item.column() != 0:
                continue

            print "uPVSingle.pvUnmonitor: ", item, item.text()
            print "uPVSingle.pvUnmonitor: monitoring: ", repr(self.pvMonitors)

            pvName = str(item.text())
            if pvName in self.pvMonitors:
                print "uPVSingle.pvUnmonitor: removing monitor for:", pvName

                pv = self.pvMonitors[pvName]
                iioc = self.iocList.find(pv.iocName)
                iioc.pvMonitorStop(pv.pvName, self.pvMonitorSlot)
                del self.pvMonitors[pvName]

                rows.append(item.row())

        rows.reverse()
        for row in rows:
            self.ui.tableWidget.removeRow(row)
            self.ui.tableWidget.resizeColumnToContents(0)

    def tableSelect(self):
        if self.ui.tableWidget.selectedItems():
            self.ui.pushButton_unmonitor.setEnabled(True)
        else:
            self.ui.pushButton_unmonitor.setDisabled(True)
#===============================================================================
# CA callback slots
#===============================================================================

    @QtCore.pyqtSlot('QObject*')
    def pvGetSlot(self, iPV):
        print "iPVSingle.pvGetSlot: iPV=", iPV, ", value=", iPV.value
        self.ui.label_pvValueRead.setText(str(iPV.value))

    @QtCore.pyqtSlot('QObject*')
    def pvPutSlot(self, iPV):
        print "iPVSingle.pvPutSlot: iPV=", iPV, ", value=", iPV.value

    @QtCore.pyqtSlot('QObject*')
    def pvMonitorSlot(self, iPV):
        print "iPVSingle.pvMonitorSlot: iPV=", iPV, ", value=", iPV.value
        if not iPV.fullName in self.pvMonitors:
            return

        for nameItem in self.ui.tableWidget.findItems(iPV.fullName, QtCore.Qt.MatchExactly):
            item = self.ui.tableWidget.item(nameItem.row(), nameItem.column() + 1)
            item.setText(str(iPV.value))
            item = self.ui.tableWidget.item(nameItem.row(), nameItem.column() + 2)
            item.setText(str(iPV.isConnected()))

    @QtCore.pyqtSlot('QObject*')
    def pvConnectSlot(self, iPV):
        conn = iPV.isConnected()
        print "iPVSingle.pvConnectSlot: iPV=", iPV, ", connected=", conn
        if conn:
            self.ui.label_pvConnected.setText(str("True"))
        else:
            self.ui.label_pvConnected.setText(str("False"))
