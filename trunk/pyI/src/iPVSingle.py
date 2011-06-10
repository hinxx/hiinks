'''
Created on Jun 7, 2011

@author: hinko
'''

from PyQt4 import QtCore, QtGui
from ui.uiPVSingle import Ui_PVSingle

class iPVSingle(QtGui.QWidget):

    def __init__(self, parent, caAccess):
        QtGui.QWidget.__init__(self, parent)
        print "iPVSingle.init:"

        self.pvMonitors = dict()

        self.caAccess = caAccess
        QtCore.QObject.connect(self.caAccess,
                               QtCore.SIGNAL("sigGet(QObject*)"), self.caGetSlot)
        QtCore.QObject.connect(self.caAccess,
                               QtCore.SIGNAL("sigPut(QObject*)"), self.caPutSlot)
        QtCore.QObject.connect(self.caAccess,
                               QtCore.SIGNAL("sigMonitor(QObject*)"), self.caMonitorSlot)

        #self.ui = uic.loadUi('ui/uiPVSingle.ui', self)
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

    def show(self):
        print "iPVSingle.show:"

    def hide(self):
        print "iPVSingle.hide:"

    def pvGet(self):
        iocName = str(self.ui.lineEdit_iocName.text())
        pvName = str(self.ui.lineEdit_pvName.text())

        if len(iocName) == 0 or len(pvName) == 0:
            return

        print "iPVSingle.pvGet: IOC=", iocName, ", PV=", pvName
        fullName = iocName + pvName
        o = (fullName, None)
        self.caAccess.get([o])

    def pvPut(self):
        iocName = str(self.ui.lineEdit_iocName.text())
        pvName = str(self.ui.lineEdit_pvName.text())
        pvValue = str(self.ui.lineEdit_pvValueWrite.text())

        if len(iocName) == 0 or len(pvName) == 0:
            return

        print "iPVSingle.pvPut: IOC=", iocName, ", PV=", pvName, ", value=", pvValue
        fullName = iocName + pvName
        o = (fullName, pvValue)
        self.caAccess.put([o])

    def pvMonitor(self):
        print "iPVSingle.pvMonitor:"

        iocName = str(self.ui.lineEdit_iocName.text())
        pvName = str(self.ui.lineEdit_pvName.text())

        if len(iocName) == 0 or len(pvName) == 0:
            return

        print "iPVSingle.pvMonitor: IOC=", iocName, ", PV=", pvName
        fullName = iocName + pvName

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

        self.ui.tableWidget.resizeColumnToContents(0)

        print "iPVSingle.pvMonitor: Start monitoring PV=", fullName
        o = (fullName, None)
        self.pvMonitors[fullName] = self.caAccess.monitor([o])

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
                self.caAccess.monitorStop(pv)
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
    def caGetSlot(self, caJob):
        print "iPVSingle.caGetSlot: iPV=", caJob.pvName, ", value=", caJob.pvGetValue
        iocName = str(self.ui.lineEdit_iocName.text())
        pvName = str(self.ui.lineEdit_pvName.text())
        fullName = iocName + pvName
        if fullName == caJob.pvName:
            self.ui.label_pvValueRead.setText(str(caJob.pvGetValue))

            print "iPVSingle.caGetSlot: iPV=", caJob.pvName, ", connected=", caJob.connected
            if caJob.connected:
                self.ui.label_pvConnected.setText(str("True"))
            else:
                self.ui.label_pvConnected.setText(str("False"))

    @QtCore.pyqtSlot('QObject*')
    def caPutSlot(self, caJob):
        print "iPVSingle.caPutSlot: iPV=", caJob.pvName, ", value=", caJob.pvGetValue
        iocName = str(self.ui.lineEdit_iocName.text())
        pvName = str(self.ui.lineEdit_pvName.text())
        fullName = iocName + pvName
        if fullName == caJob.pvName:
            self.ui.label_pvValueRead.setText(str(caJob.pvGetValue))

            print "iPVSingle.caPutSlot: iPV=", caJob.pvName, ", connected=", caJob.connected
            if caJob.connected:
                self.ui.label_pvConnected.setText(str("True"))
            else:
                self.ui.label_pvConnected.setText(str("False"))

    @QtCore.pyqtSlot('QObject*')
    def caMonitorSlot(self, caJob):
        print "iPVSingle.caMonitorSlot: PV=", caJob.pvName, ", value=", caJob.pvGetValue
        if not caJob.pvName in self.pvMonitors:
            return

        for nameItem in self.ui.tableWidget.findItems(caJob.pvName, QtCore.Qt.MatchExactly):
            item = self.ui.tableWidget.item(nameItem.row(), nameItem.column() + 1)
            item.setText(str(caJob.pvGetValue))
            item = self.ui.tableWidget.item(nameItem.row(), nameItem.column() + 2)
            item.setText(str(caJob.connected))
