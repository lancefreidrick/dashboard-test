from typing import Tuple, List, Optional
from datetime import timedelta
from server.config import database
from server.models.merchant_model import Merchant
from server.models.search_option_model import SearchOption
from server.models.payment_model import Payment
from server.models.person_model import Person
from server.models.invoice_model import Invoice
from server.utilities.helper import map_invoice_status


def search_payments(search_option: SearchOption) -> Tuple[List[list], int]:
    report_start, report_end = search_option.reporting_date_at_four()
    due_start, due_end = search_option.due_date_range()

    reference_id = search_option.reference_id
    transaction_id = search_option.transaction_id

    params = [
        search_option.search_term if not reference_id and not transaction_id else None,
        reference_id,
        transaction_id,
        search_option.merchant_id,
        search_option.project,
        search_option.payment_method,
        map_invoice_status(search_option.status),
        search_option.localize_start_date()\
            if search_option.start_date else None,
        search_option.localize_end_date() + (timedelta(days=1) - timedelta(milliseconds=1))\
            if search_option.end_date else None,
        report_start,
        report_end,
        due_start,
        due_end,
        search_option.size,
        search_option.skip()
    ]
    rows = database.func('invoicing.search_payments', params)
    if not rows:
        return [], 0

    payments = [Payment.map(e) for e in rows]
    total_count = rows[0]['total_count']
    return payments, total_count


def get_merchant_payments(merchant: Merchant, search_option: SearchOption) -> Tuple[list, int]:
    report_start_date, report_end_date = search_option.reporting_date_at_four()

    params = [
        merchant.merchant_id,
        search_option.search_term if not search_option.reference_id else None,
        search_option.reference_id,
        search_option.localize_start_date() if search_option.start_date\
            and not (search_option.search_term or search_option.reference_id) else None,
        search_option.localize_end_date() + (timedelta(days=1) - timedelta(
            milliseconds=1)) if search_option.end_date\
                and not (search_option.search_term or search_option.reference_id) else None,
        report_start_date,
        report_end_date,
        search_option.settlement_reference_id,
        map_invoice_status(search_option.status),
        search_option.project,
        search_option.project_name,
        search_option.project_category,
        search_option.payment_method,
        search_option.payment_type,
        search_option.size,
        search_option.skip()
    ]
    rows = database.func('invoicing.get_merchant_payments', params)
    if not rows:
        return [], 0

    payment = [Payment.map(e) for e in rows]
    total_count = rows[0]['total_count']
    return payment, total_count


def find_payment_by_invoice_id(invoice_id: int) -> Optional[Payment]:
    params = [invoice_id]
    rows = database.func('invoicing.find_payment_by_invoice_id', params)
    if not rows:
        return None

    return Payment.map(rows[0])


def find_payment_by_ids(invoice_id: int, transaction_id: int, merchant: Merchant) -> Optional[Payment]:
    db_params = [
        merchant.merchant_code,
        invoice_id,
        transaction_id
    ]
    queried_merchant_payment = database.func('invoicing.find_payment_by_ids', db_params)
    if not queried_merchant_payment:
        return None
    return Payment.map(queried_merchant_payment[0])


def find_payment_by_reference_id(payment_reference_id: str, merchant: Merchant) -> Optional[Payment]:
    db_params = [
        merchant.merchant_code,
        payment_reference_id
    ]
    queried_merchant_payment = database.func('invoicing.find_payment_by_reference_id', db_params)
    if not queried_merchant_payment:
        return None
    return Payment.map(queried_merchant_payment[0])


def find_payment_by_multiple_ids(invoice_id: int, external_transaction_id: str,
                                 merchant: Merchant) -> Optional[Payment]:
    db_params = [
        merchant.merchant_id,
        external_transaction_id,
        invoice_id
    ]
    queried_merchant_payment = database.func('invoicing.find_payment_by_multiple_ids', db_params)
    if not queried_merchant_payment:
        return None
    return Payment.map(queried_merchant_payment[0])


def get_settled_payments(merchant: Merchant, settlement_reference_id: str) -> Tuple[list, int]:
    db_params = [
        merchant.merchant_code,
        settlement_reference_id,
    ]
    queried_payments = database.func('invoicing.get_settled_payments', db_params)
    if not queried_payments:
        return [], 0

    payment = [Payment.map(e) for e in queried_payments]
    total_count = queried_payments[0]['total_count']
    return payment, total_count


def update_offline_payment(payment: Payment, updated_by: Person) -> Tuple[bool, str]:
    db_params = [
        payment.transaction_id,
        payment.invoice_id,
        payment.payment_method.payment_method_id,
        payment.bill.total[0],
        payment.bill.total[1],
        payment.bill.fee[0],
        payment.bill.fee[1],
        payment.bill.converted[0],
        payment.bill.converted[1],
        payment.bill.qwx_rate[0],
        payment.bill.qwx_rate[1],
        payment.bill.qwx_rate[2],
        payment.payment_method.issuer,
        payment.payment_method.origin,
        payment.complete_notes,
        updated_by.id,
        updated_by.name,
    ]
    rows = database.func('invoicing.update_offline_payment', db_params)
    if not rows:
        return False, 'Cannot update the offline payment to paid'

    return rows[0]['status'] == 'success', rows[0]['message']


def refund_payment(payment: Payment, refunded_by: Person) -> Tuple[bool, str]:
    params = [
        payment.transaction_id,
        payment.invoice_id,
        payment.bill.refund[0],
        payment.bill.refund[1],
        payment.refund_reason,
        payment.refund_notes,
        refunded_by.id,
        refunded_by.name
    ]
    rows = database.func('invoicing.refund_payment_by_id', params)
    if not rows:
        return False, 'Cannot update the payment to refunded'

    return rows[0]['status'] == 'success', rows[0]['message']


def get_next_scheduled_invoice(payment: Payment) -> Tuple[Invoice, int]:
    params = [payment.transaction_reference_id, 120, 0]
    rows = database.func('invoicing.get_enrollment_invoices', params)
    if not rows:
        return [], 0

    invoices = [Invoice.map(i) for i in rows]
    remaining_invoices = [
        inv for inv in invoices
        if inv.due_at > payment.invoice_due_at
            and inv.invoice_reference_id != payment.invoice_reference_id
            and inv.status.code == 'SCHED'
    ]
    return remaining_invoices[0], len(remaining_invoices)
