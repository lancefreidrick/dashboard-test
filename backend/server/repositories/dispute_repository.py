from typing import Optional, Tuple, List

from server.config import database
from server.models.person_model import Person
from server.models.dispute_model import Dispute
from server.models.payment_model import Payment
from server.models.search_option_model import SearchOption


def find_dispute_by_id(dispute_id: int) -> Optional[Dispute]:
    db_params = [
        dispute_id
    ]

    result = database.func('invoicing.find_dispute_by_id', db_params)

    if not result:
        return None

    return Dispute.map(result[0])


def find_dispute_by_invoice_id(invoice_id: int) -> Optional[Dispute]:
    db_params = [
        invoice_id
    ]

    result = database.func('invoicing.find_dispute_by_invoice_id', db_params)

    if not result:
        return None

    return Dispute.map(result[0])


def update_dispute_by_id(dispute: Dispute, dispute_update: dict, updated_by: Person) -> Tuple[bool, str]:
    params = [
        dispute.id,
        dispute.invoice_id,
        dispute_update.get('status'),
        updated_by.id,
        dispute_update.get('notes')
    ]
    rows = database.func('invoicing.update_dispute_by_id', params)
    if not rows:
        return False, 'Cannot update dispute status as of the moment'

    return rows[0]['status'] == 'success', rows[0]['message']


def dispute_payment(dispute: Dispute, payment: Payment, disputed_by: Person) -> Tuple[int, bool, str]:
    params = [
        payment.transaction_id,
        dispute.invoice_id,
        dispute.reference_id,
        dispute.reason,
        disputed_by.id
    ]
    rows = database.func('invoicing.dispute_payment_by_invoice_id', params)
    if not rows:
        return 0, False, 'Cannot dispute payment as of the moment'

    return rows[0]['dispute_id'], rows[0]['status'] == 'success', rows[0]['message']


def search_disputes(search_option: SearchOption) -> Tuple[List[Dispute], int]:
    db_params = [
        search_option.search_term,
        search_option.invoice_id,
        search_option.merchant_id,
        search_option.project,
        [s for s in search_option.status.split(',')],
        search_option.start_date,
        search_option.end_date,
        search_option.size,
        search_option.skip()
    ]

    result = database.func('invoicing.search_disputes', db_params)

    if not result:
        return [], 0

    return [Dispute.map(x) for x in result], result[0]['total_count']
