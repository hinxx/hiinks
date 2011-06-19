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

#===============================================================================
# iQLabel
#===============================================================================
class iQLabel(QtGui.QLabel):
    """
    iQLabel is extended QtGui.QLabel that is aware of PV property changes.
    """

    def __init__(self, text = ''):
        QtGui.QLabel.__init__(self, text)
        iLog.info("enter")

        self.defaultLook = self.styleSheet()
        self.pvObj = None

    def iValueSet(self, value):
        self.setText(value)

    def iValueGet(self):
        return self.text()

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

#===============================================================================
# iQLineEdit
#===============================================================================
class iQLineEdit(QtGui.QLineEdit):
    """
    iQLineEdit is extended QtGui.QLineEdit that is aware of PV property changes.
    """

    def __init__(self, text = ''):
        QtGui.QLineEdit.__init__(self, text)
        iLog.info("enter")

        self.defaultLook = self.styleSheet()
        self.pvObj = None

    def iValueSet(self, value):
        self.setText(value)

    def iValueGet(self):
        return self.text()

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

#===============================================================================
# iQComboBox
#===============================================================================
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

    def iValueSet(self, value):
        value = value - 1
        self.setCurrentIndex(value)

    def iValueGet(self):
        return self.currentIndex() - 1

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

#===============================================================================
# iQTableWidgetItem
#===============================================================================
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

    def iValueSet(self, value):
        return self._widget.iValueSet(value)

    def iValueGet(self):
        return self._widget.iValueGet()

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

#===============================================================================
# iQTreeWidgetItem
#===============================================================================
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

    def iValueSet(self, value):
        return self._widget.iValueSet(value)

    def iValueGet(self):
        return self._widget.iValueGet()

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


class iQGraphicsView(QtGui.QGraphicsView):
    """
    iQGraphicsView is extended QtGui.QGraphicsView that is aware of PV property changes.
    """

    def __init__(self, parent = None):
        QtGui.QGraphicsView.__init__(self, parent)
        iLog.info("enter")

        self.iWidgets = []
        self.yMax = 0
        self.yScale = 10000
        self.iXslice = 0

        self.range = [(0, 0), (0, 0)]
        self.scene = QtGui.QGraphicsScene()
        self.setScene(self.scene)

        self.boundingrect = QtGui.QGraphicsRectItem(0, 0, 0, 0)
        self.centerLine = QtGui.QGraphicsLineItem(0, 0, 0, 0)

        self.scene.addItem(self.boundingrect)
        self.scene.addItem(self.centerLine)

    def mousePressEvent(self, event):
        iLog.info("x %d, y %d" % (event.x(), event.y()))
        self.range[0] = (event.x(), event.y())

    def mouseReleaseEvent(self, event):
        iLog.info("x %d, y %d" % (event.x(), event.y()))
        self.range[1] = (event.x(), event.y())

    def resizeEvent(self, event):
        iLog.debug("enter")

        w = self.width()
        h = self.height()
        iLog.info("graphics view w %d, h %d" % (w, h))

        self.scene.setSceneRect(0, 0, w - 10, h - 10)
        self.boundingrect.setRect(5, 5, w - 20, h - 20)
        y2 = h / 2
        self.centerLine.setLine(0, y2, w - 10, y2)

        if len(self.iWidgets):
            self.iXslice = int(w / (len(self.iWidgets) + 1))

        self.setYMaxValue(self.yMax, True)


        # Refresh the plot
        self.positionWidgets()
        #self.showWidgets()

    def addWidget(self, widget):
        widget.iIndexSet(len(self.iWidgets))
        self.iWidgets.append(widget)
        self.iXslice = int(self.width() / (len(self.iWidgets) + 1))

        # Refresh the plot
        self.positionWidgets()

    def showWidgets(self, start = None, end = None):
        for w in self.iWidgets:
            w.show()

    def positionWidgets(self, start = None, end = None):
        for w in self.iWidgets:
            w.setPos()

    def setYMaxValue(self, value, force = False):
        iLog.debug("enter")

        if not value:
            return

        value = abs(int(value))

        iLog.info("old Y max %d" % (self.yMax))
        if self.yMax < value:
            self.yMax = value
            force = True
            iLog.info("new Y max %d" % (self.yMax))

        if force:
            self.ySpan = int(self.height() / 2) - 20
            self.yScale = int(self.yMax / self.ySpan)
            iLog.info("new Y scale %d, Y span %d" % (self.yScale, self.ySpan))

            # Refresh the plot
            self.positionWidgets()

