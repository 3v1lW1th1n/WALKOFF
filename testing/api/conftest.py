import json
import pytest
from starlette.testclient import TestClient

import api.server.app as app


@pytest.fixture
def api():
    app.mongo.erase_db()
    app.mongo.init_db()
    yield TestClient(app.app)
    app.mongo.erase_db()
    app.mongo.init_db()
    # connect_to_redis_pool(config.REDIS_URI).flushall()


@pytest.fixture
def auth_header(api: TestClient):
    response = api.post("http://localhost/walkoff/api/auth/login",
                        data=json.dumps({"username": "admin", "password": "admin"}),
                        headers={'content-type': "application/json"})
    tokens = response.json()
    header = {"Authorization": f"Bearer {tokens['access_token']}",
              "content-type": "application/json"}
    return header


@pytest.fixture
def super_auth_header(api: TestClient):
    response = api.post("http://localhost/walkoff/api/auth/login",
                        data=json.dumps({"username": "super_admin", "password": "super_admin"}),
                        headers={'content-type': "application/json"})
    tokens = response.json()
    header = {"Authorization": f"Bearer {tokens['access_token']}",
              "content-type": "application/json"}
    return header
