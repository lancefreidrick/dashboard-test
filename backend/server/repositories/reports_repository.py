""" reports_repository.py """
import re
from datetime import datetime

from server.config import database
from server.models.merchant_model import Merchant
from server.models.search_option_model import SearchOption


def get_revenue_summary(merchant: Merchant, start_date, end_date) -> list:
    db_params = [
        merchant.merchant_id,
        start_date,
        end_date
    ]
    queried_revenues = database.func('invoicing.get_revenue_summary', db_params)
    mapped_revenues = [
        {
            'transaction_date': qr['transaction_date'],
            'total_base_currency': qr['total_base_currency'],
            'total_base_amount': qr['total_base_amount'],
            'total_charged_currency': qr['total_charged_currency'],
            'total_charged_amount': qr['total_charged_amount'],
            'transaction_count': qr['transaction_count']
        }
        for qr in queried_revenues
    ]
    return mapped_revenues


def get_project_payment_type_summary(
        merchant: Merchant,
        start_date: datetime,
        end_date: datetime) -> list:
    db_params = [
        merchant.merchant_id,
        start_date,
        end_date
    ]
    queried_payments = database.func('invoicing.get_project_payment_type_summary', db_params)
    mapped_payments = [
        {
            'projectName': qp['project_name'],
            'paymentType': qp['payment_type_name'],
            'baseAmount': float(qp['base_amount']),
            'baseCurrency': qp['base_currency'],
        }
        for qp in queried_payments
    ]
    return mapped_payments


def get_total_payments_by_type(merchant: Merchant) -> list:
    db_params = [merchant.merchant_id]
    queried_payment_type_count = database.func('invoicing.get_total_payments_by_type', db_params)
    if not queried_payment_type_count:
        return []

    payment_type_count = [
        {
            'paymentTypeName': e.get('payment_type_name'),
            'fullCount': e.get('full_count')
        }
        for e in queried_payment_type_count
    ]

    return payment_type_count



def get_payment_statistics(merchant: Merchant, start_date: datetime, end_date: datetime) -> dict:
    db_params = [
        merchant.merchant_id,
        start_date.date(),
        end_date.date()
    ]
    rows = database.func('auditing.get_payment_statistics', db_params)
    if not rows:
        return {}

    stats = dict()
    for row in rows:
        group_name = row['group_name']
        key_name = group_name[0].lower() + re.sub(' ', '', group_name)[1:]
        column_data = [row['column_name'], row['column_value']]
        if key_name in stats:
            stats[key_name]['items'].append(column_data)
        else:
            stats[key_name] = {'label': group_name, 'items': [column_data]}
    return stats


def get_payment_method_reports(merchant: Merchant, start_date: datetime, end_date: datetime) -> list:
    db_params = [
        merchant.merchant_id,
        start_date.date(),
        end_date.date()
    ]
    rows = database.func('auditing.get_payment_method_reports', db_params)
    if not rows:
        return []

    return [
        {
            'method': row['payment_method_name'] or 'Unknown',
            'origin': row['payment_method_origin'] or 'Unknown',
            'provider': row['payment_method_provider'] or 'Unknown',
            'currency': row['base_currency'] or 'PHP',
            'amount': float(row['total_base_amount'] or 0),
            'count': row['total_payments'] or 0
        }
        for row in rows
    ]

def get_payment_method_reports_admin(merchant: Merchant, start_date: datetime, end_date: datetime) -> list:
    db_params = [
        merchant.merchant_id,
        start_date.date(),
        end_date.date()
    ]
    rows = database.func('auditing.get_payment_method_reports_admin', db_params)
    if not rows:
        return []

    return [
        {   
            'method': row.get('payment_method_name', 'Unknown'),
            'origin': row.get('payment_method_origin', 'Unknown'),
            'iso': row.get('payment_method_origin_iso', 'Unknown'),
            'provider': row.get('payment_method_provider', 'Unknown'),
            'currency': row.get('base_currency', 'PHP'),
            'amount': float(row.get('total_base_amount', 0)),
            'count': row.get('total_payments', 0)
        }
        for row in rows
    ]


def get_paid_payments_by_project_report(merchant: Merchant, start_date: datetime, end_date: datetime) -> list:
    db_params = [
        merchant.merchant_id,
        start_date.date(),
        end_date.date()
    ]
    rows = database.func('auditing.get_paid_payments_by_project_report', db_params)
    if not rows:
        return []

    return [
        {
            'project': row['project_name'] or 'Unknown',
            'source': row['transaction_source'] or 'Unknown',
            'paymentType': row['payment_type_name'] or 'Unknown',
            'currency': row['base_currency'] or 'PHP',
            'amount': float(row['total_base_amount'] or 0),
            'count': row['total_payments'] or 0
        }
        for row in rows
    ]

def get_summary_payments_by_payment_type(merchant: Merchant, search_option: SearchOption) -> list:
    db_params = [
        merchant.merchant_id,
        search_option.localize_start_date(),
        search_option.localize_end_date(),
    ]
    rows = database.func('auditing.get_summary_payments_by_payment_type', db_params)
    if not rows:
        return []

    return [
        {
            'project': row.get('project_name', 'Unknown'),
            'category': row.get('project_category', 'Unknown'),
            'currency': row.get('base_currency', 'Unknown'),
            'rfCount': row.get('rf_count', 0),
            'rfSum': float(row.get('rf_sum', 0)),
            'maCount': row.get('ma_count', 0),
            'maSum': float(row.get('ma_sum', 0)),
            'dpCount': row.get('dp_count', 0),
            'dpSum': float(row.get('dp_sum', 0)),
        }
        for row in rows
    ]

