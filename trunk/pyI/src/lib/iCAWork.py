'''
Created on Jun 8, 2011

@author: hinko
'''
from iConf import iLog
from iHelper import _raise

import threading, Queue
from epics import ca, dbr

from iThreader import iThreader

caActionGet = 'get'
caActionPut = 'put'
caActionMonitor = 'monitor'
caActions = (caActionGet, caActionPut, caActionMonitor)

class iCAWork(iThreader):

    def __init__(self,
                 pvList,
                 caAction,
                 numThreads = 1,
                 doneCB = None,
                 monitorCB = None,
                 connectedCB = None):

        iThreader.__init__(self, numThreads)
        iLog.info("enter")

        if not caAction in caActions:
            _raise (self, "Invalid CA action argument '%s'" % (str(caAction)))
            return

        if not isinstance(pvList, list):
            _raise (self, "Invalid PV list argument '%s'" % (type(pvList)))
            return

        if doneCB:
            if not callable(doneCB):
                _raise (self, "Invalid done callback argument '%s'" % (type(doneCB)))
                return

        if monitorCB:
            if not callable(monitorCB):
                _raise (self, "Invalid monitor callback argument '%s'" % (type(monitorCB)))
                return

        iLog.info("connectedCB=%s" % (type(connectedCB)))
        if connectedCB:
            if not callable(connectedCB):
                _raise (self, "Invalid connected callback argument '%s'" % (type(connectedCB)))
                return

        self.caAction = caAction
        self.pvList = dict()

        for pvTuple in pvList:
            if not isinstance(pvTuple, tuple):
                _raise (self, "Invalid PV argument '%s'" % (type(pvTuple)))
                return

            pvName, pvValue = pvTuple
            iLog.info("Adding PV pvName=%s, pvValue=%s" % (pvName, pvValue))

            self.pvList[pvName] = dict({'name': pvName,
                                        'action': self.caAction,
                                        'value': None,
                                        'newValue': pvValue,
                                        'connected': False,
                                        'success': False,
                                        'valid': False,
                                        'monitor': None})

        self.doneCB = doneCB
        self.monitorCB = monitorCB
        self.connectedCB = connectedCB

        iLog.info("done")

    def close(self):
        iLog.info("done")
        self.stopMonitor()

    def get_data(self):
        iLog.info("enter")

        iLog.info("data: %s" % (self.pvList.keys()))
        return self.pvList.keys()

    def _caOnConnectionChange(self, pvname = None, conn = None, chid = None):
        iLog.info("enter")
        ca.show_cache()

        iLog.info("pvName=%s, connected=%s, chid=%s" % (pvname, str(conn), str(chid)))

        return

        pvData = self.pvList[pvname]

        pvData['connected'] = conn
        pvData['success'] = (conn == True)
        pvData['valid'] = True
        if not conn:
            pvData['value'] = None

        if (pvData['connected'] == True and pvData['action'] == caActionMonitor and
                not pvData['monitor']):

            iLog.warning("PV monitor not subscribed for pvName=%s" % (pvname))

            try:
                pvData['monitor'] = ca.create_subscription(chid,
                                                           callback = self._caOnMonitorChange)
            except ca.CASeverityException as caex:
                iLog.error("MONITOR CASeverityException pvName=%s, eventID=%s, exception=%s" % (str(pvname), str(pvData['monitor']), caex))
                ca.show_cache()
            finally:
                iLog.info("MONITOR pvName=%s, eventID=%s" % (str(pvname), str(pvData['monitor'])))

        if pvData['connected'] == True and pvData['action'] != caActionMonitor:
            iLog.warning("PV get/put value is None for pvName=%s" % (pvname))
            pvData['value'] = ca.get(chid)
            iLog.warning("PV get/put value is updated for pvName=%s, pvValue=%s" % (pvname, str(pvData['value'])))

        if hasattr(self.connectedCB, '__call__'):
            self.connectedCB(pvData)

    def _caOnMonitorChange(self, chid = None, status = None, count = None, ftype = None, pvname = None, value = None, **kwds):
        iLog.info("enter")
        ca.show_cache()

        #print "iCAmonitor._caOnMonitorChange:", pvname, value, repr(kwds)
        pvData = self.pvList[pvname]

        pvData['valid'] = True
        pvData['value'] = value
        pvData['connected'] = ca.isConnected(chid)
        pvData['success'] = (status == 1)

        if hasattr(self.monitorCB, '__call__'):
            self.monitorCB(pvData)

    def stopMonitor(self, pvName = None):
        iLog.info("enter")

        if pvName:
            pvData = self.pvList[pvName]

            if not pvData['monitor']:
                iLog.info("No monitor for pvName=%s" % (pvData['name']))
                return

            iLog.info("Stopping monitor for pvName=%s" % (pvData['name']))
            ca.clear_subscription(pvData['monitor'][2])
            ca.flush_io()
            pvData['monitor'] = None
        else:
            for pvData in self.pvList.values():

                if not pvData['monitor']:
                    iLog.info("No monitor for pvName=%s" % (pvData['name']))
                    continue

                iLog.info("Stopping monitor for pvName=%s" % (pvData['name']))
                ca.clear_subscription(pvData['monitor'][2])
                ca.flush_io()
                pvData['monitor'] = None

        ca.flush_io()

    def handle_data(self, pvName):
        iLog.info("enter")

        iLog.info("pvName=%s" % str(pvName))
        if not isinstance(pvName, str):
            _raise (self, "Invalid PV data object argument '%s'" % (type(pvName)))
            return

        pvData = self.pvList[pvName]

        ca.use_initial_context()
        #print "iCAget.handle_data: ca.current_context():", ca.current_context()

        # Try to connect CA channel, but don't wait for completion
        chid = ca.create_channel(pvName, callback = self._caOnConnectionChange)

        if not ca.isConnected(chid):
            #print "iCAget.handle_data: PV not connected! PV=", pvName
            ca.connect_channel(chid, timeout = 2.0)

        if not ca.isConnected(chid):
            #print "iCAget.handle_data: PV still not connected! PV=", pvData.pvName
            iLog.warning("PV still not connected, pvName=%s" % str(pvName))
            #return False
        else:
            pvData['connected'] = True

        #print "iCAget.handle_data: PV is connected, PV=", pvName
        if self.caAction == caActionGet:

            iLog.info("GET pvName=%s" % str(pvName))
            pvData['value'] = ca.get(chid)
            pvData['success'] = True
            #print "iCAget.handle_data: GET value: ", pvData.pvName, "=", pvData.pvGetValue

        elif self.caAction == caActionPut:

            iLog.info("PUT pvName=%s" % str(pvName))
            ret = ca.put(chid, pvData['newValue'], wait = True)
            if ret == 1:
                #print "iCAput.handle_data: PUT value: ", pvData.pvName, "=", pvData.pvPutValue
                pvData['value'] = ca.get(chid)
                #print "iCAput.handle_data: GET value: ", pvData.pvName, "=", pvData.pvGetValue
                pvData['success'] = True

        elif self.caAction == caActionMonitor:

            iLog.info("MONITOR pvName=%s, chid=%s, connected=%s" % (str(pvName), chid, ca.isConnected(chid)))
            # Subscribe to events
            try:
                pvData['monitor'] = ca.create_subscription(chid,
                                                           callback = self._caOnMonitorChange)
            except ca.CASeverityException as caex:
                iLog.error("MONITOR CASeverityException pvName=%s, eventID=%s, exception=%s" % (str(pvName), str(pvData['monitor']), caex))
                ca.show_cache()
            finally:
                #print "pvData['monitor']: ", pvData['monitor']
                iLog.info("MONITOR pvName=%s, eventID=%s" % (str(pvName), str(pvData['monitor'])))

        return True

    def handle_result(self, pvName, result):
        iLog.info("enter")

        pvData = self.pvList[pvName]
        pvData['valid'] = True

        if hasattr(self.monitorCB, '__call__'):
            self.monitorCB(pvData)

    def prerun(self):
        iLog.info("enter")

        #self.res = []

    def postrun(self):
        iLog.info("enter")

        if hasattr(self.doneCB, '__call__'):
            self.doneCB(self.pvList)

        #return self.res


