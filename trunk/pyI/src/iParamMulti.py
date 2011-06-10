'''
Created on Jun 3, 2011

@author: hinko
'''

from PyQt4 import QtCore, QtGui
from lib.iHelper import *
from ui.uiParamMulti import Ui_ParamMulti


class iParamMulti(QtGui.QWidget):
    def __init__(self, parent, caAccess):
        QtGui.QWidget.__init__(self, parent)
        print "iParamMulti.init:"

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

        #self.ui = uic.loadUi('ui/uiParamMulti.ui', self)
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
        print "iParamMulti.show:"

    def hide(self):
        print "iParamMulti.hide:"

    def close(self):
        print "iParamMulti.close:"

    def populate(self):
        print "iParamMulti.populate:"

        self.batchDummy()

        # Some tree widgets properties
        self.ui.treeWidget.setColumnWidth(0, 180)
        self.ui.treeWidget.setColumnWidth(1, 120)
        self.ui.treeWidget.setColumnWidth(2, 100)
        self.ui.treeWidget.setFocusPolicy(QtCore.Qt.NoFocus)

    def doChangePV(self):
        print "iParamMulti.doChangePV: current pvName=", self.pvName
        pvName = str(self.ui.lineEdit_pvName.text())
        print "iParamMulti.doChangePV: have pvName=", pvName

        if not len(pvName):
            print "iParamMulti.doChangePV: invalid have pvName=", pvName
            return

        if self.pvName == pvName:
            print "iParamMulti.doChangePV: already showing pvName=", pvName
            return

        self.pvName = pvName

        print "iParamMulti.doChangePV: new pvName=", self.pvName

        self.populate()
        self.changeItemWidget()
        self.doPVRefresh()

    def doPVRefresh(self):
        print "iParamMulti.doPVRefresh:"
        pvList = []
        for x in range(0, self.ui.treeWidget.topLevelItemCount()):
            item = self.ui.treeWidget.topLevelItem(x)
            print "iParamMulti.doPVRefresh: PV item=", item
            for pvName, pvItem, iocObj, pvObj in self.itemList:
                if pvItem == item:

                    if not pvObj:
                        raise ValueError, 'iParamMulti.doPVRefresh: iPV object not found: ' + pvName

                    fullName = iocObj.name + pvGetName(pvObj)
                    if pvIsModeValue(pvObj):
                        print "iParamMulti.doPVRefresh: PV name=", fullName
                        o = (fullName, None)
                        pvList.append(o)

                    break

        self.caAccess.get(pvList)

    def doPVApply(self):
        print "iParamMulti.doPVApply:"
        pvList = []
        for x in range(0, self.ui.treeWidget.topLevelItemCount()):
            item = self.ui.treeWidget.topLevelItem(x)
            if item.checkState(3) == QtCore.Qt.Checked:
                print "iParamMulti.doPVApply: PV item=", item
                for pvName, pvItem, iocObj, pvObj in self.itemList:
                    if pvItem == item:
                        widget = self.ui.treeWidget.itemWidget(pvItem, 2)
                        pvValue = None
                        if isinstance(widget, QtGui.QLineEdit):
                            pvValue = str(widget.text())
                        elif isinstance(widget, QtGui.QComboBox):
                            pvValue = widget.currentIndex()

                        if not pvObj:
                            raise ValueError, 'iParamMulti.doPVApply: iPV object not found:', pvName

                        fullName = None
                        if pvIsModeValue(pvObj):
                            fullName = iocObj.name + pvPutName(pvObj)
#                        elif pvIsModeCommand(pvObj):
#                            pvValue = 1
#                            fullName = iocObj.name + pvCmdName(pvObj)

                        print "iParamMulti.doPVApply: PV name=", fullName, "=", pvValue

                        break

                o = (fullName, pvValue)
                pvList.append(o)
                pvItem.setCheckState(3, False)

        self.caWork = self.caAccess.put(pvList)

