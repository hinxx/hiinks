'''
Created on Jun 3, 2011

@author: hinko
'''

from PyQt4 import QtCore, QtGui
from lib.iHelper import *
from ui.uiParamSingle import Ui_ParamSingle

class iParamSingle(QtGui.QWidget):

    def __init__(self, parent, caAccess):
        QtGui.QWidget.__init__(self, parent)
        print "iParamSingle.init:"

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
        print "iParamSingle.show:"

    def hide(self):
        print "iParamSingle.hide:"

    def close(self):
        print "iParamSingle.close:"

    def populate(self):
        print "iParamSingle.populate:"

        self.batchDummy()

        # Some tree widgets properties
        self.ui.treeWidget.setColumnWidth(0, 180)
        self.ui.treeWidget.setColumnWidth(1, 120)
        self.ui.treeWidget.setColumnWidth(2, 100)
        self.ui.treeWidget.setFocusPolicy(QtCore.Qt.NoFocus)

    def doChangeIOC(self):
        print "iParamSingle.doChangeIOC: current iocName=", self.iocName
        iocName = str(self.ui.lineEdit_iocName.text())
        print "iParamSingle.doChangeIOC: have iocName=", iocName

        if not len(iocName):
            print "iParamSingle.doChangeIOC: invalid have iocName=", iocName
            return

        if self.iocName == iocName:
            print "iParamSingle.doChangeIOC: already showing iocName=", iocName
            return

        self.iocName = iocName

        print "iParamSingle.doChangeIOC: new iocName=", self.iocName

        self.doPVRefresh()

    def doPVRefresh(self):
        print "iParamSingle.doPVRefresh:"
        pvList = []

        for pvName, pvItem, pvObj in self.itemList:
            fullName = self.iocName + pvGetName(pvObj)
            if pvIsModeValue(pvObj):
                print "iParamSingle.doPVRefresh: PV name=", fullName
                o = (fullName, None)
                pvList.append(o)

        self.caAccess.get(pvList)

    def doPVApply(self):
        print "iParamSingle.doPVApply:"
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

            print "iParamSingle.doPVApply: PV name=", fullName, "=", pvValue

            o = (fullName, pvValue)
            pvList.append(o)
            pvItem.setCheckState(2, False)

        self.caWork = self.caAccess.put(pvList)

#===============================================================================
# CA callback slots
#===============================================================================

    @QtCore.pyqtSlot('QObject*')
    def caGetSlot(self, caJob):
        print "iParamSingle.caGetSlot: iPV=", caJob.pvName, ", value=", caJob.pvGetValue

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

                print "iParamSingle.caGetSlot: PV name=", pvName, "=", caJob.pvGetValue

    @QtCore.pyqtSlot('QObject*')
    def caPutSlot(self, caJob):
        print "iParamSingle.caPutSlot: iPV=", caJob.pvName, ", value=", caJob.pvGetValue

    @QtCore.pyqtSlot('QObject*')
    def caMonitorSlot(self, caJob):
        print "iParamSingle.caMonitorSlot: PV=", caJob.pvName, ", value=", caJob.pvGetValue

    @QtCore.pyqtSlot('QObject*')
    def caWorkDoneSlot(self, caWork):
        print "iParamSingle.caWorkDoneSlot: caWork=", caWork
        if not caWork == self.caWork:
            print "iParamSingle.caWorkDoneSlot: not our work self.caWork=", self.caWork
            return

        pvList = []
        for caJob, caResult in caWork.res:
            print "iParamSingle.caWorkDoneSlot: PV=", caJob.pvName, "=", caJob.pvGetValue, "SUCCESS=", caJob.success

            for pvName, pvItem, pvObj in self.itemList:
                fullName = self.iocName + pvPutName(pvObj)

                if not pvIsModeValue(pvObj):
                    continue

                if not fullName == caJob.pvName:
                    continue

                print "iParamSingle.caWorkDoneSlot: GET after PUT for PV=", fullName
                fullName = self.iocName + pvGetName(pvObj)
                o = (fullName, None)
                pvList.append(o)

        self.caAccess.get(pvList)
        self.caWork = None

#===============================================================================
# Tree items
#===============================================================================
    def addItems(self, group, parent):
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
                for v, s in pvObj.enums:
                    l.append(s)
                widget.addItems(l)
                pvItem.setCheckState(2, False)
            else:
                pvItem.setText(1, "UDF")

            if pvObj.widget:
                self.ui.treeWidget.setItemWidget(pvItem, 1, widget)

            self.itemList.append((fullName, pvItem, pvObj))


    def batchDummy(self):

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

