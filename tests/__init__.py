from hubapi.schema import *
from os import environ
import uuid


def setup_package():
    Org.insert([dict(org_name="datajoint", org_id=uuid.uuid4())])
    db_inst = '{}:3306'.format(environ.get('DJ_HOST', 'fakeservices.datajoint.io'))
    DatabaseInstance.insert([dict(database_dsn=db_inst, database_id=uuid.uuid4())])
    Pipeline.insert([dict(pipeline_name="travis", **(Org & 'org_name="datajoint"').fetch1('KEY'), **(DatabaseInstance & 'database_dsn="{}"'.format(db_inst)).fetch1('KEY'), pipeline_id=uuid.uuid4())])


def teardown_package():
    Pipeline.delete_quick()
    DatabaseInstance.delete_quick()
    Org.delete_quick()
