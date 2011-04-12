'''
Created on Apr 10, 2011

@author: hinko
'''

import sys
from PyQt4 import QtCore, QtGui, Qt
import os
import pylirc
import time

from ui.pylirc_ui1 import Ui_MainWindow

#from pyGecko import pyGecko
#import time

class Main(QtGui.QMainWindow):
    '''
    Main GUI class.
    '''

    def __init__(self, parent = None):
        '''
        Initialize Gecko.
        '''
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        print "LIRC remote"

        # Timer version
#        self.count = 0
#        self.blocking = 0
#        pylirc.init("pylirc", "pylirc.conf", self.blocking)
#
#        self.Timer = QtCore.QTimer(self)
#        self.Timer.setInterval(500)
#        QtCore.QObject.connect(self.Timer, QtCore.SIGNAL("timeout()"), self.updateUI1)
#        self.Timer.start(500)

        # Threaded version
        self.lirc_thread = pyLircWorker()
        QtCore.QObject.connect(self.lirc_thread, QtCore.SIGNAL("key(QString, int)"), self.updateUI2)

    def updateUI1(self):
        print "updateUI: called %3d times" % self.count

#        s = self.pylirc.nextcode(1)
        s = pylirc.nextcode(1)

        while (s):
            for code in s:
                print "Command: %s, Repeat: %d" % (code["config"], code["repeat"])
            s = pylirc.nextcode(1)

        self.count += 1



    def updateUI2(self, key, repeat):
        print "updateUI: Lirc: %s %d" % (key, repeat)


###############################################################################

# The Worker Thread
# The worker thread is implemented as a PyQt thread rather than a Python thread
# since we want to take advantage of the signals and slots mechanism to
# communicate with the main application.

class pyLircWorker(QtCore.QThread):

    def __init__(self, parent = None):

        QtCore.QThread.__init__(self, parent)

        # The exiting attribute is used to tell the thread to stop processing.
        self.exiting = False

#        self.gecko = None
        self.pollwait = 0.3
        self.blocking = 0
        pylirc.init("pylirc", "pylirc.conf", self.blocking)
        self.doRun()


    # Before a Worker object is destroyed, we need to ensure that it stops
    # processing. For this reason, we implement the following method in a
    # way that indicates to the part of the object that performs the
    # processing that it must stop, and waits until it does so.

    def __del__(self):

        self.exiting = True
        self.wait()

    # For convenience, we define a method to set up the attributes required
    # by the thread before starting it.

    def doRun(self, gecko = None):

        #self.gecko = gecko
        self.start()

    # The start() method is a special method that sets up the thread and calls
    # our implementation of the run() method. We provide the render() method
    # instead of letting our own run() method take extra arguments because
    # the run() method is called by PyQt itself with no arguments.

    # The run() method is where we perform the processing that occurs in the
    # thread provided by the Worker instance:

    def run(self):

        # Note: This is never called directly. It is called by Qt once the
        # thread environment has been set up.

        print "This is Lirc THREAD.."

        # We draw the number of stars requested as long as the exiting attribute
        # remains False. This additional check allows us to terminate the
        # thread on demand by setting the exiting attribute to True at any time.

        while not self.exiting:

            # For status read we send the main thread information about
            # statuswhere by emitting our custom output() signal:

            #hit = self.gecko.breakpointHit()
            s = pylirc.nextcode(1)

            while (s):
                for code in s:
                    print "Command: %s, Repeat: %d" % (code["config"], code["repeat"])
                    self.emit(QtCore.SIGNAL("key(QString, int)"), code["config"], code["repeat"])

                #s = pylirc.nextcode(1)
                s = []


            #print "This is Lirc THREAD.."
            time.sleep(self.pollwait)

    def cancel(self):
        self.exiting = True
        self.wait()

###############################################################################
#
#
#        MAIN
#
#
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    myapp = Main()
    myapp.show()
    print "Executing!"
    ret = app.exec_()
    print "Ended!"
    sys.exit(ret)
