""" tests.api.test_user_controller.py """
# pylint: disable=redefined-outer-name,global-statement,unused-argument
# ^^^ this
import json
import pytest
from pymongo import MongoClient
from server.config.environment import config

url = '/xqwapi/users'

__token = None
__refresh_token = None
__http_client_id = 'abcde12345abcde12345abcde12345abcde12345'
__users = []

@pytest.fixture
def admin_client(client):
    global __token, __refresh_token
    response = client.post('/xqwapi/login', data=json.dumps({
        'email': 'cincinnatus@qwikwire.com',
        'password': 'Password123',
        'clientId': __http_client_id
    }), headers={
        'Content-Type': 'application/json'
    })
    __token = response.json.get('authenticationToken')
    __refresh_token = response.json.get('refreshToken')
    yield client
    __token = None
    __refresh_token = None

@pytest.fixture
def merchant_admin_client(client):
    global __token, __refresh_token
    response = client.post('/xqwapi/login', data=json.dumps({
        'email': 'caesar@qwikwire.com',
        'password': 'Password123',
        'clientId': __http_client_id
    }), headers={
        'Content-Type': 'application/json'
    })
    __token = response.json.get('authenticationToken')
    __refresh_token = response.json.get('refreshToken')
    yield client
    __token = None
    __refresh_token = None

@pytest.fixture
def merchant_staff_client(client):
    global __token, __refresh_token
    response = client.post('/xqwapi/login', data=json.dumps({
        'email': 'marius@qwikwire.com',
        'password': 'Password123',
        'clientId': __http_client_id
    }), headers={
        'Content-Type': 'application/json'
    })
    __token = response.json.get('authenticationToken')
    __refresh_token = response.json.get('refreshToken')
    yield client
    __token = None
    __refresh_token = None

@pytest.fixture
def staff_client(client):
    global __token, __refresh_token
    response = client.post('/xqwapi/login', data=json.dumps({
        'email': 'augustus@qwikwire.com',
        'password': 'Password123',
        'clientId': __http_client_id
    }), headers={
        'Content-Type': 'application/json'
    })
    __token = response.json.get('authenticationToken')
    __refresh_token = response.json.get('refreshToken')
    yield client
    __token = None
    __refresh_token = None

@pytest.fixture
def another_merchant_admin_client(client):
    global __token, __refresh_token
    response = client.post('/xqwapi/login', data=json.dumps({
        'email': 'vercingetorix@qwikwire.com',
        'password': 'Password123',
        'clientId': __http_client_id
    }), headers={
        'Content-Type': 'application/json'
    })
    __token = response.json.get('authenticationToken')
    __refresh_token = response.json.get('refreshToken')
    yield client
    __token = None
    __refresh_token = None

@pytest.fixture
def get_users(client):
    global __users
    client = MongoClient(host=config.mongodb_host, port=config.mongodb_port)
    __users = client['directory']['users'].find()
    yield client
    __users = []

## API: GET USERS

