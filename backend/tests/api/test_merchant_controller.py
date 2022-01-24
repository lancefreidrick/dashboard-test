""" tests.api.test_merchant_controller.py """
# pylint: disable=redefined-outer-name,global-statement,unused-argument
# ^^^ this
from enum import Enum
import json
from tests.utils.token_storage import token_storage

url = '/xqwapi/merchants'

class Categories(Enum):
    DEFAULT = 1
    REAL_ESTATE = 2
    BPO = 3

## GET MERCHANTS

def test_get_merchants_as_admin_successfully(a_client, test_data):
    """
    GET /xqwapi/merchants
    """
    res = a_client.get(url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['merchants'] is not None
    assert data['totalCount'] == 6
    assert 'address' in data['merchants'][0]
    assert 'categoryDescription' in data['merchants'][0]
    assert 'categoryId' in data['merchants'][0]
    assert 'categoryName' in data['merchants'][0]
    assert 'code' in data['merchants'][0]
    assert 'id' in data['merchants'][0]
    assert 'invoicingMode' in data['merchants'][0]
    assert 'isActive' in data['merchants'][0]
    assert 'isPortals3Configured' in data['merchants'][0]
    assert 'isPublic' in data['merchants'][0]
    assert 'name' in data['merchants'][0]
    assert 'paymentModes' in data['merchants'][0]
    assert 'paymentTypes' in data['merchants'][0]
    assert 'projects' in data['merchants'][0]
    assert 'timezone' in data['merchants'][0]

def test_get_merchants_as_staff_successfully(s_client, test_data):
    """
    GET /xqwapi/merchants
    """
    res = s_client.get(url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['merchants'] is not None
    assert data['totalCount'] == 6

def test_get_merchants_as_merchant_admin_successfully(ma_client, test_data):
    """
    GET /xqwapi/merchants
    """
    res = ma_client.get(url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['merchants'] is not None
    assert data['totalCount'] == 1

def test_get_merchants_as_merchant_staff_successfully(ms_client, test_data):
    """
    GET /xqwapi/merchants
    """
    res = ms_client.get(url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['merchants'] is not None
    assert data['totalCount'] == 1

def test_get_merchants_as_another_merchant_admin_successfully(ama_client, test_data):
    """
    GET /xqwapi/merchants
    """
    res = ama_client.get(url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['merchants'] is not None
    assert data['totalCount'] == 1

def test_get_merchants_without_token(client, test_data):
    """
    GET /xqwapi/merchants
    """
    res = client.get(url, headers={
        'Content-Type': 'application/json'
    })
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized access'

def test_get_merchants_as_multiple_merchant_admin_successfully(mma_client, test_data):
    """
    GET /xqwapi/merchants
    """
    res = mma_client.get(url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['merchants'] is not None
    assert data['totalCount'] == 2

def test_get_merchants_on_page_2(a_client, test_data):
    """
    GET /xqwapi/merchants
    """
    get_url = '{0}?page={1}&size={2}'.format(url, 2, 2)
    res = a_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['merchants'] is not None
    assert len(data['merchants']) == 2
    assert data['totalCount'] == 6

## FIND MERCHANT BY ID

def test_find_merchant_by_code_as_admin_successfully(a_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>
    """
    get_url = '{}/rome'.format(url)
    res = a_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'address' in data
    assert 'categoryDescription' in data
    assert 'categoryId' in data
    assert 'categoryName' in data
    assert 'code' in data
    assert 'id' in data
    assert 'invoicingMode' in data
    assert 'isActive' in data
    assert 'isPortals3Configured' in data
    assert 'isPublic' in data
    assert 'logo' in data
    assert 'name' in data
    assert 'paymentModes' in data
    assert 'paymentTypes' in data
    assert 'projects' in data
    assert 'timezone' in data

def test_find_merchant_by_code_as_staff_successfully(s_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>
    """
    get_url = '{}/rome'.format(url)
    res = s_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None

def test_find_merchant_by_code_as_merchant_admin_successfully(ma_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>
    """
    get_url = '{}/rome'.format(url)
    res = ma_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None

def test_find_merchant_by_code_as_merchant_staff_successfully(ms_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>
    """
    get_url = '{}/rome'.format(url)
    res = ms_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None

def test_find_merchant_by_code_as_merchant_agent_successfully(mag_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>
    """
    get_url = '{}/rome'.format(url)
    res = mag_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None

def test_find_merchant_by_code_as_another_merchant_admin(ama_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>
    """
    get_url = '{}/rome'.format(url)
    res = ama_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to get this merchant'

def test_find_merchant_by_code_as_multiple_merchant_admin_successfully(mma_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>
    """
    get_url = '{}/rome'.format(url)
    res = mma_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None

def test_find_merchant_by_code_without_token(client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>
    """
    get_url = '{}/rome'.format(url)
    res = client.get(get_url, headers={
        'Content-Type': 'application/json',
    })
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized access'

def test_find_merchant_by_code_not_found(ma_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>
    """
    get_url = '{}/romanrepublic'.format(url)
    res = ma_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Merchant does not exist'

## UPDATE MERCHANT

def test_update_merchant_as_admin_successfully(a_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>
    """
    post_url = '{0}/{1}'.format(url, 'rome')
    res = a_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': 'Roma',
        'category': Categories.DEFAULT.value,
        'address': {
            'addressOne': 'Palace of the Emperor',
            'addressTwo': 'Rome',
            'addressThree': 'Roman Empire'
        },
        'timezone': 'Asia/Manila'
    }))
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'message' in data
    assert data['message'] == 'Merchant account information has been saved'

def test_update_merchant_as_staff_successfully(s_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>
    """
    post_url = '{0}/{1}'.format(url, 'rome')
    res = s_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': 'Roma',
        'category': Categories.DEFAULT.value,
        'address': {
            'addressOne': 'Palace of the Emperor',
            'addressTwo': 'Rome',
            'addressThree': 'Roman Empire'
        },
        'timezone': 'Asia/Singapore'
    }))
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'message' in data
    assert data['message'] == 'Merchant account information has been saved'

def test_update_merchant_as_merchant_admin_successfully(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>
    """
    post_url = '{0}/{1}'.format(url, 'rome')
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': 'Rome',
        'category': Categories.DEFAULT.value,
        'address': {
            'addressOne': 'Palace of the Emperor',
            'addressTwo': 'Rome',
            'addressThree': 'Roman Empire'
        },
        'timezone': 'Asia/Manila'
    }))
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'message' in data
    assert data['message'] == 'Merchant account information has been saved'

def test_update_merchant_as_merchant_staff(ms_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>
    """
    post_url = '{0}/{1}'.format(url, 'rome')
    res = ms_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': 'Rome',
        'category': Categories.DEFAULT.value,
        'address': {
            'addressOne': 'Palace of the Emperor',
            'addressTwo': 'Rome',
            'addressThree': 'Roman Empire'
        },
        'timezone': 'Asia/Singapore'
    }))
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_update_merchant_as_another_merchant_admin(ama_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>
    """
    post_url = '{0}/{1}'.format(url, 'rome')
    res = ama_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': 'Rome',
        'category': Categories.DEFAULT.value,
        'address': {
            'addressOne': 'Palace of the Emperor',
            'addressTwo': 'Rome',
            'addressThree': 'Roman Empire'
        },
        'timezone': 'Asia/Singapore'
    }))
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to update the merchant'

def test_update_merchant_as_multiple_merchant_admin_successfully(mma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>
    """
    post_url = '{0}/{1}'.format(url, 'rome')
    res = mma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': 'Rome',
        'category': Categories.DEFAULT.value,
        'address': {
            'addressOne': 'Palace of the Emperor',
            'addressTwo': 'Rome',
            'addressThree': 'Roman Empire'
        },
        'timezone': 'Asia/Singapore'
    }))
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Merchant account information has been saved'

def test_update_merchant_without_token(client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>
    """
    post_url = '{0}/{1}'.format(url, 'rome')
    res = client.post(post_url, headers={
        'Content-Type': 'application/json'
    }, data=json.dumps({
        'name': 'Roma Republika',
        'category': Categories.DEFAULT.value,
        'address': {
            'addressOne': 'Palace of the Emperor',
            'addressTwo': 'Rome',
            'addressThree': 'Roman Empire'
        },
        'timezone': 'Asia/Singapore'
    }))
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized access'

def test_update_merchant_on_empty_request_body(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>
    """
    post_url = '{0}/{1}'.format(url, 'rome')
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({}))
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert data['message'] == 'Submitted merchant has form validation errors'
    assert data['fields'] == {
        'name': ['Missing data for required field.'],
        'timezone': ['Missing data for required field.'],
        'category': ['Missing data for required field.'],
        'address': ['Missing data for required field.']
    }

def test_update_merchant_on_name_more_than_50chars(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>
    """
    post_url = '{0}/{1}'.format(url, 'rome')
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': 'Roma Republika Roma Republika Roma Republika Roma Republika Roma Republika Roma Republika',
        'category': Categories.DEFAULT.value,
        'address': {
            'addressOne': 'Palace of the Emperor',
            'addressTwo': 'Rome',
            'addressThree': 'Roman Empire'
        },
        'timezone': 'Asia/Singapore'
    }))
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert data['message'] == 'Submitted merchant has form validation errors'
    assert data['fields'] == {
        'name': ['Length must be between 3 and 50.']
    }

def test_update_merchant_on_invalid_timezone(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>
    """
    post_url = '{0}/{1}'.format(url, 'rome')
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': 'Rome',
        'category': Categories.DEFAULT.value,
        'address': {
            'addressOne': 'Palace of the Emperor',
            'addressTwo': 'Rome',
            'addressThree': 'Roman Empire'
        },
        'timezone': 'Invalid/Timezone'
    }))
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert data['message'] == 'Submitted merchant has form validation errors'
    assert data['fields'] == {
        'timezone': ['Must be a valid timezone']
    }

def test_update_merchant_on_empty_addresses(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>
    """
    post_url = '{0}/{1}'.format(url, 'rome')
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': 'Rome',
        'category': Categories.DEFAULT.value,
        'address': {
            'addressOne': None,
            'addressTwo': None,
            'addressThree': None
        },
        'timezone': 'Asia/Manila'
    }))
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert data['message'] == 'Submitted merchant has form validation errors'
    assert data['fields'] == {
        'address': {
            'addressTwo': ['Field may not be null.'],
            'addressThree': ['Field may not be null.'],
            'addressOne': ['Field may not be null.']
        }
    }

def test_update_merchant_on_empty_category(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>
    """
    post_url = '{0}/{1}'.format(url, 'rome')
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': 'Rome',
        'category': 100,
        'address': {
            'addressOne': 'Palace of the Emperor',
            'addressTwo': 'Rome',
            'addressThree': 'Roman Empire'
        },
        'timezone': 'Asia/Manila'
    }))
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert data['message'] == 'Category does not exist'

def test_update_merchant_does_not_exist(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>
    """
    post_url = '{0}/{1}'.format(url, 'catch22')
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': 'Rome',
        'category': 100,
        'address': {
            'addressOne': 'Palace of the Emperor',
            'addressTwo': 'Rome',
            'addressThree': 'Roman Empire'
        },
        'timezone': 'Asia/Manila'
    }))
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Merchant does not exist'

