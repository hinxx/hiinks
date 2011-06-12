'''
Created on Jun 3, 2011

@author: hinko
'''

#===============================================================================
# COMMENTS
#===============================================================================
# TODO: provide select all/none buttons in gui 
#===============================================================================

from lib.iConf import iLog

from PyQt4 import QtCore, QtGui
from lib.iHelper import *
from ui.uiParamSingle import Ui_ParamSingle

class iParamSingle(QtGui.QWidget):

    def __init__(self, parent, caAccess):
        QtGui.QWidget.__init__(self, parent)
        iLog.debug("enter")

        self.iocName = None
        self.pvList = pvList()
        self.iocList = iocList()
        self.itemList = []
        self.caWork = None

        self.caAccess = caAccess
        QtCore.QObject.connect(self.caAccess,
                               QtCore.SIGNAL("sigGet(QObject*)"), self.caGetSlot)
        QtCore.QObject.connect(self.caAccess,
                               QtCore.SIGNAL("sigPut(QObject*)"), self.caPutSlot)
        QtCore.QObject.connect(self.caAccess,
                               QtCore.SIGNAL("sigMonitor(QObject*)"), self.caMonitorSlot)
        QtCore.QObject.connect(self.caAccess,
                               QtCore.SIGNAL("sigDone(QObject*)"), self.caWorkDoneSlot)

        self.ui = Ui_ParamSingle()
        self.ui.setupUi(self)

        QtCore.QObject.connect(self.ui.pushButton_apply,
                               QtCore.SIGNAL("clicked()"), self.doPVApply)
        QtCore.QObject.connect(self.ui.pushButton_refresh,
                               QtCore.SIGNAL("clicked()"), self.doPVRefresh)
        QtCore.QObject.connect(self.ui.pushButton_changeIOC,
                               QtCore.SIGNAL("clicked()"), self.doChangeIOC)

        self.doChangeIOC()
        self.populate()

    def show(self):
        iLog.debug("enter")

    def hide(self):
        iLog.debug("enter")

    def close(self):
        iLog.debug("enter")

    def populate(self):
        iLog.debug("enter")

        self.batchDummy()

        # Some tree widgets properties
        self.ui.treeWidget.setColumnWidth(0, 180)
        self.ui.treeWidget.setColumnWidth(1, 120)
        self.ui.treeWidget.setColumnWidth(2, 100)
        self.ui.treeWidget.setFocusPolicy(QtCore.Qt.NoFocus)

    def doChangeIOC(self):
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

        self.doPVRefresh()

    def doPVRefresh(self):
        iLog.debug("enter")

        pvList = []

        for pvName, pvItem, pvObj in self.itemList:
            fullName = self.iocName + pvGetName(pvObj)
            if pvIsModeValue(pvObj):
                iLog.debug("pvName=%s" % fullName)
                o = (fullName, None)
                pvList.append(o)

        self.caAccess.get(pvList)

    def doPVApply(self):
        iLog.debug("enter")

        pvList = []

        for pvName, pvItem, pvObj in self.itemList:
            if not pvItem.checkState(2) == QtCore.Qt.Checked:
                continue

            widget = self.ui.treeWidget.itemWidget(pvItem, 1)
            pvValue = None
            if isinstance(widget, QtGui.QLineEdit):
                pvValue = str(widget.text())
            elif isinstance(widget, QtGui.QComboBox):
                pvValue = widget.currentIndex()

            fullName = None
            if pvIsModeValue(pvObj):
                fullName = self.iocName + pvPutName(pvObj)
            elif pvIsModeCommand(pvObj):
                pvValue = 1
                fullName = self.iocName + pvCmdName(pvObj)
            else:
                raise ValueError, 'iParamSingle.doPVApply: invalid iPV mode:', pvObj.mode

            iLog.debug("pvName=%s, pvValue=%s" % (fullName, pvValue))

            o = (fullName, pvValue)
            pvList.append(o)
            pvItem.setCheckState(2, False)

        self.caWork = self.caAccess.put(pvList)

