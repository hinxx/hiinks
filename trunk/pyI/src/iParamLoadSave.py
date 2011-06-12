'''
Created on Jun 3, 2011

@author: hinko
'''

#===============================================================================
# COMMENTS
#===============================================================================
# TODO: provide select all/none buttons in gui 
#===============================================================================

from lib.iConf import iLog, iDefaultPVDataDir
from lib.iPVTree import iPVTree
from lib.iIOCTree import iIOCTree

from PyQt4 import QtCore, QtGui
import time

from ui.uiParamLoadSave import Ui_ParamLoadSave
import os

class iParamLoadSave(QtGui.QWidget):
    def __init__(self, parent, caAccess):
        QtGui.QWidget.__init__(self, parent)
        iLog.debug("enter")

        self.pvName = None
        self.pvTree = iPVTree(self)
        self.iocTree = iIOCTree(self)
        self.iocTrees = dict()
        self.itemList = None
        self.caWork = None
        self.xmlFile = None
        self.savePrefix = 'pvData'

        for iocName in self.iocTree.mGetAttribute('name'):
            iLog.info("Adding PV tree for IOC %s" % (iocName))
            self.iocTrees[iocName] = iPVTree(self)



        self.caAccess = caAccess
#        QtCore.QObject.connect(self.caAccess,
#                               QtCore.SIGNAL("sigGet(QObject*)"), self.caGetSlot)
#        QtCore.QObject.connect(self.caAccess,
#                               QtCore.SIGNAL("sigPut(QObject*)"), self.caPutSlot)
#        QtCore.QObject.connect(self.caAccess,
#                               QtCore.SIGNAL("sigMonitor(QObject*)"), self.caMonitorSlot)
        QtCore.QObject.connect(self.caAccess,
                               QtCore.SIGNAL("sigDone(QObject*)"), self.caWorkDoneSlot)

        self.ui = Ui_ParamLoadSave()
        self.ui.setupUi(self)

        QtCore.QObject.connect(self.ui.pushButton_load,
                               QtCore.SIGNAL("clicked()"), self.doLoad)
        QtCore.QObject.connect(self.ui.pushButton_save,
                               QtCore.SIGNAL("clicked()"), self.doSave)
        QtCore.QObject.connect(self.ui.pushButton_saveas,
                               QtCore.SIGNAL("clicked()"), self.doSaveAs)

        QtCore.QObject.connect(self.ui.pushButton_iocAll,
                               QtCore.SIGNAL("clicked()"), self.doIOCAll)
        QtCore.QObject.connect(self.ui.pushButton_iocNone,
                               QtCore.SIGNAL("clicked()"), self.doIOCNone)
        QtCore.QObject.connect(self.ui.pushButton_pvAll,
                               QtCore.SIGNAL("clicked()"), self.doPVAll)
        QtCore.QObject.connect(self.ui.pushButton_pvNone,
                               QtCore.SIGNAL("clicked()"), self.doPVNone)
        QtCore.QObject.connect(self.ui.lineEdit_savePrefix,
                               QtCore.SIGNAL("textChanged(QString)"), self.savePrefixSet)

#        self.doChangePV()
        self.savePrefixSet('pvData')
        self.populate()

    def show(self):
        iLog.debug("enter")

    def hide(self):
        iLog.debug("enter")

    def close(self):
        iLog.debug("enter")

    def populate(self):
        iLog.debug("enter")

        # show IOC list
        for iocName in self.iocTree.mGetAttribute('name'):
            item = QtGui.QListWidgetItem(iocName)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Checked)
            self.ui.listWidget_ioc.addItem(item)

        # show PV list
        for pvName in self.pvTree.mGetAttribute('name'):
            item = QtGui.QListWidgetItem(pvName)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Checked)
            self.ui.listWidget_pv.addItem(item)

        self.ui.listWidget_ioc.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.listWidget_pv.setFocusPolicy(QtCore.Qt.NoFocus)

    def savePrefixSet(self, txt):
        iLog.info("enter")
        self.savePrefix = 'pvData'
        if len(txt) > 0:
            self.savePrefix = str(txt)
        self.ui.label_saveFile.setText(self.savePrefix + '-<IOC name>-<stamp YYYYMMDDHHmmss>.xml')

    def doLoad(self):
        iLog.info("enter")

#        fd = QtGui.QFileDialog(self)
#        self.xmlFile = fd.getOpenFileName()
#        if os.path.isfile(self.xmlFile):
#            userPvList = pvList(self.xmlFile)

    def doSave(self, saveas = False):
        iLog.info("enter")

        self.doPVRefresh()

    def doSaveAs(self):
        iLog.info("enter")
        self.doSave(saveas = True)

    def doIOCAll(self):
        iLog.info("enter")
        for x in range(self.ui.listWidget_ioc.count()):
            item = self.ui.listWidget_ioc.item(x)
            item.setCheckState(QtCore.Qt.Checked)

    def doIOCNone(self):
        iLog.info("enter")
        for x in range(self.ui.listWidget_ioc.count()):
            item = self.ui.listWidget_ioc.item(x)
            item.setCheckState(QtCore.Qt.Unchecked)

    def doPVAll(self):
        iLog.info("enter")
        for x in range(self.ui.listWidget_pv.count()):
            item = self.ui.listWidget_pv.item(x)
            item.setCheckState(QtCore.Qt.Checked)

    def doPVNone(self):
        iLog.info("enter")
        for x in range(self.ui.listWidget_pv.count()):
            item = self.ui.listWidget_pv.item(x)
            item.setCheckState(QtCore.Qt.Unchecked)

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
        self.itemList = dict()

        for x in range(self.ui.listWidget_ioc.count()):
            iocItem = self.ui.listWidget_ioc.item(x)
            if iocItem.checkState() != QtCore.Qt.Checked:
                continue

            iocName = str(iocItem.text())

            for xx in range(self.ui.listWidget_pv.count()):
                pvItem = self.ui.listWidget_pv.item(xx)
                if pvItem.checkState() != QtCore.Qt.Checked:
                    continue

                pvName = str(pvItem.text())

                if self.pvTree.pvIsModeValue(pvName):
                    fullName = iocName + self.pvTree.pvGetName(pvName)
                    iLog.debug("pvName=%s" % fullName)
                    o = (fullName, None)
                    pvList.append(o)
                    self.itemList[fullName] = (iocName, pvName)

        iLog.info("self.itemList: %s" % (repr(self.itemList)))
        self.caAccess.get(pvList)

    def doPVApply(self):
        iLog.debug("enter")
