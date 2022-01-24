""" tests.api.test_transaction_controller.py """
# pylint: disable=redefined-outer-name,global-statement,unused-argument
# ^^^ this
import json
import pytest
from server.config import jsonwebtoken

url = '/xqwapi/merchants/{}/transactions'

__token = None
__refresh_token = None
__http_client_id = 'abcde12345abcde12345abcde12345abcde12345'

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

## API: GET MERCHANT TRANSACTION BY ID

def test_get_transaction_by_id_successfully(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/transactions/<transaction_id>
    """
    t_id = 'ZC2OGVXJ7WQHPQ2K'
    get_url = '{}/{}'.format(url.format('rome'), t_id)
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    data_copy = {
        'adminNotes': 'Test notes',
        'baseAmount': ['PHP', 31220.44],
        'clientNotes': 'No notes written here',
        'createdAt': '2021-01-03T17:55:26.327000+08:00',
        'customFields': {
            'justNumber': {'label': 'JUST Number', 'value': '0101'},
            'unitNumber': {'label': 'Unit Number', 'value': '1010'}
        },
        'customerEmail': 'kyle@qwikwire.com',
        'customerName': 'Nina Santiago',
        'customerPhone': '427977',
        'expiresat': '2021-01-03T18:25:26.327000+08:00',
        'externalTransactionId': 'ZC2OGVXJ7WQHPQ2K',
        'merchantCode': 'rome',
        'merchantId': 90000,
        'merchantName': 'Roman Empire',
        'paidAt': None,
        'paymentMethodName': 'cc',
        'paymentMode': None,
        'paymentType': 'ROMA-VL',
        'paymentTypeName': 'Vicesima libertatis',
        'projectCategory': 'temple',
        'projectCode': None,
        'projectId': '100001',
        'projectKey': 'pantheon',
        'projectName': 'Pantheon',
        'referenceId': 'QW-P-UDZXVPBF',
        'submittedAt': None,
        'transactionId': 9000013,
        'transactionSource': 'test',
        'transactionStatus': 'SUCCESS',
        'transactionType': 'PAYMENT',
        'updatedAt': '2021-01-04T08:04:04.541450+08:00'
    }
    for key in data_copy:
        assert key in data
        assert data_copy[key] == data[key]

def test_get_transaction_by_id_as_admin_successfully(admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/transactions/<transaction_id>
    """
    t_id = 'ZC2OGVXJ7WQHPQ2K'
    get_url = '{}/{}'.format(url.format('rome'), t_id)
    res = admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'transactionId' in data
    assert 'externalTransactionId' in data
    assert 'referenceId' in data

def test_get_transaction_by_id_as_staff_successfully(staff_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/transactions/<transaction_id>
    """
    t_id = 'ZC2OGVXJ7WQHPQ2K'
    get_url = '{}/{}'.format(url.format('rome'), t_id)
    res = staff_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'transactionId' in data
    assert 'externalTransactionId' in data
    assert 'referenceId' in data

def test_get_transaction_by_id_as_admin_on_incorrect_merchant(admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/transactions/<transaction_id>
    """
    t_id = 'ZC2OGVXJ7WQHPQ2K'
    get_url = '{}/{}'.format(url.format('parthia'), t_id)
    res = admin_client.get(get_url, headers={
        'content-type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data.get('message') == 'Transaction does not exist'

def test_get_transaction_by_id_without_token(client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/transactions/<transaction_id>
    """
    t_id = 'ZC2OGVXJ7WQHPQ2K'
    get_url = '{}/{}'.format(url.format('rome'), t_id)
    res = client.get(get_url, headers={
        'Content-Type': 'application/json',
    })
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data.get('message') == 'Unauthorized access'

def test_get_transaction_by_id_on_incorrect_merchant(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/transactions/<transaction_id>
    """
    t_id = 'ZC2OGVXJ7WQHPQ2K'
    get_url = '{}/{}'.format(url.format('parthia'), t_id)
    res = merchant_admin_client.get(get_url, headers={
        'content-type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data.get('message') == 'You are not allowed to get the merchant transactions'

def test_get_transaction_by_id_merchant_does_not_exist(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/transactions/<transaction_id>
    """
    t_id = 'WOWDTBOFW7SWYTN3'
    get_url = '{}/{}'.format(url.format('romanrepublic'), t_id)
    res = merchant_admin_client.get(get_url, headers={
        'content-type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data.get('message') == 'Merchant does not exist'

def test_get_transaction_by_id_does_not_exist(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/transactions/<transaction_id>
    """
    t_id = 'WOWDTBOFW7SWYTN3'
    get_url = '{}/{}'.format(url.format('rome'), t_id)
    res = merchant_admin_client.get(get_url, headers={
        'content-type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data.get('message') == 'Transaction does not exist'

def test_get_transaction_by_id_as_merchant_staff(merchant_staff_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/transactions/<transaction_id>
    """
    t_id = 'WOWDTBOFW7SWYTN3'
    get_url = '{}/{}'.format(url.format('rome'), t_id)
    res = merchant_staff_client.get(get_url, headers={
        'content-type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data.get('message') == 'Transaction does not exist'

def test_get_transaction_by_id_as_merchant_staff_user_transaction_does_not_exist(merchant_staff_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/transactions/<transaction_id>
    """
    t_id = 'ABCD000000000000'
    get_url = '{}/{}'.format(url.format('rome'), t_id)
    res = merchant_staff_client.get(get_url, headers={
        'content-type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data.get('message') == 'Transaction does not exist'

def test_get_transaction_by_id_as_another_user(another_merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/transactions/<transaction_id>
    """
    t_id = 'WOWDTBOFW7SWYTN3'
    get_url = '{}/{}'.format(url.format('rome'), t_id)
    res = another_merchant_admin_client.get(get_url, headers={
        'content-type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data.get('message') == 'You are not allowed to get the merchant transactions'

## API: SEARCH TRANSACTIONS

def test_search_transaction_using_name_as_admin_successfully(admin_client, test_data):
    """
    GET /xqwapi/transaction/search
    """
    res = admin_client.get('/xqwapi/transactions/search?query=Karla', headers={
        'content-type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'transactions' in data
    assert 'totalCount' in data
    assert 'page' in data
    assert 'size' in data
    assert len(data['transactions']) > 0

# def test_search_transaction_using_email_as_admin_successfully(admin_client, test_data):
#     """
#     GET /xqwapi/transaction/search
#     """
#     res = admin_client.get('/xqwapi/transactions/search?query=jesse@qwikwire.com', headers={
#         'content-type': 'application/json',
#         'Authorization': 'Bearer {}'.format(__token or ''),
#         'X-Client-Id': __http_client_id,
#         'X-Refresh-Token': __refresh_token
#     })
#     data = res.json
#     assert res.status_code == 200
#     assert data is not None
#     assert 'transactions' in data
#     assert 'totalCount' in data
#     assert 'page' in data
#     assert 'size' in data
#     assert len(data['transactions']) > 0

def test_search_transaction_using_reference_id_as_admin_successfully(admin_client, test_data):
    """
    GET /xqwapi/transaction/search
    """
    res = admin_client.get('/xqwapi/transactions/search?query=QW-P-YVFC7NGR', headers={
        'content-type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'transactions' in data
    assert 'totalCount' in data
    assert 'page' in data
    assert 'size' in data
    assert len(data['transactions']) == 1

def test_search_transaction_using_transaction_id_as_admin_successfully(admin_client, test_data):
    """
    GET /xqwapi/transaction/search
    """
    res = admin_client.get('/xqwapi/transactions/search?query=QNF7HSIWR76RPYWU', headers={
        'content-type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'transactions' in data
    assert 'totalCount' in data
    assert 'page' in data
    assert 'size' in data
    assert len(data['transactions']) == 1

def test_search_transaction_as_staff_successfully(staff_client, test_data):
    """
    GET /xqwapi/transaction/search
    """
    res = staff_client.get('/xqwapi/transactions/search?query=QNF7HSIWR76RPYWU', headers={
        'content-type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert 'transactions' in data
    assert 'totalCount' in data
    assert 'page' in data
    assert 'size' in data
    assert len(data['transactions']) == 1

def test_search_transaction_as_merchant_admin(merchant_admin_client, test_data):
    """
    GET /xqwapi/transaction/search
    """
    res = merchant_admin_client.get('/xqwapi/transactions/search?query=QNF7HSIWR76RPYWU', headers={
        'content-type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert 'transactions' in data
    assert 'totalCount' in data
    assert 'page' in data
    assert 'size' in data
    assert len(data['transactions']) == 1

def test_search_transaction_as_another_merchant_admin(another_merchant_admin_client, test_data):
    """
    GET /xqwapi/transaction/search
    """
    res = another_merchant_admin_client.get('/xqwapi/transactions/search?query=QNF7HSIWR76RPYWU', headers={
        'content-type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'transactions' in data
    assert 'totalCount' in data
    assert 'page' in data
    assert 'size' in data
    assert len(data['transactions']) == 0

## API: EXPORT transactions

def test_export_transactions_successfully(merchant_admin_client, test_data):
    """
    GET /xqwapi/transactions/export
    """
    export_auth_res = merchant_admin_client.post('/xqwapi/auth/export', headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    auth_data = export_auth_res.json
    assert export_auth_res.status_code == 200
    assert auth_data is not None
    assert 'exportToken' in auth_data

    export_url = '/xqwapi/transactions/export?token={}'.format(auth_data['exportToken'])
    res = merchant_admin_client.get(export_url)
    csv = str(res.data, 'utf-8')
    assert res.status_code == 200
    assert csv is not None

    # Do not include custom columns due to reordering problems
    lines = csv.splitlines()
    assert lines[0]
    assert lines[0].startswith(
        'transactionId,referenceId,xsrfKey,projectName,projectCategory,merchantId,merchantName,'
        'billTotal,billBase,billFee,billConverted,paymentMethod,transactionType,paymentMode,'
        'paymentType,status,customerName,customerEmail,customerPhone,createdAt,expiresAt')

def test_export_transactions_as_admin_successfully(admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/transactions/export
    """
    export_auth_res = admin_client.post('/xqwapi/auth/export', headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    auth_data = export_auth_res.json
    assert export_auth_res.status_code == 200
    assert auth_data is not None
    assert 'exportToken' in auth_data

    export_url = '/xqwapi/transactions/export?token={}'.format(auth_data['exportToken'])
    res = admin_client.get(export_url)
    csv = str(res.data, 'utf-8')
    assert res.status_code == 200
    assert csv is not None

    # Do not include custom columns due to reordering problems
    lines = csv.splitlines()
    assert lines[0]
    assert lines[0].startswith(
        'transactionId,referenceId,xsrfKey,projectName,projectCategory,merchantId,merchantName,'
        'billTotal,billBase,billFee,billConverted,paymentMethod,transactionType,paymentMode,'
        'paymentType,status,customerName,customerEmail,customerPhone,createdAt,expiresAt')

def test_export_transactions_as_staff_successfully(staff_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/transactions/export
    """
    export_auth_res = staff_client.post('/xqwapi/auth/export', headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    auth_data = export_auth_res.json
    assert export_auth_res.status_code == 200
    assert auth_data is not None
    assert 'exportToken' in auth_data

    export_url = '/xqwapi/transactions/export?token={}'.format(auth_data['exportToken'])
    res = staff_client.get(export_url)
    csv = str(res.data, 'utf-8')
    assert res.status_code == 200
    assert csv is not None

    # Do not include custom columns due to reordering problems
    lines = csv.splitlines()
    assert lines[0]
    assert lines[0].startswith(
        'transactionId,referenceId,xsrfKey,projectName,projectCategory,merchantId,merchantName,'
        'billTotal,billBase,billFee,billConverted,paymentMethod,transactionType,paymentMode,'
        'paymentType,status,customerName,customerEmail,customerPhone,createdAt,expiresAt')

def test_export_transactions_without_export_token(client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/transactions/export
    """
    export_url = '/xqwapi/transactions/export'
    res = client.get(export_url)
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized to export transactions'

def test_export_transactions_as_merchant_staff(merchant_staff_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/transactions/export
    """
    export_auth_res = merchant_staff_client.post('/xqwapi/auth/export', headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    auth_data = export_auth_res.json
    assert export_auth_res.status_code == 403
    assert auth_data is not None
    assert auth_data['message'] == 'You are not allowed here'

def test_export_transactions_on_random_token(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/transactions/export
    """
    random_token = '218578t1y3hnqisahniqweiu'
    export_url = '/xqwapi/transactions/export?token={}'.format(random_token)
    res = merchant_admin_client.get(export_url)
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized to export transactions'

def test_export_transactions_on_invalid_token(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/transactions/export
    """
    invalid_token = jsonwebtoken.encode({
        'user': {
            'id': '5c6fac029387ae13e29', #unknown ID
            'email': 'pompey@qwikwire.com'
        },
        'merchant': {
            'id': 'china',
            'name': 'China'
        },
        'sessionkey': '125t8yghwmdskjfhn19mj19'
    }, 3)
    export_url = '/xqwapi/transactions/export?token={}'.format(invalid_token)
    res = merchant_admin_client.get(export_url)
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized to export transactions'

def test_export_transactions_on_missing_user_on_invalid_token(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/transactions/export
    """
    invalid_token = jsonwebtoken.encode({
        'merchant': {
            'id': 'china',
            'name': 'China'
        },
        'sessionkey': '125t8yghwmdskjfhn19mj19'
    }, 3)
    export_url = '/xqwapi/transactions/export?token={}'.format(invalid_token)
    res = merchant_admin_client.get(export_url)
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized to export transactions'

def test_export_transactions_on_missing_merchant_on_invalid_token(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/transactions/export
    """
    invalid_token = jsonwebtoken.encode({
        'user': {
            'id': '5c6fac029387ae13e29dd', #unknown ID
            'email': 'pompey@qwikwire.com'
        },
        'sessionkey': '125t8yghwmdskjfhn19mj19'
    }, 3)
    export_url = '/xqwapi/transactions/export?token={}'.format(invalid_token)
    res = merchant_admin_client.get(export_url)
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized to export transactions'

## TODO: Tests create, get and delete logs
