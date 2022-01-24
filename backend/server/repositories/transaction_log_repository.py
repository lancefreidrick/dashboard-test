""" transaction_log_repository.py """
from typing import Tuple, List

from server.config import database
from server.models.transaction_log_model import TransactionLog
from server.models.person_model import Person
from server.models.search_option_model import SearchOption


def get_logs(
        transaction_id: int,
        invoice_id: int,
        search_option: SearchOption) -> Tuple[List[TransactionLog], int]:
    """
    Returns the transaction invoice logs in (logs, total_count)
    """
    params = [
        transaction_id,
        invoice_id,
        search_option.size,
        search_option.skip()
    ]
    rows = database.func('invoicing.get_transaction_invoice_logs', params)
    if not rows:
        return [], 0

    logs = [TransactionLog.map(l) for l in rows]
    total_count = rows[0]['total_count']
    return logs, total_count


def submit_log(
        transaction_id: str,
        invoice_id: str,
        submitted_log: dict,
        submitted_by: Person) -> Tuple[bool, str]:
    params = [
        transaction_id,
        invoice_id,
        submitted_log.get('content'),
        submitted_by.id
    ]
    rows = database.func('invoicing.submit_transaction_invoice_log', params)
    if not rows:
        return False, 'We are not able to record the transaction log'

    return rows[0]['status'] == 'success', rows[0]['message']


def remove_log(
        transaction_log: TransactionLog,
        submitted_by: Person) -> Tuple[bool, str]:
    params = [
        transaction_log.log_id,
        transaction_log.transaction_id,
        transaction_log.invoice_id,
        submitted_by.id
    ]
    rows = database.func('invoicing.remove_transaction_invoice_log', params)
    if not rows:
        return False, 'We are not able to remove the transaction log'

    return rows[0]['status'] == 'success', rows[0]['message']
