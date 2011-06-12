'''
Created on Jun 11, 2011

@author: hinko
'''

from iConf import *

from lxml import etree
from PyQt4 import QtCore

class iXMLTree(QtCore.QObject):
    def __init__(self, parent, xmlFile, tag):
        QtCore.QObject.__init__(self, parent)
        iLog.debug("enter")

        self.xmlFile = xmlFile
        self.xmlTree = _xmlTree(xmlFile)
        self.tag = tag

        if not self.xmlTree:
            raise ValueError, "iXMLTree.init: Failed to load XML file %s" % xmlFile
        if not self.tag:
            raise ValueError, "iXMLTree.init: Element tag needs to be specified!"

    def iProp(self, iName):
        iLog.debug("enter")

        iLog.debug("Looking for iName=%s" % (iName))
        root = self.xmlTree.getroot()

        for child in root:
            iLog.debug("Child self.tag=%s, child.tag=%s, child.name=%s, iName=%s" % (self.tag, child.tag, child.get('name'), iName))

            if child.tag == self.tag and child.get('name') == iName:
                iLog.info("Found element value=%s" % (iName))
                return child

        iLog.warning("Not found iName=%s" % (iName))
        return False

    def iGet(self, iName, iTag):
        iLog.debug("enter")

        iLog.debug("Looking for iName=%s, tag=%s" % (iName, iTag))
        root = self.xmlTree.getroot()

        for child in root:
            iLog.debug("Child self.tag=%s, child.tag=%s, child.name=%s, iName=%s" % (self.tag, child.tag, child.get('name'), iName))

            if child.tag == self.tag and child.get('name') == iName:

                for prop in child:
                    iLog.debug("Looking at element tag=%s, value=%s" % (prop.tag, prop.text))
                    if prop.tag == iTag:
                        iLog.info("Found element tag=%s, value=%s" % (prop.tag, prop.text))
                        # return element text/value
                        return prop.text

        iLog.warning("Not found tag=%s, iName=%s" % (iTag, iName))
        return False

    def iSet(self, iName, iValue, iTag):
        iLog.debug("enter")

        iLog.debug("Looking for iName=%s, tag=%s" % (iName, iTag))
        root = self.xmlTree.getroot()

        if not isinstance(iValue, str):
            iLog.warning("iValue is not string.. trying to use str()..")
            iValue = str(iValue)

        for child in root:
            iLog.debug("Child self.tag=%s, child.tag=%s, child.name=%s, iName=%s" % (self.tag, child.tag, child.get('name'), iName))

            if child.tag == self.tag and child.get('name') == iName:

                for prop in child:
                    iLog.debug("Looking at element tag=%s, value=%s" % (prop.tag, prop.text))
                    if prop.tag == iTag:
                        iLog.debug("Found element tag=%s, value=%s" % (prop.tag, prop.text))
                        # set element text/value
                        prop.text = iValue
                        iLog.info("New value element tag=%s, value=%s" % (prop.tag, prop.text))
                        return True

        iLog.warning("Not found tag=%s, iName=%s" % (iTag, iName))
        return False

    def iGetAttribute(self, iName, iTag):
        iLog.debug("enter")

        iLog.debug("Looking for iName=%s, tag=%s" % (iName, iTag))
        root = self.xmlTree.getroot()

        for child in root:
            iLog.debug("Child self.tag=%s, child.tag=%s, child.name=%s, iName=%s" % (self.tag, child.tag, child.get('name'), iName))

            if child.tag == self.tag and child.get('name') == iName:

                iLog.info("Found attribute attr=%s, value=%s" % (iTag, child.get(iTag)))
                # return element attribute
                return child.get(iTag)

        iLog.warning("Not found tag=%s, iName=%s" % (iTag, iName))
        return False

    def iSetAttribute(self, iName, iValue, iTag):
        iLog.debug("enter")

        iLog.debug("Looking for iName=%s, tag=%s" % (iName, iTag))
        root = self.xmlTree.getroot()

        if not isinstance(iValue, str):
            iLog.warning("iValue is not string.. trying to use str()..")
            iValue = str(iValue)

        for child in root:
            iLog.debug("Child self.tag=%s, child.tag=%s, child.name=%s, iName=%s" % (self.tag, child.tag, child.get('name'), iName))

            if child.tag == self.tag and child.get('name') == iName:

                iLog.debug("Found attribute attr=%s, value=%s" % (iTag, child.get(iTag)))
                # set element attribute
                child.set(iTag, iValue)
                iLog.info("New value attribute attr=%s, value=%s" % (iTag, child.get(iTag)))
                return True

        iLog.warning("Not found tag=%s, iName=%s" % (iTag, iName))
        return False

    def iDump(self, iName):
        iLog.debug("enter")

        iLog.info("%s: %s" % (self.tag, iName))
        root = self.xmlTree.getroot()

        for child in root:
            if child.tag == self.tag and child.get('name') == iName:
                iLog.info("%s %s" % (self.tag, child.get('name')))
                for prop in child:
                    iLog.info("%10s = '%s'" % (prop.tag, prop.text))
                return True

        iLog.warning("Not found iName=%s" % (iName))
        return False

    def tDump(self):
        iLog.debug("enter")

        root = self.xmlTree.getroot()

        for child in root:
            iLog.info("%s %s" % (self.tag, child.get('name')))
            for prop in child:
                iLog.info("%10s = '%s'" % (prop.tag, prop.text))

    def mGet(self, iTag):
        iLog.debug("enter")

        iLog.debug("Looking for tag=%s" % (iTag))
        root = self.xmlTree.getroot()

        txtList = []

        for child in root:
            iLog.debug("Child self.tag=%s, child.tag=%s" % (self.tag, child.tag))

            if child.tag == self.tag:

                for prop in child:
                    iLog.debug("Looking at element tag=%s, value=%s" % (prop.tag, prop.text))
                    if prop.tag == iTag:
                        iLog.info("Found element tag=%s, value=%s" % (prop.tag, prop.text))
                        # append element text/value
                        txtList.append(prop.text)

        if len(txtList) == 0:
            iLog.warning("Not found tag=%s" % (iTag))

        return txtList

    def mGetAttribute(self, iTag):
        iLog.debug("enter")

        iLog.debug("Looking for tag=%s" % (iTag))
        root = self.xmlTree.getroot()

        txtList = []

        for child in root:
            iLog.debug("Child self.tag=%s, child.tag=%s" % (self.tag, child.tag))

            if child.tag == self.tag:

                iLog.info("Found attribute attr=%s, value=%s" % (iTag, child.get(iTag)))
                # append element attribute
                txtList.append(child.get(iTag))

        if len(txtList) == 0:
            iLog.warning("Not found tag=%s" % (iTag))

        return txtList

