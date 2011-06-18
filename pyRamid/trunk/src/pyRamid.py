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


from iGLobals import iLog, iInitIOCs, iDefaultIOCTreeXMLFile, iInitPVs, \
    iDefaultPVTreeXMLFile, iInitHandler, iGlobalHandle
from iHelper import xmlToObjectParser
from iPVHandler import iPVHandler


from PyQt4 import QtCore, QtGui
import sys
import time

from ui.win1 import Ui_MainWindow
from iPanelTest import iPanelTest
from iPanelSingleIOCParam import iPanelSingleIOCParam
from iPanelMultiIOCParam import iPanelMultiIOCParam
from iPanelDummy import iPanelDummy

class Main(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, None)

        iLog.info("Log started")

        # Initialize global objects
        iInitIOCs(xmlToObjectParser(iDefaultIOCTreeXMLFile, 'iIOCObj'))
        iInitPVs(xmlToObjectParser(iDefaultPVTreeXMLFile, 'iPVObj'))
        iInitHandler(iPVHandler(self))
        iLog.info("Globals initialized..")

        self.uiPanels = dict()
        self.uiInit()
        iLog.info("UI initialized..")

        self.ui.toolBox.setCurrentIndex(0)
        self.uiToolboxChange(0)

    def uiInit(self):
        iLog.debug("enter")

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        QtCore.QObject.connect(self.ui.pushButton_exit, QtCore.SIGNAL("clicked()"), self.doClose)
        QtCore.QObject.connect(self.ui.toolBox, QtCore.SIGNAL("currentChanged(int)"), self.uiToolboxChange)

        self.uiPanel = None
        panel = iPanelTest()
        self.uiPanels[str(panel.objectName())] = panel
        panel = iPanelSingleIOCParam()
        self.uiPanels[str(panel.objectName())] = panel
        panel = iPanelMultiIOCParam()
        self.uiPanels[str(panel.objectName())] = panel
        panel = iPanelDummy()
        self.uiPanels[str(panel.objectName())] = panel

        iLog.debug("self.uiPanels: %s" % (self.uiPanels))
        # Dummy panels
#        self.uiPanels['iPanelOrbit'] = iPanelDummy()
#        self.uiPanels['iPanelOverview'] = iPanelDummy()
#        self.uiPanels['iPanelConfiguration'] = iPanelDummy()
#        self.uiPanels['iPanelStatus'] = iPanelDummy()
#        self.uiPanels['iPanelLoadSaveParam'] = iPanelDummy()

    def uiToolboxChange(self, index):
        iLog.debug("enter")

        page = self.ui.toolBox.itemText(index)
        iLog.debug("page=%s, panel=%s" % (page, self.uiPanel))

        if page == 'Test':
            self.uiPanelShow(page, 'PanelTest')
        elif page == 'Parameters (Single IOC)':
            self.uiPanelShow(page, 'PanelSingleIOCParam')
        elif page == 'Parameters (Multi IOC)':
            self.uiPanelShow(page, 'PanelMultiIOCParam')

        # Dummy panels
        elif page == 'Load && save':
            self.uiPanelShow(page, "PanelDummy")
        elif page == 'Overview':
            self.uiPanelShow(page, 'PanelDummy')
        elif page == 'Orbit':
            self.uiPanelShow(page, 'PanelDummy')
        elif page == 'Configuration':
            self.uiPanelShow(page, 'PanelDummy')
        elif page == 'Status':
            self.uiPanelShow(page, 'PanelDummy')
        else:
            iLog.error("unknown page=%s" % page)
            self.uiPanelShow(page, 'PanelDummy')

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

        pvHandler = iGlobalHandle()
        pvHandler.close()
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


