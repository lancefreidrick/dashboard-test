from typing import Tuple, List, Optional
from json import dumps as json_dumps
from datetime import timedelta, datetime
import pytz
from server.config import database, mongodb
from server.models.person_model import Person
from server.models.merchant_model import Merchant
from server.models.search_option_model import SearchOption
from server.models.enrollment_model import Enrollment
from server.models.invoice_model import Invoice
from server.utilities.helper import map_transaction_status


def search_enrollments(search_option: SearchOption) -> Tuple[List[Enrollment], int]:
    ref_id = search_option.reference_id
    tx_id = search_option.transaction_id

    params = [
        search_option.search_term if not ref_id and not tx_id else None,
        ref_id,
        tx_id,
        search_option.merchant_id,
        search_option.project,
        map_transaction_status(search_option.status),
        search_option.payment_type,
        search_option.localize_start_date()\
            if search_option.start_date else None,
        search_option.localize_end_date() + (timedelta(days=1) - timedelta(milliseconds=1))\
            if search_option.end_date else None,
        search_option.size,
        search_option.skip()
    ]
    rows = database.func('invoicing.search_enrollments', params)
    if not rows:
        return [], 0

    enrollments = [Enrollment.map(e) for e in rows]
    total_count = rows[0]['total_count']
    return enrollments, total_count


def get_merchant_enrollments(merchant: Merchant, search_option: SearchOption) -> Tuple[list, int]:
    ref_id = search_option.reference_id

    params = [
        merchant.merchant_id,
        search_option.search_term if not ref_id else None,
        ref_id,
        search_option.localize_start_date().astimezone(pytz.utc) if search_option.start_date else None,
        search_option.localize_end_date().astimezone(pytz.utc) + (timedelta(days=1) - timedelta(
            milliseconds=1)) if search_option.end_date else None,
        map_transaction_status(search_option.status),
        search_option.project,
        search_option.payment_type,
        search_option.size,
        search_option.skip()
    ]
    queried_merchant_enrollments = database.func('invoicing.get_merchant_enrollments', params)
    if not queried_merchant_enrollments:
        return [], 0
    enrollments = [Enrollment.map(e) for e in queried_merchant_enrollments]
    total_count = queried_merchant_enrollments[0]['total_count']
    return enrollments, total_count


def find_enrollment_by_transaction_id(transaction_id: int) -> Optional[Enrollment]:
    params = [transaction_id]
    rows = database.func('invoicing.find_enrollment_by_transaction_id', params)
    if not rows:
        return None

    return Enrollment.map(rows[0])


def find_merchant_enrollment_by_external_transaction_id(external_transaction_id: str,
                                                        merchant: Merchant) -> Optional[Enrollment]:
    params = [external_transaction_id, merchant.merchant_id]
    rows = database.func('invoicing.find_merchant_enrollment_by_external_transaction_id', params)
    if not rows:
        return None

    return Enrollment.map(rows[0])


def find_enrollment_by_reference_id(enrollment_reference_id: str, merchant: Merchant) -> Optional[Enrollment]:
    db_params = [
        merchant.merchant_code,
        enrollment_reference_id
    ]
    queried_merchant_enrollment = database.func('invoicing.find_enrollment_by_reference_id', db_params)
    if not queried_merchant_enrollment:
        return None
    return Enrollment.map(queried_merchant_enrollment[0])


def get_enrollment_invoices(enrollment: Enrollment, search_option: SearchOption) -> Tuple[list, int]:
    db_params = [
        enrollment.transaction_reference_id,
        search_option.size,
        search_option.skip()
    ]
    result = database.func('invoicing.get_enrollment_invoices', db_params)
    if not result:
        return [], 0
    invoices = [Invoice.map(i) for i in result]
    return invoices, result[0]['total_count']


def approve_enrollment(
    enrollment: Enrollment, approved_by: Person, merchant: Merchant) -> Tuple[bool, str]:

    invoices = [
        {
            'referenceId': i['referenceId'],
            'description': i['description'],
            'dueAt': i['dueAt'].isoformat()
        } for i in enrollment.generate_scheduled_invoices()
    ]
    if not invoices:
        return False, 'Invoices were not generated successfully'

    db_params = [
        merchant.merchant_id,
        enrollment.transaction_id,
        approved_by.id,
        approved_by.name,
        json_dumps(invoices)
    ]
    rows = database.func('invoicing.approve_enrollment_by_transaction_id', db_params)
    if not rows:
        return False, 'No rows returned'
    return rows[0]['status'] == 'success', rows[0]['message']


def decline_enrollment(
    enrollment: Enrollment, merchant: Merchant, declined_by: Person, comment: str) -> Tuple[bool, str]:

    db_params = [
        merchant.merchant_id,
        enrollment.transaction_id,
        declined_by.id,
        declined_by.name,
        comment or None
    ]
    rows = database.func('invoicing.decline_enrollment_by_transaction_id', db_params)
    if not rows:
        return False, 'No rows returned'
    return rows[0]['status'] == 'success', rows[0]['message']


def cancel_enrollment(
    enrollment: Enrollment, merchant: Merchant, cancelled_by: Person, comment: str) -> Tuple[bool, str]:

    is_cancelled, _ = _cancel_enrollment_mgd(enrollment, merchant, comment)
    if not is_cancelled:
        return False, 'Enrollment was not cancelled'

    db_params = [
        merchant.merchant_id,
        enrollment.transaction_id,
        cancelled_by.id,
        cancelled_by.name,
        comment or None
    ]
    rows = database.func('invoicing.cancel_enrollment_by_transaction_id', db_params)
    if not rows:
        return False, 'Enrollment was not cancelled'

    return rows[0]['status'] == 'success', rows[0]['message']


def _cancel_enrollment_mgd(
    enrollment: Enrollment, merchant: Merchant, comment: str) -> Tuple[bool, str]:
    """
    This is a cancel enrollment method for Mongodb.
    As of the moment, auto-debit reads/writes in the Mongodb
    which means invoices needs to be updated in Mongodb to avoid unwanted updates.
    """
    db_name = 'invoicing' if merchant.invoicing_mode == 'project' else 'billing'
    client = mongodb.get()
    with client.start_session() as session:
        with session.start_transaction():
            enrollments_db = session.client.get_database(db_name)['enrollments']
            invoices_db = session.client.get_database(db_name)['invoices']

            enrollment_query = {
                'merchantId': merchant.merchant_code,
                'referenceId': enrollment.transaction_reference_id
            }
            update_result = enrollments_db.update_one(enrollment_query, {
                '$set': {
                    'status': 'CANCELLED',
                    'cancelledAt': datetime.now(),
                    'cancelledComment': comment
                }
            })

            invoices_query = {
                'merchantId': merchant.merchant_code,
                'enrollmentId': enrollment.transaction_reference_id,
                'status': 'SCHED',
            }
            invoices_result = invoices_db.update_many(invoices_query, {
                '$set': {'status': 'CANCELLED'}
            })

    if update_result and update_result.matched_count != 1:
        return False, 'Unable to cancel the enrollment'

    if invoices_result and invoices_result.matched_count == 0:
        return False, 'Unable to cancel the invoices for this enrollment'

    return True, 'Enrollment has been cancelled'
