""" tests.api.test_merchant_controller.py """
# pylint: disable=redefined-outer-name,global-statement,unused-argument
# ^^^ this
from enum import Enum
import json
from tests.utils.token_storage import token_storage

url = '/xqwapi/merchants/{}/members'
member_url = '/xqwapi/merchants/{}/members/{}'
notif_url = '/xqwapi/merchants/{}/notifications'
email_url = '/xqwapi/merchants/{}/members/{}/invite'

class Categories(Enum):
    DEFAULT = 1
    REAL_ESTATE = 2
    BPO = 3

## GET MERCHANT MEMBERS

def test_get_merchant_members_as_admin_successfully(a_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/members
    """
    get_url = url.format(90000)
    res = a_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['members'] is not None
    assert data['totalCount'] == 5
    assert 'email' in data['members'][0]
    assert 'firstName' in data['members'][0]
    assert 'lastName' in data['members'][0]
    assert 'merchantRole' in data['members'][0]

def test_get_merchant_members_as_merchant_admin_successfully(ma_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/members
    """
    get_url = url.format(90000)
    res = ma_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['members'] is not None
    assert data['totalCount'] == 5
    assert 'email' in data['members'][0]
    assert 'firstName' in data['members'][0]
    assert 'lastName' in data['members'][0]
    assert 'merchantRole' in data['members'][0]

def test_get_merchant_members_as_merchant_staff(ms_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/members
    """
    get_url = url.format(90000)
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

def test_get_merchant_members_as_merchant_agent(mag_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/members
    """
    get_url = url.format(90000)
    res = mag_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_get_merchant_members_non_existing_merchant(ma_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/members
    """
    get_url = url.format(9900000)
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

def test_get_merchant_members_as_another_merchant_admin(ama_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/members
    """
    get_url = url.format(90000)
    res = ama_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_get_merchant_members_as_admin_no_members(a_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/members
    """
    get_url = url.format(90001)
    res = a_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert len(data['members']) == 0
    assert data['totalCount'] == 0

def test_get_merchant_members_as_another_merchant_staff_multiple_merchants(vma_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/members
    """
    get_url = url.format(90006)
    res = vma_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_get_merchant_members_as_another_merchant_agent_multiple_merchants(vma_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/members
    """
    get_url = url.format(90004)
    res = vma_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_get_merchant_members_as_merchant_admin_multiple_merchants(vma_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/members
    """
    get_url = url.format(90002)
    res = vma_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['members'] is not None
    assert data['totalCount'] == 2
    assert 'email' in data['members'][0]
    assert 'firstName' in data['members'][0]
    assert 'lastName' in data['members'][0]
    assert 'merchantRole' in data['members'][0]

# GET MERCHANT ROLES

def test_get_merchant_roles_as_admin(a_client, test_data):
    """
    GET /xqwapi/merchants/roles
    """
    res = a_client.get('/xqwapi/merchants/roles', headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['systemRoles'] is not None
    assert data['merchantRoles'] is not None

def test_get_merchant_roles_as_merchant_admin(ma_client, test_data):
    """
    GET /xqwapi/merchants/roles
    """
    res = ma_client.get('/xqwapi/merchants/roles', headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['systemRoles'] is not None
    assert data['merchantRoles'] is not None

# GET MERCHANT MEMBER NOTIFICATION SETTING

def test_get_merchant_member_notification_setting_as_admin(a_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/members/<user_id>
    """
    get_url = member_url.format(90000, 1000000)
    res = a_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to get another user\'s information'

def test_get_merchant_member_notification_setting_as_merchant_admin_successfully(ma_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/members/<user_id>
    """
    get_url = member_url.format(90000, 1000000)
    res = ma_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['canReceiveDailyTransactionEmails'] is True
    assert data['canReceivePaymentEmails'] is True
    assert data['canReceiveSettlementEmails'] is True

def test_get_merchant_member_notification_setting_as_merchant_staff(ms_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/members/<user_id>
    """
    get_url = member_url.format(90000, 1000001)
    res = ms_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert data is not None
    assert data['canReceiveDailyTransactionEmails'] is False
    assert data['canReceivePaymentEmails'] is True
    assert data['canReceiveSettlementEmails'] is False

def test_get_merchant_member_notification_setting_as_merchant_agent(mag_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/members/<user_id>
    """
    get_url = member_url.format(90000, 1000000)
    res = mag_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_get_merchant_member_notification_setting_as_another_merchant_staff_multiple_merchants(vma_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/members/<user_id>
    """
    get_url = member_url.format(90006, 1000014)
    res = vma_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_get_merchant_member_notification_setting_as_another_merchant_agent_multiple_merchants(vma_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/members/<user_id>
    """
    get_url = member_url.format(90004, 1000014)
    res = vma_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_get_merchant_member_notification_setting_as_merchant_admin_multiple_merchants(vma_client, test_data):
    """
    GET /xqwapi/merchants/<merchant_id>/members/<user_id>
    """
    get_url = member_url.format(90002, 1000014)
    res = vma_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['canReceiveDailyTransactionEmails'] is True
    assert data['canReceivePaymentEmails'] is True
    assert data['canReceiveSettlementEmails'] is True

# UPDATE MERCHANT MEMBER ROLE

def test_update_merchant_member_role_as_merchant_admin_successfully(ma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/members/<user_id>/roles/<role_id>
    """
    new_url = member_url.format(90000, 1000001)
    post_url = ('{}/roles/{}').format(new_url, 10)
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })

    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Merchant member role has been updated'

    # Roll back to original role
    new_url = member_url.format(90000, 1000001)
    post_url = ('{}/roles/{}').format(new_url, 20)
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })

    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Merchant member role has been updated'

def test_update_merchant_member_role_as_merchant_staff(ms_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/members/<user_id>/roles/<role_id>
    """
    new_url = member_url.format(90000, 1000001)
    post_url = ('{}/roles/{}').format(new_url, 10)
    res = ms_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Merchant member role has been updated'

def test_update_merchant_member_role_as_merchant_agent(mag_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/members/<user_id>/roles/<role_id>
    """
    new_url = member_url.format(90000, 1000000)
    post_url = ('{}/roles/{}').format(new_url, 10)
    res = mag_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_update_merchant_member_role_non_existing_merchant(ma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/members/<user_id>/roles/<role_id>
    """
    new_url = member_url.format(919191, 1000000)
    post_url = ('{}/roles/{}').format(new_url, 10)
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Merchant does not exist'

def test_update_merchant_member_role_as_another_merchant_admin(ama_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/members/<user_id>/roles/<role_id>
    """
    new_url = member_url.format(90000, 1000000)
    post_url = ('{}/roles/{}').format(new_url, 10)
    res = ama_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_update_merchant_member_role_user_not_found(ma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/members/<user_id>/roles/<role_id>
    """
    new_url = member_url.format(90000, 10000001)
    post_url = ('{}/roles/{}').format(new_url, 10)
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert data['message'] == 'User not found'

def test_update_merchant_member_role_user_not_found_disabled(ma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/members/<user_id>/roles/<role_id>
    """
    new_url = member_url.format(90000, 1000012)
    post_url = ('{}/roles/{}').format(new_url, 10)
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert data['message'] == 'User not found'

def test_update_merchant_member_role_change_owner_role(ma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/members/<user_id>/roles/<role_id>
    """
    new_url = member_url.format(90000, 1000000)
    post_url = ('{}/roles/{}').format(new_url, 20)
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert data['message'] == 'You are not allowed to update the merchant account owner\'s role'

def test_update_merchant_member_role_as_another_merchant_staff_multiple_merchants(vma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/members/<user_id>/roles/<role_id>
    """
    new_url = member_url.format(90006, 1000014)
    post_url = ('{}/roles/{}').format(new_url, 20)
    print(post_url)
    res = vma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_update_merchant_member_role_as_another_merchant_agent_multiple_merchants(vma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/members/<user_id>/roles/<role_id>
    """
    new_url = member_url.format(90004, 1000014)
    post_url = ('{}/roles/{}').format(new_url, 20)
    res = vma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_update_merchant_member_role_as_merchant_admin_multiple_merchants(vma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/members/<user_id>/roles/<role_id>
    """
    new_url = member_url.format(90002, 1000015)
    post_url = ('{}/roles/{}').format(new_url, 20)
    res = vma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Merchant member role has been updated'

# ADD MERCHANT MEMBER

def test_add_merchant_member_non_existing_merchant(ma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/members
    """
    post_url = url.format(9000000)
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Merchant does not exist'

def test_add_merchant_member_not_allowed_to_add_members(ama_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/members
    """
    post_url = url.format(90000)
    res = ama_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_add_merchant_member_missing_fields(ma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/members
    """
    post_url = url.format(90000)
    res = ma_client.post(post_url, data=json.dumps({
        'email': 'marcus@qwikwire.com',
        'merchantrole': 20
    }), headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert data['message'] == 'Added member has missing fields'
    assert data['fields'] is not None
    assert len(data['fields']) == 2

def test_add_merchant_member_as_merchant_staff(ms_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/members
    """
    post_url = url.format(90000)
    res = ms_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_add_merchant_member_as_merchant_agent(mag_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/members
    """
    post_url = url.format(90000)
    res = mag_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_add_merchant_member_as_merchant_admin_successfully(ma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/members
    """
    post_url = url.format(90000)
    res = ma_client.post(post_url, data=json.dumps({
        'email': 'jm@qwikwire.com',
        'firstname': 'JM',
        'lastname': 'Cabrera',
        'merchantrole': 20
    }), headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 201
    assert data is not None
    assert data['message'] == 'New merchant member jm@qwikwire.com created'
    assert data['person'] is not None
    assert 'email' in data['person']
    assert 'firstName' in data['person']
    assert 'lastName' in data['person']
    assert 'merchantRole' in data['person']

def test_add_merchant_member_as_another_merchant_staff_multiple_merchants(vma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/members
    """
    post_url = url.format(90006)
    print(post_url)
    res = vma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_add_merchant_member_as_another_merchant_agent_multiple_merchants(vma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/members
    """
    post_url = url.format(90004)
    res = vma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_add_merchant_member_as_merchant_admin_multiple_merchants(vma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/members
    """
    post_url = url.format(90002)
    res = vma_client.post(post_url, data=json.dumps({
        'email': 'jm+1@qwikwire.com',
        'firstname': 'JM',
        'lastname': 'Cabrera',
        'merchantrole': 20
    }), headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 201
    assert data is not None
    assert data['message'] == 'New merchant member jm+1@qwikwire.com created'
    assert data['person'] is not None
    assert 'email' in data['person']
    assert 'firstName' in data['person']
    assert 'lastName' in data['person']
    assert 'merchantRole' in data['person']

# DELETE MERCHANT MEMBER

def test_delete_merchant_member_non_existing_merchant(ma_client, test_data):
    """
    DELETE /xqwapi/merchants/<merchant_id>/members/<user_id>
    """
    delete_url = member_url.format(90000000, 1000013)
    res = ma_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Merchant does not exist'

def test_delete_merchant_member_as_another_merchant_admin(ama_client, test_data):
    """
    DELETE /xqwapi/merchants/<merchant_id>/members/<user_id>
    """
    delete_url = member_url.format(90000, 1000013)
    res = ama_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_delete_merchant_member_non_existing_user(ma_client, test_data):
    """
    DELETE /xqwapi/merchants/<merchant_id>/members/<user_id>
    """
    delete_url = member_url.format(90000, 1000013111)
    res = ma_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert data['message'] == 'User not found'

def test_delete_merchant_member_user_not_enabled(ma_client, test_data):
    """
    DELETE /xqwapi/merchants/<merchant_id>/members/<user_id>
    """
    delete_url = member_url.format(90000, 1000012)
    res = ma_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert data['message'] == 'User not found'

def test_delete_merchant_member_user_not_enabled(ma_client, test_data):
    """
    DELETE /xqwapi/merchants/<merchant_id>/members/<user_id>
    """
    delete_url = member_url.format(90000, 1000000)
    res = ma_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert data['message'] == 'You are not allowed to remove the merchant account owner'

def test_delete_merchant_member_as_merchant_admin_successfully(ma_client, test_data):
    """
    DELETE /xqwapi/merchants/<merchant_id>/members/<user_id>
    """
    delete_url = member_url.format(90000, 1000016)
    res = ma_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Member has been removed'

def test_delete_merchant_member_as_another_merchant_staff_multiple_merchants(vma_client, test_data):
    """
    DELETE /xqwapi/merchants/<merchant_id>/members/<user_id>
    """
    delete_url = member_url.format(90006, 1000017)
    res = vma_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_delete_merchant_member_as_another_merchant_agent_multiple_merchants(vma_client, test_data):
    """
    DELETE /xqwapi/merchants/<merchant_id>/members/<user_id>
    """
    delete_url = member_url.format(90004, 1000017)
    res = vma_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_delete_merchant_member_as_merchant_admin_multiple_merchants(vma_client, test_data):
    """
    DELETE /xqwapi/merchants/<merchant_id>/members/<user_id>
    """
    delete_url = member_url.format(90002, 1000017)
    res = vma_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Member has been removed'

# UPDATE MERCHANT MEMBER NOTIFICATION SETTINGS

def test_update_merchant_member_notification_settings_non_existing_merchant(ma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/notifications
    """
    post_url = notif_url.format(9000011)
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Merchant does not exist'

def test_update_merchant_member_notification_settings_as_another_merchant_admin(ama_client, test_data):
    """
    POST  /xqwapi/merchants/<merchant_id>/notifications
    """
    post_url = notif_url.format(90000)
    res = ama_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_update_merchant_member_notification_settings_as_merchant_staff(ms_client, test_data):
    """
    POST  /xqwapi/merchants/<merchant_id>/notifications
    """
    post_url = notif_url.format(90000)
    res = ms_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_update_merchant_member_notification_settings_as_merchant_agent(mag_client, test_data):
    """
    POST  /xqwapi/merchants/<merchant_id>/notifications
    """
    post_url = notif_url.format(90000)
    res = mag_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_update_merchant_member_notification_settings_as_merchant_admin_successfully(ma_client, test_data):
    """
    POST  /xqwapi/merchants/<merchant_id>/notifications
    """
    post_url = notif_url.format(90000)
    res = ma_client.post(post_url, data=json.dumps({
        'canReceiveDailyTransactionEmails': True,
        'canReceivePaymentEmails': True,
        'canReceiveSettlementEmails': False
    }), headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Merchant member notifications settings has been updated'

def test_update_merchant_member_notification_settings_as_another_merchant_staff_multiple_merchants(vma_client, test_data):
    """
    POST  /xqwapi/merchants/<merchant_id>/notifications
    """
    post_url = notif_url.format(90006)
    res = vma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_update_merchant_member_notification_settings_as_another_merchant_agent_multiple_merchants(vma_client, test_data):
    """
    POST  /xqwapi/merchants/<merchant_id>/notifications
    """
    post_url = notif_url.format(90004)
    res = vma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_update_merchant_member_notification_settings_as_merchant_admin_multiple_merchants(vma_client, test_data):
    """
    POST  /xqwapi/merchants/<merchant_id>/notifications
    """
    post_url = notif_url.format(90002)
    res = vma_client.post(post_url, data=json.dumps({
        'canReceiveDailyTransactionEmails': True,
        'canReceivePaymentEmails': True,
        'canReceiveSettlementEmails': False
    }), headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Merchant member notifications settings has been updated'

# SEND MERCHANT MEMBER INVITE

def test_send_merchant_member_invite_non_existing_merchant(ma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/members/<email>/invite
    """
    post_url = email_url.format(9000011, 'marcus@qwikwire.com')
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Merchant does not exist'

def test_send_merchant_member_invite_as_merchant_staff(ms_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/members/<email>/invite
    """
    post_url = email_url.format(90000, 'marcus@qwikwire.com')
    res = ms_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_send_merchant_member_invite_as_merchant_agent(mag_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/members/<email>/invite
    """
    post_url = email_url.format(90000, 'marcus@qwikwire.com')
    res = mag_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_send_merchant_member_invite_as_another_merchant_admin(ama_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/members/<email>/invite
    """
    post_url = email_url.format(90000, 'marcus@qwikwire.com')
    res = ama_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_send_merchant_member_invite_non_existing_user(ma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/members/<email>/invite
    """
    post_url = email_url.format(90000, 'marcussssss@qwikwire.com')
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert data['message'] == 'No user with email marcussssss@qwikwire.com found'

def test_send_merchant_member_invite_user_from_another_merchant(ma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/members/<email>/invite
    """
    post_url = email_url.format(90000, 'vercingetorix@qwikwire.com')
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to invite users from another merchant'

def test_send_merchant_member_invite_as_another_merchant_staff_multiple_merchants(vma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/members/<email>/invite
    """
    post_url = email_url.format(90006, 'mabini@qwikwire.com')
    res = vma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_send_merchant_member_invite_as_another_merchant_agent_multiple_merchants(vma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/members/<email>/invite
    """
    post_url = email_url.format(90004, 'mabini@qwikwire.com')
    res = vma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'