class iQGraphicsWidget(QtGui.QGraphicsWidget):
    """
    iQGraphicsWidget is extended QtGui.QGraphicsWidget that is aware of PV property changes.
    """

    def __init__(self, view, pvObj):
        QtGui.QGraphicsWidget.__init__(self)
        iLog.info("enter")

        self.pvObj = pvObj
        self.iIndex = 0
        self.iView = view

        self.line = QtGui.QGraphicsLineItem(0, 0, 0, 0)
        self.bubble = QtGui.QGraphicsEllipseItem(0, 0, 0, 0)
        #self.cross = QtGui.QGraphicsEllipseItem(0, 0, 0, 0)

        # Tooltip has name and value
        tip = "%s: <b>UDF</b> <i>(UDF)</i>" % (self.pvObj.nameGetFull())
        self.bubble.setToolTip(tip)
        #self.cross.setToolTip(tip)

        view.scene.addItem(self.line)
        view.scene.addItem(self.bubble)

    #def iValueSet(self, value):
    #    self.setText(value)

    def iValueGet(self):
        return self.y()

    def iIndexSet(self, iIndex):
        self.iIndex = iIndex

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
        iLog.info("Called for pvObj=%s pvName=%s, pvValue=%s, pvConnected=%s" %
                   (pvObj, pvObj.nameGetFull(), pvObj.value, pvObj.connected))

        if self.pvObj != pvObj:
            if self.pvObj:
                self.pvObj.disconnectOneShotSignal(self.slotOneShot)
            self.pvObj = pvObj

        self.setPos()

    @QtCore.pyqtSlot('QObject*')
    def slotPeriodic(self, pvObj):
        """
        Triggered by iPVObj slotPeriodic() signal when value changes.
        Takes iPVObj as argument.
        """

        iLog.debug("enter")
        iLog.info("Called for pvName=%s, pvValue=%s, pvConnected=%s" %
                   (pvObj.nameGetFull(), pvObj.value, pvObj.connected))

        if self.pvObj != pvObj:
            if self.pvObj:
                self.pvObj.disconnectOneShotSignal(self.slotOneShot)
            self.pvObj = pvObj

        self.setPos()

    def connectPVObj(self, pvObj, periodic = False):
        iLog.debug("enter")

        if not periodic:
            pvObj.connectOneShotSignal(self.slotOneShot)
        else:
            pvObj.connectPeriodicSignal(self.slotPeriodic)

    def disconnectPVObj(self, pvObj, periodic = False):
        iLog.debug("enter")

        if not periodic:
            pvObj.disconnectOneShotSignal(self.slotOneShot)
        else:
            pvObj.disconnectPeriodicSignal(self.slotPeriodic)

    def setPos(self):
        iLog.debug("enter")

        if not self.pvObj:
            iLog.warning("called before self.pvObj was set?!?!")
            return

        xPos = int(self.iView.iXslice * (self.iIndex + 1))
        yPosMiddle = int(self.iView.height() / 2)
        # Initial position
        yPosOther = yPosMiddle

        iLog.info("%s: value %s, xPos %d, yPosMiddle %d, yPosOther %d" %
                   (self.pvObj.nameGetFull(), self.pvObj.value, xPos, yPosMiddle, yPosOther))

        if self.pvObj.value:
            self.iView.setYMaxValue(self.pvObj.value)

            yValue = int(self.pvObj.value)

            # FIXME!!!
            yScale = self.iView.yScale

            if yValue != 0:
                yPosOther = yPosMiddle - int(yValue / yScale)

            iLog.info("%s: value %s, xPos %d, yPosMiddle %d, yPosOther %d, yScale %d" %
                   (self.pvObj.nameGetFull(), self.pvObj.value, xPos, yPosMiddle, yPosOther, yScale))


        self.line.setLine(xPos, yPosMiddle, xPos, yPosOther)
        self.bubble.setRect(xPos - 4, yPosOther - 3, 8, 5)

        if self.pvObj.connected:
            self.bubble.setBrush(QtGui.QColor(0, 255, 0, 160))
            tip = "%s: <b>%s</b> <i>(connected)</i>" % (self.pvObj.nameGetFull(), self.pvObj.value)
        else:
            self.bubble.setBrush(QtGui.QColor(255, 0, 0, 160))
            tip = "%s: <b>%s</b> <b><i>(UNCONNECTED)</i><b>" % (self.pvObj.nameGetFull(), self.pvObj.value)

        # Tooltip has name and value
        self.bubble.setToolTip(tip)
