from pytest import fixture

from .conftest import TOKEN
from ..sync import JupyterHubClient

@fixture(scope='module')
def client(app):
    return JupyterHubClient(TOKEN, url=app.hub.server.url + 'api')

def test_list_users(app, client):
    users = client.list_users()
    assert sorted(u['name'] for u in users) == ['admin', 'user']


    