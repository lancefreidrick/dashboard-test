from typing import Tuple
from datetime import timedelta
import pytz
from server.config import database
from server.models.merchant_model import Merchant
from server.models.person_model import Person
from server.models.transaction_model import Transaction
from server.models.search_option_model import SearchOption


def get_merchant_transactions(merchant: Merchant, search_option: SearchOption) -> Tuple[list, int]:
    db_params = [
        merchant.merchant_code,
        search_option.localize_start_date().astimezone(pytz.utc) if search_option.start_date else None,
        search_option.localize_end_date().astimezone(pytz.utc) + (timedelta(days=1) - timedelta(
            milliseconds=1)) if search_option.end_date else None,
        search_option.project,
        search_option.show_incomplete,
        search_option.size,
        search_option.skip()
    ]
    rows = database.func('invoicing.get_merchant_transactions', db_params)
    if not rows:
        return [], 0

    transactions = [Transaction.map_from_row(r) for r in rows]
    return transactions, rows[0]['full_count']


def find_transaction_by_external_transaction_id(transaction_id: str, merchant: Merchant) -> Transaction:
    db_params = [
        transaction_id,
        merchant.merchant_code
    ]
    rows = database.func('invoicing.find_transaction_by_external_transaction_id', db_params)
    if not rows:
        return []
    return Transaction.map_from_row(rows[0])


def search_transactions(search_option: SearchOption, user: Person) -> Tuple[list, int]:
    search_term = search_option.search_term
    search_term = search_term.replace(' ', ' & ') if search_term else ''

    db_params = [
        user.id,
        search_term,
        search_option.size,
        search_option.skip()
    ]
    rows = database.func('invoicing.search_transactions', db_params)
    if not rows:
        return [], 0

    transactions = [Transaction.map_from_row(row) for row in rows]
    total_count = rows[0]['total_count']
    return transactions, total_count
