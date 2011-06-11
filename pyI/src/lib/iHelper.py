'''
Created on Jun 9, 2011

@author: hinko
'''
import iConf

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
        raise SystemExit, "domGetElement: invalid nr of elements!"

    return domGetText(tags[0].childNodes)

#===============================================================================
# IOC handling
#===============================================================================

class iIOC(object):
    def __init__(self, name, **kwargs):
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
        print "iIOC.dump:"
        print " .name     ", self.name
        print " .text     ", self.text
        print " .enabled  ", self.enabled
        print " .ip       ", self.ip
        print " .group    ", self.group
        print " .comment  ", self.comment

def iocList(xmlFile = None):
    l = []

    if not xmlFile:
        xmlFile = iConf.iDefaultIOClistXmlFile

    print "pvList: parsing XML file", xmlFile
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

    print "pvList: IOC list: size=", len(l)

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
        print "iPV.dump:"
        print " .name      ", self.name
        print " .text      ", self.text
        print " .enabled   ", self.enabled
        print " .value     ", self.value
        print " .getSuffix ", self.getSuffix
        print " .putSuffix ", self.putSuffix
        print " .cmdSuffix ", self.cmdSuffix
        print " .mode      ", self.mode
        print " .group     ", self.group
        print " .access    ", self.access
        print " .format    ", self.format
        print " .widget    ", self.widget
        print " .strings   ", self.strings
        print " .enums     ", self.enums
        print " .comment   ", self.comment

def pvList(xmlFile = None):
    l = []

    if not xmlFile:
        xmlFile = iConf.iDefaultPVlistXmlFile

    print "pvList: parsing XML file", xmlFile
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
            print "pvList: tag ", tag, "=", txt
            #print "pvList: x", repr(x)

        # .. handle enums - create dict() val: str
        xx = []
        domEnums = domE.getElementsByTagName('enums')
        print "domEnums=", domEnums
        for domEnum in domEnums:
            print "domEnum=", domEnum
            domEnum1 = domEnum.getElementsByTagName('enum')
            print "domEnum1=", domEnum1
            for domEnum2 in domEnum1:
                print "domEnum2=", domEnum2
                v = domEnum2.getAttribute("val")
                s = domEnum2.getAttribute("str")
                xx.append((v, s))
                print "pvList: enum ", v, "=", s
                print "pvList: xx ", repr(xx)

        # set enums dict()
        x['enums'] = xx
        print "pvList: x", repr(x)

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

    print "pvList: IOC list: size=", len(l)

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

    for k, v in kwargs.items():
        for pv in pvList:
            if hasattr(pv, k):
                print "pvListFind: comparing:", eval('pv.' + k), "==", v
                if eval('pv.' + k) == v:
                    return pv
            else:
                raise ValueError, 'pvListFind: invalid key: ' + k

def pvGetName(pv):
    if hasattr(pv, 'getSuffix'):
        if pv.getSuffix:
            return pv.name + pv.getSuffix
    return pv.name

def pvPutName(pv):
    if hasattr(pv, 'putSuffix'):
        if pv.putSuffix:
            return pv.name + pv.putSuffix
    return pv.name

def pvCmdName(pv):
    if hasattr(pv, 'cmdSuffix'):
        if pv.cmdSuffix:
            return pv.name + pv.cmdSuffix
    return pv.name

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

