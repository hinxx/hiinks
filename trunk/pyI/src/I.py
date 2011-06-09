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

from PyQt4 import QtCore, QtGui, uic

from lib.iCA import iCA

from widgets.iPVSingle import iPVSingle


class Main(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, None)

        # CA access layer
        self.caAccess = iCA(self)

        #iocList = iIOCList()
        self.uiPanels = dict()

        # Dictionary containing all known IOCs (IOCname: uIOC object)
        self.iocList = dict()

        self.ui = uic.loadUi('ui/win1.ui', self)
        self.uiInit()

        print "main.init: DONE"

        self.uiToolboxChange(0)

    def uiInit(self):
        print "uiInit:"

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
        self.uiPanels["iPVSingle"] = iPVSingle(self, self.caAccess)

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

#===============================================================================
# Close
#===============================================================================
    def close(self):
        print "main.close:"
        self.caAccess.close()
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

