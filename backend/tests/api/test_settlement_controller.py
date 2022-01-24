""" tests.api.test_settlement_controller.py """
# pylint: disable=redefined-outer-name,global-statement,unused-argument,too-many-lines
import json
import pytest

__token = None
__refresh_token = None
__http_client_id = 'abcde12345abcde12345abcde12345abcde12345'

url = '/xqwapi/merchants/{}/settlements'
payments_url = '/xqwapi/merchants/{}/payments'
settlement_url = '/xqwapi/merchants/{}/settlements/{}'

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

## API: GET MERCHANT SETTLEMENTS

def test_get_settlements_as_admin_successfully_base_data(admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/settlements
    """
    get_url = url.format('rome')
    res = admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert len(data['settlements']) == 3
    assert data['totalCount'] == 3
    data_copy = {
        'createdAt': '2021-01-09T20:00:00.923289+08:00',
        'fileDirectory': 'settlement-reports/rome/ce9b75f5-dc02-4c5f-b6a6-4733b96ec68d',
        'fileId': 80002,
        'fileName': 'minertocat.png',
        'fileType': 'image/png',
        'fileUrl': (
            'https://aqwire-dashboard-staging2.s3.amazonaws.com/'
            'settlement-reports/rome/ce9b75f5-dc02-4c5f-b6a6-4733b96ec68d/minertocat.png'
        ),
        'merchantCode': 'rome',
        'merchantName': 'Roman Empire',
        'settledByEmail': 'cincinnatus@qwikwire.com',
        'settledByFirstName': 'Lucius Quinctius',
        'settledById': 1000003,
        'settledByLastName':
        'Cincinnatus',
        'settledDate': '2021-01-09',
        'settlementId': 90002,
        'settlementNotes': None,
        'settlementReferenceId': 'QW-S-AAABBCC2',
        'totalPaymentCount': 1,
        'totalSettlementAmount': ['PHP', 31257.38],
        'updatedAt': '2021-01-09T21:00:40.385054+08:00'
    }
    settlement = data['settlements'][0]
    for key in data_copy:
        assert key in settlement
        assert data_copy[key] == settlement[key]


def test_get_settlements_as_staff_successfully_base_data(staff_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/settlements
    """
    get_url = url.format('rome')
    res = staff_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert len(data['settlements']) == 3
    assert data['totalCount'] == 3

def test_get_settlements_as_merchant_admin_successfully_base_data(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/settlements
    """
    get_url = url.format('rome')
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert len(data['settlements']) == 3
    assert data['totalCount'] == 3

def test_get_settlements_as_merchant_staff(merchant_staff_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/settlements
    """
    get_url = url.format('rome')
    res = merchant_staff_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_get_settlements_as_merchant_agent(merchant_agent_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/settlements
    """
    get_url = url.format('rome')
    res = merchant_agent_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_get_settlements_as_another_user(another_merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/settlements
    """
    get_url = url.format('rome')
    res = another_merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to get the settlements for this merchant.'

def test_get_settlements_merchant_does_not_exist(admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/settlements
    """
    get_url = url.format('romanrepublic')
    res = admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Merchant does not exist.'

## GET SETTLEMENT API

def test_get_settlement_as_admin_successfully(admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/settlements/<settlement_id>
    """
    settlement_reference_id = 'QW-S-AAABBCC0'
    get_url = settlement_url.format('rome', settlement_reference_id)
    res = admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    data_copy = {
        'createdAt': '2021-01-08T19:24:31.923289+08:00',
        'fileDirectory': 'settlement-reports/rome/f3f24020-ddc0-4d80-98ba-3e7fed608f31',
        'fileId': 80000,
        'fileName': 'boxertocat_octodex.png',
        'fileType': 'image/png',
        'fileUrl': (
            'https://aqwire-dashboard-staging2.s3.amazonaws.com/'
            'settlement-reports/rome/f3f24020-ddc0-4d80-98ba-3e7fed608f31/boxertocat_octodex.png'
        ),
        'merchantCode': 'rome',
        'merchantName': 'Roman Empire',
        'settledByEmail': 'cincinnatus@qwikwire.com',
        'settledByFirstName': 'Lucius Quinctius',
        'settledById': 1000003,
        'settledByLastName': 'Cincinnatus',
        'settledDate': '2021-01-07',
        'settlementId': 90000,
        'settlementNotes': 'Test notes for the settlement',
        'settlementReferenceId': 'QW-S-AAABBCC0',
        'totalPaymentCount': 2,
        'totalSettlementAmount': ['PHP', 33993.68],
        'updatedAt': '2021-01-08T19:25:21.385054+08:00'
    }
    for key in data_copy:
        assert key in data
        assert data_copy[key] == data[key]

def test_get_settlement_as_staff_successfully(staff_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/settlements/<settlement_id>
    """
    settlement_reference_id = 'QW-S-AAABBCC0'
    get_url = settlement_url.format('rome', settlement_reference_id)
    res = staff_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None

def test_get_settlement_as_merchant_admin_successfully(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/settlements/<settlement_id>
    """
    settlement_reference_id = 'QW-S-AAABBCC0'
    get_url = settlement_url.format('rome', settlement_reference_id)
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None

def test_get_settlement_as_merchant_staff_successfully(merchant_staff_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/settlements/<settlement_id>
    """
    settlement_reference_id = 'QW-S-AAABBCC0'
    get_url = settlement_url.format('rome', settlement_reference_id)
    res = merchant_staff_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_get_settlement_as_merchant_agent_successfully(merchant_agent_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/settlements/<settlement_id>
    """
    settlement_reference_id = 'QW-S-AAABBCC0'
    get_url = settlement_url.format('rome', settlement_reference_id)
    res = merchant_agent_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_get_settlement_not_found(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/settlements/<settlement_id>
    """
    settlement_reference_id = 'QW-S-AAABBCC9'
    get_url = settlement_url.format('rome', settlement_reference_id)
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Settlement report not found.'

def test_get_settlement_on_different_merchant(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/settlements/<settlement_id>
    """
    settlement_reference_id = 'QW-S-AAABBCC3'
    get_url = settlement_url.format('rome', settlement_reference_id)
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to get settlements for this merchant.'

def test_get_settlement_using_another_merchant(another_merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/settlements/<settlement_id>
    """
    settlement_reference_id = 'QW-S-AAABBCC1'
    get_url = settlement_url.format('rome', settlement_reference_id)
    res = another_merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to get settlements for this merchant.'

def test_get_settlement_on_incorrect_merchant(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/settlements/<settlement_id>
    """
    settlement_reference_id = 'QW-S-AAABBCC1'
    get_url = settlement_url.format('romanrepublic', settlement_reference_id)
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Merchant does not exist.'

## CREATE SETTLEMENT API

def test_create_settlement_as_admin_successfully(admin_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/settlements
    """
    get_payments_url = '{}?status=PAID'.format(payments_url.format('rome'))
    res = admin_client.get(get_payments_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    invoice_ids = [
        (p['invoiceId'], p['paymentReferenceId'])
        for p in data['payments']
    ]
    post_url = url.format('rome')
    res = admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'invoiceIds': [invoice_ids[0][0]],
        'settlementFileId': 80004,
        'settledDate': '2020-01-13',
        'settlementNotes': None
    }))
    data = res.json
    assert res.status_code == 201
    assert data is not None
    assert 'message' in data
    assert data['message'] == 'Settlement report has been created'
    assert 'referenceId' in data
    assert 'settlementId' in data

def test_create_settlement_as_staff_successfully(staff_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/settlements
    """
    get_payments_url = '{}?status=PAID'.format(payments_url.format('rome'))
    res = staff_client.get(get_payments_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    invoice_ids = [
        (p['invoiceId'], p['paymentReferenceId'])
        for p in data['payments']
    ]
    post_url = url.format('rome')
    res = staff_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'invoiceIds': [invoice_ids[0][0]],
        'settlementFileId': 80005,
        'settledDate': '2020-01-13',
        'settlementNotes': 'This is a test settlement'
    }))
    data = res.json
    assert res.status_code == 201
    assert data is not None
    assert 'message' in data
    assert data['message'] == 'Settlement report has been created'
    assert 'referenceId' in data
    assert 'settlementId' in data

def test_create_settlement_as_merchant_admin(merchant_admin_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/settlements
    """
    get_payments_url = '{}?status=PAID'.format(payments_url.format('rome'))
    res = merchant_admin_client.get(get_payments_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    invoice_ids = [
        (p['invoiceId'], p['paymentReferenceId'])
        for p in data['payments']
    ]
    post_url = url.format('rome')
    res = merchant_admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'invoiceIds': [invoice_ids[0][0]],
        'settlementFileId': 80006,
        'settledDate': '2020-01-13',
        'settlementNotes': None
    }))
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert 'message' in data
    assert data['message'] == 'You are not allowed here'

def test_create_settlement_as_merchant_staff(merchant_staff_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/settlements
    """
    get_payments_url = '{}?status=PAID'.format(payments_url.format('rome'))
    res = merchant_staff_client.get(get_payments_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    invoice_ids = [
        (p['invoiceId'], p['paymentReferenceId'])
        for p in data['payments']
    ]
    post_url = url.format('rome')
    res = merchant_staff_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'invoiceIds': [invoice_ids[0][0]],
        'settlementFileId': 80006,
        'settledDate': '2020-01-13',
        'settlementNotes': None
    }))
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert 'message' in data
    assert data['message'] == 'You are not allowed here'

def test_create_settlement_as_merchant_agent(merchant_agent_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/settlements
    """
    get_payments_url = '{}?status=PAID'.format(payments_url.format('rome'))
    res = merchant_agent_client.get(get_payments_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    invoice_ids = [
        (p['invoiceId'], p['paymentReferenceId'])
        for p in data['payments']
    ]
    post_url = url.format('rome')
    res = merchant_agent_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'invoiceIds': [invoice_ids[0][0]],
        'settlementFileId': 80006,
        'settledDate': '2020-01-13',
        'settlementNotes': None
    }))
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert 'message' in data
    assert data['message'] == 'You are not allowed here'

def test_create_settlement_as_another_merchant_admin(another_merchant_admin_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/settlements
    """
    post_url = url.format('rome')
    res = another_merchant_admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'invoiceIds': [120000], # Just a random number
        'settlementFileId': 80006,
        'settledDate': '2020-01-13',
        'settlementNotes': None
    }))
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert 'message' in data
    assert data['message'] == 'You are not allowed here'

def test_create_settlement_on_another_merchant_file(admin_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/settlements
    """
    get_payments_url = '{}?status=PAID'.format(payments_url.format('rome'))
    res = admin_client.get(get_payments_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    invoice_ids = [
        (p['invoiceId'], p['paymentReferenceId'])
        for p in data['payments']
    ]
    post_url = url.format('rome')
    res = admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'invoiceIds': [invoice_ids[0][0]],
        'settlementFileId': 80007, # Owned by 90001 (parthia)
        'settledDate': '2020-01-13',
        'settlementNotes': None
    }))
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert 'message' in data
    assert data['message'] == 'The submitted settlement file does not exist'

def test_create_settlement_on_duplicate_invoice_ids(admin_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/settlements
    """
    get_payments_url = '{}?status=PAID'.format(payments_url.format('rome'))
    res = admin_client.get(get_payments_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    invoice_ids = [
        (p['invoiceId'], p['paymentReferenceId'])
        for p in data['payments']
    ]
    post_url = url.format('rome')
    res = admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'invoiceIds': [invoice_ids[0][0], invoice_ids[0][0]],
        'settlementFileId': 80006,
        'settledDate': '2020-01-13',
        'settlementNotes': None
    }))
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert 'message' in data
    assert data['message'] == 'The payments on the settlement report have duplicate items'

def test_create_settlement_on_empty_body(admin_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/settlements
    """
    post_url = url.format('rome')
    res = admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({}))
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert 'message' in data
    assert data['message'] == 'The submitted settlement is not valid'

def test_create_settlement_on_invalid_invoices(admin_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/settlements
    """
    post_url = url.format('rome')
    res = admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'invoiceIds': [],
        'settlementFileId': 80006,
        'settledDate': None,
        'settlementNotes': None
    }))
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert 'message' in data
    assert data['message'] == 'The submitted settlement is not valid'

def test_create_settlement_on_invalid_settled_date(admin_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/settlements
    """
    get_payments_url = '{}?status=PAID'.format(payments_url.format('rome'))
    res = admin_client.get(get_payments_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    invoice_ids = [
        (p['invoiceId'], p['paymentReferenceId'])
        for p in data['payments']
    ]
    post_url = url.format('rome')
    res = admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'invoiceIds': [invoice_ids[0][0]],
        'settlementFileId': 80006,
        'settledDate': None,
        'settlementNotes': None
    }))
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert 'message' in data
    assert data['message'] == 'The submitted settlement is not valid'

# DELETE SETTLEMENT API

def test_delete_settlement_as_admin_successfully(admin_client, test_data):
    """
    DELETE /xqwapi/merchants/<merchant_id>/settlements/<settlement_id>
    """
    settlement_reference_id = 'QW-S-AAABBCC0'
    post_url = settlement_url.format('rome', settlement_reference_id)
    res = admin_client.delete(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    assert res.status_code == 204
    assert not res.data

def test_delete_settlement_as_staff_successfully(staff_client, test_data):
    """
    DELETE /xqwapi/merchants/<merchant_id>/settlements/<settlement_id>
    """
    settlement_reference_id = 'QW-S-AAABBCC1'
    post_url = settlement_url.format('rome', settlement_reference_id)
    res = staff_client.delete(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    print(res.data)
    assert res.status_code == 204
    assert not res.data

def test_delete_settlement_as_merchant_admin(merchant_admin_client, test_data):
    """
    DELETE /xqwapi/merchants/<merchant_id>/settlements/<settlement_id>
    """
    settlement_reference_id = 'QW-S-AAABBCC2'
    post_url = settlement_url.format('rome', settlement_reference_id)
    res = merchant_admin_client.delete(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_delete_settlement_as_merchant_staff(merchant_staff_client, test_data):
    """
    DELETE /xqwapi/merchants/<merchant_id>/settlements/<settlement_id>
    """
    settlement_reference_id = 'QW-S-AAABBCC2'
    post_url = settlement_url.format('rome', settlement_reference_id)
    res = merchant_staff_client.delete(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_delete_settlement_as_merchant_agent(merchant_agent_client, test_data):
    """
    DELETE /xqwapi/merchants/<merchant_id>/settlements/<settlement_id>
    """
    settlement_reference_id = 'QW-S-AAABBCC2'
    post_url = settlement_url.format('rome', settlement_reference_id)
    res = merchant_agent_client.delete(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_delete_settlement_not_found(admin_client, test_data):
    """
    DELETE /xqwapi/merchants/<merchant_id>/settlements/<settlement_id>
    """
    settlement_reference_id = 'QW-S-AAABBCC9'
    post_url = settlement_url.format('rome', settlement_reference_id)
    res = admin_client.delete(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Settlement report does not exist'

def test_delete_settlement_on_merchant_does_not_exist(admin_client, test_data):
    """
    DELETE /xqwapi/merchants/<merchant_id>/settlements/<settlement_id>
    """
    settlement_reference_id = 'QW-S-AAABBCC2'
    post_url = settlement_url.format('romanrepublic', settlement_reference_id)
    res = admin_client.delete(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Merchant does not exist'

def test_delete_settlement_on_incorrect_merchant(admin_client, test_data):
    """
    DELETE /xqwapi/merchants/<merchant_id>/settlements/<settlement_id>
    """
    settlement_reference_id = 'QW-S-AAABBCC2'
    post_url = settlement_url.format('parthia', settlement_reference_id)
    res = admin_client.delete(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'Settlement report belongs to another merchant'
