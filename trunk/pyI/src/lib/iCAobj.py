'''
Created on Jun 8, 2011

@author: hinko
'''


class iCAobj(object):
    def __init__(self, pvName, pvPutValue = None):
        self.pvName = pvName
        self.pvGetValue = None
        self.pvPutValue = pvPutValue
        self.success = None
        self.monitor = None
