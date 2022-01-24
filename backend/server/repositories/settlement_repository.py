from typing import Tuple, List, Optional

from server.config import database
from server.models.merchant_model import Merchant
from server.models.person_model import Person
from server.models.search_option_model import SearchOption
from server.models.settlement_model import Settlement, SettlementFile
from server.utilities.code_generator import generate_ref_id


def search_settlements(search_option: SearchOption) -> Tuple[List[Settlement], int]:
    params = [
        search_option.merchant_id,
        search_option.reporting_date.date() if search_option.reporting_date else None,
        search_option.search_term or None,
        search_option.size,
        search_option.skip()
    ]
    rows = database.func('invoicing.search_settlements', params)
    if not rows:
        return [], 0

    settlements = [Settlement.map(s) for s in rows]
    total_count = rows[0]['total_count']
    return settlements, total_count


def find_settlement_by_id(settlement_id: int) -> Optional[Settlement]:
    params = [settlement_id]
    rows = database.func('invoicing.find_settlement_by_id', params)
    if not rows:
        return None

    return Settlement.map(rows[0])


def create_settlement(
        merchant: Merchant,
        settlement_data: Settlement.RequestData,
        settlement_file: SettlementFile,
        settled_by: Person) -> Tuple[bool, str, int, Optional[str]]:
    settlement_reference_id = generate_ref_id('Settlement')
    db_params = [
        settlement_reference_id,
        merchant.merchant_id,
        [int(i) for i in settlement_data.invoice_ids],
        settled_by.id,
        settled_by.name,
        settlement_file.settlement_file_id,
        settlement_data.settled_date,
        settlement_data.settlement_notes
    ]
    rows = database.func('invoicing.create_settlement', db_params)
    if not rows:
        return False, 'Settlement has not been created', -1, None

    result = rows[0]
    return (
        result['status'] == 'success',
        result['message'],
        result['created_settlement_id'],
        settlement_reference_id
    )


def update_settlement_settled_date(settlement_reference_id: str, date_settled: str) -> Tuple[bool, str]:
    db_params = [
        settlement_reference_id,
        date_settled
    ]
    result = database.func('invoicing.update_settlement_settled_date', db_params)
    return result[0]['status'] == 'success', result[0]['message']


def update_settlement_payments(settlement_reference_id: str, invoice_ids: list) -> Tuple[bool, str]:
    if not invoice_ids:
        return False, 'Please select at least 1 payment transaction.'

    db_params = [
        settlement_reference_id,
        [int(i) for i in invoice_ids]
    ]
    result = database.func('invoicing.update_settlement_payments', db_params)
    if result[0]['status'] != 'success':
        return False, 'Unable to update settlement'
    return True, result[0]['status']


def get_merchant_settlements(merchant: Merchant, search_option: SearchOption) -> Tuple[list, int]:
    db_params = [
        merchant.merchant_code,
        search_option.reporting_date.date() if search_option.reporting_date else None,
        search_option.search_term or None,
        search_option.size,
        search_option.skip()
    ]
    queried_merchant_settlements = database.func('invoicing.get_merchant_settlements', db_params)
    if not queried_merchant_settlements:
        return [], 0

    settlements = [Settlement.map(s) for s in queried_merchant_settlements]
    total_count = queried_merchant_settlements[0]['total_count']
    return settlements, total_count


def find_settlement_by_reference_id(reference_id: str) -> Optional[Settlement]:
    db_params = [reference_id]
    rows = database.func('invoicing.find_settlement_by_reference_id', db_params)
    if not rows:
        return None
    return Settlement.map(rows[0])


def delete_settlement(settlement: Settlement, deleted_by: Person) -> Tuple[bool, str]:
    db_params = [
        settlement.settlement_id,
        deleted_by.name
    ]
    rows = database.func('invoicing.delete_settlement_by_id', db_params)
    if not rows:
        return False, 'Settlement report has not been deleted'

    return rows[0]['status'] == 'success', rows[0]['message']


def add_settlement_file(settlement_file: SettlementFile) -> Tuple[bool, str, Optional[int]]:
    db_params = [
        settlement_file.merchant.merchant_id,
        settlement_file.unique_identifier,
        settlement_file.s3_file_directory,
        settlement_file.s3_file_name,
        settlement_file.s3_domain_name,
        settlement_file.s3_bucket_name,
        settlement_file.s3_file_url,
        settlement_file.s3_file_type
    ]
    rows = database.func('invoicing.add_settlement_file', db_params)
    if not rows:
        return False, 'Settlement file has not been saved', None

    result = rows[0]
    return (
        result['status'] == 'success',
        result['message'],
        result['created_settlement_file_id']
    )


def find_settlement_file_by_id(merchant: Merchant, settlement_file_id: int) -> Optional[SettlementFile]:
    db_params = [
        merchant.merchant_id,
        settlement_file_id
    ]
    rows = database.func('invoicing.find_settlement_file_by_id', db_params)
    if not rows:
        return None
    return SettlementFile.map(rows[0])
