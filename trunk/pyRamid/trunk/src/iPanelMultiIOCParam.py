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

from ui.uiPanelMultiIOCParam import Ui_PanelMultiIOCParam

class iPanelMultiIOCParam(QtGui.QWidget):

    def __init__(self, parent, pvHandler):
        QtGui.QWidget.__init__(self, parent)
        iLog.debug("enter")

        self.pvMonitors = dict()
        self.iocName = None
        self.pvName = None
        self.pvTree = iPVTree(self)
        self.iocTree = iIOCTree(self)

        self.pvHandler = pvHandler

        self.ui = Ui_PanelMultiIOCParam()
        self.ui.setupUi(self)
