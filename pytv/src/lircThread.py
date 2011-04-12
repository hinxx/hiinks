'''
Created on Apr 10, 2011

@author: hinko
'''

from PyQt4 import QtCore, QtGui, Qt
import pylirc
import time

###############################################################################

# The Worker Thread
# The worker thread is implemented as a PyQt thread rather than a Python thread
# since we want to take advantage of the signals and slots mechanism to
# communicate with the main application.

class LircThread(QtCore.QThread):

    def __init__(self, parent = None, process_name = 'pylirc', config_file = 'pylirc.conf'):

        QtCore.QThread.__init__(self, parent)

        # The exiting attribute is used to tell the thread to stop processing.
        self.exiting = False

        # Process name used in config file
        self.process_name = process_name

        # Config file where lirc buttons are assigned
        self.config_file = config_file


    # Before a Worker object is destroyed, we need to ensure that it stops
    # processing. For this reason, we implement the following method in a
    # way that indicates to the part of the object that performs the
    # processing that it must stop, and waits until it does so.

    def __del__(self):
        print "Deleting pyLirc thread object .."

        self.exiting = True
        self.wait()

    # For convenience, we define a method to set up the attributes required
    # by the thread before starting it.

    def doRun(self, blocking = 0, pollwait = 0.3):

        self.blocking = blocking
        # Time to sleep between calls to pylirc.nextcode(1)
        self.pollwait = pollwait
        # Init pylirc
        pylirc.init(self.process_name, self.config_file, self.blocking)

        # Start the thread
        print "Starting pyLirc thread .."
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

        print "pyLirc thread running .."

        # We draw the number of stars requested as long as the exiting attribute
        # remains False. This additional check allows us to terminate the
        # thread on demand by setting the exiting attribute to True at any time.

        while not self.exiting:

            # For status read we send the main thread information about
            # status where by emitting our custom output() signal:

            s = pylirc.nextcode(1)

            while (s):
                for code in s:
                    #print "Command: %s, Repeat: %d" % (code["config"], code["repeat"])
                    self.emit(QtCore.SIGNAL("key(QString, int)"), code["config"], code["repeat"])

                if self.blocking:
                    s = []
                else:
                    s = pylirc.nextcode(1)


            #print "This is Lirc THREAD.."
            time.sleep(self.pollwait)

        # Clean up pylirc
        pylirc.exit()

    def cancel(self):
        print "Canceling pyLirc thread .."

        self.exiting = True
        self.wait()
