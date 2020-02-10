import re
import requests
from requests.adapters import HTTPAdapter
from datajoint.errors import DataJointError
import pymysql as client

HUB_PROTOCOL = 'hub://'
REQUEST_PROTOCOL = 'https://'
API_ROUTE = '/api'
API_TARGETS = dict(PROJECT='/project')

session = requests.Session()
session.mount(REQUEST_PROTOCOL, HTTPAdapter(max_retries=3))


def get_host_hook(host_input):
    hub_path = re.findall('/[:._\-a-zA-Z0-9]+', host_input)
    if re.match(HUB_PROTOCOL, host_input) and len(hub_path) > 2:
        try:
            resp = session.get('{}{}{}{}'.format(REQUEST_PROTOCOL,
                hub_path[0][1:], API_ROUTE, API_TARGETS['PROJECT']),
                params={'org_name': hub_path[1][1:], 'project_name': hub_path[2][1:]},
                timeout=10)
            if resp.status_code == 200:
                return resp.json()[0]['database_dsn']
            elif resp.status_code == 204:
                raise DataJointError(
                    'DataJoint Hub database resource `{}/{}/{}` not found.'.format(
                    hub_path[0][1:], hub_path[1][1:], hub_path[2][1:]))
            elif resp.status_code == 404:
                raise DataJointError(
                    'DataJoint Hub endpoint `{}{}{}{}` unavailable.'.format(
                    REQUEST_PROTOCOL, hub_path[0][1:], API_ROUTE, API_TARGETS['PROJECT']))
        except requests.exceptions.SSLError:
            raise DataJointError(
                'TLS security violation on DataJoint Hub target `{}{}{}`.'.format(
                REQUEST_PROTOCOL, hub_path[0][1:], API_ROUTE))
        except requests.exceptions.ConnectionError:
            raise DataJointError(
                'Unable to reach DataJoint Hub target `{}{}{}`.'.format(
                REQUEST_PROTOCOL, hub_path[0][1:], API_ROUTE))
    elif not re.match('.*/', host_input):
        return host_input
    else:
        raise DataJointError('Malformed database host `{}`.'.format(host_input))


def connect_host_hook(connection_obj):
    try:
        connection_obj.connect()
    except client.err.OperationalError:
        if not connection_obj.is_connected:
            target = [int(v) if i == 1 else v
                for i, v in enumerate(
                get_host_hook(connection_obj.conn_info['host_input']).split(':'))]
            target[1] = connection_obj.conn_info['port'] if len(target) == 1 else target[1]
            if (target[0] != connection_obj.conn_info['host'] or
                    target[1] != connection_obj.conn_info['port']):
                connection_obj.conn_info['host'], connection_obj.conn_info['port'] = target
                connection_obj.connect()
            else:
                raise


# import re
# import requests
# from requests.adapters import HTTPAdapter
# from datajoint.errors import DataJointError
# import pymysql as client

# HUB_PROTOCOL = 'hub://'
# REQUEST_PROTOCOL = 'https://'
# API_ROUTE = '/api'
# API_TARGETS = dict(PROJECT='/projects')

# session = requests.Session()
# session.mount(REQUEST_PROTOCOL, HTTPAdapter(max_retries=3))


# def get_host_hook(host_input):
#     hub_path = re.findall('/[:._\-a-zA-Z0-9]+', host_input)
#     if re.match(HUB_PROTOCOL, host_input) and len(hub_path) > 2:
#         try:
#             resp = session.get('{}{}{}{}/{}'.format(REQUEST_PROTOCOL,
#                 hub_path[0][1:], API_ROUTE, API_TARGETS['PROJECT'], hub_path[2][1:]),
#                 params={'org_name': hub_path[1][1:]},
#                 timeout=10)
#             if resp.status_code == 200:
#                 return resp.json()[0]['database_dsn']
#             elif resp.status_code == 404:
#                 raise DataJointError(
#                     'DataJoint Hub database resource `{}/{}/{}` not found.'.format(
#                     hub_path[0][1:], hub_path[1][1:], hub_path[2][1:]))
#             elif resp.status_code == 406:
#                 raise DataJointError(
#                     'DataJoint Hub endpoint `{}{}{}{}` unavailable.'.format(
#                     REQUEST_PROTOCOL, hub_path[0][1:], API_ROUTE, API_TARGETS['PROJECT']))
#         except requests.exceptions.SSLError:
#             raise DataJointError(
#                 'TLS security violation on DataJoint Hub target `{}{}{}`.'.format(
#                 REQUEST_PROTOCOL, hub_path[0][1:], API_ROUTE))
#         except requests.exceptions.ConnectionError:
#             raise DataJointError(
#                 'Unable to reach DataJoint Hub target `{}{}{}`.'.format(
#                 REQUEST_PROTOCOL, hub_path[0][1:], API_ROUTE))
#     elif not re.match('.*/', host_input):
#         return host_input
#     else:
#         raise DataJointError('Malformed database host `{}`.'.format(host_input))


# def connect_host_hook(connection_obj):
#     try:
#         connection_obj.connect()
#     except client.err.OperationalError:
#         if not connection_obj.is_connected:
#             target = [int(v) if i == 1 else v
#                 for i, v in enumerate(
#                 get_host_hook(connection_obj.conn_info['host_input']).split(':'))]
#             target[1] = connection_obj.conn_info['port'] if len(target) == 1 else target[1]
#             if (target[0] != connection_obj.conn_info['host'] or
#                     target[1] != connection_obj.conn_info['port']):
#                 connection_obj.conn_info['host'], connection_obj.conn_info['port'] = target
#                 connection_obj.connect()
#             else:
#                 raise
