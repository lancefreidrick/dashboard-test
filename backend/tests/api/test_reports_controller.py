""" tests.api.test_reports_controller.py """
# pylint: disable=redefined-outer-name,global-statement,unused-argument
# ^^^ this
import json
import pytest

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

## API: GET MERCHANT TRANSACTIONS

# def test_get_revenue_summary_by_date_range_as_admin_successfully(admin_client, test_data):
#     """
#     GET /xqwapi/reports/revenue
#     """
#     url = '/xqwapi/reports/revenue?merchant=romanempire&startday=2019-06-01&endday=2019-06-30'
#     res = admin_client.get(url, headers={
#         'Content-Type': 'application/json',
#         'Authorization': 'Bearer {}'.format(__token or ''),
#         'X-Client-Id': __http_client_id,
#         'X-Refresh-Token': __refresh_token
#     })
#     data = res.json
#     assert res.status_code == 200
#     assert data is not None
#     assert 'merchant' in data
#     assert 'currency' in data
#     assert 'dailyTransactionAmount' in data
#     assert 'totalBaseAmount' in data
#     assert 'totalFeeAmount' in data
#     assert 'totalChargedAmount' in data
#     assert 'totalCount' in data

# def test_get_revenue_summary_by_date_range_as_staff_successfully(staff_client, test_data):
#     """
#     GET /xqwapi/reports/revenue
#     """
#     url = '/xqwapi/reports/revenue?merchant=romanempire&startday=2019-06-01&endday=2019-06-30'
#     res = staff_client.get(url, headers={
#         'Content-Type': 'application/json',
#         'Authorization': 'Bearer {}'.format(__token or ''),
#         'X-Client-Id': __http_client_id,
#         'X-Refresh-Token': __refresh_token
#     })
#     data = res.json
#     assert res.status_code == 200
#     assert data is not None
#     assert 'merchant' in data
#     assert 'currency' in data
#     assert 'dailyTransactionAmount' in data
#     assert 'totalBaseAmount' in data
#     assert 'totalFeeAmount' in data
#     assert 'totalChargedAmount' in data
#     assert 'totalCount' in data

# def test_get_revenue_summary_by_date_range_as_merchant_admin_successfully(merchant_admin_client, test_data):
#     """
#     GET /xqwapi/reports/revenue
#     """
#     url = '/xqwapi/reports/revenue?merchant=romanempire&startday=2019-06-01&endday=2019-06-30'
#     res = merchant_admin_client.get(url, headers={
#         'Content-Type': 'application/json',
#         'Authorization': 'Bearer {}'.format(__token or ''),
#         'X-Client-Id': __http_client_id,
#         'X-Refresh-Token': __refresh_token
#     })
#     data = res.json
#     assert res.status_code == 200
#     assert data is not None
#     assert 'merchant' in data
#     assert 'currency' in data
#     assert 'dailyTransactionAmount' in data
#     assert 'totalBaseAmount' in data
#     assert 'totalFeeAmount' in data
#     assert 'totalChargedAmount' in data
#     assert 'totalCount' in data

# def test_get_revenue_summary_by_date_range_as_merchant_staff(merchant_staff_client, test_data):
#     """
#     GET /xqwapi/reports/revenue
#     """
#     url = '/xqwapi/reports/revenue?merchant=romanempire&startday=2019-05-01&endday=2019-05-31'
#     res = merchant_staff_client.get(url, headers={
#         'Content-Type': 'application/json',
#         'Authorization': 'Bearer {}'.format(__token or ''),
#         'X-Client-Id': __http_client_id,
#         'X-Refresh-Token': __refresh_token
#     })
#     data = res.json
#     assert res.status_code == 403
#     assert data is not None
#     assert data['message'] == 'You are not allowed here'

# def test_get_transactions_by_date_range_as_admin(admin_client, test_data):
#     """
#     GET /xqwapi/reports/transactions
#     """
#     url = '/xqwapi/reports/transactions?merchant=romanempire&startday=2019-05-01&endday=2019-05-31'
#     res = admin_client.get(url, headers={
#         'Content-Type': 'application/json',
#         'Authorization': 'Bearer {}'.format(__token or ''),
#         'X-Client-Id': __http_client_id,
#         'X-Refresh-Token': __refresh_token
#     })
#     data = res.json
#     assert res.status_code == 200
#     assert data is not None
#     assert 'merchant' in data
#     assert 'currency' in data
#     assert 'transactions' in data
#     assert 'totalBaseAmount' in data
#     assert 'totalTransactionFee' in data
#     assert 'totalChargedAmount' in data
#     assert 'totalCount' in data

# def test_get_transactions_by_date_range_as_staff(staff_client, test_data):
#     """
#     GET /xqwapi/reports/transactions
#     """
#     url = '/xqwapi/reports/transactions?merchant=romanempire&startday=2019-05-01&endday=2019-05-31'
#     res = staff_client.get(url, headers={
#         'Content-Type': 'application/json',
#         'Authorization': 'Bearer {}'.format(__token or ''),
#         'X-Client-Id': __http_client_id,
#         'X-Refresh-Token': __refresh_token
#     })
#     data = res.json
#     assert res.status_code == 200
#     assert data is not None
#     assert 'merchant' in data
#     assert 'currency' in data
#     assert 'transactions' in data
#     assert 'totalBaseAmount' in data
#     assert 'totalTransactionFee' in data
#     assert 'totalChargedAmount' in data
#     assert 'totalCount' in data

# def test_get_transactions_by_date_range_as_merchant_admin(merchant_admin_client, test_data):
#     """
#     GET /xqwapi/reports/transactions
#     """
#     url = '/xqwapi/reports/transactions?merchant=romanempire&startday=2019-05-01&endday=2019-05-31'
#     res = merchant_admin_client.get(url, headers={
#         'Content-Type': 'application/json',
#         'Authorization': 'Bearer {}'.format(__token or ''),
#         'X-Client-Id': __http_client_id,
#         'X-Refresh-Token': __refresh_token
#     })
#     data = res.json
#     assert res.status_code == 200
#     assert data is not None
#     assert 'merchant' in data
#     assert 'currency' in data
#     assert 'transactions' in data
#     assert 'totalBaseAmount' in data
#     assert 'totalTransactionFee' in data
#     assert 'totalChargedAmount' in data
#     assert 'totalCount' in data

# def test_get_transactions_by_date_range_as_merchant_staff(merchant_staff_client, test_data):
#     """
#     GET /xqwapi/reports/transactions
#     """
#     url = '/xqwapi/reports/transactions?merchant=romanempire&startday=2019-05-01&endday=2019-05-31'
#     res = merchant_staff_client.get(url, headers={
#         'Content-Type': 'application/json',
#         'Authorization': 'Bearer {}'.format(__token or ''),
#         'X-Client-Id': __http_client_id,
#         'X-Refresh-Token': __refresh_token
#     })
#     data = res.json
#     assert res.status_code == 403
#     assert data is not None
#     assert data['message'] == 'You are not allowed here'
