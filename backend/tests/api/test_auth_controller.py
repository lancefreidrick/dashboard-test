""" tests.api.test_auth_controller.py """
# pylint: disable=redefined-outer-name,global-statement,unused-argument
# ^^^ this
import json
from tests.utils.token_storage import token_storage

headers = {
    'Content-Type': 'application/json'
}

## LOG IN

def test_login_with_email_password_successfully(client, test_data):
    """
    POST /login
    """
    form = {
        'email': 'cincinnatus@qwikwire.com',
        'password': 'Password123',
        'clientId': 'abcde12345abcde12345abcde12345abcde12345'
    }
    url = '/xqwapi/login'
    response = client.post(url, data=json.dumps(form), headers=headers)
    data = response.json
    assert response.status_code == 200
    assert data is not None
    assert data['authenticationToken'] is not None
    assert data['refreshToken'] is not None

def test_login_with_no_email_password(client, test_data):
    """
    POST /login
    """
    form = {}
    url = '/xqwapi/login'
    response = client.post(url, data=json.dumps(form), headers=headers)
    data = response.json
    assert response.status_code == 401
    assert data is not None
    assert data['message'] == 'Missing credentials'

def test_login_with_no_request_body(client, test_data):
    """
    POST /login
    """
    url = '/xqwapi/login'
    response = client.post(url, headers=headers)
    data = response.json
    assert response.status_code == 400
    assert data is not None
    assert data['message'] == 'Bad request'

def test_login_with_empty_email_and_password(client):
    """
    POST /login
    """
    form = {
        'email': None,
        'password': None,
        'clientId': 'abcde12345abcde12345abcde12345abcde12345'
    }
    url = '/xqwapi/login'
    response = client.post(url, data=json.dumps(form), headers=headers)
    data = response.json
    assert response.status_code == 401
    assert data is not None
    assert data['message'] == 'Missing credentials'

def test_login_user_does_not_exist(client, test_data):
    """
    POST /login
    """
    form = {
        'email': 'cincinna@qwikwire.com',
        'password': 'password',
        'clientId': 'abcde12345abcde12345abcde12345abcde12345'
    }
    url = '/xqwapi/login'
    response = client.post(url, data=json.dumps(form), headers=headers)
    data = response.json
    assert response.status_code == 404
    assert data is not None
    assert data['message'] == 'User does not exist'

def test_login_with_incorrect_password(client, test_data):
    """
    POST /login
    """
    form = {
        'email': 'caesar@qwikwire.com',
        'password': 'password',
        'clientId': 'abcde12345abcde12345abcde12345abcde12345'
    }
    url = '/xqwapi/login'
    response = client.post(url, data=json.dumps(form), headers=headers)
    data = response.json
    assert response.status_code == 401
    assert data is not None
    assert data['message'] == 'Invalid email or password'

def test_login_user_disabled(client, test_data):
    """
    POST /login
    """
    form = {
        'email': 'napoleon@qwikwire.com',
        'password': 'password',
        'clientId': 'abcde12345abcde12345abcde12345abcde12345'
    }
    url = '/xqwapi/login'
    response = client.post(url, data=json.dumps(form), headers=headers)
    data = response.json
    assert response.status_code == 401
    assert data is not None
    assert data['message'] == 'User is deactivated. Please contact administrators'

def test_login_user_as_payer(client, test_data):
    """
    POST /login
    """
    form = {
        'email': 'elizabeth@qwikwire.com',
        'password': 'password',
        'clientId': 'abcde12345abcde12345abcde12345abcde12345'
    }
    url = '/xqwapi/login'
    response = client.post(url, data=json.dumps(form), headers=headers)
    data = response.json
    assert response.status_code == 404
    assert data is not None
    assert data['message'] == 'User does not exist'

## LOG OUT

def test_logout_successfully(client, test_data):
    form = {
        'email': 'caesar@qwikwire.com',
        'password': 'Password123',
        'clientId': 'abcde12345abcde12345abcde12345abcde12345'
    }
    login_response = client.post('/xqwapi/login', data=json.dumps(form), headers=headers)
    assert login_response.status_code == 200
    token = login_response.json['authenticationToken']
    refresh_token = login_response.json['refreshToken']

    logout_response = client.post('/xqwapi/logout', headers={
        'Content-Type': 'application/json',
        'X-Client-Id': 'abcde12345abcde12345abcde12345abcde12345',
        'X-Refresh-Token': refresh_token,
        'Authorization': 'Bearer {}'.format(token)
    })
    assert logout_response.status_code == 200
    assert logout_response.json['message'] == 'Logout successful'

def test_logout_without_token(client, test_data):
    url = '/xqwapi/logout'
    logout_response = client.post(url, headers=headers)
    assert logout_response.status_code == 401
    data = logout_response.json
    assert data is not None
    assert data['message'] == 'Unauthorized access'

def test_logout_with_invalid_token(client, test_data):
    url = '/xqwapi/logout?token=123'
    logout_response = client.post(url, headers=headers)
    assert logout_response.status_code == 401
    data = logout_response.json
    assert data is not None
    assert data['message'] == 'Unauthorized access'

# EXPORT AUTH

def test_export_auth_as_admin_successfully(a_client, test_data):
    """
    POST /auth/<merchant_id>/export
    """
    url = '/xqwapi/auth/export'
    res = a_client.post(url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert 'exportToken' in data

def test_export_auth_as_staff(s_client, test_data):
    """
    POST /auth/<merchant_id>/export
    """
    url = '/xqwapi/auth/export'
    res = s_client.post(url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert 'exportToken' in data

def test_export_auth_as_merchant_admin_successfully(ma_client, test_data):
    """
    POST /auth/<merchant_id>/export
    """
    url = '/xqwapi/auth/export'
    res = ma_client.post(url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert 'exportToken' in data

def test_export_auth_as_merchant_staff(ms_client, test_data):
    """
    POST /auth/<merchant_id>/export
    """
    url = '/xqwapi/auth/export'
    res = ms_client.post(url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data['message'] == 'You are not allowed here'

def test_export_auth_without_token(client, test_data):
    """
    POST /auth/<merchant_id>/export
    """
    url = '/xqwapi/auth/export'
    res = client.post(url, headers={
        'Content-Type': 'application/json'
    })
    data = res.json
    assert res.status_code == 401
    assert data['message'] == 'Unauthorized access'
