""" tests.api.test_account_controller.py """
# pylint: disable=redefined-outer-name,global-statement,unused-argument
# ^^^ this
import json
import pytest

__token = None
__refresh_token = None
__http_client_id = 'abcde12345abcde12345abcde12345abcde12345'
__users = []

@pytest.fixture
def user_client(client):
    global __token, __refresh_token
    response = client.post('/xqwapi/login', data=json.dumps({
        'email': 'genghis@qwikwire.com',
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

## API: GET ACCOUNT INFO

def test_get_account_info_successfully(user_client, test_data):
    """
    GET /xqwapi/account/info
    """
    res = user_client.get('/xqwapi/account/info', headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data

def test_update_account_information_successfully(user_client, test_data):
    """
    POST /xqwapi/account/info
    """
    res = user_client.post('/xqwapi/account/info', headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'firstname': 'Genghis',
        'lastname': 'Khan',
        'email': 'genghis@qwikwire.com'
    }))
    data = res.json
    assert res.status_code == 200
    assert data['message'] == 'Account information has been updated'
    assert data['person']['firstName'] == 'Genghis'
    assert data['person']['lastName'] == 'Khan'
    assert data['person']['email'] == 'genghis@qwikwire.com'

def test_update_account_password_with_wrong_password(user_client, test_data):
    """
    POST /xqwapi/account/password
    """
    res = user_client.post('/xqwapi/account/password', headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'currentPassword': 'AWrongPassword542',
        'newPassword': 'QwikiePay123'
    }))
    assert res.status_code == 401

def test_update_account_password_with_weak_password(user_client, test_data):
    """
    POST /xqwapi/account/password
    """
    res = user_client.post('/xqwapi/account/password', headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'currentPassword': 'Password123',
        'newPassword': 'easypassword'
    }))
    assert res.status_code == 401

def test_update_account_password_successfully(user_client, test_data):
    """
    POST /xqwapi/account/password
    """
    res = user_client.post('/xqwapi/account/password', headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'currentPassword': 'Password123',
        'newPassword': 'QwikiePay123'
    }))
    data = res.json
    assert res.status_code == 200
    assert data['message'] == 'Account password has been updated'
