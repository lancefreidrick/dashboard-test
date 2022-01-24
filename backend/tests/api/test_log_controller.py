""" tests.api.test_plog_controller.py """
# pylint: disable=redefined-outer-name,global-statement,unused-argument
# ^^^ this
import json
import pytest

__token = None
__refresh_token = None
__http_client_id = 'abcde12345abcde12345abcde12345abcde12345'

url = '/xqwapi/logs/{}'

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
def merchant_agent_client(client):
    global __token, __refresh_token
    response = client.post('/xqwapi/login', data=json.dumps({
        'email': 'brutus@qwikwire.com',
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

## API: GET PAYMENT LOGS

def test_get_payment_logs_as_admin_successfully(admin_client, test_data):
    """
    GET /xqwapi/logs/<transaction_id>/invoices/<invoice_id>
    """
    r_id = '9000025'
    t_id = '9000025'
    get_url = '{}/invoices/{}'.format(url.format(t_id), r_id)
    res = admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'logs' in data
    assert 'totalCount' in data
    assert data['totalCount'] == 6

    first_log = data['logs'][0]
    last_log = data['logs'][-1:][0]
    assert 'action' in first_log
    assert 'level' in first_log
    assert 'metadata' in first_log

    assert 'invoiceId' in first_log
    assert 'logId' in first_log
    assert 'content' in first_log
    assert 'createdAt' in first_log
    assert 'createdById' in first_log
    assert 'createdByName' in first_log
    assert 'content' in first_log
    assert 'status' in first_log
    assert 'transactionId' in first_log
    assert 'updatedAt' in first_log
    assert 'updatedById' in first_log
    assert 'updatedByName' in first_log

    assert first_log['logId'] < last_log['logId'] # We return the logs in descending order

def test_get_payment_logs_as_staff_successfully(staff_client, test_data):
    """
    GET /xqwapi/logs/<transaction_id>/invoices/<invoice_id>
    """
    r_id = '9000025'
    t_id = '9000025'
    get_url = '{}/invoices/{}'.format(url.format(t_id), r_id)
    res = staff_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'logs' in data
    assert 'totalCount' in data
    assert data['totalCount'] == 6

    first_log = data['logs'][0]
    last_log = data['logs'][-1:][0]
    assert 'action' in first_log
    assert 'level' in first_log
    assert 'metadata' in first_log

    assert 'invoiceId' in first_log
    assert 'logId' in first_log
    assert 'content' in first_log
    assert 'createdAt' in first_log
    assert 'createdById' in first_log
    assert 'createdByName' in first_log
    assert 'content' in first_log
    assert 'status' in first_log
    assert 'transactionId' in first_log
    assert 'updatedAt' in first_log
    assert 'updatedById' in first_log
    assert 'updatedByName' in first_log

    assert first_log['logId'] < last_log['logId'] # We return the logs in descending order

def test_get_payment_logs_as_merchant_admin_successfully(merchant_admin_client, test_data):
    """
    GET /xqwapi/logs/<transaction_id>/invoices/<invoice_id>
    """
    r_id = '9000025'
    t_id = '9000025'
    get_url = '{}/invoices/{}'.format(url.format(t_id), r_id)
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'logs' in data
    assert 'totalCount' in data
    assert data['totalCount'] == 6

    first_log = data['logs'][0]
    last_log = data['logs'][-1:][0]
    assert 'action' not in first_log
    assert 'level' not in first_log
    assert 'metadata' not in first_log

    assert 'invoiceId' in first_log
    assert 'logId' in first_log
    assert 'content' in first_log
    assert 'createdAt' in first_log
    assert 'createdById' in first_log
    assert 'createdByName' in first_log
    assert 'content' in first_log
    assert 'status' in first_log
    assert 'transactionId' in first_log
    assert 'updatedAt' in first_log
    assert 'updatedById' in first_log
    assert 'updatedByName' in first_log

    assert first_log['logId'] < last_log['logId'] # We return the logs in descending order

def test_get_payment_logs_as_merchant_staff_successfully(merchant_staff_client, test_data):
    """
    GET /xqwapi/logs/<transaction_id>/invoices/<invoice_id>
    """
    r_id = '9000025'
    t_id = '9000025'
    get_url = '{}/invoices/{}'.format(url.format(t_id), r_id)
    res = merchant_staff_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'logs' in data
    assert 'totalCount' in data
    assert data['totalCount'] == 6

    first_log = data['logs'][0]
    last_log = data['logs'][-1:][0]
    assert 'action' not in first_log
    assert 'level' not in first_log
    assert 'metadata' not in first_log

    assert 'invoiceId' in first_log
    assert 'logId' in first_log
    assert 'content' in first_log
    assert 'createdAt' in first_log
    assert 'createdById' in first_log
    assert 'createdByName' in first_log
    assert 'content' in first_log
    assert 'status' in first_log
    assert 'transactionId' in first_log
    assert 'updatedAt' in first_log
    assert 'updatedById' in first_log
    assert 'updatedByName' in first_log

    assert first_log['logId'] < last_log['logId'] # We return the logs in descending order

def test_get_payment_logs_as_merchant_agent_successfully(merchant_agent_client, test_data):
    """
    GET /xqwapi/logs/<transaction_id>/invoices/<invoice_id>
    """
    r_id = '9000025'
    t_id = '9000025'
    get_url = '{}/invoices/{}'.format(url.format(t_id), r_id)
    res = merchant_agent_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'logs' in data
    assert 'totalCount' in data
    assert data['totalCount'] == 6

    first_log = data['logs'][0]
    last_log = data['logs'][-1:][0]

    assert 'action' not in first_log
    assert 'level' not in first_log
    assert 'metadata' not in first_log

    assert 'invoiceId' in first_log
    assert 'logId' in first_log
    assert 'content' in first_log
    assert 'createdAt' in first_log
    assert 'createdById' in first_log
    assert 'createdByName' in first_log
    assert 'content' in first_log
    assert 'status' in first_log
    assert 'transactionId' in first_log
    assert 'updatedAt' in first_log
    assert 'updatedById' in first_log
    assert 'updatedByName' in first_log

    assert first_log['logId'] < last_log['logId'] # We return the logs in descending order

def test_get_payment_logs_without_token(client, test_data):
    """
    GET /xqwapi/logs/<transaction_id>/invoices/<invoice_id>
    """
    r_id = '9000025'
    t_id = '9000025'
    get_url = '{}/invoices/{}'.format(url.format(t_id), r_id)
    res = client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 401
    assert 'message' in data
    assert data['message'] == 'Unauthorized access'

def test_get_payment_logs_payment_does_not_exist(merchant_admin_client, test_data):
    """
    GET /xqwapi/logs/<transaction_id>/invoices/<invoice_id>
    """
    r_id = '90000201023'
    t_id = '9000020192'
    get_url = '{}/invoices/{}'.format(url.format(t_id), r_id)
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert 'message' in data
    assert data['message'] == 'Payment does not exist'

def test_get_payment_logs_with_no_logs(merchant_admin_client, test_data):
    """
    GET /xqwapi/logs/<transaction_id>/invoices/<invoice_id>
    """
    r_id = '3'
    t_id = '9000001'
    get_url = '{}/invoices/{}'.format(url.format(t_id), r_id)
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert 'logs' in data
    assert 'totalCount' in data
    assert not data['logs']
    assert data['totalCount'] == 0

def test_get_payment_logs_as_another_merchant_admin(another_merchant_admin_client, test_data):
    """
    GET /xqwapi/logs/<transaction_id>/invoices/<invoice_id>
    """
    r_id = '9000025'
    t_id = '9000025'
    get_url = '{}/invoices/{}'.format(url.format(t_id), r_id)
    res = another_merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert 'message' in data
    assert data['message'] == 'You are not allowed to get on this method'

## API: SUBMIT PAYMENT LOG

def test_submit_payment_log_as_admin_successfully(admin_client, test_data):
    """
    POST /xqwapi/logs/<transaction_id>/invoices/<invoice_id>
    """
    r_id = '9000018'
    t_id = '9000018'
    post_url = '{}/invoices/{}'.format(url.format(t_id), r_id)
    res = admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'content': 'This is a good content right here.'
    }))
    data = res.json
    assert res.status_code == 201
    assert 'message' in data
    assert data['message'] == 'Submitted log has been saved'

