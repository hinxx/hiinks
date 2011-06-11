'''
Created on Jun 9, 2011

@author: hinko
'''
from iConf import *

#===============================================================================
# XML and DOM handling
#===============================================================================
import xml.dom.minidom

def domGetText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def domGetElement(domObj, tag, default = None):
    tags = domObj.getElementsByTagName(tag)
    if not tags:
        return default
    if len(tags) == 0:
        return default
    if len(tags) != 1:
        raise ValueError, "domGetElement: invalid nr of elements: " + len(tags)

    return domGetText(tags[0].childNodes)

#===============================================================================
# IOC handling
#===============================================================================

class iIOC(object):
    def __init__(self, name, **kwargs):
        iLog.debug("enter")

        self.name = name
        self.ip = None
        self.group = None
        self.text = None
        self.enabled = True
        self.comment = None

        for k, v in kwargs.items():
            if k == 'group':
                self.group = v
            elif k == 'ip':
                self.ip = v
            elif k == 'text':
                self.text = v
            elif k == 'enabled':
                self.enabled = v
            elif k == 'comment':
                self.comment = v
            else:
                raise ValueError, 'iIOC: invalid key: ' + k


    def dump(self):
        iLog.debug(".name     =%s" % self.name)
        iLog.debug(".text     =%s" % self.text)
        iLog.debug(".enabled  =%s" % self.enabled)
        iLog.debug(".ip       =%s" % self.ip)
        iLog.debug(".group    =%s" % self.group)
        iLog.debug(".comment  =%s" % self.comment)

def iocList(xmlFile = None):
    iLog.debug("enter")

    l = []

    if not xmlFile:
        xmlFile = iDefaultIOClistXmlFile

    iLog.debug("parsing XML xmlFile=%s" % xmlFile)
    dom = xml.dom.minidom.parse(xmlFile)
    if not dom:
        raise ValueError, "pvList: Failed to parse XML file " + xmlFile
        return None

    domEs = dom.getElementsByTagName('ioc')

    for domE in domEs:
        domName = domGetElement(domE, 'name')
        if not domName:
            raise ValueError, "pvList: IOC name missing!"
            return None

        # retrieve all the elements, except enums ..
        x = dict()
        for tag in ['name', 'text', 'ip', 'group', 'comment', 'enabled']:
            txt = domGetElement(domE, tag, default = '')
            x[tag] = txt

        # create IOC object
        item = iIOC(x['name'],
                   text = x['text'],
                   ip = x['ip'],
                   group = x['group'],
                   enabled = x['enabled'],
                   comment = x['comment'],
                   )
        l.append(item)

    iLog.debug("IOC item count=%s" % len(l))

    return l

def iocListDummy():
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

#===============================================================================
# PV handling
#===============================================================================
class iPV(object):
    def __init__(self, name, **kwargs):
        iLog.debug("enter")
        self.name = name

        # Supplied in kwargs
        self.getSuffix = None
        self.putSuffix = None
        self.cmdSuffix = None
        self.mode = 'value'
        self.group = None
        self.access = 'read-only'
        self.format = 'str'
        self.widget = None
        self.strings = None
        self.enums = None
        self.enabled = True
        self.comment = None
        self.value = None
        self.text = None

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
            elif k == 'text':
                self.text = v
            elif k == 'enums':
                if isinstance(v, list):
                    self.enums = v
            elif k == 'comment':
                self.comment = v
            elif k == 'enabled':
                if v == 'True' or v == 'true' or v == '1':
                    self.enabled = True
                else:
                    self.enabled = False
            elif k == 'value':
                self.value = v
            else:
                raise ValueError, 'iPV: invalid key:', k

    def dump(self):
        iLog.debug("enter")
        iLog.debug(".name      =%s" % self.name)
        iLog.debug(".text      =%s" % self.text)
        iLog.debug(".enabled   =%s" % self.enabled)
        iLog.debug(".value     =%s" % self.value)
        iLog.debug(".getSuffix =%s" % self.getSuffix)
        iLog.debug(".putSuffix =%s" % self.putSuffix)
        iLog.debug(".cmdSuffix =%s" % self.cmdSuffix)
        iLog.debug(".mode      =%s" % self.mode)
        iLog.debug(".group     =%s" % self.group)
        iLog.debug(".access    =%s" % self.access)
        iLog.debug(".format    =%s" % self.format)
        iLog.debug(".widget    =%s" % self.widget)
        iLog.debug(".strings   =%s" % self.strings)
        iLog.debug(".enums     =%s" % self.enums)
        iLog.debug(".comment   =%s" % self.comment)

