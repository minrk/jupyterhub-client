# jupyterhub-client

[![Build Status](https://travis-ci.org/minrk/jupyterhub-client.svg?branch=master)](https://travis-ci.org/minrk/jupyterhub-client)

Example Python client(s) for the JupyterHub REST API.
There's a synchronous client implemented with Requests,
and an async client using tornado coroutines.


## sync example

```bash
export JPY_API_TOKEN=`jupyterhub token`
```

```python
import os
from jupyterhub_client import JupyterHubClient

hub = JupyterHubClient(os.environ['JPY_API_TOKEN'])
users = hub.list_users()
```


## async example

```bash
export JPY_API_TOKEN=`jupyterhub token`
```

```python
import os
from jupyterhub_client.async import AsyncJupyterHubClient
from tornado import gen

@gen.coroutine
def stuff():
    hub = AsyncJupyterHubClient(os.environ['JPY_API_TOKEN'])
    users = yield hub.list_users()
    yield hub.stop_server('bonk')
```

