"""Async JupyterHub Client

Each method returns a tornado Future.
"""

import json

from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.ioloop import IOLoop
from tornado import gen

from .base import BaseJupyterHubClient

class AsyncJupyterHubClient(BaseJupyterHubClient):
    def _impl_init(self, client=None):
        if client is None:
            client = AsyncHTTPClient()
        self._client = client

    @gen.coroutine
    def fetch(self, url, method, body):
        request = HTTPRequest(url,
            method=method,
            headers={
                'Authorization': 'token %s' % self._token,
            },
            body=body,
            )
        resp = yield self._client.fetch(request)
        if resp.body:
            return json.loads(resp.body.decode('utf8'))
