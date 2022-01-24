""" merchant_payment_method_repository.py """
from typing import List, Tuple
from server.config import database
from server.models.person_model import Person
from server.models.merchant_model import Merchant
from server.models.merchant_payment_method_model import MerchantPaymentMethod


def get_merchant_payment_methods(merchant: Merchant) -> List[MerchantPaymentMethod]:
    params = [merchant.merchant_id]
    rows = database.func('directory.get_merchant_payment_methods', params)
    if not rows:
        return []

    payment_methods = [MerchantPaymentMethod.map_from_row(row) for row in rows]
    payment_methods.sort()
    return payment_methods


def activate_payment_method(
        merchant: Merchant,
        method: MerchantPaymentMethod,
        activated_by: Person) -> Tuple[bool, str]:
    params = [
        merchant.merchant_id,
        method.merchant_payment_method_id,
        activated_by.id,
        activated_by.name
    ]
    rows = database.func('directory.activate_merchant_payment_method', params)
    if not rows:
        return False, 'Unable to activate the payment method'

    return rows[0]['status'] == 'success', rows[0]['message']


def disable_payment_method(
        merchant: Merchant,
        method: MerchantPaymentMethod,
        disabled_by: Person) -> Tuple[bool, str]:
    params = [
        merchant.merchant_id,
        method.merchant_payment_method_id,
        disabled_by.id,
        disabled_by.name
    ]
    rows = database.func('directory.disable_merchant_payment_method', params)
    if not rows:
        return False, 'Unable to disable the payment method'

    return rows[0]['status'] == 'success', rows[0]['message']
