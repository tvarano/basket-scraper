
import os
import tempfile

import pytest

import odds


@pytest.fixture
def client():
    db_fd, odds.app.config['DATABASE'] = tempfile.mkstemp()
    odds.app.config['TESTING'] = True
    print("HELLOO")

    yield odds.app.test_client() 

    os.close(db_fd)
    os.unlink(odds.app.config['DATABASE'])

def test_root(client):
    rv = client.get('/')
    print(rv.data)
    assert rv.data == b"why are you here"

def test_scrape(client):
    rv = client.get('/scrape')
    print(rv.data)
    assert True