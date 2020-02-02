# normally you should not import plugin first
# this is a hack since nosetests forces source import first
import sys
import importlib
import datajoint
importlib.reload(sys.modules['datajoint'])
import datajoint as dj
