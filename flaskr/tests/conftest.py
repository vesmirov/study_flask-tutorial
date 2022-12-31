import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    # creates and opens a temp file, returning the file descriptor and the path
    db_fb, db_path = tempfile.mkstemp()

    # overrides the database path and tells flask that the app is in test mode
    app = create_app({'TESTING': True, 'DATABASE': db_path})
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fb)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """creates a test client, which allows us to exclude a server startup"""

    return app.test_client()


@pytest.fixture
def runner(app):
    """creates a runner, that can call the Click commands registered with the application"""

    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self.client = client

    def login(self, username='test', password='test'):
        return self.client.post('/auth/login/', data={'username': username, 'password': password})

    def logout(self):
        return self.client.get('/auth/logout/')


@pytest.fixture
def auth(client):
    """allows to log in as the test user"""

    return AuthActions(client)
