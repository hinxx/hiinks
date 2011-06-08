'''
Created on Jun 8, 2011

@author: hinko
'''

import threading, Queue

class iThreader:
    def __init__(self, numthreads, workDoneCB):
        self._numthreads = numthreads
        self.workDoneCB = None

        if callable(workDoneCB):
            self.workDoneCB = workDoneCB
            print "iThreader.init: workDoneCB=", workDoneCB

    def get_data(self):
        raise NotImplementedError, "You must implement get_data as a function that returns an iterable"
        raise RuntimeError

    def handle_data(self, data):
        raise NotImplementedError, "You must implement handle_data as a function that returns anything"
        raise RuntimeError

    def handle_result(self, data, result):
        raise NotImplementedError, "You must implement handle_result as a function that does anything"
        raise RuntimeError

    def _handle_data(self):
        while 1:
            x = self.Q.get()
            if x is None:
                break
            self.DQ.put((x, self.handle_data(x)))

    def _handle_result(self):
        while 1:
            x, xa = self.DQ.get()
            if x is None:
                break
            self.handle_result(x, xa)

    def run(self):
        if hasattr(self, "prerun"):
            self.prerun()

        self.Q = Queue.Queue()
        self.DQ = Queue.Queue()

        ts = []
        for x in range(self._numthreads):
            t = threading.Thread(target = self._handle_data)
            t.start()
            ts.append(t)

        at = threading.Thread(target = self._handle_result)
        at.start()

        try :
            for x in self.get_data():
                self.Q.put(x)
        except NotImplementedError, e:
            print e

        for x in range(self._numthreads):
            self.Q.put(None)

        for t in ts:
            t.join()

        self.DQ.put((None, None))
        at.join()

        if hasattr(self, "postrun"):
            return self.postrun()
        return None

"""
based on http://code.activestate.com/recipes/302746-simplest-useful-i-hope-thread-pool-example/

Justin A 6 years, 9 months ago  # | flag

I like my version better :-).

import threading,Queue
import socket

import socket
#import time,random # temp

class Threader:
    def __init__(self, numthreads):
        self._numthreads=numthreads

    def get_data(self,):
        raise NotImplementedError, "You must implement get_data as a function that returns an iterable"
        return range(10000)
    def handle_data(self,data):
        raise NotImplementedError, "You must implement handle_data as a function that returns anything"
        time.sleep(random.randrange(1,5))
        return data*data
    def handle_result(self, data, result):
        raise NotImplementedError, "You must implement handle_result as a function that does anything"
        print data, result

    def _handle_data(self):
        while 1:
            x=self.Q.get()
            if x is None:
                break
            self.DQ.put((x,self.handle_data(x)))

    def _handle_result(self):
        while 1:
            x,xa=self.DQ.get()
            if x is None:
                break
            self.handle_result(x, xa)

    def run(self):
        if hasattr(self, "prerun"):
            self.prerun()
        self.Q=Queue.Queue()
        self.DQ=Queue.Queue()
        ts=[]
        for x in range(self._numthreads):
            t=threading.Thread(target=self._handle_data)
            t.start()
            ts.append(t)

        at=threading.Thread(target=self._handle_result)
        at.start()

        try :
            for x in self.get_data():
                self.Q.put(x)
        except NotImplementedError, e:
            print e
        for x in range(self._numthreads):
            self.Q.put(None)
        for t in ts:
            t.join()
        self.DQ.put((None,None))
        at.join()
        if hasattr(self, "postrun"):
            return self.postrun()
        return None

Then you can use it like:

from threader import Threader
import time

class ttest(Threader):
    def get_data(self):
        return range(100)

    def handle_data(self,data):
        return data*data

    def handle_result(self, data, result):
        self.res.append((data,result))
        #print "%d: %d" % (data, result)

    def prerun(self):
        self.res=[]
    def postrun(self):
        return self.res



a=ttest(10)
for n,ns in  a.run():
    print n,ns

silly example, but you get the point :-)


"""
