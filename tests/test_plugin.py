from datajoint.plugin import connection_plugins


def test_check_plugin_status():
    assert(connection_plugins['hub']['verified'])
