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
        Triggered by iPVObj slotOneShot() signal when value changes.
        Takes iPVObj as argument.
        """

        iLog.debug("enter")
        iLog.info("Called for pvName=%s, pvValue=%s, pvConnected=%s" %
                   (pvObj.name, pvObj.value, pvObj.connected))

        if self.pvObj != pvObj:
            if self.pvObj:
                self.pvObj.disconnectOneShotSignal(self.slotOneShot)
            self.pvObj = pvObj

        if pvObj.value is None:
            self.setText('UDF')
        else:
            self.setText(str(pvObj.value))

        if pvObj.connected:
            self.setStyleSheet(self.defaultLook)
        else:
            self.setStyleSheet("QLabel { background-color : darkRed; color : red; }");

    @QtCore.pyqtSlot('QObject*')
    def slotPeriodic(self, pvObj):
        """
        Triggered by iPVObj slotPeriodic() signal when value changes.
        Takes iPVObj as argument.
        """

        iLog.debug("enter")
        iLog.info("Called for pvName=%s, pvValue=%s, pvConnected=%s" %
                   (pvObj.name, pvObj.value, pvObj.connected))

        if self.pvObj != pvObj:
            if self.pvObj:
                self.pvObj.disconnectOneShotSignal(self.slotOneShot)
            self.pvObj = pvObj

        if pvObj.value is None:
            self.setText('UDF')
        else:
            self.setText(str(pvObj.value))

        if pvObj.connected:
            self.setStyleSheet(self.defaultLook)
        else:
            self.setStyleSheet("QLabel { background-color : darkRed; color : red; }");

class iQLineEdit(QtGui.QLineEdit):
    """
    iQLineEdit is extended QtGui.QLineEdit that is aware of PV property changes.
    """

    def __init__(self, text = ''):
        QtGui.QLineEdit.__init__(self, text)
        iLog.info("enter")

        self.defaultLook = self.styleSheet()
        self.pvObj = None

    #===========================================================================
    # CA callback slots
    #===========================================================================

    @QtCore.pyqtSlot('QObject*')
    def slotOneShot(self, pvObj):
        """
        Triggered by iPVObj slotOneShot() signal when value changes.
        Takes iPVObj as argument.
        """

        iLog.debug("enter")
        iLog.info("Called for pvName=%s, pvValue=%s, pvConnected=%s" %
                   (pvObj.name, pvObj.value, pvObj.connected))

        if self.pvObj != pvObj:
            if self.pvObj:
                self.pvObj.disconnectOneShotSignal(self.slotOneShot)
            self.pvObj = pvObj

        if pvObj.value is None:
            self.setText('UDF')
        else:
            self.setText(str(pvObj.value))

        if pvObj.connected:
            self.setStyleSheet(self.defaultLook)
        else:
            self.setStyleSheet("QLineEdit { background-color : darkRed; color : red; }");

    @QtCore.pyqtSlot('QObject*')
    def slotPeriodic(self, pvObj):
        """
        Triggered by iPVObj slotPeriodic() signal when value changes.
        Takes iPVObj as argument.
        """

        iLog.debug("enter")
        iLog.info("Called for pvName=%s, pvValue=%s, pvConnected=%s" %
                   (pvObj.name, pvObj.value, pvObj.connected))

        if self.pvObj != pvObj:
            if self.pvObj:
                self.pvObj.disconnectOneShotSignal(self.slotOneShot)
            self.pvObj = pvObj

        if pvObj.value is None:
            self.setText('UDF')
        else:
            self.setText(str(pvObj.value))

        if pvObj.connected:
            self.setStyleSheet(self.defaultLook)
        else:
            self.setStyleSheet("QLineEdit { background-color : darkRed; color : red; }");

class iQComboBox(QtGui.QComboBox):
    """
    iQComboBox is extended QtGui.QComboBox that is aware of PV property changes.
    """

    def __init__(self, text = ''):
        QtGui.QComboBox.__init__(self)
        iLog.info("enter")

        self.defaultLook = self.styleSheet()
        self.pvObj = None
        self.iText = text

    #===========================================================================
    # CA callback slots
    #===========================================================================

    @QtCore.pyqtSlot('QObject*')
    def slotOneShot(self, pvObj):
        """
        Triggered by iPVObj slotOneShot() signal when value changes.
        Takes iPVObj as argument.
        """

        iLog.debug("enter")
        iLog.info("Called for pvName=%s, pvValue=%s, pvConnected=%s" %
                   (pvObj.name, pvObj.value, pvObj.connected))

        if self.pvObj != pvObj:
            if self.pvObj:
                self.pvObj.disconnectOneShotSignal(self.slotOneShot)
            self.pvObj = pvObj
            self.clear()
            self.addItem('UDF')
            self.addItems(pvObj.enumStr.split(' '))

        if pvObj.value is None:
            self.setCurrentIndex(0)
        else:
            self.setCurrentIndex(pvObj.value + 1)

        if pvObj.connected:
            self.setStyleSheet(self.defaultLook)
        else:
            self.setStyleSheet("QComboBox { background-color : darkRed; color : red; }");

    @QtCore.pyqtSlot('QObject*')
    def slotPeriodic(self, pvObj):
        """
        Triggered by iPVObj slotPeriodic() signal when value changes.
        Takes iPVObj as argument.
        """

        iLog.debug("enter")
        iLog.info("Called for pvName=%s, pvValue=%s, pvConnected=%s" %
                   (pvObj.name, pvObj.value, pvObj.connected))

        if self.pvObj != pvObj:
            if self.pvObj:
                self.pvObj.disconnectOneShotSignal(self.slotOneShot)
            self.pvObj = pvObj
            self.clear()
            self.addItems(pvObj.enumStr.split(' '))

        if pvObj.value is None or len(pvObj.value) == 0:
            self.setCurrentIndex(0)
        else:
            self.setCurrentIndex(int(pvObj.value))

        if pvObj.connected:
            self.setStyleSheet(self.defaultLook)
        else:
            self.setStyleSheet("QComboBox { background-color : darkRed; color : red; }");

class iQTableWidgetItem(QtGui.QTableWidgetItem):
    """
    iQTableWidgetItem is extended QtGui.QTableWidgetItem that is aware of PV property changes.
    """

    def __init__(self, text = '', iType = 'iQLabel'):
        QtGui.QTableWidgetItem.__init__(self, '')
        iLog.info("enter")

        if iType == 'iQLabel':
            self._widget = iQLabel("UDF")
        elif iType == 'iQLineEdit':
            self._widget = iQLineEdit("UDF")
        elif iType == 'iQComboBox':
            self._widget = iQComboBox(text)
        else:
            iLog.error("widget type '%s' not supported" % (iType))
            iRaise(self, "widget type '%s' not supported" % (iType))

        self.iType = iType

    def connectPVObj(self, pvObj, periodic = False):
        iLog.debug("enter")

        if not periodic:
            pvObj.connectOneShotSignal(self._widget.slotOneShot)
        else:
            pvObj.connectPeriodicSignal(self._widget.slotPeriodic)

    def disconnectPVObj(self, pvObj, periodic = False):
        iLog.debug("enter")

        if not periodic:
            pvObj.disconnectOneShotSignal(self._widget.slotOneShot)
        else:
            pvObj.disconnectPeriodicSignal(self._widget.slotPeriodic)

class iQTreeWidgetItem(QtGui.QTreeWidgetItem):
    """
    iQTreeWidgetItem is extended QtGui.QTreeWidgetItem that is aware of PV property changes.
    """

    def __init__(self, text = [], iType = 'iQLabel'):
        QtGui.QTreeWidgetItem.__init__(self, text)
        iLog.info("enter")

        if iType == 'iQLabel':
            self._widget = iQLabel("UDF")
        elif iType == 'iQLineEdit':
            self._widget = iQLineEdit("UDF")
        elif iType == 'iQComboBox':
            self._widget = iQComboBox(text)
        else:
            iLog.error("widget type '%s' not supported" % (iType))
            iRaise(self, "widget type '%s' not supported" % (iType))

        self.iType = iType

    def connectPVObj(self, pvObj, periodic = False):
        iLog.debug("enter")

        if not periodic:
            pvObj.connectOneShotSignal(self._widget.slotOneShot)
        else:
            pvObj.connectPeriodicSignal(self._widget.slotPeriodic)

    def disconnectPVObj(self, pvObj, periodic = False):
        iLog.debug("enter")

        if not periodic:
            pvObj.disconnectOneShotSignal(self._widget.slotOneShot)
        else:
            pvObj.disconnectPeriodicSignal(self._widget.slotPeriodic)