## GET MERCHANT CATEGORIES

def test_get_merchant_categories_as_admin_successfully(a_client, test_data):
    """
    GET /xqapi/merchants/categories
    """
    get_url = '{0}/categories'.format(url)
    res = a_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert len(data) == 3
    assert 'id' in data[0]
    assert 'name' in data[0]
    assert 'description' in data[0]

def test_get_merchant_categories_as_staff_successfully(s_client, test_data):
    """
    GET /xqapi/merchants/categories
    """
    get_url = '{0}/categories'.format(url)
    res = s_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert len(data) == 3
    assert 'id' in data[0]
    assert 'name' in data[0]
    assert 'description' in data[0]

def test_get_merchant_categories_as_merchant_admin_successfully(ma_client, test_data):
    """
    GET /xqapi/merchants/categories
    """
    get_url = '{0}/categories'.format(url)
    res = ma_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert len(data) == 3
    assert 'id' in data[0]
    assert 'name' in data[0]
    assert 'description' in data[0]

def test_get_merchant_categories_as_merchant_staff(ms_client, test_data):
    """
    GET /xqapi/merchants/categories
    """
    get_url = '{0}/categories'.format(url)
    res = ms_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_get_merchant_categories_as_another_merchant_admin_successfully(ama_client, test_data):
    """
    GET /xqapi/merchants/categories
    """
    get_url = '{0}/categories'.format(url)
    res = ama_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert len(data) == 3
    assert 'id' in data[0]
    assert 'name' in data[0]
    assert 'description' in data[0]

def test_get_merchant_categories_as_multiple_merchant_admin_successfully(mma_client, test_data):
    """
    GET /xqapi/merchants/categories
    """
    get_url = '{0}/categories'.format(url)
    res = mma_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert len(data) == 3
    assert 'id' in data[0]
    assert 'name' in data[0]
    assert 'description' in data[0]

def test_get_merchant_categories_without_token(client, test_data):
    """
    GET /xqapi/merchants/categories
    """
    get_url = '{0}/categories'.format(url)
    res = client.get(get_url, headers={
        'Content-Type': 'application/json',
    })
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized access'
