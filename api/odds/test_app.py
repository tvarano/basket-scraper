
import os
import tempfile
import json
import pytest

import odds


@pytest.fixture
def client():
    db_fd, odds.app.config['DATABASE'] = tempfile.mkstemp()
    odds.app.config['TESTING'] = True

    yield odds.app.test_client() 

    os.close(db_fd)
    os.unlink(odds.app.config['DATABASE'])

def test_root(client):
    rv = client.get('/')
    print(rv.data)
    assert rv.data == b"why are you here"

# def test_scrape(client):
#     rv = client.get('/scrape')
#     print(rv.data)
#     assert False

def test_search(client): 
    rv = client.get('/search')
    print(rv.data)

def test_search_put(client): 
    rv = client.post('/search', data=json.dumps({'Country': 'Germany'}))
    print(rv.data)
    assert False