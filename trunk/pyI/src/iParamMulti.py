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
from ui.uiParamMulti import Ui_ParamMulti

class iParamMulti(QtGui.QWidget):
    def __init__(self, parent, caAccess):
        QtGui.QWidget.__init__(self, parent)
        iLog.debug("enter")

        self.pvName = None
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

        self.ui = Ui_ParamMulti()
        self.ui.setupUi(self)

        QtCore.QObject.connect(self.ui.pushButton_apply,
                               QtCore.SIGNAL("clicked()"), self.doPVApply)
        QtCore.QObject.connect(self.ui.pushButton_refresh,
                               QtCore.SIGNAL("clicked()"), self.doPVRefresh)
        QtCore.QObject.connect(self.ui.pushButton_changePV,
                               QtCore.SIGNAL("clicked()"), self.doChangePV)

        self.doChangePV()
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

    def doChangePV(self):
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

        self.populate()
        self.changeItemWidget()
        self.doPVRefresh()

    def doPVRefresh(self):
        iLog.debug("enter")

        pvList = []

        for pvName, pvItem, iocObj, pvObj in self.itemList:
            fullName = iocObj.name + pvGetName(pvObj)
            if pvIsModeValue(pvObj):
                iLog.debug("pvName=%s" % fullName)
                o = (fullName, None)
                pvList.append(o)

        self.caAccess.get(pvList)

    def doPVApply(self):
        iLog.debug("enter")

        pvList = []

        for pvName, pvItem, iocObj, pvObj in self.itemList:
            if not pvItem.checkState(3) == QtCore.Qt.Checked:
                continue

            widget = self.ui.treeWidget.itemWidget(pvItem, 2)
            pvValue = None
            if isinstance(widget, QtGui.QLineEdit):
                pvValue = str(widget.text())
            elif isinstance(widget, QtGui.QComboBox):
                pvValue = widget.currentIndex()

            fullName = None
            if pvIsModeValue(pvObj):
                fullName = iocObj.name + pvPutName(pvObj)
            else:
                raise ValueError, 'iParamMulti.doPVApply: invalid iPV mode:', pvObj.mode

            iLog.debug("pvName=%s, pvValue=%s" % (fullName, pvValue))

            o = (fullName, pvValue)
            pvList.append(o)
            pvItem.setCheckState(3, False)

        self.caWork = self.caAccess.put(pvList)

#===============================================================================
# CA callback slots
#===============================================================================

    @QtCore.pyqtSlot('QObject*')
    def caGetSlot(self, caJob):
        iLog.debug("enter")

        for pvName, pvItem, iocObj, pvObj in self.itemList:
            fullName = iocObj.name + pvGetName(pvObj)

            if not pvIsModeValue(pvObj):
                continue

            if fullName == caJob.pvName:
                widget = self.ui.treeWidget.itemWidget(pvItem, 2)
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

            for pvName, pvItem, iocObj, pvObj in self.itemList:
                fullName = iocObj.name + pvPutName(pvObj)

                if not pvIsModeValue(pvObj):
                    continue

                if not fullName == caJob.pvName:
                    continue

                iLog.debug("doing GET for PUT, %s => %s" % (fullName, iocObj.name + pvGetName(pvObj)))
                fullName = iocObj.name + pvGetName(pvObj)
                o = (fullName, None)
                pvList.append(o)

        self.caAccess.get(pvList)
        self.caWork = None

#===============================================================================
# Tree items
#===============================================================================
    def addItems(self):
        iLog.debug("enter")

        pvObj = pvListFind(self.pvList, name = self.pvName)
        if not pvObj:
            return

        for iocObj in self.iocList:
            fullName = iocObj.name + pvObj.name
            item = QtGui.QTreeWidgetItem([iocObj.name, pvObj.name])
            self.ui.treeWidget.addTopLevelItem(item)

            self.itemList.append((fullName, item, iocObj, pvObj))

    def changeItemWidget(self):
        iLog.debug("enter")

        pvObjNew = pvListFind(self.pvList, name = self.pvName)
        if not pvObjNew:
            return

        itemList = []
        for pvName, pvItem, iocObj, pvObj in self.itemList:

            fullName = iocObj.name + pvPutName(pvObjNew)
            pvItem.setText(1, pvObjNew.name)

            check = False
            if pvObjNew.widget == 'QLabel':
                widget = QtGui.QLabel()
                if pvObjNew.strings:
                    widget.setText(pvObjNew.strings[0])
                else:
                    widget.setText("UDF")
            elif pvObjNew.widget == 'QLineEdit':
                widget = QtGui.QLineEdit()
                widget.setText("UDF")
                check = True
            elif pvObjNew.widget == "QComboBox":
                widget = QtGui.QComboBox()
                widget.addItems(pvObjNew.strings)
                check = True
            else:
                pvItem.setText(2, "UDF")

            if check:
                pvItem.setFlags(pvItem.flags() | QtCore.Qt.ItemIsUserCheckable)
                pvItem.setCheckState(3, False)
            else:
                pvItem.setFlags(pvItem.flags() & ~QtCore.Qt.ItemIsUserCheckable)
                pvItem.setData(3, QtCore.Qt.CheckStateRole, QtCore.QVariant());

            if pvObjNew.widget:
                self.ui.treeWidget.setItemWidget(pvItem, 2, widget)

            iLog.debug("new pvName=%s" % pvObjNew.name)

            itemList.append((fullName, pvItem, iocObj, pvObjNew))

        self.itemList = itemList


    def batchDummy(self):
        iLog.debug("enter")

        pvObj = pvListFind(self.pvList, name = self.pvName)
        if not pvObj:
            return

        if len(self.itemList) != 0:
            return

        self.addItems()