def test_submit_payment_log_as_staff_successfully(staff_client, test_data):
    """
    POST /xqwapi/logs/<transaction_id>/invoices/<invoice_id>
    """
    r_id = '9000018'
    t_id = '9000018'
    post_url = '{}/invoices/{}'.format(url.format(t_id), r_id)
    res = staff_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'content': 'This is a better content, probably.'
    }))
    data = res.json
    assert res.status_code == 201
    assert 'message' in data
    assert data['message'] == 'Submitted log has been saved'

def test_submit_payment_log_as_merchant_admin_successfully(merchant_admin_client, test_data):
    """
    POST /xqwapi/logs/<transaction_id>/invoices/<invoice_id>
    """
    r_id = '9000018'
    t_id = '9000018'
    post_url = '{}/invoices/{}'.format(url.format(t_id), r_id)
    res = merchant_admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'content': 'This is just not another log here.'
    }))
    data = res.json
    assert res.status_code == 201
    assert 'message' in data
    assert data['message'] == 'Submitted log has been saved'

def test_submit_payment_log_as_merchant_staff_successfully(merchant_staff_client, test_data):
    """
    POST /xqwapi/logs/<transaction_id>/invoices/<invoice_id>
    """
    r_id = '9000018'
    t_id = '9000018'
    post_url = '{}/invoices/{}'.format(url.format(t_id), r_id)
    res = merchant_staff_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'content': 'Another log bites the dust\n\nThen another one, another one'
    }))
    data = res.json
    assert res.status_code == 201
    assert 'message' in data
    assert data['message'] == 'Submitted log has been saved'

