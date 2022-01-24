""" tests.api.test_enrollment_controller.py """
# pylint: disable=redefined-outer-name,global-statement,unused-argument,too-many-lines
# ^^^ this
import json
from datetime import date
from dateutil.parser import parse as dt_parse
import pytest
from server.config import jsonwebtoken

__token = None
__refresh_token = None
__http_client_id = 'abcde12345abcde12345abcde12345abcde12345'

url = '/xqwapi/merchants/{}/enrollments'

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

# API: GET MERCHANT ENROLLMENTS

def test_get_enrollments_as_admin_successfully(admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments
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
    assert len(data['enrollments']) == 10

    enrollment = data['enrollments'][0]
    assert 'baseAmount' in enrollment
    assert 'createdAt' in enrollment
    assert 'customerEmail' in enrollment
    assert 'customerName' in enrollment
    assert 'customerPhone' in enrollment
    assert 'enrollmentEndDate' in enrollment
    assert 'enrollmentMonths' in enrollment
    assert 'enrollmentReferenceId' in enrollment
    assert 'enrollmentStartDate' in enrollment
    assert 'externalTransactionId' in enrollment
    assert 'merchantCode' in enrollment
    assert 'merchantId' in enrollment
    assert 'merchantName' in enrollment
    assert 'paymentMode' in enrollment
    assert 'paymentType' in enrollment
    assert 'paymentTypeName' in enrollment
    assert 'projectCategory' in enrollment
    assert 'projectCode' in enrollment
    assert 'projectName' in enrollment
    assert 'transactionId' in enrollment
    assert 'transactionStatus' in enrollment
    assert 'transactionType' in enrollment
    assert data['totalCount'] > 0
    assert data['size'] == 10
    assert data['page'] == 1

def test_get_enrollments_as_staff_successfully(staff_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments
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
    assert len(data['enrollments']) == 10
    assert data['totalCount'] > 0
    assert data['size'] == 10
    assert data['page'] == 1

def test_get_enrollments_as_merchant_admin_successfully(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments
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
    assert len(data['enrollments']) == 10
    assert data['totalCount'] > 0
    assert data['size'] == 10
    assert data['page'] == 1

def test_get_enrollments_as_merchant_staff(merchant_staff_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments
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
    assert data is not None
    assert data['enrollments']
    assert data['totalCount'] > 0
    assert data['size'] == 10
    assert data['page'] == 1

def test_get_enrollments_as_merchant_agent(merchant_agent_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments
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
    assert data['enrollments']
    assert data['totalCount'] > 0
    assert data['size'] == 10
    assert data['page'] == 1

def test_get_enrollments_as_another_admin(another_merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments
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
    assert data['message'] == 'You are not allowed to get the merchant enrollments'

def test_get_enrollments_without_token(client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments
    """
    get_url = url.format('rome')
    res = client.get(get_url, headers={
        'Content-Type': 'application/json'
    })
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized access'

def test_get_enrollments_on_ongoing_status_sucessfully(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments
    """
    get_url = '{}?{}'.format(url.format('rome'), 'status=ONGOING')
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert len(data['enrollments']) == 6
    assert data['totalCount'] > 0
    assert data['size'] == 10
    assert data['page'] == 1

def test_get_enrollments_on_project_pantheon_successfully(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments
    """
    get_url = '{}?{}'.format(url.format('rome'), 'project=100001&size=20')
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert len(data['enrollments']) == 20
    assert data['totalCount'] > 0
    assert data['size'] == 20
    assert data['page'] == 1

def test_get_enrollments_on_created_at_succesfully(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments
    """
    get_url = '{}?{}'.format(url.format('rome'), 'startday=2020-11-01&endday=2020-11-30&size=20')
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert len(data['enrollments']) == 1
    assert data['totalCount'] > 0
    assert data['size'] == 20
    assert data['page'] == 1

def test_get_enrollments_on_invalid_start_end_dates(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments
    """
    get_url = '{}?{}'.format(url.format('rome'), 'startday=2019-01-00&endday=2019')
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert len(data['enrollments']) == 10
    assert data['totalCount'] > 0
    assert data['size'] == 10
    assert data['page'] == 1

def test_get_enrollments_on_empty_page_and_size(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments
    """
    get_url = '{}?{}'.format(url.format('rome'), 'size=23&page=11')
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert not data['enrollments']
    assert data['totalCount'] == 0
    assert data['size'] == 23
    assert data['page'] == 11

def test_get_enrollments_on_invalid_page_and_size(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments
    """
    get_url = '{}?{}'.format(url.format('rome'), 'size=a&page=b')
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert len(data['enrollments']) == 10
    assert data['totalCount'] > 0
    assert data['size'] == 10
    assert data['page'] == 1

## API: GET ENROLLMENT BY ID

def test_get_enrollment_by_id_merchant_admin_successfully(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>
    """
    e_id = 'QW-E-PTMZG7PC'
    get_url = '{}/{}'.format(url.format('rome'), e_id)
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
        'baseAmount': ['PHP', 6771660.04],
        'createdAt': '2020-11-29T03:30:05.087000+08:00',
        'customFields': {
            'justNumber': {'label': 'JUST Number', 'value': '0101'},
            'unitNumber': {'label': 'Unit Number', 'value': '1010'}
        },
        'customerEmail': 'archie@qwikwire.com',
        'customerName': 'Cindy De Vera',
        'customerPhone': '641355',
        'enrollmentComment': None,
        'enrollmentEndDate': '2024-11-01T19:00:00+08:00',
        'enrollmentMonths': 48,
        'enrollmentReferenceId': 'QW-E-PTMZG7PC',
        'enrollmentStartDate': '2020-12-01T19:00:00+08:00',
        'externalTransactionId': '5FLJDWBN7RK6KDDB',
        'merchantCode': 'rome',
        'merchantId': 90000,
        'merchantName': 'Roman Empire',
        'paymentMethodBillingAddress': None,
        'paymentMethodCardLastFour': '3654',
        'paymentMethodCustomerName': 'thVgmoWW',
        'paymentMethodExpiry': None,
        'paymentMethodId': 9000005,
        'paymentMethodIssuer': 'Qwikwire',
        'paymentMethodName': 'cc',
        'paymentMethodOrigin': 'Vietnam',
        'paymentMethodProcessor': 'SB',
        'paymentMethodProcessorId': None,
        'paymentMethodProvider': 'Visa',
        'paymentMethodStatus': None,
        'paymentMethodType': None,
        'paymentMode': None,
        'paymentType': 'ROMA-VL',
        'paymentTypeName': 'Vicesima libertatis',
        'projectCategory': 'temple',
        'projectCode': None,
        'projectName': 'Pantheon',
        'transactionId': '9000005',
        'transactionStatus': 'ONGOING',
        'transactionType': 'ENROLLMENT'
    }
    for key in data_copy:
        assert key in data
        assert data_copy[key] == data[key]

def test_get_enrollment_by_id_merchant_staff_successfully(merchant_staff_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>
    """
    e_id = 'QW-E-PTMZG7PC'
    get_url = '{}/{}'.format(url.format('rome'), e_id)
    res = merchant_staff_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'transactionId' in data
    assert 'enrollmentReferenceId' in data

def test_get_enrollment_by_id_merchant_agent_successfully(merchant_agent_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>
    """
    e_id = 'QW-E-PTMZG7PC'
    get_url = '{}/{}'.format(url.format('rome'), e_id)
    res = merchant_agent_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'transactionId' in data
    assert 'enrollmentReferenceId' in data

def test_get_enrollment_by_id_as_admin_successfully(admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>
    """
    e_id = 'QW-E-PTMZG7PC'
    get_url = '{}/{}'.format(url.format('rome'), e_id)
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
    assert 'enrollmentReferenceId' in data

def test_get_enrollment_by_id_as_staff_successfully(staff_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>
    """
    e_id = 'QW-E-PTMZG7PC'
    get_url = '{}/{}'.format(url.format('rome'), e_id)
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
    assert 'enrollmentReferenceId' in data

def test_get_enrollment_by_id_as_another_merchant_admin(another_merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>
    """
    e_id = 'QW-E-PTMZG7PC'
    get_url = '{}/{}'.format(url.format('rome'), e_id)
    res = another_merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to get this enrollment'

def test_get_enrollment_by_id_without_token(client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>
    """
    e_id = 'QW-E-PTMZG7PC'
    get_url = '{}/{}'.format(url.format('rome'), e_id)
    res = client.get(get_url, headers={
        'Content-Type': 'application/json'
    })
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized access'

def test_get_enrollment_by_id_merchant_does_not_exist(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>
    """
    e_id = 'QW-E-PTMZG7PC'
    get_url = '{}/{}'.format(url.format('romanrepublic'), e_id)
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

def test_get_enrollment_by_id_merchant_does_not_exist_as_admin(admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>
    """
    e_id = 'QW-E-PTMZG7PC'
    get_url = '{}/{}'.format(url.format('romanrepublic'), e_id)
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

def test_get_enrollment_by_id_enrollment_does_not_exist(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>
    """
    e_id = 'QW-E-P1111111'
    get_url = '{}/{}'.format(url.format('rome'), e_id)
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Enrollment does not exist'

def test_get_enrollment_by_id_on_incorrect_merchant(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>
    """
    e_id = 'QW-E-PTMZG7PC'
    get_url = '{}/{}'.format(url.format('parthia'), e_id)
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to get this enrollment'

## API: GET ENROLLMENT INVOICES

def test_get_invoices_by_enrollment_as_merchant_admin_successfully(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>
    """
    e_id = 'QW-E-Z4VCHDPM'
    get_url = '{}/{}/invoices'.format(url.format('rome'), e_id)
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'invoices' in data
    assert 'totalCount' in data
    assert data['totalCount'] == 55
    data_copy = {
      'billBase': ['PHP', 2718.49],
      'billConverted': ['USD', 58.82],
      'billFee': ['USD', 0.0],
      'billTotal': ['USD', 58.82],
      'createdAt': '2020-09-26T14:05:06.818000+08:00',
      'dueAt': '2020-12-02T01:00:00+08:00',
      'invoiceDescription': 'Avida Land Corporation Auto Debit Enrollment ID: QW-E-Z4VCHDPM - Payment #2',
      'invoiceReferenceId': 'QW-I-JFRE36RS',
      'paidAt': '2020-12-01T16:01:53.502000+08:00',
      'paymentReferenceId': 'QW-P-Q2ZYMZUF',
      'retryAttemptCount': 0,
      'status': 'SETTLED',
      'submittedAt': None,
      'updatedAt': '2021-01-04T07:56:12.049092+08:00'
    }
    invoices = [i for i in data['invoices'] if i['invoiceReferenceId'] == 'QW-I-JFRE36RS']
    assert invoices
    assert invoices[0]
    assert 'invoiceId' in invoices[0]
    for key in data_copy:
        assert key in invoices[0]
        assert data_copy[key] == invoices[0][key]

def test_get_invoices_by_enrollment_as_merchant_staff_successfully(merchant_staff_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>
    """
    e_id = 'QW-E-Z4VCHDPM'
    get_url = '{}/{}/invoices'.format(url.format('rome'), e_id)
    res = merchant_staff_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'invoices' in data
    assert 'totalCount' in data

def test_get_invoices_by_enrollment_as_merchant_agent_successfully(merchant_agent_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>
    """
    e_id = 'QW-E-Z4VCHDPM'
    get_url = '{}/{}/invoices'.format(url.format('rome'), e_id)
    res = merchant_agent_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'invoices' in data
    assert 'totalCount' in data

def test_get_invoices_by_enrollment_as_admin_successfully(admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>
    """
    e_id = 'QW-E-Z4VCHDPM'
    get_url = '{}/{}/invoices'.format(url.format('rome'), e_id)
    res = admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'invoices' in data
    assert 'totalCount' in data

def test_get_invoices_by_enrollment_as_staff_successfully(staff_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>
    """
    e_id = 'QW-E-Z4VCHDPM'
    get_url = '{}/{}/invoices'.format(url.format('rome'), e_id)
    res = staff_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'invoices' in data
    assert 'totalCount' in data

def test_get_invoices_by_enrollment_as_another_user(another_merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>
    """
    e_id = 'QW-E-Z4VCHDPM'
    get_url = '{}/{}/invoices'.format(url.format('rome'), e_id)
    res = another_merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to get the enrollment invoices'

def test_get_invoices_by_enrollment_without_token(client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>
    """
    e_id = 'QW-E-Z4VCHDPM'
    get_url = '{}/{}/invoices'.format(url.format('rome'), e_id)
    res = client.get(get_url, headers={
        'Content-Type': 'application/json'
    })
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized access'

def test_get_invoices_by_enrollment_merchant_does_not_exist(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>
    """
    e_id = 'QW-E-Z4VCHDPM'
    get_url = '{}/{}/invoices'.format(url.format('romanrepublic'), e_id)
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

def test_get_invoices_by_enrollment_merchant_does_not_exist_as_admin(admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>
    """
    e_id = 'QW-E-Z4VCHDPM'
    get_url = '{}/{}/invoices'.format(url.format('romanrepublic'), e_id)
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

def test_get_invoices_by_enrollment_enrollment_does_not_exist(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>
    """
    e_id = 'QW-E-Z1111111'
    get_url = '{}/{}/invoices'.format(url.format('rome'), e_id)
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Enrollment does not exist'

def test_get_invoices_by_enrollment_on_incorrect_merchant(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>
    """
    e_id = 'QW-E-Z4VCHDPM'
    get_url = '{}/{}/invoices'.format(url.format('parthia'), e_id)
    res = merchant_admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to get the enrollment invoices'

def test_get_invoices_by_enrollment_on_incorrect_merchant_as_admin(admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>
    """
    e_id = 'QW-E-Z4VCHDPM'
    get_url = '{}/{}/invoices'.format(url.format('parthia'), e_id)
    res = admin_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Enrollment does not exist'

## API: EXPORT ENROLLMENTS

def test_export_enrollments_successfully(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/export
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
        'externalTransactionId,enrollmentReferenceId,transactionId,merchantCode,'
        'xsrfKey,projectName,projectCategory,billBase,transactionType,transactionStatus,'
        'paymentMode,paymentType,status,customerName,customerEmail,customerPhone,baseAmount,baseCurrency,'
        'enrollmentMonths,enrollmentStartDate,enrollmentEndDate,createdAt'
    )

def test_export_enrollments_as_merchant_staff(merchant_staff_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/export
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

def test_export_enrollments_as_admin_successfully(admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/export
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
        'externalTransactionId,enrollmentReferenceId,transactionId,merchantCode,'
        'xsrfKey,projectName,projectCategory,billBase,transactionType,transactionStatus,'
        'paymentMode,paymentType,status,customerName,customerEmail,customerPhone,baseAmount,baseCurrency,'
        'enrollmentMonths,enrollmentStartDate,enrollmentEndDate,createdAt'
    )

def test_export_enrollments_as_staff_successfully(staff_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/export
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

    export_url = '{}/export?token={}'.format(url.format('rome'), auth_data['exportToken'])
    res = staff_client.get(export_url)
    csv = str(res.data, 'utf-8')
    assert res.status_code == 200
    assert csv is not None

    # Do not include custom columns due to reordering problems
    lines = csv.splitlines()
    assert lines[0]
    assert lines[0].startswith(
        'externalTransactionId,enrollmentReferenceId,transactionId,merchantCode,'
        'xsrfKey,projectName,projectCategory,billBase,transactionType,transactionStatus,'
        'paymentMode,paymentType,status,customerName,customerEmail,customerPhone,baseAmount,baseCurrency,'
        'enrollmentMonths,enrollmentStartDate,enrollmentEndDate,createdAt'
    )

def test_export_enrollments_without_export_token(client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/export
    """
    res = client.get('{}/export'.format(url.format('rome')))
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized to export enrollments'

def test_export_enrollments_on_incorrect_merchant(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/export
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

    export_url = '{}/export?token={}'.format(url.format('gaul'), auth_data['exportToken'])
    res = merchant_admin_client.get(export_url)
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to export enrollments'

def test_export_enrollments_on_random_token(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/export
    """
    random_token = '218578t1y3hnqisahniqweiu'
    export_url = '{}/export?token={}'.format(url.format('rome'), random_token)
    res = merchant_admin_client.get(export_url)
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized to export enrollments'

def test_export_enrollments_on_invalid_token(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/export
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
    export_url = '{}/export?token={}'.format(url.format('rome'), invalid_token)
    res = merchant_admin_client.get(export_url)
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized to export enrollments'

def test_export_enrollments_on_missing_user_on_invalid_token(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/export
    """
    invalid_token = jsonwebtoken.encode({
        'merchant': {
            'id': 'china',
            'name': 'China'
        },
        'sessionkey': '125t8yghwmdskjfhn19mj19'
    }, 3)
    export_url = '{}/export?token={}'.format(url.format('rome'), invalid_token)
    res = merchant_admin_client.get(export_url)
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized to export enrollments'

def test_export_enrollments_on_missing_merchant_on_invalid_token(merchant_admin_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/enrollments/export
    """
    invalid_token = jsonwebtoken.encode({
        'user': {
            'id': '5c6fac029387ae13e29dd', #unknown ID
            'email': 'pompey@qwikwire.com'
        },
        'sessionkey': '125t8yghwmdskjfhn19mj19'
    }, 3)
    export_url = '{}/export?token={}'.format(url.format('rome'), invalid_token)
    res = merchant_admin_client.get(export_url)
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized to export enrollments'

## APPROVE ENROLLMENT

def test_approve_enrollment_as_merchant_admin_successfully(merchant_admin_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/approve
    """
    e_id = 'QW-E-FFN1111A'
    post_url = '{}/{}/approve'.format(url.format('rome'), e_id)
    res = merchant_admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'message' in data
    assert data['message'] == 'Enrollment has been approved'

def test_approve_enrollment_as_merchant_staff_successfully(merchant_staff_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/approve
    """
    e_id = 'QW-E-FFN2222B'
    post_url = '{}/{}/approve'.format(url.format('rome'), e_id)
    res = merchant_staff_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert 'message' in data
    assert data['message'] == 'You are not allowed here'

def test_approve_enrollment_as_admin_successfully(admin_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/approve
    """
    e_id = 'QW-E-FFN2222B'
    post_url = '{}/{}/approve'.format(url.format('rome'), e_id)
    res = admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'message' in data
    assert data['message'] == 'Enrollment has been approved'

def test_approve_enrollment_as_staff_successfully(staff_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/approve
    """
    e_id = 'QW-E-FFN3333C'
    post_url = '{}/{}/approve'.format(url.format('rome'), e_id)
    res = staff_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'message' in data
    assert data['message'] == 'Enrollment has been approved'

def test_approve_enrollment_with_invalid_start_date(staff_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/approve
    """
    e_id = 'QW-E-FFN4444D'
    post_url = '{}/{}/approve'.format(url.format('rome'), e_id)
    res = staff_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert 'message' in data
    assert data['message'] == 'Enrollment has not been approved'

    get_url = '{}/{}/invoices'.format(url.format('rome'), e_id)
    invoices_res = staff_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    invoices_data = invoices_res.json
    assert invoices_res.status_code == 200
    assert invoices_data is not None
    assert 'totalCount' in invoices_data
    assert 'invoices' in invoices_data
    assert not invoices_data['invoices']

def test_approve_enrollment_with_big_month_span(staff_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/approve
    """
    e_id = 'QW-E-FFN596GG'
    post_url = '{}/{}/approve'.format(url.format('rome'), e_id)
    res = staff_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert 'message' in data
    assert data['message'] == 'Enrollment has not been approved'

    get_url = '{}/{}/invoices'.format(url.format('rome'), e_id)
    invoices_res = staff_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    invoices_data = invoices_res.json
    assert invoices_res.status_code == 200
    assert invoices_data is not None
    assert 'totalCount' in invoices_data
    assert 'invoices' in invoices_data
    assert not invoices_data['invoices']

def test_approve_enrollment_with_negative_month_span(staff_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/approve
    """
    e_id = 'QW-E-9212CRJQ'
    post_url = '{}/{}/approve'.format(url.format('rome'), e_id)
    res = staff_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert 'message' in data
    assert data['message'] == 'Enrollment has not been approved'

    get_url = '{}/{}/invoices'.format(url.format('rome'), e_id)
    invoices_res = staff_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    invoices_data = invoices_res.json
    assert invoices_res.status_code == 200
    assert invoices_data is not None
    assert 'totalCount' in invoices_data
    assert 'invoices' in invoices_data
    assert not invoices_data['invoices']

def test_approve_enrollment_as_another_user(another_merchant_admin_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/approve
    """
    e_id = 'QW-E-9212CR12'
    post_url = '{}/{}/approve'.format(url.format('rome'), e_id)
    res = another_merchant_admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to approve an enrollment'

def test_approve_enrollment_without_token(client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/approve
    """
    e_id = 'QW-E-9212CR12'
    post_url = '{}/{}/approve'.format(url.format('rome'), e_id)
    res = client.post(post_url, headers={
        'Content-Type': 'application/json'
    })
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized access'

def test_approve_enrollment_merchant_does_not_exist(merchant_admin_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/approve
    """
    e_id = 'QW-E-9212CR12'
    post_url = '{}/{}/approve'.format(url.format('romanrepublic'), e_id)
    res = merchant_admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Merchant does not exist'

def test_approve_enrollment_merchant_does_not_exist_as_admin(admin_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/approve
    """
    e_id = 'QW-E-9212CR12'
    post_url = '{}/{}/approve'.format(url.format('romanrepublic'), e_id)
    res = admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Merchant does not exist'

def test_approve_enrollment_does_not_exist(merchant_admin_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/approve
    """
    e_id = 'QW-E-A000000'
    post_url = '{}/{}/approve'.format(url.format('rome'), e_id)
    res = merchant_admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Enrollment does not exist'

def test_approve_enrollment_on_incorrect_merchant(merchant_admin_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/approve
    """
    e_id = 'QW-E-9212CR12'
    post_url = '{}/{}/approve'.format(url.format('parthia'), e_id)
    res = merchant_admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to approve an enrollment'

## DECLINE ENROLLMENT

def test_decline_enrollment_as_merchant_admin_successfully(merchant_admin_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/decline
    """
    e_id = 'QW-E-FFN44509'
    post_url = '{}/{}/decline'.format(url.format('rome'), e_id)
    res = merchant_admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({'comment': 'Enrollment is invalid'}))
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'message' in data
    assert data['message'] == 'Enrollment has been declined'

def test_decline_enrollment_as_merchant_staff_successfully(merchant_staff_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/decline
    """
    e_id = 'QW-E-FFN44510'
    post_url = '{}/{}/decline'.format(url.format('rome'), e_id)
    res = merchant_staff_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({'comment': 'Enrollment is invalid'}))
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert 'message' in data
    assert data['message'] == 'You are not allowed here'

def test_decline_enrollment_as_admin_successfully(admin_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/decline
    """
    e_id = 'QW-E-FFN44511'
    post_url = '{}/{}/decline'.format(url.format('rome'), e_id)
    res = admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({'comment': 'Enrollment is invalid'}))
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'message' in data
    assert data['message'] == 'Enrollment has been declined'

def test_decline_enrollment_as_staff_successfully(staff_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/decline
    """
    e_id = 'QW-E-FFN44512'
    post_url = '{}/{}/decline'.format(url.format('rome'), e_id)
    res = staff_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({'comment': 'Enrollment is invalid'}))
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'message' in data
    assert data['message'] == 'Enrollment has been declined'

def test_decline_enrollment_as_another_user(another_merchant_admin_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/decline
    """
    e_id = 'QW-E-FFN0136X'
    post_url = '{}/{}/decline'.format(url.format('rome'), e_id)
    res = another_merchant_admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({'comment': 'Enrollment is invalid'}))
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to decline an enrollment'

def test_decline_enrollment_without_token(client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/decline
    """
    e_id = 'QW-E-FFN0136X'
    post_url = '{}/{}/decline'.format(url.format('rome'), e_id)
    res = client.post(post_url, headers={
        'Content-Type': 'application/json'
    }, data=json.dumps({'comment': 'Enrollment is invalid'}))
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized access'

def test_decline_enrollment_merchant_does_not_exist(merchant_admin_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/decline
    """
    e_id = 'QW-E-FFN0136X'
    post_url = '{}/{}/decline'.format(url.format('romanrepublic'), e_id)
    res = merchant_admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({'comment': 'Enrollment is invalid'}))
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Merchant does not exist'

def test_decline_enrollment_merchant_does_not_exist_as_admin(admin_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/decline
    """
    e_id = 'QW-E-FFN0136X'
    post_url = '{}/{}/decline'.format(url.format('romanrepublic'), e_id)
    res = admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({'comment': 'Enrollment is invalid'}))
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Merchant does not exist'

def test_decline_enrollment_does_not_exist(merchant_admin_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/decline
    """
    e_id = 'QW-E-F0000000'
    post_url = '{}/{}/decline'.format(url.format('rome'), e_id)
    res = merchant_admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({'comment': 'Enrollment is invalid'}))
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Enrollment does not exist'

def test_decline_enrollment_on_incorrect_merchant(merchant_admin_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/decline
    """
    e_id = 'QW-E-FFN0136X'
    post_url = '{}/{}/decline'.format(url.format('parthia'), e_id)
    res = merchant_admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({'comment': 'Enrollment is invalid'}))
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to decline an enrollment'

def test_decline_enrollment_wihout_comment(merchant_admin_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/decline
    """
    e_id = 'QW-E-FFN0136X'
    post_url = '{}/{}/decline'.format(url.format('parthia'), e_id)
    res = merchant_admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({}))
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert data['message'] == 'The comment is missing'

## CANCEL ENROLLMENT

def test_cancel_enrollment_as_merchant_admin_successfully(merchant_admin_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/cancel
    """
    e_id = 'QW-E-YFRGF36S'
    post_url = '{}/{}/cancel'.format(url.format('rome'), e_id)
    res = merchant_admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({'comment': 'Enrollment is invalid'}))
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'message' in data
    assert data['message'] == 'Enrollment has been cancelled'

def test_cancel_enrollment_as_merchant_staff_successfully(merchant_staff_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/cancel
    """
    e_id = 'QW-E-X2KFCXHV'
    post_url = '{}/{}/cancel'.format(url.format('rome'), e_id)
    res = merchant_staff_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({'comment': 'Enrollment is invalid'}))
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert 'message' in data
    assert data['message'] == 'You are not allowed here'

def test_cancel_enrollment_as_admin_successfully(admin_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/cancel
    """
    e_id = 'QW-E-X2KFCXHV'
    post_url = '{}/{}/cancel'.format(url.format('rome'), e_id)
    res = admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({'comment': 'Enrollment is invalid'}))
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'message' in data
    assert data['message'] == 'Enrollment has been cancelled'

def test_cancel_enrollment_as_staff_successfully(staff_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/cancel
    """
    e_id = 'QW-E-VN5553AN'
    post_url = '{}/{}/cancel'.format(url.format('rome'), e_id)
    res = staff_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({'comment': 'Enrollment is invalid'}))
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'message' in data
    assert data['message'] == 'Enrollment has been cancelled'

def test_cancel_enrollment_as_another_user(another_merchant_admin_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/cancel
    """
    e_id = 'QW-E-2VJUCKEY'
    post_url = '{}/{}/cancel'.format(url.format('rome'), e_id)
    res = another_merchant_admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({'comment': 'Enrollment is invalid'}))
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to cancel an enrollment'

def test_cancel_enrollment_without_token(client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/cancel
    """
    e_id = 'QW-E-2VJUCKEY'
    post_url = '{}/{}/cancel'.format(url.format('rome'), e_id)
    res = client.post(post_url, headers={
        'Content-Type': 'application/json'
    }, data=json.dumps({'comment': 'Enrollment is invalid'}))
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized access'

def test_cancel_enrollment_merchant_does_not_exist(merchant_admin_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/cancel
    """
    e_id = 'QW-E-2VJUCKEY'
    post_url = '{}/{}/cancel'.format(url.format('romanrepublic'), e_id)
    res = merchant_admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({'comment': 'Enrollment is invalid'}))
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Merchant does not exist'

def test_cancel_enrollment_merchant_does_not_exist_as_admin(admin_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/cancel
    """
    e_id = 'QW-E-2VJUCKEY'
    post_url = '{}/{}/cancel'.format(url.format('romanrepublic'), e_id)
    res = admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({'comment': 'Enrollment is invalid'}))
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Merchant does not exist'

def test_cancel_enrollment_does_not_exist(merchant_admin_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/cancel
    """
    e_id = 'QW-E-F0000111'
    post_url = '{}/{}/cancel'.format(url.format('rome'), e_id)
    res = merchant_admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({'comment': 'Enrollment is invalid'}))
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Enrollment does not exist'

def test_cancel_enrollment_on_incorrect_merchant(merchant_admin_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/cancel
    """
    e_id = 'QW-E-2VJUCKEY'
    post_url = '{}/{}/cancel'.format(url.format('parthia'), e_id)
    res = merchant_admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({'comment': 'Enrollment is invalid'}))
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to cancel an enrollment'

def test_cancel_enrollment_wihout_comment(merchant_admin_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/enrollments/<enrollment_reference_id>/cancel
    """
    e_id = 'QW-E-2VJUCKEY'
    post_url = '{}/{}/cancel'.format(url.format('rome'), e_id)
    res = merchant_admin_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(__token or ''),
        'X-Client-Id': __http_client_id,
        'X-Refresh-Token': __refresh_token
    }, data=json.dumps({}))
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert data['message'] == 'The comment is missing'
