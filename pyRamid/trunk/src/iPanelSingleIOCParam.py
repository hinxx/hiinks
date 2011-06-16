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

from ui.uiPanelSingleIOCParam import Ui_PanelSingleIOCParam

class iPanelSingleIOCParam(QtGui.QWidget):

    def __init__(self, parent, pvHandler):
        QtGui.QWidget.__init__(self, parent)
        iLog.debug("enter")

        self.pvMonitors = dict()
        self.iocName = None
        self.pvName = None
        self.pvTree = iPVTree(self)
        self.iocTree = iIOCTree(self)

        self.pvHandler = pvHandler

        self.ui = Ui_PanelSingleIOCParam()
        self.ui.setupUi(self)

        self.ui.pushButton_apply.clicked.connect(self.pvApply)
        self.ui.pushButton_refresh.clicked.connect(self.pvRefresh)
        self.ui.pushButton_changeIOC.clicked.connect(self.iocChange)
        self.ui.lineEdit_iocName.textChanged.connect(self.iocTextChanged)
        self.connect(self.ui.comboBox_iocName, QtCore.SIGNAL('activated(QString)'), self.iocComboChanged)

        iocName = str(self.ui.lineEdit_iocName.text())

        self.ui.comboBox_iocName.addItem('-- unknown --')
        self.ui.comboBox_iocName.addItems(self.iocTree.mGetAttribute('name'))

        self.iocTextChanged(iocName)

        #self.iocChange()
        #self.populate()

    def show(self):
        iLog.debug("enter")

    def hide(self):
        iLog.debug("enter")

    def close(self):
        iLog.debug("enter")

    def iocComboChanged(self, txt):
        iLog.debug("enter")
        iLog.debug("New IOC text '%s'" % (txt))
        self.ui.lineEdit_iocName.setText(txt)

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

    def iocChange(self):
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

        self.pvRefresh()

    def populate(self):
        iLog.debug("enter")
        """
        iocObj = pvListFind(self.iocList, name = self.iocName)
        if not iocObj:
            return

        if len(self.itemList) != 0:
            return

        item = QtGui.QTreeWidgetItem(["Dummy"])
        self.ui.treeWidget.addTopLevelItem(item)
        self.addItems('dummy', item)

        item = QtGui.QTreeWidgetItem(["Interlock"])
        self.ui.treeWidget.addTopLevelItem(item)
        self.addItems('interlock', item)



        # Some tree widgets properties
        self.ui.treeWidget.setColumnWidth(0, 180)
        self.ui.treeWidget.setColumnWidth(1, 120)
        self.ui.treeWidget.setColumnWidth(2, 100)
        self.ui.treeWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        """

    def pvRefresh(self):
        iLog.debug("enter")

        iocName = str(self.ui.lineEdit_iocName.text())

        if len(iocName) == 0:
            iLog.error("Invalid iocName argument length")
            return

        self.iocName = iocName
        iLog.info("self.iocName=%s" % self.iocName)

        for pvName in self.pvTree.mGetAttribute('name'):
            pvNameWSuffix = self.pvTree.pvGetName(pvName)
            iLog.info("PV %s, PV w suffix %s" % (pvName, pvNameWSuffix))


    def pvApply(self):
        iLog.debug("enter")

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