def test_submit_payment_log_as_merchant_agent_successfully(merchant_agent_client, test_data):
    """
    POST /xqwapi/logs/<transaction_id>/invoices/<invoice_id>
    """
    r_id = '9000018'
    t_id = '9000018'
    post_url = '{}/invoices/{}'.format(url.format(t_id), r_id)
    res = merchant_agent_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'content': 'The log is blowin\' in the wind...'
    }))
    data = res.json
    assert res.status_code == 201
    assert 'message' in data
    assert data['message'] == 'Submitted log has been saved'

def test_submit_payment_log_as_another_merchant_admin(another_merchant_admin_client, test_data):
    """
    POST /xqwapi/logs/<transaction_id>/invoices/<invoice_id>
    """
    r_id = '9000018'
    t_id = '9000018'
    post_url = '{}/invoices/{}'.format(url.format(t_id), r_id)
    res = another_merchant_admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'content': 'King and Queen of logs'
    }))
    data = res.json
    assert res.status_code == 403
    assert 'message' in data
    assert data['message'] == 'You are not allowed to get on this method'

def test_submit_payment_log_payment_does_not_exist(merchant_admin_client, test_data):
    """
    POST /xqwapi/logs/<transaction_id>/invoices/<invoice_id>
    """
    r_id = '90000181231'
    t_id = '900001812124'
    post_url = '{}/invoices/{}'.format(url.format(t_id), r_id)
    res = merchant_admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'content': 'Now the night has gone, now the night has gone away...'
    }))
    data = res.json
    assert res.status_code == 404
    assert 'message' in data
    assert data['message'] == 'Payment does not exist'

def test_submit_payment_log_on_long_content_successfully(merchant_admin_client, test_data):
    """
    POST /xqwapi/logs/<transaction_id>/invoices/<invoice_id>
    """
    r_id = '9000018'
    t_id = '9000018'
    post_url = '{}/invoices/{}'.format(url.format(t_id), r_id)
    res = merchant_admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'content': (
            'I know your eyes in the morning sun,\
            I feel you touch me in the pouring rain\
            and the moment that you wander far from me\
            I wanna feel you in my arms again\
            And you come to me on a summer breeze\
            Keep me warm in your love then you softly leave'
        )
    }))
    data = res.json
    assert res.status_code == 201
    assert 'message' in data
    assert data['message'] == 'Submitted log has been saved'

## API: REMOVE PAYMENT LOG

def test_remove_payment_log_as_admin_successfully(admin_client, test_data):
    """
    DELETE /xqwapi/logs/<transaction_id>/invoices/<invoice_id>/<log_id>/logs
    """
    r_id = '9000018'
    t_id = '9000018'
    l_id = '10000011'
    delete_url = '{}/invoices/{}/logs/{}'.format(url.format(t_id), r_id, l_id)
    res = admin_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert 'message' in data
    assert data['message'] == 'Log has been removed'

def test_remove_payment_log_as_staff_successfully(staff_client, test_data):
    """
    DELETE /xqwapi/logs/<transaction_id>/invoices/<invoice_id>/<log_id>/logs
    """
    r_id = '9000018'
    t_id = '9000018'
    l_id = '10000012'
    delete_url = '{}/invoices/{}/logs/{}'.format(url.format(t_id), r_id, l_id)
    res = staff_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert 'message' in data
    assert data['message'] == 'Log has been removed'

def test_remove_payment_log_as_merchant_admin_successfully(merchant_admin_client, test_data):
    """
    DELETE /xqwapi/logs/<transaction_id>/invoices/<invoice_id>/<log_id>/logs
    """
    r_id = '9000018'
    t_id = '9000018'
    l_id = '10000013'
    delete_url = '{}/invoices/{}/logs/{}'.format(url.format(t_id), r_id, l_id)
    res = merchant_admin_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert 'message' in data
    assert data['message'] == 'Log has been removed'

