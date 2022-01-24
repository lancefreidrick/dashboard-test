""" tests.api.test_merchant_payment_method_controller.py """
# pylint: disable=redefined-outer-name,global-statement,unused-argument
# ^^^ this
from tests.utils.token_storage import token_storage

url = '/xqwapi/merchants/{}/payment-methods'
action_url = '/xqwapi/merchants/{}/payment-methods/{}/{}'

m_rome_id = 90000
m_not_exist = 90099

pm_usd_card_id = 100001
pm_php_card_id = 100001
pm_ach_id = 100002
pm_ewallet_id = 100003
pm_directdebit_id = 100004
pm_paypal_id = 100004
pm_ideal_id = 100005
pm_applepay_id = 100006

pm_alipay_id = 100007
pm_wechatpay_id = 100008
pm_googlepay_id = 100009
pm_mspay_id = 100010
pm_sepa_id = 100011
pm_sofort_id = 100012
pm_cartes_id = 100013

## API: GET MERCHANT PAYMENT METHODS

def test_get_payment_methods_as_admin_successfully(a_client, test_data):
    """
    GET /xqapi/merchants/<merchant_code>/payment-methods
    """
    get_url = url.format(m_rome_id)
    res = a_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'channels' in data[0]
    assert 'code' in data[0]
    assert 'currency' in data[0]
    assert 'isAutoDebitEnabled' in data[0]
    assert 'isEnabled' in data[0]
    assert 'mode' in data[0]
    assert 'mpmId' in data[0]
    assert 'paymentProcessor' in data[0]
    assert 'updatedAt' in data[0]
    assert data[0]['code'] == 'card'
    assert data[1]['code'] == 'card'
    assert len(data) == 14

def test_get_payment_methods_as_staff_successfully(s_client, test_data):
    """
    GET /xqapi/merchants/<merchant_code>/payment-methods
    """
    get_url = url.format(m_rome_id)
    res = s_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'channels' in data[0]
    assert 'code' in data[0]
    assert 'currency' in data[0]
    assert 'isAutoDebitEnabled' in data[0]
    assert 'isEnabled' in data[0]
    assert 'mode' in data[0]
    assert 'mpmId' in data[0]
    assert 'paymentProcessor' in data[0]
    assert 'updatedAt' in data[0]
    assert len(data) == 14

def test_get_payment_methods_as_merchant_admin_successfully(ma_client, test_data):
    """
    GET /xqapi/merchants/<merchant_code>/payment-methods
    """
    get_url = url.format(m_rome_id)
    res = ma_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert len(data) == 14

def test_get_merchant_payment_methods_as_merchant_staff_successfully(ms_client, test_data):
    """
    GET /xqapi/merchants/<merchant_code>/payment-methods
    """
    get_url = url.format(m_rome_id)
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

def test_get_payment_methods_as_another_merchant_admin(ama_client, test_data):
    """
    GET /xqapi/merchants/<merchant_code>/payment-methods
    """
    get_url = url.format(m_rome_id)
    res = ama_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to get payment methods'

def test_get_payment_methods_as_multiple_merchant_admin_successfully(mma_client, test_data):
    """
    GET /xqapi/merchants/<merchant_code>/payment-methods
    """
    get_url = url.format(m_rome_id)
    res = mma_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert len(data) == 14

def test_get_payment_methods_on_merchant_does_not_exist(ma_client, test_data):
    """
    GET /xqapi/merchants/<merchant_code>/payment-methods
    """
    get_url = url.format(m_not_exist)
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

def test_get_payment_methods_without_token(client, test_data):
    """
    GET /xqapi/merchants/<merchant_code>/payment-methods
    """
    get_url = url.format(m_rome_id)
    res = client.get(get_url, headers={
        'Content-Type': 'application/json'
    })
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized access'

## API: ACTIVATE MERCHANT PAYMENT METHODS

