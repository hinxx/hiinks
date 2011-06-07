'''
Created on Jun 7, 2011

@author: hinko
'''
import os
import sys
import time

from PyQt4 import QtCore, QtGui, Qt

from ui.clipboard1 import Ui_MainWindow


class Main(QtGui.QMainWindow):

    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, None)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        QtCore.QObject.connect(self.ui.pushButton_get,
                               QtCore.SIGNAL("clicked()"), self.pvGet)

    def pvGet(self):
#        self.iocName = "iocName"
#        self.pvName = "pvName"
#        print "iPVSingle.pvGet: IOC=", self.iocName, ", PV=", self.pvName

#        self.iocName = self.ui.lineEdit_iocName.text()
#        self.pvName = self.ui.lineEdit_pvName.text()
#        print "iPVSingle.pvGet: self.IOC=", self.iocName, ", self.PV=", self.pvName

        iocName = str(self.ui.lineEdit_iocName.text())
        pvName = str(self.ui.lineEdit_pvName.text())
        print "iPVSingle.pvGet: self.IOC=", iocName, ", self.PV=", pvName


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

