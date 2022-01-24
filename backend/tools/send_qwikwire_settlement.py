"""
send_qwikwire_settlement.py
"""
# pylint: disable=broad-except

import os
import io
import base64
from datetime import datetime, timedelta
from typing import Tuple
from dotenv import load_dotenv
import pytz
from pymongo import MongoClient
import psycopg2
import pandas as pd
from python_http_client import exceptions
from sendgrid import (
    SendGridAPIClient, Mail, Attachment, FileContent, FileType,
    FileName, Disposition, ContentId
)

ASIA_MANILA_TZ = 'Asia/Manila'
FN_NAME = 'send_qwikwire_settlement'

load_dotenv()

mongodb = MongoClient(
    host=os.environ.get('MONGODB_HOST'),
    port=int(os.environ.get('MONGODB_PORT')) or 27017)

pgdb = psycopg2.connect(os.environ.get('PG_CONNECTION_STRING'))

sendgrid_secret_key = os.getenv('SENDGRID_SECRET_KEY')
app_client_url = os.getenv('APP_CLIENT_URL')

subtracted_days = 1
sender = 'Engineering Team <developers@qwikwire.com>'
recipients = [
    'kenneth@qwikwire.com',
    'sherville@qwikwire.com',
    'jesse@qwikwire.com',
    'maddie@qwikwire.com'
]


def map_payment_method(transaction: dict) -> Tuple[str, str]:
    """
    Returns a tuple of payment method name and provider
    """
    if transaction['source'] == 'portal3':
        if 'cc' in transaction and transaction['cc']:
            provider = transaction['cc']['provider']
            return 'Credit Card', provider.upper()

        elif 'ach' in transaction and transaction['ach']:
            account_type = transaction['ach']['accountType']
            return 'ACH', account_type.upper()

        elif 'pp' in transaction and transaction['pp']:
            return 'PayPal', 'N/A'

        elif 'ewallet' in transaction and transaction['ewallet']:
            ewallet_type = transaction['ewallet']['type']
            return 'E-Wallet', ewallet_type.upper()

        elif 'directDebit' in transaction and transaction['directDebit']:
            bank_channel_code = transaction['directDebit']['bankChannelCode']
            return 'Online Banking', bank_channel_code.replace('BA_', '')

    old_provider = transaction.get('cc', {'provider': 'N/A'}).get('provider') or ''
    return 'Credit Card', old_provider.upper()


def get_project_codes(row: dict) -> Tuple[str, str]:
    """
    Returns company code, project code
    """
    project_fields = row.get('project_fields')
    if not project_fields:
        return row.get('project_code'), None

    fields = project_fields.get('fields')
    if fields and isinstance(project_fields['fields'], list):
        company_code = next((i.get('value') for i in fields if i.get('name') == 'companyCode'), None)
        project_code = next((i.get('value') for i in fields if i.get('name') == 'projectCode'), None)
        return company_code, project_code

    return None, None