def test_get_users_as_admin_successfully(admin_client, test_data):
    """
    GET /xqwapi/users
    """
    res = admin_client.get(url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data
    assert data['totalCount'] > 0
    assert data['users'][0]
    assert 'email' in data['users'][0]
    assert 'id' in data['users'][0]
    assert 'firstName' in data['users'][0]
    assert 'lastName' in data['users'][0]
    assert 'scopes' in data['users'][0]
    assert 'systemRole' in data['users'][0]
    assert 'merchantRole' in data['users'][0]

def test_get_users_as_staff_successfully(staff_client, test_data):
    """
    GET /xqwapi/users
    """
    res = staff_client.get(url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data
    assert data['totalCount'] > 0
    assert data['users']
    assert 'email' in data['users'][0]
    assert 'id' in data['users'][0]
    assert 'firstName' in data['users'][0]
    assert 'lastName' in data['users'][0]
    assert 'scopes' in data['users'][0]
    assert 'systemRole' in data['users'][0]

def test_get_users_as_merchant_admin(merchant_admin_client, test_data):
    """
    GET /xqwapi/users
    """
    res = merchant_admin_client.get(url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data['message'] == 'You are not allowed here'


## API: GET USER BY ID

def test_get_user_by_id_as_admin_successfully(admin_client, test_data):
    """
    GET /xqwapi/users/<user_id>
    """
    get_url = '{}/{}'.format(url, '1000002')
    res = admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data
    assert 'email' in data
    assert 'id' in data
    assert 'firstName' in data
    assert 'lastName' in data
    assert 'scopes' in data
    assert 'systemRole' in data
    assert 'merchantRole' in data
    assert 'isEnabled' in data
    assert 'isAccountConfirmed' in data
    assert data['systemRole'][0] == 70
    assert data['merchantRole'][0] == 30

def test_get_higher_user_by_id_as_staff(staff_client, test_data):
    """
    GET /xqwapi/users/<user_id>
    """
    get_url = '{}/{}'.format(url, '1000003')
    res = staff_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data
    assert 'email' in data
    assert 'id' in data
    assert 'firstName' in data
    assert 'lastName' in data
    assert 'scopes' in data
    assert 'systemRole' in data
    assert 'merchantRole' in data
    assert 'isEnabled' in data
    assert 'isAccountConfirmed' in data

def test_get_higher_user_by_id_as_merchant_admin(merchant_admin_client, test_data):
    """
    GET /xqwapi/users/<user_id>
    """
    get_url = '{}/{}'.format(url, '1000004')
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data['message'] == 'You are not allowed here'

def test_get_user_by_id_user_does_not_exist(admin_client, test_data):
    """
    GET /xqwapi/users/<user_id>
    """
    get_url = '{}/{}'.format(url, '1000020')
    res = admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data['message'] == 'User does not exist'

# ## API: CREATE USER

def test_create_user_as_admin_successfully(admin_client, test_data):
    """
    POST /xqwapi/users
    """
    res = admin_client.post(url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'email': 'sulla@qwikwire.com',
        'firstname': 'Lucius Cornelius',
        'lastname': 'Sulla',
        'systemrole': 10,
        'merchantRole': 10,
        'merchant': []
    }))
    data = res.json
    assert res.status_code == 201
    assert data['message'] == 'New user sulla@qwikwire.com created'

def test_create_user_as_staff_successfully(staff_client, test_data):
    """
    POST /xqwapi/users
    """
    res = staff_client.post(url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'email': 'pompey@qwikwire.com',
        'firstname': 'Gnaeus Pompey',
        'lastname': 'Magnus',
        'systemrole': 10,
        'merchant': []
    }))
    data = res.json
    assert res.status_code == 201
    assert data['message'] == 'New user pompey@qwikwire.com created'

def test_create_user_admin_as_staff(staff_client, test_data):
    """
    POST /xqwapi/users
    """
    res = staff_client.post(url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'email': 'crassus@qwikwire.com',
        'firstname': 'Marcus Licinius',
        'lastname': 'Crassus',
        'systemrole': 70,
        'merchantrole': 10,
        'merchant': ['aboitizland', 'alveo']
    }))
    data = res.json
    assert res.status_code == 201
    assert data['message'] == 'New user crassus@qwikwire.com created'

def test_create_user_as_merchant_admin(merchant_admin_client, test_data):
    """
    POST /xqwapi/users
    """
    res = merchant_admin_client.post(url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'email': 'crassus@qwikwire.com',
        'firstname': 'Marcus Licinius',
        'lastname': 'Crassus',
        'systemrole': 70,
        'merchantrole': 10,
        'merchant': ['aboitizland', 'alveo']
    }))
    data = res.json
    assert res.status_code == 403
    assert data['message'] == 'Lower role users cannot create higher role users'

def test_create_user_on_existing_email(admin_client, test_data):
    """
    POST /xqwapi/users
    """
    res = admin_client.post(url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'email': 'caesar@qwikwire.com',
        'firstname': 'Julisu',
        'lastname': 'Caesar',
        'systemrole': 70,
        'merchantrole': 10,
        'merchant': ['aboitizland', 'alveo']
    }))
    data = res.json
    assert res.status_code == 400
    assert data['message'] == 'User with email caesar@qwikwire.com already exists'

def test_create_user_on_empty_email(admin_client, test_data):
    """
    POST /xqwapi/users
    """
    res = admin_client.post(url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'firstname': 'Marcus Licinius',
        'lastname': 'Crassus',
        'systemrole': 70,
        'merchantrole': 10,
        'merchant': ['aboitizland', 'alveo']
    }))
    data = res.json
    assert res.status_code == 400
    assert data['message'] == 'The email is missing'