#===============================================================================
# CA callback slots
#===============================================================================

    @QtCore.pyqtSlot('QObject*')
    def caGetSlot(self, caJob):
        iLog.debug("enter")

        for pvName, pvItem, pvObj in self.itemList:
            fullName = self.iocName + pvGetName(pvObj)

            if not pvIsModeValue(pvObj):
                continue

            if fullName == caJob.pvName:
                widget = self.ui.treeWidget.itemWidget(pvItem, 1)
                if isinstance(widget, QtGui.QLabel):
                    widget.setText(str(caJob.pvGetValue))
                elif isinstance(widget, QtGui.QLineEdit):
                    widget.setText(str(caJob.pvGetValue))
                elif isinstance(widget, QtGui.QComboBox):
                    widget.setCurrentIndex(caJob.pvGetValue)

                iLog.debug("pvName=%s, value=%s, success=%s" % (caJob.pvName, caJob.pvGetValue, caJob.success))

    @QtCore.pyqtSlot('QObject*')
    def caPutSlot(self, caJob):
        iLog.debug("enter")
        iLog.debug("pvName=%s, value=%s, success=%s" % (caJob.pvName, caJob.pvGetValue, caJob.success))

    @QtCore.pyqtSlot('QObject*')
    def caMonitorSlot(self, caJob):
        iLog.debug("enter")
        iLog.debug("pvName=%s, value=%s, success=%s" % (caJob.pvName, caJob.pvGetValue, caJob.success))

    @QtCore.pyqtSlot('QObject*')
    def caWorkDoneSlot(self, caWork):
        iLog.debug("enter")

        iLog.debug("caWork=%s" % caWork)
        if not caWork == self.caWork:
            iLog.debug("skipping caWork=%s, want self.caWork=%s" % (caWork, self.caWork))
            return

        pvList = []
        for caJob, caResult in caWork.res:
            iLog.debug("pvName=%s, value=%s, success=%s" % (caJob.pvName, caJob.pvGetValue, caJob.success))

            for pvName, pvItem, pvObj in self.itemList:
                fullName = self.iocName + pvPutName(pvObj)

                if not pvIsModeValue(pvObj):
                    continue

                if not fullName == caJob.pvName:
                    continue

                iLog.debug("doing GET for PUT, %s => %s" % (fullName, self.name + pvGetName(pvObj)))
                fullName = self.iocName + pvGetName(pvObj)
                o = (fullName, None)
                pvList.append(o)

        self.caAccess.get(pvList)
        self.caWork = None

#===============================================================================
# Tree items
#===============================================================================
    def addItems(self, group, parent):
        iLog.debug("enter")

        for pvObj in self.pvList:
            if pvObj.group != group:
                continue

            fullName = self.iocName + pvObj.name
            pvItem = QtGui.QTreeWidgetItem([pvObj.text])
            parent.addChild(pvItem)

            if pvObj.widget == 'QLabel':
                widget = QtGui.QLabel()
                if pvObj.strings:
                    widget.setText(pvObj.strings[0])
                    pvItem.setCheckState(2, False)
                else:
                    widget.setText("UDF")
            elif pvObj.widget == 'QLineEdit':
                widget = QtGui.QLineEdit()
                widget.setText("UDF")
                pvItem.setCheckState(2, False)
            elif pvObj.widget == "QComboBox":
                pvObj.dump()
                widget = QtGui.QComboBox()
                l = []
                iLog.info("combo pvName=%s" % pvObj.name)
                for v, s in pvObj.enums:
                    l.append(s)
                widget.addItems(l)
                pvItem.setCheckState(2, False)
            else:
                pvItem.setText(1, "UDF")

            if pvObj.widget:
                self.ui.treeWidget.setItemWidget(pvItem, 1, widget)

            iLog.debug("new pvName=%s" % pvObj.name)

            self.itemList.append((fullName, pvItem, pvObj))


    def batchDummy(self):
        iLog.debug("enter")

        iocObj = pvListFind(self.iocList, name = self.iocName)
        if not iocObj:
            return

        if len(self.itemList) != 0:
            return

        item = QtGui.QTreeWidgetItem(["Dummy"])
        self.ui.treeWidget.addTopLevelItem(item)
        self.addItems('dummy', item)
#
#        item = QtGui.QTreeWidgetItem(["More dummies"])
#        self.ui.treeWidget.addTopLevelItem(item)
#        self.addItems('dummy2', item)

        item = QtGui.QTreeWidgetItem(["Interlock"])
        self.ui.treeWidget.addTopLevelItem(item)
        self.addItems('interlock', item)

