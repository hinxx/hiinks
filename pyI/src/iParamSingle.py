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

        #self.ui = uic.loadUi('ui/uiParamSingle.ui', self)
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
        for x in range(0, self.ui.treeWidget.topLevelItemCount()):
            item = self.ui.treeWidget.topLevelItem(x)
            for c in range(0, item.childCount()):
                child = item.child(c)
                print "iParamSingle.doPVRefresh: PV child=", child
                for pvName, pvChild, pvObj in self.itemList:
                    if pvChild == child:

                        if not pvObj:
                            raise ValueError, 'iParamSingle.doPVRefresh: iPV object not found: ' + pvName

                        fullName = self.iocName + pvGetName(pvObj)
                        if pvIsModeValue(pvObj):
                            print "iParamSingle.doPVRefresh: PV name=", fullName
                            o = (fullName, None)
                            pvList.append(o)

                        break
        self.caAccess.get(pvList)

    def doPVApply(self):
        print "iParamSingle.doPVApply:"
        pvList = []
        for x in range(0, self.ui.treeWidget.topLevelItemCount()):
            item = self.ui.treeWidget.topLevelItem(x)
            for c in range(0, item.childCount()):
                child = item.child(c)
                if child.checkState(2) == QtCore.Qt.Checked:
                    print "iParamSingle.doPVApply: PV child=", child
                    for pvName, pvChild, pvObj in self.itemList:
                        if pvChild == child:
                            widget = self.ui.treeWidget.itemWidget(pvChild, 1)
                            pvValue = None
                            if isinstance(widget, QtGui.QLineEdit):
                                pvValue = str(widget.text())
                            elif isinstance(widget, QtGui.QComboBox):
                                pvValue = widget.currentIndex()

                            if not pvObj:
                                raise ValueError, 'iParamSingle.doPVApply: iPV object not found:', pvName

                            fullName = None
                            if pvIsModeValue(pvObj):
                                fullName = self.iocName + pvPutName(pvObj)
                            elif pvIsModeCommand(pvObj):
                                pvValue = 1
                                fullName = self.iocName + pvCmdName(pvObj)

                            print "iParamSingle.doPVApply: PV name=", fullName, "=", pvValue

                            break

                    o = (fullName, pvValue)
                    pvList.append(o)
                    pvChild.setCheckState(2, False)

        self.caWork = self.caAccess.put(pvList)

#===============================================================================
# CA callback slots
#===============================================================================

    @QtCore.pyqtSlot('QObject*')
    def caGetSlot(self, caJob):
        print "iParamSingle.caGetSlot: iPV=", caJob.pvName, ", value=", caJob.pvGetValue

        for pvName, pvChild, pvObj in self.itemList:
            if not pvObj:
                raise ValueError, 'iParamSingle.caGetSlot: iPV object not found: ' + pvName
            fullName = self.iocName + pvGetName(pvObj)

            if not pvIsModeValue(pvObj):
                continue

            if fullName == caJob.pvName:

                widget = self.ui.treeWidget.itemWidget(pvChild, 1)
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
#        iocName = str(self.ui.lineEdit_iocName.text())
#        pvName = str(self.ui.lineEdit_pvName.text())
#        fullName = iocName + pvName
#        if fullName == caJob.pvName:
#            self.ui.label_pvValueRead.setText(str(caJob.pvGetValue))
#
#            print "iParamSingle.caPutSlot: iPV=", caJob.pvName, ", connected=", caJob.connected
#            if caJob.connected:
#                self.ui.label_pvConnected.setText(str("True"))
#            else:
#                self.ui.label_pvConnected.setText(str("False"))

    @QtCore.pyqtSlot('QObject*')
    def caMonitorSlot(self, caJob):
        print "iParamSingle.caMonitorSlot: PV=", caJob.pvName, ", value=", caJob.pvGetValue
#        if not caJob.pvName in self.pvMonitors:
#            return
#
#        for nameItem in self.ui.tableWidget.findItems(caJob.pvName, QtCore.Qt.MatchExactly):
#            item = self.ui.tableWidget.item(nameItem.row(), nameItem.column() + 1)
#            item.setText(str(caJob.pvGetValue))
#            item = self.ui.tableWidget.item(nameItem.row(), nameItem.column() + 2)
#            item.setText(str(caJob.connected))

    @QtCore.pyqtSlot('QObject*')
    def caWorkDoneSlot(self, caWork):
        print "iParamSingle.caWorkDoneSlot: caWork=", caWork
        if not caWork == self.caWork:
            print "iParamSingle.caWorkDoneSlot: not our work self.caWork=", self.caWork
            return

        pvList = []
        for caJob, caResult in caWork.res:
            print "iParamSingle.caWorkDoneSlot: PV=", caJob.pvName, "=", caJob.pvGetValue, "SUCCESS=", caJob.success

            for pvName, pvChild, pvObj in self.itemList:
                if not pvObj:
                    raise ValueError, 'iParamSingle.caWorkDoneSlot: iPV object not found: ' + pvName
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
    def addTreeChildren(self, group, parent):
        for pv in self.pvList:
            if pv.group == group:
                fullName = self.iocName + pv.pv
                child = QtGui.QTreeWidgetItem([pv.name])
                parent.addChild(child)

                if pv.widget == 'QLabel':
                    widget = QtGui.QLabel()
                    if pv.strings:
                        widget.setText(pv.strings[0])
                        child.setCheckState(2, False)
                    else:
                        widget.setText("UDF")
                elif pv.widget == 'QLineEdit':
                    widget = QtGui.QLineEdit()
                    widget.setText("UDF")
                    child.setCheckState(2, False)
                elif pv.widget == "QComboBox":
                    widget = QtGui.QComboBox()
                    widget.addItems(pv.strings)
                    child.setCheckState(2, False)
#                elif pv.widget == "QPushButton":
#                    widget = QtGui.QPushButton()
#                    widget.setText(pv.strings[0])
#                    QtCore.QObject.connect(self.widget,
#                                QtCore.SIGNAL('clicked()'),
#                                self.pushbuttonCallback)
                else:
                    child.setText(1, "UDF")

                if pv.widget:
                    self.ui.treeWidget.setItemWidget(child, 1, widget)

                self.itemList.append((fullName, child, pv))


    def batchDummy(self):

        item = QtGui.QTreeWidgetItem(["Dummy"])
        self.ui.treeWidget.addTopLevelItem(item)
        self.addTreeChildren('dummy', item)

        item = QtGui.QTreeWidgetItem(["More dummies"])
        self.ui.treeWidget.addTopLevelItem(item)
        self.addTreeChildren('dummy2', item)

        item = QtGui.QTreeWidgetItem(["Interlock"])
        self.ui.treeWidget.addTopLevelItem(item)
        self.addTreeChildren('Interlock', item)

