from datajoint.plugin import discovered_plugins


def test_check_plugin_status():
    assert(discovered_plugins['raphael_connection_hub']['verified'])