def test_create_user_on_empty_firstname(admin_client, test_data):
    """
    POST /xqwapi/users
    """
    res = admin_client.post(url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'email': 'crassus@qwikwire.com',
        'lastname': 'Crassus',
        'systemrole': 70,
        'merchantrole': 10,
        'merchant': ['aboitizland', 'alveo']
    }))
    data = res.json
    assert res.status_code == 400
    assert data['message'] == 'The firstname is missing'

def test_create_user_on_empty_lastname(admin_client, test_data):
    """
    POST /xqwapi/users
    """
    res = admin_client.post(url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'email': 'crassus@qwikwire.com',
        'firstname': 'Marcus Licinius',
        'systemrole': 70,
        'merchantrole': 10,
        'merchant': ['aboitizland', 'alveo']
    }))
    data = res.json
    assert res.status_code == 400
    assert data['message'] == 'The lastname is missing'

def test_create_user_on_empty_role(admin_client, test_data):
    """
    POST /xqwapi/users
    """
    res = admin_client.post(url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'email': 'crassus@qwikwire.com',
        'firstname': 'Marcus Licinius',
        'lastname': 'Crassus',
        'merchant': ['aboitizland', 'alveo']
    }))
    data = res.json
    assert res.status_code == 400
    assert data['message'] == 'The systemrole is missing'

def test_create_user_on_invalid_role(admin_client, test_data):
    """
    POST /xqwapi/users
    """
    res = admin_client.post(url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'email': 'crassus@qwikwire.com',
        'firstname': 'Marcus Licinius',
        'lastname': 'Crassus',
        'systemrole': 'abc'
    }))
    data = res.json
    assert res.status_code == 400
    assert data['message'] == 'The user has an invalid role'

## API: UPDATE USER

def test_update_user_as_admin_successfully(admin_client, test_data):
    """
    POST /xqwapi/users
    """
    post_url = '{}/{}'.format(url, '1000006')
    res = admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'firstname': 'Hannibal123',
        'lastname': 'Barca123',
        'systemrole': 70,
        'merchantrole': 20
    }))
    data = res.json
    assert res.status_code == 200
    assert data['message'] == 'User has been updated'

def test_update_user_as_staff_successfully(staff_client, test_data):
    """
    POST /xqwapi/users
    """
    post_url = '{}/{}'.format(url, '1000006')
    res = staff_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'firstname': 'Hannibal',
        'lastname': 'Barca',
        'systemrole': 70,
        'merchantrole': 10
    }))
    data = res.json
    assert res.status_code == 200
    assert data['message'] == 'User has been updated'

def test_update_user_admin_as_staff(staff_client, test_data):
    """
    POST /xqwapi/users
    """
    post_url = '{}/{}'.format(url, '1000003')
    res = staff_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'firstname': 'Lucius',
        'lastname': 'Cincinnatus',
        'systemrole': 10
    }))
    data = res.json
    assert res.status_code == 200
    assert data['message'] == 'User has been updated'

def test_update_user_as_merchant_admin(merchant_admin_client, test_data):
    """
    POST /xqwapi/users
    """
    post_url = '{}/{}'.format(url, '1000003')
    res = merchant_admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'firstname': 'Lucius',
        'lastname': 'Cincinnatus',
        'systemrole': 20
    }))
    data = res.json
    assert res.status_code == 403
    assert data['message'] == 'You are not allowed here'

def test_update_user_as_admin_user_does_not_exist(admin_client, test_data):
    """
    POST /xqwapi/users
    """
    post_url = '{}/{}'.format(url, '1000020')
    res = admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'firstname': 'Lucius',
        'lastname': 'Cincinnatus',
        'systemrole': 20
    }))
    data = res.json
    print(data)
    assert res.status_code == 404
    assert data['message'] == 'User does not exist'

def test_update_user_as_admin_firstname_required(admin_client, test_data):
    """
    POST /xqwapi/users
    """
    post_url = '{}/{}'.format(url, '1000004')
    res = admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'lastname': 'Thurinus',
        'systemrole': 30
    }))
    data = res.json
    assert res.status_code == 400
    assert data['message'] == 'The firstname is missing'

