# normally you should not import plugin first
# this is a hack since nosetests forces source import first
import sys
import importlib
import datajoint
importlib.reload(sys.modules['datajoint'])
import datajoint as dj
from hubapi.schema import *
from os import environ
import uuid


def setup_package():
    Org.insert([dict(org_name="datajoint", org_id=uuid.uuid4())])
    db_inst = '{}:3306'.format(environ.get('DJ_HOST', 'fakeservices.datajoint.io'))
    DatabaseInstance.insert([dict(database_dsn=db_inst, database_id=uuid.uuid4())])
    Project.insert([dict(project_name="travis", **(Org & 'org_name="datajoint"').fetch1('KEY'), **(DatabaseInstance & 'database_dsn="{}"'.format(db_inst)).fetch1('KEY'), project_id=uuid.uuid4())])


def teardown_package():
    Project.delete_quick()
    DatabaseInstance.delete_quick()
    Org.delete_quick()
