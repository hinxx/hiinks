'''
Created on Jun 7, 2011

@author: hinko
'''

#===============================================================================
# COMMENTS
#===============================================================================
# TODO: provide combo boxes for known iocs and pvs, along with lineedit input 
#===============================================================================

from iHelper import iRaise, iLog, iPVActionValGet, iPVActionValPut, \
    iPVActionMonAdd, iPVActionMonRem

from PyQt4 import QtCore, QtGui

from iPVTree import iPVTree
from iIOCTree import iIOCTree

from ui.uiPanelTest import Ui_PanelTest

class iPanelTest(QtGui.QWidget):

    def __init__(self, parent, pvHandler):
        QtGui.QWidget.__init__(self, parent)
        iLog.debug("enter")

        self.pvMonitors = dict()
        self.iocName = None
        self.pvName = None
        self.pvTree = iPVTree(self)
        self.iocTree = iIOCTree(self)

        self.pvHandler = pvHandler

        self.ui = Ui_PanelTest()
        self.ui.setupUi(self)

        self.ui.pushButton_get.clicked.connect(self.pvGet)
        self.ui.pushButton_put.clicked.connect(self.pvPut)
        self.ui.pushButton_monitor.clicked.connect(self.pvMonitor)
        self.ui.pushButton_unmonitor.clicked.connect(self.pvUnmonitor)
        self.ui.tableWidget.itemSelectionChanged.connect(self.tableSelect)
        self.ui.lineEdit_iocName.textChanged.connect(self.iocTextChanged)
        self.ui.lineEdit_pvName.textChanged.connect(self.pvTextChanged)
        self.connect(self.ui.comboBox_iocName, QtCore.SIGNAL('activated(QString)'), self.iocComboChanged)
        self.connect(self.ui.comboBox_pvName, QtCore.SIGNAL('activated(QString)'), self.pvComboChanged)

        self.ui.pushButton_unmonitor.setDisabled(True)

        iocName = str(self.ui.lineEdit_iocName.text())
        pvName = str(self.ui.lineEdit_pvName.text())

        self.ui.comboBox_iocName.addItem('-- unknown --')
        self.ui.comboBox_iocName.addItems(self.iocTree.mGetAttribute('name'))
        self.ui.comboBox_pvName.addItem('-- unknown --')
        self.ui.comboBox_pvName.addItems(self.pvTree.mGetAttribute('name'))
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

        if len(iocName) == 0 or len(pvName) == 0:
            return

        self.iocName = iocName
        self.pvName = pvName
        iLog.debug("self.pvName=%s" % self.pvName)

        pvGet = iocName + self.pvTree.pvGetName(pvName)
        pvPut = iocName + self.pvTree.pvPutName(pvName)

        self.ui.label_pvMonitorName.setText("GET %s" % (pvGet))
        self.ui.label_pvSPName.setText("PUT %s" % (pvPut))

        iLog.debug("Real PV name %s" % pvGet)
        self.pvHandler.pvJobs.setPVProperty(pvGet, 'slotConnChanged', self.slotConnChanged)
        self.pvHandler.pvJobs.setPVProperty(pvGet, 'slotValueChanged', self.slotValueChanged)
        self.pvHandler.enqeue(iPVActionValGet, [pvGet])

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

        # FIXME: Handle _CMD!
        pvGet = iocName + self.pvTree.pvGetName(pvName)
        pvPut = iocName + self.pvTree.pvPutName(pvName)

        self.ui.label_pvMonitorName.setText("GET %s" % (pvGet))
        self.ui.label_pvSPName.setText("PUT %s" % (pvPut))

        iLog.debug("Real PV name %s" % pvPut)
        self.pvHandler.pvJobs.setPVProperty(pvPut, 'userValue', pvValue)
        self.pvHandler.pvJobs.setPVProperty(pvPut, 'slotConnChanged', self.slotConnChanged)
        self.pvHandler.pvJobs.setPVProperty(pvPut, 'slotValueChanged', self.slotValueChanged)
        self.pvHandler.enqeue(iPVActionValPut, [pvPut])

    def pvMonitor(self):
        iLog.debug("enter")

        iocName = str(self.ui.lineEdit_iocName.text())
        pvName = str(self.ui.lineEdit_pvName.text())

        if len(iocName) == 0 or len(pvName) == 0:
            return

        fullName = iocName + self.pvTree.pvGetName(pvName)

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

        self.pvHandler.pvJobs.setPVProperty(fullName, 'doMonitor', True)
        self.pvHandler.pvJobs.setPVProperty(fullName, 'slotConnChanged', self.slotConnChanged)
        self.pvHandler.pvJobs.setPVProperty(fullName, 'slotValueChanged', self.slotValueChanged)
        self.pvHandler.enqeue(iPVActionMonAdd, [fullName])

    def pvUnmonitor(self):
        iLog.debug("enter")

        rows = []
        for item in self.ui.tableWidget.selectedItems():
            if item.column() != 0:
                continue

            pvName = str(item.text())
            iLog.debug("Removing monitor for pvName=%s" % pvName)

            self.pvHandler.enqeue(iPVActionMonRem, [pvName])
            self.pvHandler.pvJobs.setPVProperty(pvName, 'doMonitor', False)

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

    @QtCore.pyqtSlot('QObject*')
    def slotConnChanged(self, pvObj):
        iLog.debug("enter")
        iLog.debug("Called for pvName=%s, pvValue=%s, pvConnected=%s" %
                   (pvObj.name, pvObj.value, pvObj.connected))

        self.slotValueChanged(pvObj)

    @QtCore.pyqtSlot('QObject*')
    def slotValueChanged(self, pvObj):
        iLog.debug("enter")
        iLog.debug("Called for pvName=%s, pvValue=%s, pvConnected=%s" %
                   (pvObj.name, pvObj.value, pvObj.connected))

        if self.iocName and self.pvName:
            iLog.info("GET/PUT pvName=%s, value=%s, success=%s" % (pvObj.name, pvObj.value, pvObj.connected))

            pvGet = self.iocName + self.pvTree.pvGetName(self.pvName)
            pvPut = self.iocName + self.pvTree.pvPutName(self.pvName)
            if pvObj.name == pvGet:
                self.ui.label_pvMonitorValue.setText("%s" % (str(pvObj.value)))
                if pvObj.connected:
                    self.ui.label_pvMonitorConnected.setText("(connected)")
                else:
                    self.ui.label_pvMonitorConnected.setText("(UN-CONNECTED)")
            elif pvObj.name == pvPut:
                self.ui.label_pvSPValue.setText("%s" % (str(pvObj.value)))
                if pvObj.connected:
                    self.ui.label_pvSPConnected.setText("(connected)")
                else:
                    self.ui.label_pvSPConnected.setText("(UN-CONNECTED)")

        if pvObj.doMonitor:
            iLog.info("MONITOR pvName=%s, value=%s, success=%s" % (pvObj.name, pvObj.value, pvObj.connected))

            for nameItem in self.ui.tableWidget.findItems(pvObj.name, QtCore.Qt.MatchExactly):
                item = self.ui.tableWidget.item(nameItem.row(), nameItem.column() + 1)
                item.setText(str(pvObj.value))
                item = self.ui.tableWidget.item(nameItem.row(), nameItem.column() + 2)
                item.setText(str(pvObj.connected))
                if pvObj.connected:
                    item.setText(str('(connected)'))
                else:
                    item.setText(str('(UN-CONNECTED)'))
