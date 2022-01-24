# cross_validate_transactions.py

import os
import io
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests
import pytz
from pymongo import MongoClient
import psycopg2
import pandas as pd

load_dotenv()

mongodb = MongoClient(
    host=os.environ.get('MONGODB_HOST'),
    port=int(os.environ.get('MONGODB_PORT')) or 27017)

pgdb = psycopg2.connect(os.environ.get('PG_CONNECTION_STRING'))

mailgun_key = os.environ.get('MAILGUN_KEY')
mailgun_domain = os.environ.get('MAILGUN_DOMAIN')

subtracted_days = 1
sender = 'AQWIRE Reports <developers@qwikwire.com>'
recipients = [
    'kenneth@qwikwire.com',
    'archie@qwikwire.com',
    'jesse@qwikwire.com',
    'jm@qwikwire.com',
    'kyle@qwikwire.com'
]


class Transaction:
    def __init__(self, data: dict):
        self.merchant_id: str = data.get('merchantId')
        self.transaction_id: str = data.get('transactionId')
        self.reference_id: str = data.get('referenceId')
        self.transaction_type: str = data.get('type')
        self.transaction_status: str = data.get('status')
        self.payment_type: str = data.get('paymentType')
        self.source: str = data.get('source')
        self.created_at: datetime = data.get('createdAt')
        self.pg_transaction_id: int = None

    def serialize(self):
        return {
            'merchant_id': self.merchant_id,
            'transaction_id': self.transaction_id,
            'reference_id': self.reference_id,
            'type': self.transaction_type,
            'status': self.transaction_status,
            'source': self.source,
            'payment_type': self.payment_type,
            'created_at': self.created_at,
            'pg_transaction_id': self.pg_transaction_id,
        }

    @staticmethod
    def headers():
        return [
            'transaction_id',
            'merchant_id',
            'reference_id',
            'type',
            'status',
            'source',
            'payment_type',
            'created_at',
            'pg_transaction_id'
        ]


def get_transactions_from_invoicing(timestamp: datetime):
    db = mongodb.get_database('invoicing')
    transactions_collection = db.get_collection('transactions')
    cursor = transactions_collection.find({
        'createdAt': {
            '$gt': timestamp - timedelta(days=subtracted_days),
            '$lte': timestamp
        }
    }).sort([
        ('_id', -1)
    ])
    return [Transaction(tx) for tx in cursor]


def get_transactions_from_billing(timestamp: datetime):
    db = mongodb.get_database('billing')
    transactions_collection = db.get_collection('transactions')
    cursor = transactions_collection.find({
        'createdAt': {
            '$gt': timestamp - timedelta(days=subtracted_days),
            '$lte': timestamp
        }
    }).sort([
        ('_id', -1)
    ])
    return [Transaction(tx) for tx in cursor]


def find_transaction_by_ext_tx_id(transaction: Transaction):
    fn = 'invoicing.find_transaction_by_external_transaction_id'
    params = [
        transaction.transaction_id,
        transaction.merchant_id
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
        existing_transaction = find_transaction_by_ext_tx_id(transaction)
        transaction.pg_transaction_id = existing_transaction[0].get('transaction_id') if existing_transaction else 0

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
    timestamp = datetime.now().astimezone(tz=pytz.timezone('Asia/Manila'))
    report_timestamp = timestamp.strftime("%Y-%d-%m")

    print(f'Retrieving transactions on {timestamp}')
    invoicing_transactions = get_transactions_from_invoicing(timestamp)
    billing_transactions = get_transactions_from_billing(timestamp)

    print(f'\tinvoicing: {len(invoicing_transactions)}')
    print(f'\tbilling: {len(billing_transactions)}')

    transactions = invoicing_transactions + billing_transactions
    df = get_transactions_data_frame(transactions)

    source_counts = df[['source', 'merchant_id']]\
        .groupby(['source'])\
        .count()\
        .to_dict()['merchant_id']
    report_source_counts = ''
    for key in source_counts:
        report_source_counts += (
            f'<tr>'
            f'<td>{key}</td>'
            f'<td>{source_counts[key]}</td>'
            f'</tr>'
        )

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
    synced_count = df[df['pg_transaction_id'] > 0]['transaction_id'].count()
    subject = f'AQWIRE Transaction cross validation report - {report_timestamp}'
    with io.open('./tools/emails/cross_validate_email_report.html', encoding='utf-8') as file:
        html = file.read()\
            .replace('{{ reportDate }}', report_timestamp)\
            .replace('{{ transactionCount }}', str(total_count))\
            .replace('{{ transactionDesyncCount }}', str(total_count - synced_count))\
            .replace('{{ sourceCounts }}', report_source_counts)\
            .replace('{{ merchantTransactionCounts }}', report_merchant_txs_counts)

        request_url = 'https://api.mailgun.net/v3/{0}/messages'.format(mailgun_domain)
        result = requests.post(
            request_url,
            auth=('api', mailgun_key),
            files=[
                ('attachment', (f'transactions-{report_timestamp}.csv', build_csv(df)))
            ],
            data={
                'from': sender,
                'to': recipients,
                'subject': subject,
                'text': html,
                'html': html
            })
        print(f'Report mailing result: {result.status_code} {result.reason}')

main()
