# normally you should not import plugin first
# this is a hack since nosetests forces source import first
import sys
import importlib
import datajoint
importlib.reload(sys.modules['datajoint'])
import datajoint as dj
from hubapi.schema import *
from os import environ


def setup_package():
    Org.insert1(['datajoint'])
    db_inst = '{}:3306'.format(environ.get('DJ_HOST', 'fakeservices.datajoint.io'))
    DatabaseInstance.insert1([db_inst])
    Project.insert1(['datajoint', 'travis', db_inst])


def teardown_package():
    Project.delete_quick()
    DatabaseInstance.delete_quick()
    Org.delete_quick()