#===============================================================================
# Common item element attributes / value
#===============================================================================
    def iNameGet(self, iName):
        iLog.debug("enter")
        return self.iGetAttribute(iName, 'name')

    def iNameSet(self, iName, iValue):
        iLog.debug("enter")
        return self.iSetAttribute(iName, iValue, 'name')

    def iValueGet(self, iName):
        iLog.info("enter")
        return self.iGet(iName, 'value')

    def iValueSet(self, iName, iValue):
        iLog.info("enter")
        return self.iSet(iName, iValue, 'value')

    def iEnabledGet(self, iName):
        iLog.debug("enter")
        return self.iGet(iName, 'enabled')

    def iEnabledSet(self, iName, iValue):
        iLog.debug("enter")
        return self.iSet(iName, iValue, 'enabled')

    def xmlOut(self, root = None):
        iLog.info("enter")
        if not root:
            iLog.warning("root not set.. using self.xmlTree")
            root = self.xmlTree.getroot()

        return etree.tostring(root, pretty_print = True)

#===============================================================================
# Method that returns XML tree that iXMLTree uses
#===============================================================================
def _xmlTree(xmlFile):
    iLog.debug("enter")

    if not xmlFile:
        raise ValueError, "xmlTree: Invalid XML file name " + xmlFile
        return None

    iLog.info("parsing XML xmlFile=%s" % xmlFile)
    tree = etree.parse(str(xmlFile))
    if not tree:
        raise ValueError, "xmlTree: Failed to parse XML file " + xmlFile
        return None

    return tree

if __name__ == '__main__':
    def test1():
        ttt = iXMLTree(None, "../conf/iIOClist.xml", "ioc")
        ttt.iNameGet('hinkoHost')
        ttt.iEnabledGet('hinkoHost')
        ttt.iDump('hinkoHost')
        ttt.tDump()

        print "1 ----------------------------"
        ttt.iNameGet('hinkoHost')
        print "2 ----------------------------"
        ttt.iNameSet('hinkoHost', 'foobar')
        print "3 ----------------------------"
        ttt.iNameGet('hinkoHost')
        print "4 ----------------------------"
        ttt.iNameGet('foobar')
        print "5 ----------------------------"
        ttt.iEnabledGet('hinkoHost1')
        print "6 ----------------------------"
        ttt.iEnabledSet('hinkoHost1', "False")
        print "7 ----------------------------"
        ttt.iEnabledGet('hinkoHost1')
        print "8 ----------------------------"
        ttt.tDump()

    test1()
    #test2()