def pvList(xmlFile = None):
    iLog.debug("enter")

    l = []

    if not xmlFile:
        xmlFile = iDefaultPVlistXmlFile

    iLog.debug("parsing XML xmlFile=%s" % xmlFile)
    dom = xml.dom.minidom.parse(xmlFile)
    if not dom:
        raise ValueError, "pvList: Failed to parse XML file " + xmlFile
        return None

    domEs = dom.getElementsByTagName('pv')

    for domE in domEs:
        domName = domGetElement(domE, 'name')
        if not domName:
            raise ValueError, "pvList: PV name missing!"
            return None

        # retrieve all the elements of, except enums ..
        x = dict()
        for tag in ['name', 'text', 'group', 'getSuffix', 'putSuffix', 'cmdSuffix',
                    'mode', 'access', 'format', 'widget', 'strings', 'enabled',
                    'value', 'comment']:
            txt = domGetElement(domE, tag, default = '')
            x[tag] = txt

        # .. handle enums - create dict() val: str
        xx = []
        domEnums = domE.getElementsByTagName('enums')
        for domEnum in domEnums:
            domEnum1 = domEnum.getElementsByTagName('enum')
            for domEnum2 in domEnum1:
                v = domEnum2.getAttribute("val")
                s = domEnum2.getAttribute("str")
                xx.append((v, s))

        # set enums dict()
        x['enums'] = xx

        # create PV object
        item = iPV(x['name'],
                   text = x['text'],
                   group = x['group'],
                   getSuffix = x['getSuffix'],
                   putSuffix = x['putSuffix'],
                   cmdSuffix = x['cmdSuffix'],
                   mode = x['mode'],
                   access = x['access'],
                   format = x['format'],
                   widget = x['widget'],
                   strings = x['strings'],
                   enums = x['enums'],
                   enabled = x['enabled'],
                   comment = x['comment'],
                   value = x['value'],
                   )
        l.append(item)
        #item.dump()

    iLog.debug("PV item count=%s" % len(l))

    return l

def pvListDummy():
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
    iLog.debug("enter")

    for k, v in kwargs.items():
        for pv in pvList:
            if hasattr(pv, k):
                #print "pvListFind: comparing:", eval('pv.' + k), "==", v
                if eval('pv.' + k) == v:
                    return pv
            else:
                raise ValueError, 'pvListFind: invalid key: ' + k

        raise ValueError, 'pvListFind: not found: ' + k

def pvGetName(pv):
    #iLog.debug("enter")

    if hasattr(pv, 'getSuffix'):
        if pv.getSuffix:
            iLog.debug("=%s" % pv.name + pv.getSuffix)
            return pv.name + pv.getSuffix

    iLog.debug("=%s" % pv.name)
    return pv.name

def pvPutName(pv):
    #iLog.debug("enter")

    if hasattr(pv, 'putSuffix'):
        if pv.putSuffix:
            iLog.debug("=%s" % pv.name + pv.putSuffix)
            return pv.name + pv.putSuffix

    iLog.debug("=%s" % pv.name)
    return pv.name

def pvCmdName(pv):
    #iLog.debug("enter")

    if hasattr(pv, 'cmdSuffix'):
        if pv.cmdSuffix:
            iLog.debug("=%s" % pv.name + pv.cmdSuffix)
            return pv.name + pv.cmdSuffix

    iLog.debug("=%s" % pv.name)
    return pv.name

def pvIsModeValue(pv):
    #iLog.debug("enter")

    if hasattr(pv, 'mode'):
        if pv.mode:
            if pv.mode == 'value':
                iLog.debug("mode is %s" % pv.mode)
                return True

    iLog.debug("mode is NOT %s" % pv.mode)
    return False

def pvIsModeCommand(pv):
    #iLog.debug("enter")

    if hasattr(pv, 'mode'):
        if pv.mode:
            if pv.mode == 'command':
                iLog.debug("mode is %s" % pv.mode)
                return True

    iLog.debug("mode is NOT %s" % pv.mode)
    return False


if __name__ == '__main__':
    print "IOCs:"
    for ioc in iocList():
        ioc.dump()

    print "PVs:"
    for pv in pvList():
        pv.dump()

