'''
Created on Jun 6, 2011

@author: hinko
'''

import os

# Set EPICS base stuff
epics_base = '/home/hinko/workspace/base-3.14.12.1'
print 'exporting EPICS_CA_MAX_ARRAY_BYTES: 16777216'
path = os.environ.get('PATH', '') + ':' + epics_base + '/bin/linux-x86'
os.environ['PATH'] = path
path = os.environ.get('LD_LIBRARY_PATH', '') + ':' + epics_base + '/lib/linux-x86'
os.environ['LD_LIBRARY_PATH'] = path
os.environ['EPICS_HOST_ARCH'] = 'linux-x86'

ips = '10.0.4.228 10.0.4.246 10.0.4.213 10.0.4.229 10.0.4.121 10.0.4.120 10.0.4.122'
print 'exporting EPICS_CA_MAX_ARRAY_BYTES: 16777216'
os.putenv('EPICS_CA_MAX_ARRAY_BYTES', '16777216')
# Note: the first import of catools must come after the environ is set up.
print 'exporting EPICS_CA_ADDR_LIST: ', ips
os.putenv('EPICS_CA_ADDR_LIST', ips)


import sys
import time

from PyQt4 import QtCore, QtGui, Qt

from ui.win1 import Ui_MainWindow
from lib.iIOCList import iIOCList
from widgets.iPVSingle import iPVSingle


class Main(QtGui.QMainWindow):

    iocList = iIOCList()
    uiPanels = dict()

    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, None)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.uiInit()

#        QtCore.QObject.connect(self.ui.pushButton_exit, QtCore.SIGNAL("clicked()"), self.doClose)

#        QtCore.QObject.connect(self.ui.pushButton_get, QtCore.SIGNAL("clicked()"), self.pvGet)
#        QtCore.QObject.connect(self.ui.pushButton_put, QtCore.SIGNAL("clicked()"), self.pvPut)
#        QtCore.QObject.connect(self.ui.pushButton_monitor, QtCore.SIGNAL("clicked()"), self.pvMonitor)
#        QtCore.QObject.connect(self.ui.pushButton_unmonitor, QtCore.SIGNAL("clicked()"), self.pvUnmonitor)

        #self.iocList = iIOCList()

        self.iocList.addIOC("hinkoHost")
        self.iocList.addIOC("hinkoHost1")
        self.iocList.addIOC("hinkoHost2")
        self.iocList.addIOC("hinkoHost3")

        self.iocList.dump()
        print "main.init: DONE"

        self.uiToolboxChange(0)

    def uiInit(self):
        print "uiInit:"
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        QtCore.QObject.connect(self.ui.pushButton_exit, QtCore.SIGNAL("clicked()"), self.doClose)
        QtCore.QObject.connect(self.ui.toolBox, QtCore.SIGNAL("currentChanged(int)"), self.uiToolboxChange)

        #self.ui.scrollAreaWidgetContents.hide()

#        QtCore.QObject.connect(self.ui.pushButton_parametersSingle,
#                               QtCore.SIGNAL("clicked()"), self.uiParamSingleShow)
#        QtCore.QObject.connect(self.ui.pushButton_parametersMulti,
#                               QtCore.SIGNAL("clicked()"), self.uiParamMultiShow)

        self.uiPanel = None
        #self.uiPanels["iParamSingle"] = iParamSingle(iocList = self.iocList)
        #self.uiPanels["iParamMulti"] = iParamMulti(iocList = self.iocList)
        self.uiPanels["iPVSingle"] = iPVSingle(iocList = self.iocList)

    def uiToolboxChange(self, index):
        page = self.ui.toolBox.itemText(index)
        print "main.uiToolboxChange: current index", index, page
        print "main.uiToolboxChange: self.uiPanel", self.uiPanel

        if page == "Overview":
            self.uiPanelShow("Overview", "iPVSingle")
#        elif page == "Parameters":
#            if self.uiPanel == "uParamSingle":
#                self.uiParamSingleShow()
#            elif self.uiPanel == "uParamMulti":
#                self.uiParamMultiShow()
        else:
            print "main.uiToolboxChange: unknown"

    def uiPanelShow(self, page, panel):
        print "main.uiPanelShow: ", page, panel

#        for k, v in self.uiPanels.items():
#            v.hide()

        if self.uiPanel:
            self.uiPanel.hide()
            self.uiPanels[self.uiPanel] = self.ui.scrollArea.takeWidget()

        self.ui.scrollArea.setWidget(self.uiPanels[panel])
        self.uiPanels[panel].show()
        self.uiPanel = panel

#    def pvGet(self):
#        print "main.pvGet:"
#
#        iocName = str(self.ui.lineEdit_iocName.text())
#        pvName = str(self.ui.lineEdit_pvName.text())
#
#        iioc = self.iocList.find(iocName)
#        print "main.pvGet: IOC=", iioc, ", name=", iioc.iocName
#
#        iioc.pvGet(pvName, self.pvGetSlot)
#
#    def pvPut(self):
#        print "main.pvPut:"
#
#        iocName = str(self.ui.lineEdit_iocName.text())
#        pvName = str(self.ui.lineEdit_pvName.text())
#        pvValue = str(self.ui.lineEdit_pvValueWrite.text())
#
#        iioc = self.iocList.find(iocName)
#
#        iioc.pvPut(pvName, pvValue)
#
#    def pvMonitor(self):
#        print "main.pvMonitor:"
#
#        iocName = str(self.ui.lineEdit_iocName.text())
#        pvName = str(self.ui.lineEdit_pvName.text())
#
#        iioc = self.iocList.find(iocName)
#
#        iioc.pvMonitorStart(pvName)
#
#    def pvUnmonitor(self):
#        print "main.pvUnmonitor:"
#
#        iocName = str(self.ui.lineEdit_iocName.text())
#        pvName = str(self.ui.lineEdit_pvName.text())
#
#        iioc = self.iocList.find(iocName)
#
#        iioc.pvMonitorStop(pvName)

#===============================================================================
# # Test slots
#===============================================================================

    @QtCore.pyqtSlot('QObject*')
    def pvGetSlot(self, iPV):
        print "main.pvGetSlot: iPV=", iPV, ", value=", iPV.value

    @QtCore.pyqtSlot('QObject*')
    def pvPutSlot(self, iPV):
        print "main.pvPutSlot: iPV=", iPV, ", value=", iPV.value

    @QtCore.pyqtSlot('QObject*')
    def pvMonitorSlot(self, iPV):
        print "main.pvMonitorSlot: iPV=", iPV, ", value=", iPV.value

    @QtCore.pyqtSlot('QObject*')
    def pvConnectSlot(self, iPV):
        print "main.pvConnectSlot: iPV=", iPV, ", connected=", iPV.isConnected()

#===============================================================================
# Close
#===============================================================================
    def close(self):
        print "main.close:"
        self.iocList.close()
        app.closeAllWindows()

    def doClose(self):
        print "main.doClose:"
        self.close()

###############################################################################
#        MAIN
###############################################################################
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    myapp = Main()
    myapp.show()
    print "Executing!"
    ret = app.exec_()
    print "Ended!"
    sys.exit(ret)

