import re
from typing import Tuple
import json
import requests

from server.config.logger import log
from server.config.environment import config
from server.models.merchant_model import Merchant, MerchantPaymentType
from server.models.person_model import Person
from server.models.payment_model import Payment, PaymentLink
from server.models.project_model import Project
from server.utilities import portals_jwt


def create_payment_link(
    merchant: Merchant,
    payment_link: PaymentLink,
    created_by: Person,
    project: Project,
    payment_type: MerchantPaymentType) -> Tuple[dict, str, any]:
    """
    Creates a payment link using Portal 3's algorithm for creating payments.
    """
    fn = 'create_payment_link'
    try:
        data = {
            'merchantId': merchant.merchant_code,
            'paymentType': payment_type.simple_code if payment_type else None,
            'project': {
                'name': project.name,
                'projectId': project.project_key,
                # empty str for now because category is required in Portals 3
                'category': project.category or ''
            } if project else None,
            'clientNotes': payment_link.client_notes,
            'customer': {
                'name': payment_link.customer_name,
                'email': payment_link.customer_email,
                'mobile': payment_link.mobile_number,
                'countryPrefix': payment_link.mobile_number_dial_code,
                'countryIso2': payment_link.mobile_number_country_code
            },
            'bill': {
                'base': {
                    'amount': payment_link.amount,
                    'currency': payment_link.currency
                }
            },
            'transactionType': 'payment',
            'source': 'payment-link',
            'adminNotes': f'Payment link for {merchant.name}',
            'expiresInMinutes': payment_link.expire_time_in_hrs * 60,
            'externalTransactionId': payment_link.external_transaction_id,
            'personId': created_by.id
        }

        headers = { 'Content-Type': 'application/json' }
        if config.portals_jwt_enabled == 'true':
            token = portals_jwt.jwt_encode()
            headers['Authorization'] = f'Bearer {token}'

        post_url = f'{config.apocalypse_url}/merchants/{merchant.merchant_code}/links/create'
        log.debug(f'{fn}: Payment link [{post_url}] payload: {data}')

        res = requests.post(post_url, data=json.dumps(data), headers=headers)
        data = res.json()

        message = data.get('message')
        errors = _rename_form_field_errors(data.get('errors'))
        if res.status_code >= 400:
            log.error(f'{fn}: Bad request: {message}')
            return False, message, errors

        if res.status_code != 201:
            log.error(f'{fn}: HTTP 201 not received: {message}')
            return False, message, errors

        return True, data, {}

    except requests.exceptions.HTTPError as e:
        log.error(f'{fn}: HTTP error: {str(e)}')
        return False, 'HTTP error has been encountered', {}

    except requests.exceptions.ConnectionError as e:
        log.error(f'{fn}: Connection error: {str(e)}')
        return False, 'Request is not able to establish a connection on an internal service', {}


def cancel_payment_link(merchant: Merchant, payment: Payment, cancelled_by: Person) -> Tuple[bool, str]:
    prefix = 'cancel_payment_link'
    try:
        data = json.dumps({ 'personId': cancelled_by.id })
        headers = { 'Content-Type': 'application/json' }
        if config.portals_jwt_enabled == 'true':
            token = portals_jwt.jwt_encode()
            headers['Authorization'] = f'Bearer {token}'

        post_url = f'{config.apocalypse_url}/merchants/{merchant.merchant_code}/links/cancel/'\
            f'{payment.external_transaction_id}'
        res = requests.post(post_url, data=data, headers=headers)
        res_json = res.json()

        message = res_json.get('message')
        if res.status_code >= 400:
            log.error(f'{prefix}: {message}')
            return False, message

        return True, res_json

    except requests.exceptions.HTTPError as e: # pylint: disable=broad-except
        message = str(e)
        log.error(f'{prefix}: {message}')
        return False, message

    except requests.exceptions.ConnectionError as e:
        message = 'Unable to establish connection on an internal service.'
        log.error(f'{prefix}: {message}')
        return False, message


def _rename_form_field_errors(data: dict):
    if not data or not isinstance(data, dict):
        return {}

    error_fields = {}
    for key in data:
        if '_' in key:
            words = key.split('_')
            sub_key = ''.join(words[:1] + [(i[0].swapcase() + i[1:] if len(i) > 0 else i) for i in words[1:]])
            error_fields[sub_key] = data[key]
        else:
            error_fields[key] = data[key]
    return error_fields
