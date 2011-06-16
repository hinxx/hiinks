'''
Created on Jun 12, 2011

@author: hinko
'''

from iHelper import iLog, iDefaultIOCTreeXMLFile

from iXMLTree import iXMLTree

class iIOCTree(iXMLTree):
    def __init__(self, parent, xmlFile = None, tag = 'ioc'):
        if not xmlFile:
            xmlFile = iDefaultIOCTreeXMLFile
        iXMLTree.__init__(self, parent, xmlFile, tag)
        iLog.debug("enter")
