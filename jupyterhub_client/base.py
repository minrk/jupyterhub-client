import logging
from urllib.parse import quote

import requests

log = logging.getLogger('jupyterhub_client')

class BaseJupyterHubClient(object):
    """Base class for JupyterHub API clients"""
    
    def __init__(self, token, *, url='http://127.0.0.1:8081/hub/api', **kwargs):
        self._token = token
        self._api = url.rstrip('/')
        self._impl_init(**kwargs)
    
    def _impl_init(self):
        """Any additional implementation-specific initialization"""
        pass
    
    def _api_request(self, path, method='GET', data=None):
        """Assemble and perform an API request"""
        if not path.startswith('/'):
            path = '/' + path
        url = self._api + path
        if data:
            body = json.dumps(data)
        else:
            body = None
        return self.fetch(url=url, method=method, body=body)
    
    def fetch(self, url, method, body):
        raise NotImplementedError("Must be implemented in a subclass")
    
    def list_users(self):
        """List users"""
        return self._api_request('/users')
    
    def create_users(self, *users):
        """Create one or more users."""
        return self._api_request('/users', method='POST', data=users)

    def delete_user(self, name):
        self._api_request('/users/{name}'.format(name=name), method='DELETE')

    def get_user(self, name):
        self._api_request('/users/{name}'.format(name=name), method='GET')

    def modify_user(self, username, admin=None, name=None):
        """Update an existing user"""

        data = {}
        if admin is not None:
            data['admin'] = admin
        if name is not None:
            data['name'] = name
        if not data:
            raise ValueError("Must specify at last one of name, admin to modify.")
        self._api_request('/users/{name}'.format(name=username), method='PATCH', data=data)

    def create_user(self, name, admin=False):
        """Create a single user"""
        return self.create_users({'name': name, 'admin': admin})

    def stop_server(self, name):
        """Stop a user's server"""
        return self._api_request('/users/{name}/server'.format(name=name), method='DELETE')

    def start_server(self, name):
        """Start a user's server"""
        return self._api_request('/users/{name}/server'.format(name=name), method='POST')

    def list_groups(self):
        """List groups"""
        return self._api_request('/groups')

    def create_group(self, name):
        """Create one or more groups."""
        return self._api_request('/groups/{name}'.format(name=name), method='POST')

    def delete_group(self, name):
        return self._api_request('/groups/{name}'.format(name=name), method='DELETE')

    def get_group(self, name):
        return self._api_request('/groups/{name}'.format(name=name), method='GET')

    def add_group_users(self, group, users):
        """Add users to a group by name"""
        return self._api_request('/groups/{name}/users'.format(name=group), method='POST', data=users)

    def drop_group_users(self, group, users):
        """Remove users from a group by name"""
        return self._api_request('/groups/{name}/users'.format(name=group), method='DELETE', data=users)

    def get_proxy_table(self):
        """Get the proxy's current routing table"""
        return self._api_request('/proxy')
    
    def new_proxy(self, ip=None, port=None, protocol=None, auth_token=None):
        """Point the Hub to a new proxy"""
        data = {}
        if ip:
            data['ip'] = ip
        if port:
            data['port'] = port
        if protocol:
            data['protocol'] = protocol
        if auth_token:
            data['auth_token'] = auth_token
        return self._api_request('/proxy', method='PATCH', data=data)

    def sync_proxy(self):
        """Force the Hub to sync with its proxy"""
        return self._api_request('/proxy', method='POST')

    def check_token(self, token):
        """Identify a user based on an API token"""
        return self._api_request('/authorizations/token/{token}'.format(token=token))

    def check_cookie(self, name, value):
        """Identify a user based on a cookie"""
        name = quote(name, safe='')
        return self._api_request('/authorizations/cookie/{name}'.format(token=token))

    def shutdown(self, proxy=None, servers=None):
        """Shutdown the Hub"""
        data = {}
        if proxy is not None:
            data['proxy'] = proxy
        if servers is not None:
            data['servers'] = servers
        return self._api_request('/shutdown', method='POST', data=data)
