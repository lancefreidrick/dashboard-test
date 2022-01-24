""" conftest """
# pylint: disable=redefined-outer-name
import json
import pytest
from app import app
from tests.utils.populate import (
    populate_directory_tables, populate_invoicing_tables,
    populate_auditing_tables, remove_tables_data
)
from tests.utils.token_storage import token_storage

@pytest.fixture
def client(request):
    app.testing = True
    test_client = app.test_client()

    def teardown():
        pass

    request.addfinalizer(teardown)
    return test_client

@pytest.fixture(scope='session')
def test_data():
    print('\nSetting up test data...')
    remove_tables_data()
    populate_directory_tables()
    populate_invoicing_tables()
    populate_auditing_tables()
    yield True
    remove_tables_data()
    print('\nTest data has been removed')


@pytest.fixture
def a_client(client):
    response = client.post('/xqwapi/login', data=json.dumps({
        'email': 'cincinnatus@qwikwire.com',
        'password': 'Password123',
        'clientId': token_storage.client_id
    }), headers={
        'Content-Type': 'application/json'
    })
    token_storage.set_tokens(response.json)
    yield client
    token_storage.clear()


@pytest.fixture(scope='function')
def ma_client(client):
    response = client.post('/xqwapi/login', data=json.dumps({
        'email': 'caesar@qwikwire.com',
        'password': 'Password123',
        'clientId': token_storage.client_id
    }), headers={
        'Content-Type': 'application/json'
    })
    token_storage.set_tokens(response.json)
    yield client
    token_storage.clear()


@pytest.fixture(scope='function')
def ms_client(client):
    response = client.post('/xqwapi/login', data=json.dumps({
        'email': 'marius@qwikwire.com',
        'password': 'Password123',
        'clientId': token_storage.client_id
    }), headers={
        'Content-Type': 'application/json'
    })
    token_storage.set_tokens(response.json)
    yield client
    token_storage.clear()


@pytest.fixture(scope='function')
def mag_client(client):
    response = client.post('/xqwapi/login', data=json.dumps({
        'email': 'brutus@qwikwire.com',
        'password': 'Password123',
        'clientId': token_storage.client_id
    }), headers={
        'Content-Type': 'application/json'
    })
    token_storage.set_tokens(response.json)
    yield client
    token_storage.clear()


@pytest.fixture(scope='function')
def s_client(client):
    response = client.post('/xqwapi/login', data=json.dumps({
        'email': 'augustus@qwikwire.com',
        'password': 'Password123',
        'clientId': token_storage.client_id
    }), headers={
        'Content-Type': 'application/json'
    })
    token_storage.set_tokens(response.json)
    yield client
    token_storage.clear()


@pytest.fixture
def ama_client(client):
    response = client.post('/xqwapi/login', data=json.dumps({
        'email': 'vercingetorix@qwikwire.com',
        'password': 'Password123',
        'clientId': token_storage.client_id
    }), headers={
        'Content-Type': 'application/json'
    })
    token_storage.set_tokens(response.json)
    yield client
    token_storage.clear()

@pytest.fixture
def mma_client(client):
    response = client.post('/xqwapi/login', data=json.dumps({
        'email': 'hannibal@qwikwire.com',
        'password': 'Password123',
        'clientId': token_storage.client_id
    }), headers={
        'Content-Type': 'application/json'
    })
    token_storage.set_tokens(response.json)
    yield client
    token_storage.clear()

@pytest.fixture
def vma_client(client):
    response = client.post('/xqwapi/login', data=json.dumps({
        'email': 'rizal@qwikwire.com',
        'password': 'Password123',
        'clientId': token_storage.client_id
    }), headers={
        'Content-Type': 'application/json'
    })
    token_storage.set_tokens(response.json)
    yield client
    token_storage.clear()