def test_activate_payment_method_as_admin_successfully(a_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/payment-methods/<payment-method-id>/activate
    """
    get_url = action_url.format(m_rome_id, pm_ach_id, 'activate')
    res = a_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Payment method has been activated'

def test_activate_method_as_staff_successfully(s_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/payment-methods/<payment-method-id>/activate
    """
    post_url = action_url.format(m_rome_id, pm_ewallet_id, 'activate')
    res = s_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Payment method has been activated'

def test_activate_payment_method_as_merchant_admin_successfully(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/payment-methods/<payment-method-id>/activate
    """
    post_url = action_url.format(m_rome_id, pm_directdebit_id, 'activate')
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Payment method has been activated'

def test_activate_payment_method_as_merchant_staff(ms_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/payment-methods/<payment-method-id>/activate
    """
    post_url = action_url.format(m_rome_id, pm_ideal_id, 'activate')
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

def test_activate_payment_method_as_multiple_merchant_admin(mma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/payment-methods/<payment-method-id>/activate
    """
    post_url = action_url.format(m_rome_id, pm_ideal_id, 'activate')
    res = mma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Payment method has been activated'

def test_activate_payment_method_as_another_merchant_admin(ama_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/payment-methods/<payment-method-id>/activate
    """
    post_url = action_url.format(m_rome_id, pm_applepay_id, 'activate')
    res = ama_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to activate this payment method'

def test_activate_payment_method_without_token(client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/payment-methods/<payment-method-id>/activate
    """
    post_url = action_url.format(m_rome_id, pm_applepay_id, 'activate')
    res = client.post(post_url, headers={
        'Content-Type': 'application/json'
    })
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized access'

def test_activate_payment_method_on_merchant_does_not_exist(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/payment-methods/<payment-method-id>/activate
    """
    post_url = action_url.format(m_not_exist, pm_cartes_id, 'activate')
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

def test_activate_payment_method_on_already_active_payment_method(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/payment-methods/<payment-method-id>/activate
    """
    post_url = action_url.format(m_rome_id, pm_cartes_id, 'activate')
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert data['message'] == 'Payment method is already active'

def test_activate_payment_method_on_payment_method_not_exist(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/payment-methods/<payment-method-id>/activate
    """
    post_url = action_url.format(m_rome_id, 999999, 'activate')
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Payment method does not exist'

## API: DISABLE MERCHANT PAYMENT METHODS

def test_disable_payment_method_as_admin_successfully(a_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/payment-methods/<payment-method-id>/disable
    """
    get_url = action_url.format(m_rome_id, pm_alipay_id, 'disable')
    res = a_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Payment method has been disabled'

def test_disable_method_as_staff_successfully(s_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/payment-methods/<payment-method-id>/disable
    """
    post_url = action_url.format(m_rome_id, pm_wechatpay_id, 'disable')
    res = s_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Payment method has been disabled'

def test_disable_payment_method_as_merchant_admin_successfully(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/payment-methods/<payment-method-id>/disable
    """
    post_url = action_url.format(m_rome_id, pm_googlepay_id, 'disable')
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Payment method has been disabled'

def test_disable_payment_method_as_merchant_staff(ms_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/payment-methods/<payment-method-id>/disable
    """
    post_url = action_url.format(m_rome_id, pm_mspay_id, 'disable')
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

def test_disable_payment_method_as_multiple_merchant_admin(mma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/payment-methods/<payment-method-id>/disable
    """
    post_url = action_url.format(m_rome_id, pm_mspay_id, 'disable')
    res = mma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Payment method has been disabled'

def test_disable_payment_method_as_another_merchant_admin(ama_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/payment-methods/<payment-method-id>/disable
    """
    post_url = action_url.format(m_rome_id, pm_sepa_id, 'disable')
    res = ama_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to disable this payment method'

def test_disable_payment_method_without_token(client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/payment-methods/<payment-method-id>/disable
    """
    post_url = action_url.format(m_rome_id, pm_sepa_id, 'disable')
    res = client.post(post_url, headers={
        'Content-Type': 'application/json'
    })
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized access'

def test_disable_payment_method_on_merchant_does_not_exist(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/payment-methods/<payment-method-id>/disable
    """
    post_url = action_url.format(m_not_exist, pm_sepa_id, 'disable')
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

def test_disable_payment_method_on_already_disabled_payment_method(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/payment-methods/<payment-method-id>/disable
    """
    post_url = action_url.format(m_rome_id, pm_applepay_id, 'disable')
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert data['message'] == 'Payment method is already disabled'

def test_disable_payment_method_on_payment_method_not_exist(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/payment-methods/<payment-method-id>/disable
    """
    post_url = action_url.format(m_rome_id, 999999, 'disable')
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Payment method does not exist'

def test_disable_payment_method_on_usd_card(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/payment-methods/<payment-method-id>/disable
    """
    post_url = action_url.format(m_rome_id, pm_usd_card_id, 'disable')
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to disable card payments'

def test_disable_payment_method_on_php_card(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/payment-methods/<payment-method-id>/disable
    """
    post_url = action_url.format(m_rome_id, pm_php_card_id, 'disable')
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to disable card payments'
