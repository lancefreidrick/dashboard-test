""" server.repositories.merchant_repository.py """
from typing import Tuple, Optional, List

from server.config import database
from server.models.merchant_model import Merchant, MerchantCategory, MerchantPaymentType
from server.models.search_option_model import SearchOption
from server.models.person_model import Person


def get_all_merchants(search_option: SearchOption = None) -> Tuple[List[Merchant], int]:
    if search_option is None:
        search_option = SearchOption()
        search_option.size = 200
        search_option.page = 1

    params = [
        search_option.search_term,
        search_option.size,
        search_option.skip()
    ]
    queried_merchants = database.func('directory.get_all_merchants', params)
    if not queried_merchants:
        return [], 0

    merchants = [Merchant.map(m) for m in queried_merchants]
    total_count = queried_merchants[0]['total_count']
    return merchants, total_count


def get_user_merchants(requested_by: Person) -> List[Merchant]:
    params = [requested_by.id]
    queried_merchants = database.func('directory.get_user_merchants', params)
    merchants = [Merchant.map(m) for m in queried_merchants]
    return merchants


def find_merchant_by_id(merchant_id: int) -> Optional[Merchant]:
    db_params = [merchant_id]
    queried_merchant = database.func('directory.find_merchant_by_id', db_params)
    merchant = list({Merchant.map(m) for m in queried_merchant})
    if not merchant:
        return None
    return merchant[0]


def find_merchant_by_code(merchant_code: str) -> Optional[Merchant]:
    db_params = [merchant_code]
    queried_merchant = database.func('directory.find_merchant_by_code', db_params)
    merchant = list({Merchant.map(m) for m in queried_merchant})
    if not merchant:
        return None
    return merchant[0]


def get_all_merchant_categories() -> List[MerchantCategory]:
    rows = database.func('directory.get_all_merchant_categories', [])
    if not rows:
        return []
    return [MerchantCategory.map(row) for row in rows]


def find_merchant_category_by_id(merchant_category_id: int) -> Optional[dict]:
    result = database.func('directory.find_merchant_category_by_id', [merchant_category_id])
    return result[0] if result else None


def update_merchant_information(merchant: Merchant) -> Tuple[bool, str]:
    db_params = [
        merchant.merchant_id,
        merchant.name,
        merchant.category_id,
        merchant.address['address_one'],
        merchant.address['address_two'],
        merchant.address['address_three'],
        merchant.timezone
    ]

    result = database.func('directory.update_merchant_info', db_params)
    return result[0]['status'] == 'success', result[0]['message']


def suspend_merchant_account(merchant: Merchant) -> Tuple[bool, str]:
    db_params = [merchant.merchant_id]

    result = database.func('directory.suspend_merchant_account', db_params)
    return result[0]['status'] == 'success', result[0]['message']

def close_merchant_account(merchant: Merchant) -> Tuple[bool, str]:
    db_params = [merchant.merchant_id]

    result = database.func('directory.close_merchant_account', db_params)
    return result[0]['status'] == 'success', result[0]['message']

def activate_merchant_account(merchant: Merchant) -> Tuple[bool, str]:
    db_params = [merchant.merchant_id]

    result = database.func('directory.activate_merchant_account', db_params)
    return result[0]['status'] == 'success', result[0]['message']

def update_merchant_category(merchant: Merchant, merchant_category: int) -> Tuple[bool, str]:
    db_params = [merchant.merchant_id, merchant_category]

    result = database.func('directory.update_merchant_category', db_params)

    return result[0]['status'] == 'success', result[0]['message']

def update_merchant_feature_flags(merchant: Merchant) -> Tuple[bool, str]:
    db_params = [
        merchant.merchant_id,
        merchant.can_manage_projects,
        merchant.can_manage_payment_methods,
        merchant.can_access_reports,
        merchant.can_copy_sales_agents,
        merchant.can_manage_payment_links,
        merchant.can_manage_notification_settings
    ]

    result = database.func('directory.update_merchant_feature_flags', db_params)
    if not result:
        return False, 'Unable to get response from update function'

    return result[0]['status'] == 'success', result[0]['message']

def get_merchant_payment_types(merchant: Merchant) -> List[MerchantPaymentType]:
    db_params = [merchant.merchant_id]
    queried_payment_types = database.func('directory.get_merchant_payment_types', db_params)

    if not queried_payment_types:
        return []

    return list({MerchantPaymentType.map(m) for m in queried_payment_types})

def get_merchant_payment_currencies(merchant_id: int) -> Optional[Merchant]:
    db_params = [merchant_id]
    queried_merchant = database.func('directory.find_merchant_by_id', db_params)

    if not queried_merchant:
        return None

    payment_currencies = queried_merchant[0].get('portal3_config').get('paymentCurrencies')
    return payment_currencies
