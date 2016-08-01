"""Fixtures for testing jupyterhub-client"""

import logging

from pytest import fixture

from jupyterhub.tests.conftest import io_loop
from jupyterhub.tests.mocking import MockHub

TOKEN = 'secret-token'

@fixture(scope='module')
def app(request):
    app = MockHub.instance(log_level=logging.DEBUG)
    app.api_tokens = {
        TOKEN: 'admin',
    }
    app.start([])
    def fin():
        MockHub.clear_instance()
        app.stop()
    request.addfinalizer(fin)
    return app