#
#        pvList = []
#
#        for pvName, pvItem, iocObj, pvObj in self.itemList:
#            if not pvItem.checkState(3) == QtCore.Qt.Checked:
#                continue
#
#            widget = self.ui.treeWidget.itemWidget(pvItem, 2)
#            pvValue = None
#            if isinstance(widget, QtGui.QLineEdit):
#                pvValue = str(widget.text())
#            elif isinstance(widget, QtGui.QComboBox):
#                pvValue = widget.currentIndex()
#
#            fullName = None
#            if pvIsModeValue(pvObj):
#                fullName = iocObj.name + pvPutName(pvObj)
#            else:
#                raise ValueError, 'iParamMulti.doPVApply: invalid iPV mode:', pvObj.mode
#
#            iLog.debug("pvName=%s, pvValue=%s" % (fullName, pvValue))
#
#            o = (fullName, pvValue)
#            pvList.append(o)
#            pvItem.setCheckState(3, False)
#
#        self.caWork = self.caAccess.put(pvList)

#===============================================================================
# CA callback slots
#===============================================================================

    @QtCore.pyqtSlot('QObject*')
    def caGetSlot(self, caJob):
        iLog.debug("enter")
        iLog.debug("pvName=%s, value=%s, success=%s" % (caJob.pvName, caJob.pvGetValue, caJob.success))

#        for pvName, pvItem, iocObj, pvObj in self.itemList:
#            fullName = iocObj.name + pvGetName(pvObj)
#
#            if not pvIsModeValue(pvObj):
#                continue
#
#            if fullName == caJob.pvName:
#                widget = self.ui.treeWidget.itemWidget(pvItem, 2)
#                if isinstance(widget, QtGui.QLabel):
#                    widget.setText(str(caJob.pvGetValue))
#                elif isinstance(widget, QtGui.QLineEdit):
#                    widget.setText(str(caJob.pvGetValue))
#                elif isinstance(widget, QtGui.QComboBox):
#                    widget.setCurrentIndex(caJob.pvGetValue)
#
#                iLog.debug("pvName=%s, value=%s, success=%s" % (caJob.pvName, caJob.pvGetValue, caJob.success))

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
        iLog.debug("got caWork=%s" % (caWork))

        for caJob, caResult in caWork.res:
            iLog.info("pvName=%s, value=%s, success=%s" % (caJob.pvName, caJob.pvGetValue, caJob.success))

            item = self.itemList[caJob.pvName]
            iocName = item[0]
            pvName = item[1]
            iLog.info("Recognized iocName=%s, pvName=%s" % (iocName, pvName))
            pvTree = self.iocTrees[iocName]
            iValue = pvTree.iValueGet(pvName)
            iLog.info("Current iValue=%s" % (iValue))
            pvTree.iValueSet(pvName, caJob.pvGetValue)
            iValue = pvTree.iValueGet(pvName)
            iLog.info("New iValue=%s" % (iValue))

        self.itemList = None

        for iocName, pvTree in self.iocTrees.items():
            file = iDefaultPVDataDir + '/' + \
                self.savePrefix + '-' + \
                iocName + '-' + \
                time.strftime("%Y%m%d%H%M%S") + \
                '.xml'

            iLog.info("Saving PV data for IOC %s to file %s" % (iocName, file))

            #pvTree.xmlOut()

            f = open(file, "w+")
            f.write(pvTree.xmlOut())
            f.close()


#        iLog.debug("caWork=%s" % caWork)
#        if not caWork == self.caWork:
#            iLog.debug("skipping caWork=%s, want self.caWork=%s" % (caWork, self.caWork))
#            return
#
#        pvList = []
#        for caJob, caResult in caWork.res:
#            iLog.debug("pvName=%s, value=%s, success=%s" % (caJob.pvName, caJob.pvGetValue, caJob.success))
#
#            for pvName, pvItem, iocObj, pvObj in self.itemList:
#                fullName = iocObj.name + pvPutName(pvObj)
#
#                if not pvIsModeValue(pvObj):
#                    continue
#
#                if not fullName == caJob.pvName:
#                    continue
#
#                iLog.debug("doing GET for PUT, %s => %s" % (fullName, iocObj.name + pvGetName(pvObj)))
#                fullName = iocObj.name + pvGetName(pvObj)
#                o = (fullName, None)
#                pvList.append(o)
#
#        self.caAccess.get(pvList)
#        self.caWork = None
