"""
sync_old_transactions.py

Its main purpose is to synchronize old enrollments from merchant-portal
to the aqwire-db because of the API's deprecation status.
"""

import os
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
import argparse
import pytz
from dotenv import load_dotenv
from pymongo import MongoClient
from redis import Redis

load_dotenv()

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--days', '-D',
    dest='days', help='Days from now', default=1)
arg_parser.add_argument('--delay', '-DL',
    dest='delay', help='Second/s delay between records published into the etl channel', default=5)
args = arg_parser.parse_args()

SUBTRACTED_DAYS = int(args.days)
DELAY_IN_SECS = int(args.delay)

mongodb = MongoClient(
    host=os.getenv('MONGODB_HOST'),
    port=int(os.getenv('MONGODB_PORT') or 27017))

redis_client = Redis(
    host=os.getenv('REDIS_HOST'),
    password=os.getenv('REDIS_PASSWORD'),
    port=int(os.getenv('REDIS_PORT') or 6379))

@dataclass
class Payment:
    enrollment_id: str
    merchant_id: str
    reference_id: str
    schema: str
    created_at: datetime

@dataclass
class Transaction:
    transaction_id: str
    merchant_id: str
    reference_id: str
    source: str
    status: str
    schema: str
    created_at: datetime

def get_enrollment_payments(db_name: str, timestamp: datetime):
    db = mongodb.get_database(db_name)
    payments_collection = db.get_collection('payments')
    cursor = payments_collection.find({
        'invoiceId': {
            '$exists': True
        },
        'createdAt': {
            '$gt': timestamp - timedelta(days=SUBTRACTED_DAYS),
            '$lte': timestamp
        }
    }).sort([
        ('_id', -1)
    ])
    return [Payment(**{
        'enrollment_id': tx['enrollmentId'],
        'merchant_id': tx['merchantId'],
        'reference_id': tx['referenceId'],
        'created_at': tx['createdAt'],
        'schema': db_name
    }) for tx in cursor]


def get_enrollment_transaction(payment: Payment) -> Transaction:
    db = mongodb.get_database(payment.schema)
    transactions_collection = db.get_collection('transactions')
    doc = transactions_collection.find_one({
        'referenceId': payment.enrollment_id,
        'merchantId': payment.merchant_id,
        'type': 'enrollment'
    })
    if not doc:
        return None

    return Transaction(**{
        'transaction_id': doc['transactionId'],
        'merchant_id': doc['merchantId'],
        'reference_id': doc['referenceId'],
        'status': doc['status'],
        'source': doc['source'],
        'created_at': doc['createdAt'],
        'schema': payment.schema
    })


def main():
    today = datetime.now().astimezone(tz=pytz.timezone('Asia/Manila'))

    retrieved_payments = []
    for schema in ['invoicing', 'billing']:
        retrieved_payments += get_enrollment_payments(schema, today)

    for payment in retrieved_payments:
        transaction = get_enrollment_transaction(payment)
        if not transaction:
            print(f'{payment.merchant_id}/{payment.reference_id}/{payment.enrollment_id} - NOT FOUND')
        else:
            key = f'{transaction.merchant_id}/{transaction.transaction_id}/{transaction.reference_id}'
            print(f'Payment#{payment.reference_id} - {key} - {transaction.status},{transaction.source}')

            if transaction.source in ['merchant-portal', 'ayalaland-ma']:
                message = f'{transaction.transaction_id},sync-old-transactions,sync'
                redis_client.publish('etl', message)

        time.sleep(DELAY_IN_SECS)


main()