#===============================================================================
# CA callback slots
#===============================================================================

    @QtCore.pyqtSlot('QObject*')
    def caGetSlot(self, caJob):
        print "iParamMulti.caGetSlot: iPV=", caJob.pvName, ", value=", caJob.pvGetValue

        for pvName, pvItem, iocObj, pvObj in self.itemList:
            if not pvObj:
                raise ValueError, 'iParamMulti.caGetSlot: iPV object not found: ' + pvName
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

                print "iParamMulti.caGetSlot: PV name=", pvName, "=", caJob.pvGetValue

    @QtCore.pyqtSlot('QObject*')
    def caPutSlot(self, caJob):
        print "iParamMulti.caPutSlot: iPV=", caJob.pvName, ", value=", caJob.pvGetValue

    @QtCore.pyqtSlot('QObject*')
    def caMonitorSlot(self, caJob):
        print "iParamMulti.caMonitorSlot: PV=", caJob.pvName, ", value=", caJob.pvGetValue

    @QtCore.pyqtSlot('QObject*')
    def caWorkDoneSlot(self, caWork):
        print "iParamMulti.caWorkDoneSlot: caWork=", caWork
        if not caWork == self.caWork:
            print "iParamMulti.caWorkDoneSlot: not our work self.caWork=", self.caWork
            return

        pvList = []
        for caJob, caResult in caWork.res:
            print "iParamSingle.caWorkDoneSlot: PV=", caJob.pvName, "=", caJob.pvGetValue, "SUCCESS=", caJob.success

            for pvName, pvItem, iocObj, pvObj in self.itemList:
                if not pvObj:
                    raise ValueError, 'iParamSingle.caWorkDoneSlot: iPV object not found: ' + pvName
                fullName = iocObj.name + pvPutName(pvObj)

                if not pvIsModeValue(pvObj):
                    continue

                if not fullName == caJob.pvName:
                    continue

                print "iParamSingle.caWorkDoneSlot: PUT PV=", fullName
                fullName = iocObj.name + pvGetName(pvObj)
                print "iParamSingle.caWorkDoneSlot: GET PV=", fullName
                o = (fullName, None)
                pvList.append(o)

        self.caAccess.get(pvList)
        self.caWork = None

#===============================================================================
# Tree items
#===============================================================================
    def addTreeTopLevel(self):
        pvObj = pvListFind(self.pvList, pv = self.pvName)
        if not pvObj:
            return

        for iocObj in self.iocList:
            fullName = iocObj.name + pvObj.pv
            item = QtGui.QTreeWidgetItem([iocObj.name, pvObj.name])
            self.ui.treeWidget.addTopLevelItem(item)

            self.itemList.append((fullName, item, iocObj, pvObj))

    def changeItemWidget(self):
        pvObjNew = pvListFind(self.pvList, pv = self.pvName)
        if not pvObjNew:
            return

        itemList = []
        #for x in range(0, self.ui.treeWidget.topLevelItemCount()):
        for pvName, pvItem, iocObj, pvObj in self.itemList:
            #pvItem = self.ui.treeWidget.topLevelItem(x)
            print "iParamSingle.changeItemWidget: PV pvItem=", pvItem

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
                print "uParamSingle.changeItemWidget: PV=", pvObjNew.pv

            itemList.append((fullName, pvItem, iocObj, pvObjNew))

        self.itemList = itemList


    def batchDummy(self):

        pvObj = pvListFind(self.pvList, pv = self.pvName)
        if not pvObj:
            return

        if len(self.itemList) != 0:
            return
#
#        item = QtGui.QTreeWidgetItem(["Dummy"])
#        self.ui.treeWidget.addTopLevelItem(item)
#        self.addTreeChildren(item)
#
#        item = QtGui.QTreeWidgetItem(["More dummies"])
#        self.ui.treeWidget.addTopLevelItem(item)
#        self.addTreeChildren(item)

        #item = QtGui.QTreeWidgetItem(["Parameter"])
        #self.ui.treeWidget.addTopLevelItem(item)
        self.addTreeTopLevel()

