'''
Created on Jun 9, 2011

@author: hinko
'''
from iGLobals import iLog, iRaise, iDefaultIOCTreeXMLFile, iDefaultPVTreeXMLFile

import os
import sys
import re
from lxml import etree

#===============================================================================
# COMMENTS
#===============================================================================
# TODO: provide other streams for logging (file, etc)
# TODO: provide other logging logging level to separate (file, etc)
# TODO: provide gui console for log output
#===============================================================================

def xmlToDictParser(xmlFile):
    iLog.debug("enter")

    iLog.debug("parsing XML xmlFile=%s" % xmlFile)
    xmlTree = etree.parse(str(xmlFile))
    if not xmlTree:
        iRaise(None, "Failed to parse XML file %s" % (xmlFile))

    root = xmlTree.getroot()
    itemDict = dict()
    itemDict['__myid__'] = []

    for item in root:

        if item.tag != 'item':
            continue
        itemText = ''
        if item.text:
            itemText = item.text
            itemText = itemText.strip()

        iLog.debug("Item tag='%s', text='%s', attrib='%s'" % (item.tag, itemText, item.attrib))

        itemName = item.get('name')
        propDict = dict()
        propDict['__myid__'] = []

        for prop in item:
            if prop.tag != 'prop':
                continue
            propText = ''
            if prop.text:
                propText = prop.text
                propText = propText.strip()
            iLog.debug(" Prop tag='%s', text='%s', attrib='%s'" % (prop.tag, propText, prop.attrib))

            propName = prop.get('name')
            propDict[propName] = propText
            propDict['__myid__'].append(propName)

        itemDict[itemName] = propDict
        itemDict['__myid__'].append(itemName)

    iLog.info("itemDict from XML file %s ready .." % (xmlFile))
    return itemDict

def xmlToObjectParser(xmlFile, className):
    iLog.debug("enter")

    mod = None

    iLog.debug("className %s" % (className))
    try:
        n = './' + className
        iLog.info("n %s" % (n))
        sys.path.append(os.path.dirname(n))
        mod = __import__(os.path.basename(n))
    finally:
        del sys.path[-1]

    iLog.debug("Class %s module %s" % (className, mod))

    iLog.info("parsing XML xmlFile '%s' into class '%s' (%s)" % (xmlFile, className, mod))
    xmlTree = etree.parse(str(xmlFile))
    if not xmlTree:
        iRaise(None, "Failed to parse XML file %s" % (xmlFile))

    root = xmlTree.getroot()
    itemDict = dict()
    itemDict['__myid__'] = []

    for item in root:

        if item.tag != 'item':
            continue
        itemText = ''
        if item.text:
            itemText = item.text
            itemText = itemText.strip()

        iLog.debug("Item tag='%s', text='%s', attrib='%s'" % (item.tag, itemText, item.attrib))

        itemName = item.get('name')
        propObj = eval("mod." + className + "()")
        propObj.name = itemName
        iLog.debug("propObj %s, name %s" % (propObj, propObj.name))

        for prop in item:
            if prop.tag != 'prop':
                continue
            propText = ''
            if prop.text:
                propText = prop.text
                propText = propText.strip()
            iLog.debug(" Prop tag='%s', text='%s', attrib='%s'" % (prop.tag, propText, prop.attrib))

            propName = prop.get('name')
            if hasattr(propObj, propName):
                setattr(propObj, propName, propText)
            else:
                iLog.error("Object type '%s' has no property '%s'" % (className, propName))

        itemDict[itemName] = propObj
        itemDict['__myid__'].append(itemName)

    iLog.info("itemDict from XML file %s ready .." % (xmlFile))
    return itemDict


def xmlToObjectParser2(xmlFile, className, matchItemName = None):
    iLog.debug("enter")

    mod = None

    iLog.debug("className %s" % (className))
    try:
        n = './' + className
        iLog.info("n %s" % (n))
        sys.path.append(os.path.dirname(n))
        mod = __import__(os.path.basename(n))
    finally:
        del sys.path[-1]

    iLog.debug("Class %s module %s" % (className, mod))

    iLog.debug("parsing XML xmlFile '%s' into class '%s' (%s)" % (xmlFile, className, mod))
    xmlTree = etree.parse(str(xmlFile))
    if not xmlTree:
        iRaise(None, "Failed to parse XML file %s" % (xmlFile))

    root = xmlTree.getroot()

    propObj = eval("mod." + className + "()")

    for item in root:

        found = None

        if item.tag != 'item':
            continue

        itemName = item.get('name')
        if itemName == matchItemName:
            found = item

        itemText = ''
        if item.text:
            itemText = item.text
            itemText = itemText.strip()

        iLog.debug("Item tag='%s', text='%s', attrib='%s'" % (item.tag, itemText, item.attrib))

        if found is None and matchItemName.startswith(itemName):
            iLog.debug("Match '%s' startswith '%s'" % (matchItemName, itemName))

            for prop in item:
                if prop.tag != 'prop':
                    continue
                propName = prop.get('name')
                if (propName == 'getSuffix' or
                    propName == 'putSuffix' or
                    propName == 'cmdSuffix'):
                    propText = ''
                    if prop.text:
                        propText = prop.text
                        propText = propText.strip()

                    iLog.debug("Found prefix '%s' for '%s'" % (propText, itemName))
                    if itemName + propText == matchItemName:
                        found = item
                        break

        if found is None:
            iLog.debug("Item '%s' not OK" % (itemName))
            continue

        # We found our match
        propObj.name = itemName
        iLog.info("propObj %s, name %s" % (propObj, propObj.name))
        for prop in item:
            propText = ''
            if prop.text:
                propText = prop.text
                propText = propText.strip()
            iLog.debug(" Prop tag='%s', text='%s', attrib='%s'" % (prop.tag, propText, prop.attrib))

            propName = prop.get('name')
            if hasattr(propObj, propName):
                if len(propText) == 0:
                    propText = None
                setattr(propObj, propName, propText)
            else:
                iLog.error("Object type '%s' has no property '%s'" % (className, propName))

        iLog.info("item object from XML file %s ready" % (xmlFile))
        return propObj

    iLog.info("item object not found in XML file %s" % (xmlFile))
    return None

def iGetIOC(name):
    iLog.debug("enter")
    return xmlToObjectParser2(iDefaultIOCTreeXMLFile, "iIOCObj", name)

def iGetPV(name):
    iLog.debug("enter")
    return xmlToObjectParser2(iDefaultPVTreeXMLFile, "iPVObj", name)


if __name__ == '__main__':
    #a = xmlToObjectParser2("conf/iPVlist.xml", "iPVObj", ':ENV:ENV_EXTSWITCH')
    #print a.name
    #b = xmlToObjectParser2("conf/iPVlist.xml", "iPVObj", ':ENV:ENV_EXTSWITCH_SP')
    #print b.name
    #c = xmlToObjectParser2("conf/iPVlist.xml", "iPVObj", ':ENV:ENV_EXTSWITCH_MONITOR')
    #print c.name
    d = xmlToObjectParser2("conf/iPVlist.xml", "iPVObj", ':ENV:ENV_EXTSWITCH_BLA')
    print d.name