def test_remove_payment_log_as_merchant_staff_successfully(merchant_staff_client, test_data):
    """
    DELETE /xqwapi/logs/<transaction_id>/invoices/<invoice_id>/<log_id>/logs
    """
    r_id = '9000018'
    t_id = '9000018'
    l_id = '10000014'
    delete_url = '{}/invoices/{}/logs/{}'.format(url.format(t_id), r_id, l_id)
    res = merchant_staff_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert 'message' in data
    assert data['message'] == 'Log has been removed'

def test_remove_payment_log_as_merchant_agent_successfully(merchant_agent_client, test_data):
    """
    DELETE /xqwapi/logs/<transaction_id>/invoices/<invoice_id>/<log_id>/logs
    """
    r_id = '9000018'
    t_id = '9000018'
    l_id = '10000015'
    delete_url = '{}/invoices/{}/logs/{}'.format(url.format(t_id), r_id, l_id)
    res = merchant_agent_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert 'message' in data
    assert data['message'] == 'Log has been removed'

def test_remove_payment_log_does_not_exist(merchant_admin_client, test_data):
    """
    DELETE /xqwapi/logs/<transaction_id>/invoices/<invoice_id>/<log_id>/logs
    """
    r_id = '9000018'
    t_id = '9000018'
    l_id = '100000110000'
    delete_url = '{}/invoices/{}/logs/{}'.format(url.format(t_id), r_id, l_id)
    res = merchant_admin_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert 'message' in data
    assert data['message'] == 'Transaction log does not exist'

def test_remove_payment_log_by_different_owner(merchant_admin_client, test_data):
    """
    DELETE /xqwapi/logs/<transaction_id>/invoices/<invoice_id>/<log_id>/logs
    """
    r_id = '9000018'
    t_id = '9000018'
    l_id = '10000016'
    delete_url = '{}/invoices/{}/logs/{}'.format(url.format(t_id), r_id, l_id)
    res = merchant_admin_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert 'message' in data
    assert data['message'] == 'You are not allowed to remove this log'

def test_remove_payment_log_by_different_owner_as_admin(admin_client, test_data):
    """
    DELETE /xqwapi/logs/<transaction_id>/invoices/<invoice_id>/<log_id>/logs
    """
    r_id = '9000018'
    t_id = '9000018'
    l_id = '10000017'
    delete_url = '{}/invoices/{}/logs/{}'.format(url.format(t_id), r_id, l_id)
    res = admin_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert 'message' in data
    assert data['message'] == 'Log has been removed'

def test_remove_payment_log_by_syslog_as_admin(admin_client, test_data):
    """
    DELETE /xqwapi/logs/<transaction_id>/invoices/<invoice_id>/<log_id>/logs
    """
    r_id = '9000018'
    t_id = '9000018'
    l_id = '10000006'
    delete_url = '{}/invoices/{}/logs/{}'.format(url.format(t_id), r_id, l_id)
    res = admin_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert 'message' in data
    assert data['message'] == 'You are not allowed to remove this log'

def test_remove_payment_log_removed_before(merchant_staff_client, test_data):
    """
    DELETE /xqwapi/logs/<transaction_id>/invoices/<invoice_id>/<log_id>/logs
    """
    r_id = '9000018'
    t_id = '9000018'
    l_id = '10000019'
    delete_url = '{}/invoices/{}/logs/{}'.format(url.format(t_id), r_id, l_id)
    res = merchant_staff_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert 'message' in data
    assert data['message'] == 'Transaction log does not exist'

def test_remove_payment_log_payment_does_not_exist(admin_client, test_data):
    """
    DELETE /xqwapi/logs/<transaction_id>/invoices/<invoice_id>/<log_id>/logs
    """
    r_id = '9000018123123'
    t_id = '9000018123123'
    l_id = '10000011'
    delete_url = '{}/invoices/{}/logs/{}'.format(url.format(t_id), r_id, l_id)
    res = admin_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert 'message' in data
    assert data['message'] == 'Payment does not exist'

def test_remove_payment_log_on_another_merchant_as_admin(admin_client, test_data):
    """
    DELETE /xqwapi/logs/<transaction_id>/invoices/<invoice_id>/<log_id>/logs
    """
    r_id = '9000018'
    t_id = '9000018'
    l_id = '10000001'
    delete_url = '{}/invoices/{}/logs/{}'.format(url.format(t_id), r_id, l_id)
    res = admin_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert 'message' in data
    assert data['message'] == 'Transaction log does not exist'
