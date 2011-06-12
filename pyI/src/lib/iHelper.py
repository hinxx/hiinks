'''
Created on Jun 9, 2011

@author: hinko
'''

def _raise(obj, msg, ex = ValueError):
    raise ex, "%s.%s: msg = '%s'" % (obj.__class__.__name__, __name__, msg)
