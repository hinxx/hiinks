'''
Created on Jun 13, 2011

@author: hinko
'''

#===============================================================================
# COMMENTS
#===============================================================================
# TODO: provide load/save gui of PV values from selected IOCs/PVs
# TODO: provide application configuration gui
# TODO: remove Qt signals from the hidden panels, reconnect on show
#===============================================================================

from iHelper import iRaise, iLog

# TODO: Fix this EPICS stuff
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



from PyQt4 import QtCore, QtGui
import sys
import time

from iPVHandler import iPVHandler

from ui.win1 import Ui_MainWindow
from iPanelTest import iPanelTest
from iPanelSingleIOCParam import iPanelSingleIOCParam
from iPanelMultiIOCParam import iPanelMultiIOCParam
from iPanelDummy import iPanelDummy

class Main(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, None)

        iLog.debug("Log started")

        self.pvHandler = iPVHandler(self)
        self.pvHandler.finished.connect(self.pvHandlerFinished)
        self.pvHandler.terminated.connect(self.pvHandlerTerminated)

        self.uiPanels = dict()

        self.uiInit()

        self.ui.toolBox.setCurrentIndex(0)
        self.uiToolboxChange(0)

    def uiInit(self):
        iLog.debug("enter")

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        QtCore.QObject.connect(self.ui.pushButton_exit, QtCore.SIGNAL("clicked()"), self.doClose)
        QtCore.QObject.connect(self.ui.toolBox, QtCore.SIGNAL("currentChanged(int)"), self.uiToolboxChange)

        #self.ui.scrollAreaWidgetContents.hide()

        self.uiPanel = None
        self.uiPanels['iPanelTest'] = iPanelTest(None, self.pvHandler)

        self.uiPanels['iPanelSingleIOCParam'] = iPanelSingleIOCParam(None, self.pvHandler)
        self.uiPanels['iPanelMultiIOCParam'] = iPanelMultiIOCParam(None, self.pvHandler)

        # Dummy panels
        self.uiPanels['iPanelOrbit'] = iPanelDummy(None, self.pvHandler)
        self.uiPanels['iPanelOverview'] = iPanelDummy(None, self.pvHandler)
        self.uiPanels['iPanelConfiguration'] = iPanelDummy(None, self.pvHandler)
        self.uiPanels['iPanelStatus'] = iPanelDummy(None, self.pvHandler)
        self.uiPanels['iPanelLoadSaveParam'] = iPanelDummy(None, self.pvHandler)

    def uiToolboxChange(self, index):
        iLog.debug("enter")

        page = self.ui.toolBox.itemText(index)
        iLog.debug("page=%s, panel=%s" % (page, self.uiPanel))

        if page == 'Test':
            self.uiPanelShow(page, 'iPanelTest')
        elif page == 'Parameters (Single IOC)':
            self.uiPanelShow(page, 'iPanelSingleIOCParam')
        elif page == 'Parameters (Multi IOC)':
            self.uiPanelShow(page, 'iPanelMultiIOCParam')
        elif page == 'Load && save':
            self.uiPanelShow(page, "iPanelLoadSaveParam")

        # Dummy panels
        elif page == 'Overview':
            self.uiPanelShow(page, 'iPanelOverview')
        elif page == 'Orbit':
            self.uiPanelShow(page, 'iPanelOrbit')
        elif page == 'Configuration':
            self.uiPanelShow(page, 'iPanelConfiguration')
        elif page == 'Status':
            self.uiPanelShow(page, 'iPanelStatus')
        else:
            iLog.error("unknown page=%s" % page)

    def uiPanelShow(self, page, panel):
        iLog.debug("enter")

        if self.uiPanel:
            self.uiPanels[self.uiPanel].hide()
            self.uiPanels[self.uiPanel] = self.ui.scrollArea.takeWidget()
        self.uiPanel = panel
        iLog.debug("page=%s, panel=%s" % (page, panel))

        self.ui.scrollArea.setWidget(self.uiPanels[self.uiPanel])
        self.uiPanels[self.uiPanel].show()

#===============================================================================
# Close
#===============================================================================
    def pvHandlerFinished(self):
        iLog.debug("enter")

    def pvHandlerTerminated(self):
        iLog.debug("enter")

    def close(self):
        iLog.debug("enter")

        self.pvHandler.close()
        self.pvHandler = None
        app.closeAllWindows()

    def doClose(self):
        iLog.debug("enter")

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


