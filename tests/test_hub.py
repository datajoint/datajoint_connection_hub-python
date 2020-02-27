from datajoint_connection_hub import ConnectionPlugin
import datajoint_connection_hub as hub
import datajoint as dj
from datajoint.errors import DataJointError
from nose.tools import assert_equal, raises
get_host = ConnectionPlugin.get_host


def test_normal_host():
    assert_equal(get_host('1.2.3.4'), '1.2.3.4')
    assert_equal(get_host('1.2.3.4:5678'), '1.2.3.4:5678')
    assert_equal(get_host('Ever.Green_Bear-Creek'), 'Ever.Green_Bear-Creek')
    assert_equal(get_host('Ever.Green_Bear-Creek:1234'), 'Ever.Green_Bear-Creek:1234')


def test_hub_host():
    host_input = 'hub://fakeservices.datajoint.io/datajoint/travis'
    dj.conn(host=host_input, reset=True)
    assert_equal(get_host(host_input), 'fakeservices.datajoint.io:3306')


@raises(DataJointError)
def test_hub_missing_pipeline():
    get_host('hub://fakeservices.datajoint.io/datajoint/test')


@raises(DataJointError)
def test_hub_no_tls():
    get_host('hub://fakeservices.datajoint.io:4000/datajoint/travis')


@raises(DataJointError)
def test_hub_incorrect_protocol():
    get_host('djhub://datajoint/travis')


@raises(DataJointError)
def test_hub_unreachable_server():
    get_host('hub://fakeservices.datajoint.io:4001/datajoint/travis')


@raises(DataJointError)
def test_hub_unreachable_endpoint():
    current = hub.API_TARGETS
    hub.API_TARGETS = {'PIPELINE': '/wrong_one'}
    try:
        get_host('hub://fakeservices.datajoint.io/datajoint/travis')
    except:
        hub.API_TARGETS = current
        raise
