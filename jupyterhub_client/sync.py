import logging

import requests

from .base import BaseJupyterHubClient

log = logging.getLogger('jupyterhub_client')

class JupyterHubClient(BaseJupyterHubClient):
    """A requests-based wrapper around the JupyterHub REST API"""

    def _impl_init(self):
        self.session = requests.session()
        self.session.headers['Authorization'] = 'token %s' % self._token

    def fetch(self, url, method, body):
        r = self.session.request(method, url, data=body)
        r.raise_for_status()
        # If there's a body, it's JSON
        if r.content:
            return r.json()

__all__ = ['JupyterHubClient']