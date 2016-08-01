from pytest import fixture

from tornado import gen
from tornado.ioloop import IOLoop

from .conftest import TOKEN
from ..async import AsyncJupyterHubClient

@fixture
def client(app, io_loop):
    # include io_loop to avoid clear_instance calls resetting the current loop
    return AsyncJupyterHubClient(TOKEN, url=app.hub.server.url + 'api')

def _run(_test, timeout=10):
    loop = IOLoop.current()
    deadline = loop.time() + timeout
    loop.run_sync(
        lambda : gen.with_timeout(deadline, _test())
    )

def test_list_users(app, io_loop, client):
    @gen.coroutine
    def _test():
        users = yield client.list_users()
        assert sorted(u['name'] for u in users) == ['admin', 'user']
    _run(_test)



