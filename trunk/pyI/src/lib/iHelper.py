'''
Created on Jun 9, 2011

@author: hinko
'''

class iIOC(object):
    def __init__(self, name, **kwargs):
        self.name = name
        self.ip = None
        self.group = 'default'
        self.rack = 'default'

        for k, v in kwargs.items():
            if k == 'group':
                self.group = v
            elif k == 'rack':
                self.rack = v
            elif k == 'ip':
                self.ip = v
            else:
                raise ValueError, 'iIOC: invalid key:', k

    def dump(self):
        print "iIOC.dump:"
        print " .name     ", self.name
        print " .ip       ", self.ip
        print " .group    ", self.group
        print " .rack     ", self.rack

def iocList():
    iocList = []
    ioc = iIOC("hinkoHost")
    iocList.append(ioc)
    ioc = iIOC("hinkoHost1")
    iocList.append(ioc)
    ioc = iIOC("hinkoHost2")
    iocList.append(ioc)
    ioc = iIOC("hinkoHost3")
    iocList.append(ioc)

    return iocList

class iPV(object):
    def __init__(self, name, pv, **kwargs):
        self.name = name
        self.pv = pv

        # Supplied in kwargs
        self.getSuffix = None
        self.putSuffix = None
        self.cmdSuffix = None
        self.mode = 'value'
        self.group = 'default'
        self.access = 'read-only'
        self.format = 'str'
        self.widget = None
        self.strings = None

        for k, v in kwargs.items():
            if k == 'group':
                self.group = v
            elif k == 'access':
                self.access = v
            elif k == 'getSuffix':
                self.getSuffix = v
            elif k == 'putSuffix':
                self.putSuffix = v
            elif k == 'cmdSuffix':
                self.cmdSuffix = v
            elif k == 'mode':
                self.mode = v
            elif k == 'format':
                self.format = v
            elif k == 'widget':
                self.widget = v
            elif k == 'strings':
                self.strings = v
            else:
                raise ValueError, 'iPV: invalid key:', k

    def dump(self):
        print "iPV.dump:"
        print " .name      ", self.name
        print " .pv        ", self.pv
        print " .getSuffix ", self.getSuffix
        print " .putSuffix ", self.putSuffix
        print " .cmdSuffix ", self.cmdSuffix
        print " .mode      ", self.mode
        print " .group     ", self.group
        print " .access    ", self.access
        print " .format    ", self.format
        print " .widget    ", self.widget
        print " .strings   ", self.strings

def pvList():
    pvList = []
    pv = iPV("dummy PV 1", ":P:ai1", group = "dummy", access = "read-write", format = "int", widget = 'QLabel')
    pvList.append(pv)
    pv = iPV("dummy PV 2", ":P:ai2", group = "dummy", access = "read-write", format = "int", widget = 'QLineEdit')
    pvList.append(pv)
    pv = iPV("dummy PV 3", ":P:ai3", group = "dummy", access = "read-write", format = "int", widget = 'QComboBox', strings = ['UDF', 'ME', 'BE', 'DE'])
    pvList.append(pv)
    pv = iPV("dummy PV 1 clone", ":P:ai1", group = "dummy2", access = "read-write", format = "int", widget = 'QComboBox', strings = ['ON', 'OFF', 'BITE ME'])
    pvList.append(pv)
    pv = iPV("dummy PV 2 clone", ":P:ai2", group = "dummy2", access = "read-write", format = "int", widget = 'QLineEdit')
    pvList.append(pv)
    pv = iPV("dummy PV 3 clone", ":P:ai3", group = "dummy2", access = "read-write", format = "int", widget = 'QLabel')
    pvList.append(pv)
    pv = iPV("X low", ":ENV:ENV_ILK_X_LOW", getSuffix = "_MONITOR", putSuffix = "_SP", cmdSuffix = "_CMD", mode = "value", group = "Interlock", access = "read-write", format = "int", widget = 'QLineEdit')
    pvList.append(pv)
    pv = iPV("X high", ":ENV:ENV_ILK_X_HIGH", getSuffix = "_MONITOR", putSuffix = "_SP", cmdSuffix = "_CMD", mode = "value", group = "Interlock", access = "read-write", format = "int", widget = 'QLineEdit')
    pvList.append(pv)
    pv = iPV("Set interlock params", ":ENV:ENV_INTERLOCK", getSuffix = "_MONITOR", putSuffix = "_SP", cmdSuffix = "_CMD", mode = "command", group = "Interlock", access = "write-only", format = "int", widget = 'QLabel', strings = ['Apply params'])
    pvList.append(pv)

    return pvList

def pvListFind(pvList, **kwargs):

    for k, v in kwargs.items():
        for pv in pvList:
            if hasattr(pv, k):
                print "pvListFind: comparing:", eval('pv.' + k), "==", v
                if eval('pv.' + k) == v:
                    return pv
            else:
                raise ValueError, 'pvListFind: invalid key:', k

def pvGetName(pv):
    if hasattr(pv, 'getSuffix'):
        if pv.getSuffix:
            return pv.pv + pv.getSuffix
    return pv.pv

def pvPutName(pv):
    if hasattr(pv, 'putSuffix'):
        if pv.putSuffix:
            return pv.pv + pv.putSuffix
    return pv.pv

def pvCmdName(pv):
    if hasattr(pv, 'cmdSuffix'):
        if pv.cmdSuffix:
            return pv.pv + pv.cmdSuffix
    return pv.pv

def pvIsModeValue(pv):
    if hasattr(pv, 'mode'):
        if pv.mode:
            if pv.mode == 'value':
                return True
    return False

def pvIsModeCommand(pv):
    if hasattr(pv, 'mode'):
        if pv.mode:
            if pv.mode == 'command':
                return True
    return False


if __name__ == '__main__':
    print "IOCs:"
    for ioc in iocList():
        ioc.dump()

    print "PVs:"
    for pv in pvList():
        pv.dump()