def test_update_user_as_admin_lastname_required(admin_client, test_data):
    """
    POST /xqwapi/users
    """
    post_url = '{}/{}'.format(url, '1000004')
    res = admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'firstname': 'Gaius Octavius',
        'systemrole': 30
    }))
    data = res.json
    assert res.status_code == 400
    assert data['message'] == 'The lastname is missing'

def test_update_user_as_admin_role_required(admin_client, test_data):
    """
    POST /xqwapi/users
    """
    post_url = '{}/{}'.format(url, '1000004')
    res = admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'firstname': 'Gaius Octavius',
        'lastname': 'Thurinus'
    }))
    data = res.json
    assert res.status_code == 400
    assert data['message'] == 'The systemrole is missing'

def test_update_user_as_admin_invalid_role(admin_client, test_data):
    """
    POST /xqwapi/users
    """
    post_url = '{}/{}'.format(url, '1000004')
    res = admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'firstname': 'Gaius Octavius',
        'lastname': 'Thurinus',
        'systemrole': 'abc'
    }))
    data = res.json
    assert res.status_code == 400
    assert data['message'] == 'The user has an invalid role'

def test_update_user_as_admin_with_merchants_successfully(admin_client, test_data):
    """
    POST /xqwapi/users
    """
    post_url = '{}/{}'.format(url, '1000004')
    res = admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'firstname': 'Gaius Octavius',
        'lastname': 'Thurinus',
        'systemrole': 70,
        'merchantrole': 20,
        'merchants': ['rome', 'parthia']
    }))
    data = res.json
    assert res.status_code == 200
    assert data['message'] == 'User has been updated'

def test_update_user_as_admin_with_merchants_do_not_exist(admin_client, test_data):
    """
    POST /xqwapi/users
    """
    post_url = '{}/{}'.format(url, '1000004')
    res = admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'firstname': 'Gaius Octavius',
        'lastname': 'Thurinus',
        'systemrole': 70,
        'merchantrole': 20,
        'merchants': ['romanempirezxc', 'parthiazxc']
    }))
    data = res.json
    assert res.status_code == 400
    assert data['message'] == 'The merchant scopes have invalid value'

def test_update_user_make_admin_with_two_merchants(admin_client, test_data):
    """
    POST /xqwapi/users
    """
    post_url = '{}/{}'.format(url, '1000004')
    res = admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'firstname': 'Gaius Octavius',
        'lastname': 'Thurinus',
        'systemrole': 10,
        'merchants': ['rome', 'parthia']
    }))
    data = res.json
    assert res.status_code == 403
    assert data['message'] == 'Not allowed to select merchants'

## API: DEACTIVATE USER

def test_deactivate_user_as_admin_successfully(admin_client, test_data):
    """
    DELETE /xqwapi/users
    """
    email = 'hannibal@qwikwire.com'
    delete_url = '{}/{}'.format(url, email)
    res = admin_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'email': email
    }))
    data = res.json
    assert res.status_code == 200
    assert data['message'] == 'User {} deactivated'.format(email)

def test_deactivate_user_as_staff(staff_client, test_data):
    """
    DELETE /xqwapi/users
    """
    email = 'hannibal@qwikwire.com'
    delete_url = '{}/{}'.format(url, email)
    res = staff_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'email': email
    }))
    data = res.json
    assert res.status_code == 403
    assert data['message'] == 'You are not allowed here'

def test_deactivate_already_activated_user(admin_client, test_data):
    """
    DELETE /xqwapi/users
    """
    email = 'napoleon@qwikwire.com'
    delete_url = '{}/{}'.format(url, email)
    res = admin_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'email': email
    }))
    data = res.json
    assert res.status_code == 400
    assert data['message'] == 'User already deactivated'

def test_deactivate_unconfirmed_user(admin_client, test_data):
    """
    DELETE /xqwapi/users
    """
    email = 'marcus@qwikwire.com'
    delete_url = '{}/{}'.format(url, email)
    res = admin_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'email': email
    }))
    data = res.json
    assert res.status_code == 400
    assert data['message'] == 'Profile must be confirmed first before deactivating'