class iCADispatcher(threading.Thread):

    # Worker cache
    _cache = dict({'__seq__': 0})

    def __init__(self, doRun):
        threading.Thread.__init__(self)
        iLog.info("enter")

        self.doRun = doRun
        self.Q = Queue.Queue()

        ca.use_initial_context()
        iLog.info("ca.current_context(): %s" % (ca.current_context()))

    def close(self):
        iLog.info("enter")
        self.doRun = False
        self.destroyWorker()
        self.schedule(None)

    def newWorker(self, pvList, caAction, doneCB = None, monitorCB = None, connectedCB = None):
        iLog.info("enter")

        if not isinstance(pvList, list):
            _raise (self, "Invalid PV list argument '%s'" % (type(pvList)))
            return

        worker = iCAWork(pvList, caAction, len(pvList), doneCB, monitorCB, connectedCB)
        self._cache['__seq__'] += 1
        self._cache[self._cache['__seq__']] = worker

        iLog.info("New worker ready, sequence nr. %d, worker %s" % (self._cache['__seq__'], str(worker)))

        return self._cache['__seq__']

    def destroyWorker(self, seq = None):
        iLog.info("enter")

        if not isinstance(seq, int):
            if seq != None:
                _raise("Invalid sequence argument value, seq = '%s'" % (type(seq)))
                return

        if seq:
            if seq not in self._cache:
                _raise("Invalid sequence argument value, seq = '%s'" % (str(seq)))
                return

            worker = self._cache[seq]
            worker.close()
            del self._cache[seq]
        else:
            for seq, worker in self._cache.items():
                if seq == '__seq__':
                    continue
                worker.close()
                del self._cache[seq]
            self._cache = dict({'__seq__': 0})

    def newGetter(self, pvList, doneCB = None, monitorCB = None, connectedCB = None):
        iLog.info("enter")


        return self.newWorker(pvList, caActionGet, doneCB, monitorCB, connectedCB)

    def newPutter(self, pvList, doneCB = None, monitorCB = None, connectedCB = None):
        iLog.info("enter")

        return self.newWorker(pvList, caActionPut, doneCB, monitorCB, connectedCB)

    def newMonitor(self, pvList, doneCB = None, monitorCB = None, connectedCB = None):
        iLog.info("enter")

        return self.newWorker(pvList, caActionMonitor, doneCB, monitorCB, connectedCB)

    def stopMonitor(self, seq, pvName = None):
        iLog.info("enter")

        if not isinstance(seq, int):
            if seq != None:
                _raise("Invalid sequence argument value, seq = '%s'" % (type(seq)))
                return

        if seq:
            if seq not in self._cache:
                _raise("Invalid sequence argument value, seq = '%s'" % (str(seq)))
                return

            iLog.info("Stopping monitor for pvName=%s" % (str(pvName)))
            worker = self._cache[seq]
            worker.stopMonitor(pvName)

    def schedule(self, seq):
        iLog.info("enter")

        if not isinstance(seq, int):
            if seq != None:
                _raise("Invalid sequence argument value, seq = '%s'" % (type(seq)))
                return

        iLog.info("Starting worker sequence nr. %s" % (str(seq)))
        self.Q.put(seq)

    def run(self):
        iLog.info("enter")

        # Loop until stopped from above
        while self.doRun:
            while 1:
                seq = self.Q.get()
                if seq is None:
                    break

                # Run the work and signal completion
                if seq not in self._cache:
                    _raise("Invalid sequence argument value, seq = '%s'" % (str(seq)))

                worker = self._cache[seq]
                worker.run()

        iLog.info("Finished doRun loop")

        iLog.info("Calling CA finalize")
        ca.finalize_libca()

        iLog.info("leave")