class Transaction:
    def __init__(self, transaction: dict, payment: dict, invoice: dict):
        self.merchant_id: str = transaction.get('merchantId')
        self.transaction_id: str = transaction.get('transactionId')
        self.reference_id: str = payment.get('referenceId')
        self.transaction_status: str = transaction.get('status')
        self.transaction_type: str = transaction.get('type')
        self.payment_type: str = transaction.get('paymentType')
        self.source: str = transaction.get('source')
        self.project_name: str = transaction.get('project', {}).get('name')
        self.project_category: str = transaction.get('project', {}).get('category')
        self.created_at: datetime = transaction.get('createdAt').astimezone(tz=pytz.timezone(ASIA_MANILA_TZ))
        self.paid_at: datetime = payment.get('createdAt').astimezone(tz=pytz.timezone(ASIA_MANILA_TZ))
        self.pg_transaction_id: int = 0
        self.pg_invoice_id: int = 0
        self.ayl_company_code: str = None
        self.ayl_project_code: str = None

        if transaction['type'] == 'payment':
            bill = transaction.get('bill') or {'base': {}, 'total': {}}
            self.base_amount: float = bill.get('base').get('amount') or 0
            self.base_currency: str = bill.get('base').get('currency')
            self.converted_amount: float = bill.get('total').get('amount')
            self.converted_currency: str = bill.get('total').get('currency')
            self.fee_amount: float = bill.get('fee').get('amount')
            self.fee_currency: str = bill.get('fee').get('currency')
            self.total_currency: str = bill.get('total').get('currency')
            self.total_amount: float = bill.get('total').get('amount') or 0
            self.waived_currency: str = bill.get('waived', {}).get('currency') or 'PHP'
            self.waived_amount: float = bill.get('waived', {}).get('amount') or 0
            self.qw_rates_base: str = bill.get('qwRates', {}).get('base') or 'USD'
            self.qw_rates_target: str = bill.get('qwRates', {}).get('target') or 'PHP'
            self.qw_rates_amount: float = bill.get('qwRates', {}).get('amount') or 0
            self.net_amount: float = bill.get('net', {}).get('amount') or self.base_amount
            self.net_currency: str = bill.get('net', {}).get('currency') or 'PHP'
        else:
            bill = invoice.get('bill') or {'base': {}, 'total': {}}
            self.base_amount: float = bill.get('base').get('amount') or 0
            self.base_currency: str = bill.get('base').get('currency')
            self.converted_amount: float = bill.get('total').get('amount')
            self.converted_currency: str = bill.get('total').get('currency')
            self.fee_amount: float = bill.get('fee').get('amount')
            self.fee_currency: str = bill.get('fee').get('currency')
            self.total_amount: float = bill.get('total').get('amount') or 0
            self.total_currency: str = bill.get('total').get('currency')
            self.waived_currency: str = 'PHP'
            self.waived_amount: float = 0
            self.qw_rates_base: str = bill.get('qwxRates', {}).get('base') or 'USD'
            self.qw_rates_target: str = bill.get('qwxRates', {}).get('target') or 'PHP'
            self.qw_rates_amount: float = bill.get('qwxRates', {}).get('amount') or 0
            self.net_amount: float = bill.get('net', {}).get('amount') or self.base_amount
            self.net_currency: str = bill.get('net', {}).get('currency') or self.base_currency

        payment_method, provider = map_payment_method(transaction)
        self.payment_method = payment_method
        self.provider = provider

    def serialize(self):
        return {
            'merchant_id': self.merchant_id,
            'transaction_id': self.transaction_id,
            'reference_id': self.reference_id,
            'type': self.transaction_type,
            'status': self.transaction_status,
            'project_name': self.project_name,
            'project_category': self.project_category,
            'ayl_company_code': self.ayl_company_code,
            'ayl_project_code': self.ayl_project_code,
            'payment_type': self.payment_type,
            'base_amount': self.base_amount,
            'base_currency': self.base_currency,
            'converted_amount': self.converted_amount,
            'converted_currency': self.converted_currency,
            'fee_amount': self.fee_amount,
            'fee_currency': self.fee_currency,
            'waived_amount': self.waived_amount,
            'waived_currency': self.waived_currency,
            'total_amount': self.total_amount,
            'total_currency': self.total_currency,
            'net_amount': self.net_amount,
            'net_currency': self.net_currency,
            'payment_method': self.payment_method,
            'payment_provider': self.provider,
            'source': self.source,
            'created_at': self.created_at,
            'paid_at': self.paid_at,
            'pg_transaction_id': self.pg_transaction_id,
            'pg_invoice_id': self.pg_invoice_id
        }

    @staticmethod
    def headers():
        return [
            'transaction_id',
            'merchant_id',
            'reference_id',
            'type',
            'status',
            'project_name',
            'project_category',
            'ayl_company_code',
            'ayl_project_code',
            'payment_type',
            'base_amount',
            'base_currency',
            'converted_amount',
            'converted_currency',
            'fee_amount',
            'fee_currency',
            'waived_amount',
            'waived_currency',
            'total_amount',
            'total_currency',
            'net_amount',
            'net_currency',
            'payment_method',
            'payment_provider',
            'source',
            'created_at',
            'paid_at',
            'pg_transaction_id',
            'pg_invoice_id'
        ]


def get_ach_payments(db_name: str, timestamp: datetime):
    db = mongodb.get_database(db_name)
    transactions_collection = db.get_collection('transactions')
    payments_collection = db.get_collection('payments')
    invoices_collection = db.get_collection('invoices')
    cursor = transactions_collection.find({
        'paidAt': {
            '$gt': timestamp - timedelta(days=subtracted_days),
            '$lte': timestamp
        },
        'status': 'SUCCESS',
        'ach': { '$exists': True }
    }).sort([
        ('_id', -1)
    ])

    payments = []
    for transaction in cursor:
        payment = payments_collection.find_one({
            'referenceId': transaction.get('referenceId'),
            'merchantId': transaction.get('merchantId')
        })

        if transaction and transaction['type'] == 'enrollment':
            invoice = invoices_collection.find_one({
                'referenceId': payment.get('invoiceId'),
                'enrollmentId': payment.get('enrollmentId')
            })
            payments.append(Transaction(transaction, payment, invoice))
        elif transaction and transaction['type'] == 'payment':
            payments.append(Transaction(transaction, payment, {}))
    return payments

