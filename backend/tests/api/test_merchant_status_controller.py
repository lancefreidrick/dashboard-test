""" tests.api.test_merchant_controller.py """
# pylint: disable=redefined-outer-name,global-statement,unused-argument
# ^^^ this
import json
from tests.utils.token_storage import token_storage

close_url = '/xqwapi/merchants/{}/close'
suspend_url = '/xqwapi/merchants/{}/suspend'
activate_url = '/xqwapi/merchants/{}/activate'

m_rome_id = 90000
m_not_exist = 90099

# Suspend Merchant

def test_update_merchant_status_suspend_as_admin_successfully(a_client, test_data):
    """
    POST /xqwapi/merchants/<int:merchant_id>/suspend
    """
    post_url = suspend_url.format(m_rome_id)
    res = a_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Merchant account has been suspended'

def test_update_merchant_status_suspend_on_merchant_does_not_exist(a_client, test_data):
    """
    POST /xqwapi/merchants/<int:merchant_id>/suspend
    """
    post_url = suspend_url.format(m_not_exist)
    res = a_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Merchant does not exist'

def test_update_merchant_status_suspend_as_merchant_admin(ma_client, test_data):
    """
    POST /xqwapi/merchants/<int:merchant_id>/suspend 
    """
    post_url = suspend_url.format(m_rome_id)
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_update_merchant_status_suspend_as_merchant_staff(ms_client, test_data):
    """
    POST /xqwapi/merchants/<int:merchant_id>/suspend 
    """
    post_url = suspend_url.format(m_rome_id)
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

def test_update_merchant_status_suspend_as_merchant_agent(mag_client, test_data):
    """
    POST /xqwapi/merchants/<int:merchant_id>/suspend 
    """
    post_url = suspend_url.format(m_rome_id)
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

def test_update_merchant_status_suspend_as_staff(s_client, test_data):
    """
    POST /xqwapi/merchants/<int:merchant_id>/suspend 
    """
    post_url = suspend_url.format(m_rome_id)
    res = s_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_update_merchant_status_suspend_as_another_merchant_admin(ama_client, test_data):
    """
    POST /xqwapi/merchants/<int:merchant_id>/suspend 
    """
    post_url = suspend_url.format(m_rome_id)
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

# Close Merchant

def test_update_merchant_status_close_as_admin_successfully(a_client, test_data):
    """
    POST /xqwapi/merchants/<int:merchant_id>/close
    """
    post_url = close_url.format(m_rome_id)
    res = a_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Merchant account has been closed'

def test_update_merchant_status_close_on_merchant_does_not_exist(a_client, test_data):
    """
    POST /xqwapi/merchants/<int:merchant_id>/close
    """
    post_url = close_url.format(m_not_exist)
    res = a_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Merchant does not exist'

def test_update_merchant_status_close_as_merchant_admin(ma_client, test_data):
    """
    POST /xqwapi/merchants/<int:merchant_id>/close
    """
    post_url = close_url.format(m_rome_id)
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_update_merchant_status_close_as_merchant_staff(ms_client, test_data):
    """
    POST /xqwapi/merchants/<int:merchant_id>/close
    """
    post_url = close_url.format(m_rome_id)
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

def test_update_merchant_status_close_as_merchant_agent(mag_client, test_data):
    """
    POST /xqwapi/merchants/<int:merchant_id>/close
    """
    post_url = close_url.format(m_rome_id)
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

def test_update_merchant_status_close_as_staff(s_client, test_data):
    """
    POST /xqwapi/merchants/<int:merchant_id>/close
    """
    post_url = close_url.format(m_rome_id)
    res = s_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_update_merchant_status_close_as_another_merchant_admin(ama_client, test_data):
    """
    POST /xqwapi/merchants/<int:merchant_id>/close
    """
    post_url = close_url.format(m_rome_id)
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

# Active Merchant

def test_update_merchant_status_activate_as_admin_successfully(a_client, test_data):
    """
    POST /xqwapi/merchants/<int:merchant_id>/activate
    """
    post_url = activate_url.format(m_rome_id)
    res = a_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Merchant account has been activated'

def test_update_merchant_status_activate_on_merchant_does_not_exist(a_client, test_data):
    """
    POST /xqwapi/merchants/<int:merchant_id>/activate
    """
    post_url = activate_url.format(m_not_exist)
    res = a_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Merchant does not exist'

def test_update_merchant_status_activate_as_merchant_admin(ma_client, test_data):
    """
    POST /xqwapi/merchants/<int:merchant_id>/activate 
    """
    post_url = activate_url.format(m_rome_id)
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_update_merchant_status_activate_as_merchant_staff(ms_client, test_data):
    """
    POST /xqwapi/merchants/<int:merchant_id>/activate 
    """
    post_url = activate_url.format(m_rome_id)
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

def test_update_merchant_status_activate_as_merchant_agent(mag_client, test_data):
    """
    POST /xqwapi/merchants/<int:merchant_id>/activate 
    """
    post_url = activate_url.format(m_rome_id)
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

def test_update_merchant_status_activate_as_staff(s_client, test_data):
    """
    POST /xqwapi/merchants/<int:merchant_id>/activate 
    """
    post_url = activate_url.format(m_rome_id)
    res = s_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_update_merchant_status_activate_as_another_merchant_admin(ama_client, test_data):
    """
    POST /xqwapi/merchants/<int:merchant_id>/activate 
    """
    post_url = activate_url.format(m_rome_id)
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

# def test_update_merchant_status_close_on_merchant_not_closed(a_client, test_data):
#     """
#     POST /xqwapi/merchants/<int:merchant_id>/close
#     """
#     post_url = url.format(m_rome_id)
#     res = a_client.post(post_url, headers={
#         'Content-Type': 'application/json',
#         'Authorization': token_storage.bearer_token,
#         'X-Client-Id': token_storage.client_id,
#         'X-Refresh-Token': token_storage.refresh_token
#     })
#     data = res.json
#     assert res.status_code == 400
#     assert data is not None
#     assert data['message'] == 'Merchant account was not closed. Please try again later.'