""" tests.api.test_payment_controller.py """
# pylint: disable=redefined-outer-name,global-statement,unused-argument
# ^^^ this
import json
import pytest
from server.config import jsonwebtoken

__token = None
__refresh_token = None
__http_client_id = 'abcde12345abcde12345abcde12345abcde12345'

url = '/xqwapi/merchants/{}/payments'

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

# API: GET MERCHANT PAYMENTS

def test_get_payments_successfully(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments
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
    assert len(data['payments']) == 10

    payment = data['payments'][0]
    assert 'invoiceId' in payment
    assert 'transactionId' in payment
    assert 'externalTransactionId' in payment
    assert 'paymentReferenceId' in payment
    assert 'transactionReferenceId' in payment
    assert 'invoiceReferenceId' in payment
    assert 'settlementReferenceId' in payment
    assert 'transactionType' in payment
    assert 'transactionStatus' in payment
    assert 'paymentStatus' in payment
    assert 'paymentMode' in payment
    assert 'paymentType' in payment
    assert 'paymentTypeName' in payment
    assert 'customerName' in payment
    assert 'customerEmail' in payment
    assert 'customerPhone' in payment
    assert 'merchantCode' in payment
    assert 'merchantName' in payment
    assert 'projectCode' in payment
    assert 'projectName' in payment
    assert 'projectCategory' in payment
    assert 'billBase' in payment
    assert 'billConverted' in payment
    assert 'billFee' in payment
    assert 'billTotal' in payment
    assert 'transactionSource' in payment
    assert 'paymentMethodName' in payment
    assert 'expiresAt' in payment
    assert 'createdAt' in payment
    assert 'updatedAt' in payment
    assert 'paidAt' in payment
    assert 'submittedAt' in payment
    assert 'dueAt' in payment
    assert 'invoiceCreatedAt' in payment
    assert 'invoiceUpdatedAt' in payment
    assert data['totalCount'] > 0
    assert data['size'] == 10
    assert data['page'] == 1

def test_get_payments_without_token(client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments
    """
    get_url = url.format('rome')
    res = client.get(get_url, headers={
        'Content-Type': 'application/json'
    })
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized access'

def test_get_payments_as_another_merchant_admin(another_merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments
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
    assert data['message'] == 'You are not allowed to get the merchant payments'

def test_get_payments_as_merchant_staff(merchant_staff_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments
    """
    get_url = url.format('rome')
    res = merchant_staff_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data['payments']
    assert data['totalCount'] > 0
    assert data['size'] == 10
    assert data['page'] == 1

def test_get_payments_as_merchant_agent(merchant_agent_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments
    """
    get_url = url.format('rome')
    res = merchant_agent_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['payments']
    assert data['totalCount'] > 0
    assert data['size'] == 10
    assert data['page'] == 1

def test_get_payments_as_admin_successfully(admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments
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
    assert len(data['payments']) == 10
    assert data['totalCount'] > 0
    assert data['size'] == 10
    assert data['page'] == 1

def test_get_payments_as_admin_on_another_merchant(admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments
    """
    get_url = url.format('gaul')
    res = admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert not data['payments']
    assert data['totalCount'] == 0
    assert data['size'] == 10
    assert data['page'] == 1

def test_get_payments_as_admin_on_incorrect_merchant(admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments
    """
    get_url = url.format('parthia123')
    res = admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Merchant does not exist'

def test_get_payments_on_page_2_and_size_5_successfully(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments
    """
    get_url = url.format('rome') + '?page=2&size=5'
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert len(data['payments']) == 5
    assert data['totalCount'] > 0
    assert data['size'] == 5
    assert data['page'] == 2

def test_get_payments_on_page_20_and_size_20_successfully(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments
    """
    get_url = url.format('rome') + '?page=50&size=50'
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert not data['payments']
    assert data['totalCount'] == 0 # since there are no payments, total cound is not available
    assert data['size'] == 50
    assert data['page'] == 50

def test_get_payments_as_admin_on_page_2_and_size_5_as_successfully(admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments
    """
    get_url = url.format('rome') + '?page=2&size=5'
    res = admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert len(data['payments']) == 5
    assert data['totalCount'] > 0
    assert data['size'] == 5
    assert data['page'] == 2

def test_get_payments_between_start_and_end_day_successfully(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments
    """
    get_url = url.format('rome') + '?size=15&startday=2020-12-01&endday=2021-01-31'
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert len(data['payments']) == 15
    assert data['totalCount'] >= 0
    assert data['size'] == 15
    assert data['page'] == 1

def test_get_payments_on_colosseum_project_successfully(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments
    """
    get_url = url.format('rome') + '?size=15&project=100000' # colosseum
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert len(data['payments']) == 15
    assert data['totalCount'] == 26
    assert data['size'] == 15
    assert data['page'] == 1

def test_get_payments_by_reporting_date_successfully(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments
    """
    get_url = url.format('rome') + '?reportdate=2020-12-14'
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert len(data['payments']) == 10
    assert data['payments'][0]['externalTransactionId'] == 'NIFABGHRBFF2GW4C'
    assert data['totalCount'] == 23
    assert data['size'] == 10
    assert data['page'] == 1

def test_get_payments_on_settlement_ref_by_id_successfully(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments
    """
    get_url = url.format('rome') + '?settlementrefid=QW-S-AAABBCC0'
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert len(data['payments']) == 2
    assert data['totalCount'] == 2
    assert data['size'] == 10
    assert data['page'] == 1
    assert data['payments'][0]['paymentReferenceId'] == 'QW-P-CJWT4NK5'
    assert data['payments'][1]['paymentReferenceId'] == 'QW-P-UHTGNPRK'

def test_get_payments_on_settlement_ref_id_does_not_exist(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments
    """
    get_url = url.format('rome') + '?settlementrefid=QW-S-AAA00000'
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert not data['payments']
    assert data['totalCount'] == 0
    assert data['size'] == 10
    assert data['page'] == 1

def test_get_payments_on_search_paid_and_settled_successfully(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments
    """
    get_url = url.format('rome') + '?status=PAID,SETTLED'
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert len(data['payments']) == 10
    assert 'paymentReferenceId' in data['payments'][0]
    assert data['totalCount'] == 39
    assert data['size'] == 10
    assert data['page'] == 1

def test_get_payments_on_search_invalid_status_successfully(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments
    """
    get_url = url.format('rome') + '?status=DELETE FROM invoicing.transaction;'
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert len(data['payments']) == 0
    assert data['totalCount'] == 0
    assert data['size'] == 10
    assert data['page'] == 1

## API: GET MERCHANT PAYMENT BY ID

def test_get_payment_by_id_on_enrollment_successfully(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments
    """
    r_id = 'QW-P-UHTGNPRK'
    get_url = '{}/{}'.format(url.format('rome'), r_id)
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'invoiceId' in data
    assert 'invoiceUpdatedAt' in data
    assert 'updatedAt' in data
    data_copy = {
        'adminNotes': 'Test notes',
        'billBase': ['PHP', 13993.68],
        'billConverted': ['USD', 302.85],
        'billFee': ['USD', 0.0],
        'billTotal': ['USD', 302.85],
        'clientNotes': 'No notes written here',
        'createdAt': '2020-09-08T12:32:04.624000+08:00',
        'customFields': {
            'justNumber': {'label': 'JUST Number', 'value': '0101'},
            'unitNumber': {'label': 'Unit Number', 'value': '1010'}
        },
        'customerEmail': 'jeff@qwikwire.com',
        'customerName': 'Karla Reyes',
        'customerPhone': '539977',
        'dueAt': '2020-12-04T00:00:00+08:00',
        'expiresAt': '2020-10-08T12:32:04.624000+08:00',
        'externalTransactionId': 'ERV45P7BSK7SFK5Q',
        'invoiceCreatedAt': '2020-09-08T12:32:04.624000+08:00',
        'invoiceReferenceId': 'QW-I-K2VR2YV6',
        'merchantCode': 'rome',
        'merchantId': 90000,
        'merchantName': 'Roman Empire',
        'oxRate': ['USD', 'PHP', 0],
        'paidAt': '2020-12-03T16:00:26.247000+08:00',
        'paymentMethodBillingAddress': None,
        'paymentMethodCardLastFour': '9715',
        'paymentMethodCustomerName': 'CVAXl6s3',
        'paymentMethodExpiry': '01/30',
        'paymentMethodId': 9000031,
        'paymentMethodIssuer': 'Qwikwire',
        'paymentMethodName': 'cc',
        'paymentMethodOrigin': 'Norway',
        'paymentMethodProcessor': 'SB',
        'paymentMethodProcessorId': None,
        'paymentMethodProvider': 'American Express',
        'paymentMethodStatus': None,
        'paymentMethodType': None,
        'paymentMode': None,
        'paymentReferenceId': 'QW-P-UHTGNPRK',
        'paymentStatus': 'SETTLED',
        'paymentType': 'ROMA-VL',
        'paymentTypeName': 'Vicesima libertatis',
        'projectCategory': 'temple',
        'projectCode': None,
        'projectName': 'Pantheon',
        'qwxRate': ['USD', 'PHP', 48.0545],
        'retryAttemptCount': 0,
        'settlementReferenceId': 'QW-S-AAABBCC0',
        'submittedAt': None,
        'transactionId': '9000031',
        'transactionReferenceId': 'QW-E-EYNDQZ53',
        'transactionSource': 'test',
        'transactionStatus': 'ONGOING',
        'transactionType': 'ENROLLMENT',
    }
    for key in data_copy:
        assert key in data
        assert data_copy[key] == data[key]

def test_get_payment_by_id_on_one_time_payment_successfully(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments
    """
    r_id = 'QW-P-G7XFSEYB'
    get_url = '{}/{}'.format(url.format('rome'), r_id)
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'invoiceId' in data
    assert 'invoiceUpdatedAt' in data
    assert 'updatedAt' in data
    data_copy = {
        'adminNotes': None,
        'billBase': ['PHP', 50000.0],
        'billConverted': ['USD', 1075.87],
        'billFee': ['USD', 0.0],
        'billTotal': ['USD', 1075.87],
        'clientNotes': 'No notes written here',
        'createdAt': '2021-01-03T18:13:56.452000+08:00',
        'customFields': {
            'justNumber': {'label': 'JUST Number', 'value': '0101'},
            'unitNumber': {'label': 'Unit Number', 'value': '1010'}
        },
        'customerEmail': 'archie@qwikwire.com',
        'customerName': 'David Adam',
        'customerPhone': '817681',
        'dueAt': None,
        'expiresAt': '2021-01-03T18:43:56.452000+08:00',
        'externalTransactionId': 'JCEJFWO5UB5WYS6G',
        'invoiceCreatedAt': '2021-01-03T18:13:56.452000+08:00',
        'invoiceReferenceId': None,
        'merchantCode': 'rome',
        'merchantId': 90000,
        'merchantName': 'Roman Empire',
        'oxRate': ['USD', 'PHP', 0],
        'paidAt': '2021-01-03T18:17:25.983000+08:00',
        'paymentMethodBillingAddress': None,
        'paymentMethodCardLastFour': '6836',
        'paymentMethodCustomerName': 'uORiO3Nw',
        'paymentMethodExpiry': None,
        'paymentMethodId': 9000015,
        'paymentMethodIssuer': 'Qwikwire',
        'paymentMethodName': 'cc',
        'paymentMethodOrigin': 'Vietnam',
        'paymentMethodProcessor': 'SB',
        'paymentMethodProcessorId': None,
        'paymentMethodProvider': 'Visa',
        'paymentMethodStatus': None,
        'paymentMethodType': None,
        'paymentMode': None,
        'paymentReferenceId': 'QW-P-G7XFSEYB',
        'paymentStatus': 'PAID',
        'paymentType': 'ROMA-VL',
        'paymentTypeName': 'Vicesima libertatis',
        'projectCategory': 'temple',
        'projectCode': None,
        'projectName': 'Pantheon',
        'qwxRate': ['USD', 'PHP', 48.3329],
        'retryAttemptCount': 0,
        'settlementReferenceId': None,
        'submittedAt': None,
        'transactionId': '9000015',
        'transactionReferenceId': 'QW-P-G7XFSEYB',
        'transactionSource': 'test',
        'transactionStatus': 'SUCCESS',
        'transactionType': 'PAYMENT'
    }
    for key in data_copy:
        assert key in data
        assert data_copy[key] == data[key]

def test_get_payment_by_id_as_admin_successfully(admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments
    """
    r_id = 'QW-P-CJWT4NK5'
    get_url = '{}/{}'.format(url.format('rome'), r_id)
    res = admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'invoiceId' in data
    assert 'transactionId' in data

def test_get_payment_by_id_as_merchant_staff(merchant_staff_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments
    """
    r_id = 'QW-P-CJWT4NK5'
    get_url = '{}/{}'.format(url.format('rome'), r_id)
    res = merchant_staff_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'invoiceId' in data
    assert 'transactionId' in data

def test_get_payment_by_id_as_admin_on_incorrect_merchant(admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments
    """
    r_id = 'QW-P-F2613223'
    get_url = '{}/{}'.format(url.format('parthia'), r_id)
    res = admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Payment does not exist'

def test_get_payment_by_id_without_token(client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments/<reference_id>
    """
    r_id = 'QW-P-F2613223'
    get_url = '{}/{}'.format(url.format('rome'), r_id)
    res = client.get(get_url, headers={
        'Content-Type': 'application/json'
    })
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized access'

def test_get_payment_by_id_on_incorrect_merchant(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments
    """
    r_id = 'QW-P-MWZSAURS'
    get_url = '{}/{}'.format(url.format('parthia'), r_id)
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to get this merchant payment'

def test_get_payment_by_id_on_merchant_does_not_exist(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments
    """
    r_id = 'QW-P-MWZSAURS'
    get_url = '{}/{}'.format(url.format('parthia123'), r_id)
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Merchant does not exist'

def test_get_payment_by_id_does_not_exist(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments
    """
    r_id = 'QW-P-F2613111'
    get_url = '{}/{}'.format(url.format('rome'), r_id)
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Payment does not exist'

def test_get_payment_by_id_as_merchant_staff_on_another_merchant(merchant_staff_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments
    """
    r_id = 'QW-P-MWZSAURS'
    get_url = '{}/{}'.format(url.format('parthia'), r_id)
    res = merchant_staff_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to get this merchant payment'

def test_get_payment_by_id_as_another_user(another_merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments
    """
    r_id = 'QW-P-MWZSAURS'
    get_url = '{}/{}'.format(url.format('rome'), r_id)
    res = another_merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to get this merchant payment'

## API: EXPORT PAYMENTS

def test_export_payments_successfully(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments/export
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

    export_url = '{}/export?token={}'.format(url.format('rome'), auth_data['exportToken'])
    res = merchant_admin_client.get(export_url)
    csv = str(res.data, 'utf-8')
    assert res.status_code == 200
    assert csv is not None

    # Do not include custom columns due to reordering problems
    lines = csv.splitlines()
    assert lines[0]
    assert lines[0].startswith(
        'transactionId,externalTransactionId,paymentReferenceId,invoiceReferenceId,enrollmentReferenceId,'
        'merchantCode,paymentStatus,settlementReferenceId,projectName,projectCategory,'
        'billBaseCurrency,billBaseAmount,billConvertedCurrency,billConvertedAmount,billFeeCurrency,billFeeAmount,'
        'billTotalCurrency,billTotalAmount,transactionType,paymentMode,paymentType,status,'
        'customerName,customerEmail,customerPhone,'
        'createdAt,submittedAt,paidAt,dueAt,transactionSource')

def test_export_payments_as_admin_successfully(admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments/export
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

    export_url = '{}/export?token={}'.format(url.format('rome'), auth_data['exportToken'])
    res = admin_client.get(export_url)
    csv = str(res.data, 'utf-8')
    assert res.status_code == 200
    assert csv is not None

    # Do not include custom columns due to reordering problems
    lines = csv.splitlines()
    assert lines[0]
    assert lines[0].startswith(
        'transactionId,externalTransactionId,paymentReferenceId,invoiceReferenceId,enrollmentReferenceId,'
        'merchantCode,paymentStatus,settlementReferenceId,projectName,projectCategory,'
        'billBaseCurrency,billBaseAmount,billConvertedCurrency,billConvertedAmount,billFeeCurrency,billFeeAmount,'
        'billTotalCurrency,billTotalAmount,transactionType,paymentMode,paymentType,status,'
        'customerName,customerEmail,customerPhone,'
        'createdAt,submittedAt,paidAt,dueAt,transactionSource')

def test_export_payments_as_staff_successfully(staff_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments/export
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

    res = staff_client.get('{}/export?token={}'.format(url.format('rome'), auth_data['exportToken']))
    csv = str(res.data, 'utf-8')
    assert res.status_code == 200
    assert csv is not None

    # Do not include custom columns due to reordering problems
    lines = csv.splitlines()
    assert lines[0]
    assert lines[0].startswith(
        'transactionId,externalTransactionId,paymentReferenceId,invoiceReferenceId,enrollmentReferenceId,'
        'merchantCode,paymentStatus,settlementReferenceId,projectName,projectCategory,'
        'billBaseCurrency,billBaseAmount,billConvertedCurrency,billConvertedAmount,billFeeCurrency,billFeeAmount,'
        'billTotalCurrency,billTotalAmount,transactionType,paymentMode,paymentType,status,'
        'customerName,customerEmail,customerPhone,'
        'createdAt,submittedAt,paidAt,dueAt,transactionSource')

def test_export_payments_without_export_token(client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments/export
    """
    res = client.get('{}/export'.format(url.format('rome')))
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized to export payments'

def test_export_payments_as_merchant_staff(merchant_staff_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments/export
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

def test_export_payments_on_incorrect_merchant(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments/export
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

    res = merchant_admin_client.get('{}/export?token={}'.format(
        url.format('gaul'),
        auth_data['exportToken']))
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to export payments'

def test_export_payments_on_random_token(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments/export
    """
    random_token = '218578t1y3hnqisahniqweiu'
    res = merchant_admin_client.get('{}/export?token={}'.format(url.format('rome'), random_token))
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized to export payments'

def test_export_payments_on_invalid_token(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments/export
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
    res = merchant_admin_client.get('{}/export?token={}'.format(url.format('rome'), invalid_token))
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized to export payments'

def test_export_payments_on_missing_user_on_invalid_token(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments/export
    """
    invalid_token = jsonwebtoken.encode({
        'merchant': {
            'id': 'china',
            'name': 'China'
        },
        'sessionkey': '125t8yghwmdskjfhn19mj19'
    }, 3)
    res = merchant_admin_client.get('{}/export?token={}'.format(url.format('rome'), invalid_token))
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized to export payments'

def test_export_payments_on_missing_merchant_on_invalid_token(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/payments/export
    """
    invalid_token = jsonwebtoken.encode({
        'user': {
            'id': '5c6fac029387ae13e29dd', #unknown ID
            'email': 'pompey@qwikwire.com'
        },
        'sessionkey': '125t8yghwmdskjfhn19mj19'
    }, 3)
    res = merchant_admin_client.get('{}/export?token={}'.format(url.format('rome'), invalid_token))
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized to export payments'

## API: REFUND PAYMENT

def test_refund_payment_as_admin_successfully(admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_code>/payments/<payment_reference_id>/refund
    """
    r_id = 'QW-P-DWJIOKML'
    post_url = '{}/{}/refund'.format(url.format('rome'), r_id)
    res = admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'refundTotalCurrency': 'USD',
        'refundTotalAmount': 2324.85,
        'refundReason': 'Fraudulent',
        'refundNotes': 'Stolen Card'
    }))
    data = res.json
    assert res.status_code == 200
    assert data['message'] == 'Payment status set to refunded'

def test_refund_payment_as_staff_successfully(staff_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_code>/payments/<payment_reference_id>/refund
    """
    r_id = 'QW-P-CJWT4NK5'
    post_url = '{}/{}/refund'.format(url.format('rome'), r_id)
    res = staff_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'refundTotalCurrency': 'USD',
        'refundTotalAmount': 430.35,
        'refundReason': 'Fraudulent',
        'refundNotes': 'Stolen Card'
    }))
    data = res.json
    assert res.status_code == 200
    assert data['message'] == 'Payment status set to refunded'

def test_refund_payment_as_merchant_admin(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_code>/payments/<payment_reference_id>/refund
    """
    r_id = 'QW-P-CJWT4NK5'
    post_url = '{}/{}/refund'.format(url.format('rome'), r_id)
    res = merchant_admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'refundTotalCurrency': 'USD',
        'refundTotalAmount': 430.35,
        'refundReason': 'Fraudulent',
        'refundNotes': 'Stolen Card'
    }))
    data = res.json
    assert res.status_code == 403
    assert data['message'] == 'You are not allowed here'

def test_refund_payment_over_refund_cap(staff_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_code>/payments/<payment_reference_id>/refund
    """
    r_id = 'QW-P-MWZSAURS'
    post_url = '{}/{}/refund'.format(url.format('rome'), r_id)
    res = staff_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({
        'refundTotalCurrency': 'USD',
        'refundTotalAmount': 999999,
        'refundReason': 'Fraudulent',
        'refundNotes': 'Stolen Card'
    }))
    data = res.json
    assert res.status_code == 400
    assert data['message'] == 'Submitted refund request contains missing or invalid required values'
