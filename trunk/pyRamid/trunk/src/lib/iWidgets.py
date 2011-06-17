'''
Created on Jun 17, 2011

@author: hinko
'''

from iHelper import iRaise, iLog

from PyQt4 import QtCore, QtGui

#===============================================================================
# iQObject
#===============================================================================
class iQObject(QtCore.QObject):
    """
    iQObject is extended QtCore.QObject that is aware of PV property changes.
    """

    def __init__(self, parent = None):
        QtCore.QObject.__init__(self, parent)
        iLog.info("enter")

#===============================================================================
# iQWidget
#===============================================================================
class iQWidget(QtGui.QWidget):
    """
    iQWidget is extended QtCore.QWidget that is aware of PV property changes.
    """

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        iLog.info("enter")

class iQLabel(QtGui.QLabel):
    """
    iQLabel is extended QtGui.QLabel that is aware of PV property changes.
    """

    def __init__(self, text = ''):
        QtGui.QLabel.__init__(self, text)
        iLog.info("enter")

        self.defaultLook = self.styleSheet()
        self.pvObj = None

    #===========================================================================
    # CA callback slots
    #===========================================================================

    @QtCore.pyqtSlot('QObject*')
    def slotOneShot(self, pvObj):
        """
        Triggered by iPVObj sigValueChanged() signal when value changes.
        Takes iPVObj as argument.
        """

        iLog.debug("enter")
        iLog.info("Called for pvName=%s, pvValue=%s, pvConnected=%s" %
                   (pvObj.name, pvObj.value, pvObj.connected))

        if not self.pvObj:
            self.pvObj = pvObj

        if self.pvObj != pvObj:
            self.pvObj.disconnectOneShotSignal(self.slotOneShot)
            self.pvObj = pvObj

        self.setText(str(pvObj.value))

        if pvObj.connected:
            self.setStyleSheet(self.defaultLook)
        else:
            self.setStyleSheet("QLabel { background-color : darkRed; color : red; }");

    @QtCore.pyqtSlot('QObject*')
    def slotPeriodic(self, pvObj):
        """
        Triggered by iPVObj sigValueChanged() signal when value changes.
        Takes iPVObj as argument.
        """

        iLog.debug("enter")
        iLog.info("Called for pvName=%s, pvValue=%s, pvConnected=%s" %
                   (pvObj.name, pvObj.value, pvObj.connected))

        if not self.pvObj:
            self.pvObj = pvObj

        if self.pvObj != pvObj:
            self.pvObj.disconnectPeriodicSignal(self.slotPeriodic)
            self.pvObj = pvObj

        self.setText(str(pvObj.value))

        if pvObj.connected:
            self.setStyleSheet(self.defaultLook)
        else:
            self.setStyleSheet("QLabel { background-color : darkRed; color : red; }");

class iQTableWidgetItem(QtGui.QTableWidgetItem):
    """
    iQTableWidgetItem is extended QtGui.QTableWidgetItem that is aware of PV property changes.
    """

    def __init__(self, text = '', iType = 'iQLabel'):
        QtGui.QTableWidgetItem.__init__(self, '')
        iLog.info("enter")

        self.iType = iType
        if self.iType == 'iQLabel':
            self._widget = iQLabel(text)

    #===========================================================================
    # CA callback slots
    #===========================================================================

    @QtCore.pyqtSlot('QObject*')
    def slotOneShot(self, pvObj):
        """
        Triggered by iPVObj sigValueChanged() signal when value changes.
        Takes iPVObj as argument.
        """

        iLog.debug("enter")
        iLog.info("Called for pvName=%s, pvValue=%s, pvConnected=%s" %
                   (pvObj.name, pvObj.value, pvObj.connected))

        self._widget.slotOneShot(pvObj)

    @QtCore.pyqtSlot('QObject*')
    def slotPeriodic(self, pvObj):
        """
        Triggered by iPVObj sigValueChanged() signal when value changes.
        Takes iPVObj as argument.
        """

        iLog.debug("enter")
        iLog.info("Called for pvName=%s, pvValue=%s, pvConnected=%s" %
                   (pvObj.name, pvObj.value, pvObj.connected))

        self._widget.slotPeriodic(pvObj)