def get_payments_from(db_name: str, timestamp: datetime):
    db = mongodb.get_database(db_name)
    transactions_collection = db.get_collection('transactions')
    payments_collection = db.get_collection('payments')
    invoices_collection = db.get_collection('invoices')
    cursor = payments_collection.find({
        'createdAt': {
            '$gt': timestamp - timedelta(days=subtracted_days),
            '$lte': timestamp
        }
    }).sort([
        ('_id', -1)
    ])

    payments = []
    for payment in cursor:
        transaction = transactions_collection.find_one({
            'transactionId': payment.get('transactionId'),
            'merchantId': payment.get('merchantId')
        })

        if 'ach' in transaction and transaction['ach']:
            continue

        if transaction and transaction['type'] == 'enrollment':
            invoice = invoices_collection.find_one({
                'referenceId': payment.get('invoiceId'),
                'enrollmentId': payment.get('enrollmentId')
            })
            payments.append(Transaction(transaction, payment, invoice))
        elif transaction and transaction['type'] == 'payment':
            payments.append(Transaction(transaction, payment, {}))

    ach_payments = get_ach_payments(db_name, timestamp)
    payments = payments + ach_payments

    return payments


def find_payment_by_reference_id(transaction: Transaction):
    fn = 'invoicing.find_payment_by_reference_id'
    params = [
        transaction.merchant_id,
        transaction.reference_id
    ]
    with pgdb.cursor() as cursor:
        cursor.callproc(fn, params)
        data = cursor.fetchall()
        column_names = [d[0] for d in cursor.description]
        mapped_data = [dict(zip(column_names, list(values))) for values in data]
        pgdb.commit()
        return mapped_data


def get_transactions_data_frame(transactions: list):
    # assign pg transaction id
    for transaction in transactions:
        rows = find_payment_by_reference_id(transaction)
        if len(rows) > 0:
            transaction.pg_transaction_id = rows[0].get('transaction_id')
            transaction.pg_invoice_id = rows[0].get('invoice_id')

            # For Ayala Land project identification
            company_code, project_code = get_project_codes(rows[0])
            transaction.ayl_company_code = company_code
            transaction.ayl_project_code = project_code

    df = pd.DataFrame(
        data=[t.serialize() for t in transactions],
        columns=Transaction.headers())
    return df


def build_csv(df: pd.DataFrame) -> str:
    buf = io.StringIO()
    df.to_csv(path_or_buf=buf, index=False)
    value = buf.getvalue()
    buf.close()
    return value


def main():
    mailer = SendGridAPIClient(api_key=sendgrid_secret_key)
    timestamp = datetime\
        .now()\
        .astimezone(tz=pytz.timezone(ASIA_MANILA_TZ))\
        .replace(hour=16, minute=0, second=0, microsecond=0)
    report_timestamp = timestamp.strftime("%Y-%d-%m")

    print(f'{FN_NAME}: Retrieving transactions on {timestamp}')
    invoicing_transactions = get_payments_from('invoicing', timestamp)
    billing_transactions = get_payments_from('billing', timestamp)

    print(f'{FN_NAME}: invoicing: {len(invoicing_transactions)}')
    print(f'{FN_NAME}: billing: {len(billing_transactions)}')

    transactions = invoicing_transactions + billing_transactions
    df = get_transactions_data_frame(transactions)

    merchant_transaction_counts = df[['transaction_id', 'merchant_id']]\
        .groupby(['merchant_id'])\
        .count()\
        .to_dict()['transaction_id']

    report_merchant_txs_counts = ''
    for key in merchant_transaction_counts:
        report_merchant_txs_counts += (
            f'<tr>'
            f'<td>{key}</td>'
            f'<td>{merchant_transaction_counts[key]}</td>'
            f'</tr>'
        )

    total_count = len(transactions)
    subject = f'AQWIRE Payment Report - {report_timestamp}'
    with io.open('./tools/emails/qwikwire_settlement_report.html', encoding='utf-8') as file:
        html = file.read()\
            .replace('{{ reportDate }}', report_timestamp)\
            .replace('{{ transactionCount }}', str(total_count))\
            .replace('{{ merchantTransactionCounts }}', report_merchant_txs_counts)

        mail = Mail(
            from_email=sender,
            to_emails=recipients,
            subject=subject,
            html_content=html)

        csv_as_str = build_csv(df)
        csv_data = base64.b64encode(bytes(csv_as_str, 'utf-8')).decode()
        attachment = Attachment()
        attachment.file_content = FileContent(csv_data)
        attachment.file_name = FileName(f'settle-payments-{report_timestamp}.csv')
        attachment.file_type = FileType('text/csv')
        attachment.disposition = Disposition('attachment')
        attachment.content_id = ContentId('Qwikwire Settlement Report')
        mail.attachment = attachment

        try:
            response = mailer.send(mail)
            print(f'{FN_NAME}: Mailing response: {response.status_code} {response.body} {response.headers}')
        except exceptions.BadRequestsError as bad_request:
            print(f'{FN_NAME}: Mailing failed: {bad_request.body}')
        except Exception as e:
            print(f'{FN_NAME}: Mailing failed: {str(e)}')

main()
