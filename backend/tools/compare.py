"""
compare.py
"""
import os
import time
from datetime import datetime
from dataclasses import dataclass
from typing import List
import argparse
import dotenv
import psycopg2
import pytz
import pandas as pd
from pymongo import MongoClient
from redis import Redis

dotenv.load_dotenv()

dsn = os.getenv('PG_CONNECTION_STRING')
mongodb = MongoClient(
    host=os.environ.get('MONGODB_HOST'),
    port=int(os.environ.get('MONGODB_PORT')) or 27017)

redis_client = Redis(
    host=os.getenv('REDIS_HOST'),
    password=os.getenv('REDIS_PASSWORD'),
    port=int(os.getenv('REDIS_PORT') or 6379))

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--start', type=str,
    required=True, dest='start_date', help='ISO formatted start date')
arg_parser.add_argument('--end', type=str,
    required=True, dest='end_date', help='ISO formatted end date')
arg_parser.add_argument('--pubsub', action='store_true',
    dest='enable_pubsub', help='Enable pubsub with delay', default=False)


class ImportArguments:
    def __init__(self, data):
        self.start_date: datetime = data.get('start_date')
        self.end_date: datetime = data.get('end_date')
        self.enable_pubsub: bool = data.get('enable_pubsub')

    @staticmethod
    def parse(data):
        tz = pytz.timezone('Asia/Manila')
        start_date = datetime.fromisoformat(data.start_date)\
            .replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=tz)
        end_date = datetime.fromisoformat(data.end_date)\
            .replace(hour=23, minute=59, second=59, microsecond=9999, tzinfo=tz)

        return ImportArguments({
            'start_date': start_date,
            'end_date': end_date,
            'enable_pubsub': data.enable_pubsub
        })


@dataclass
class PostgresTransaction:
    transaction_id: int
    external_transaction_id: str
    transaction_type_id: int
    reference_id: str
    merchant_code: str
    transaction_status_code: str
    payment_method_name: str

    def __str__(self) -> str:
        return f'{self.merchant_code}/{self.external_transaction_id}'

    def __repr__(self) -> str:
        return f'Payment({self.merchant_code},{self.external_transaction_id})'


class MongoTransaction:
    def __init__(self, tx_data: dict):
        self.transaction_id: str = tx_data.get('transactionId')
        self.merchant_id: str = tx_data.get('merchantId')
        self.reference_id: str = tx_data.get('referenceId')
        self.transaction_type: str = tx_data.get('type')
        self.status: str = tx_data.get('status')
        self.created_at: datetime = tx_data.get('createdAt')
        self.source: datetime = tx_data.get('source')
        self.paid_at: datetime = tx_data.get('paidAt')

        if 'cc' in tx_data:
            self.payment_method: str = 'cc'
        elif 'ach' in tx_data:
            self.payment_method: str = 'ach'
        elif 'pp' in tx_data:
            self.payment_method: str = 'pp'
        elif 'directDebit' in tx_data:
            self.payment_method: str = 'directdebit'
        elif 'ewallet' in tx_data:
            self.payment_method: str = 'ewallet'
        else:
            self.payment_method: str = None

    def __str__(self) -> str:
        return f'{self.merchant_id}/{self.transaction_id}'

    def __repr__(self) -> str:
        return f'Transaction({self.merchant_id},{self.transaction_id})'


def get_transactions_from_mgdb(db_name: str, start_date: datetime, end_date: datetime) -> List[MongoTransaction]:
    target_db = mongodb.get_database(db_name)
    transaction_collection = target_db.get_collection('transactions')
    transactions_cursor = transaction_collection.find({
        'createdAt': {
            '$gt': start_date,
            '$lt': end_date
        }
    })
    transactions = [MongoTransaction(t) for t in transactions_cursor]
    return transactions


def get_transactions_from_pgdb(start_date: datetime, end_date: datetime) -> List[PostgresTransaction]:
    pg_client = psycopg2.connect(dsn=dsn)
    with pg_client.cursor() as cursor:
        query = '''
        SELECT
            t.transaction_id,
            t.external_transaction_id,
            t.transaction_type_id,
            t.reference_id,
            m.merchant_code,
            ts.transaction_status_code,
            pm.payment_method_name
        FROM invoicing.transaction AS t
        INNER JOIN directory.merchant AS m
            ON m.merchant_id = t.merchant_id
        INNER JOIN invoicing.payment_method AS pm
            ON pm.payment_method_id = t.payment_method_id
        INNER JOIN invoicing.transaction_status AS ts
            ON ts.transaction_status_id = t.transaction_status_id
        WHERE t.created_at BETWEEN %s and %s
        ORDER BY t.created_at DESC
        '''
        cursor.execute(query, (
            start_date,
            end_date
        ))
        rows = cursor.fetchall()
        payments = [PostgresTransaction(*row) for row in rows]

        cursor.close()
        pg_client.close()

        return payments


def start():
    args = ImportArguments.parse(arg_parser.parse_args())

    data = []
    mgdb_transactions = get_transactions_from_mgdb('invoicing', args.start_date, args.end_date) +\
        get_transactions_from_mgdb('billing', args.start_date, args.end_date)
    print(f'Total mgdb payments: {len(mgdb_transactions)}')

    pgdb_transactions = get_transactions_from_pgdb(args.start_date, args.end_date)
    print(f'Total pgdb payments: {len(pgdb_transactions)}')

    for mp in mgdb_transactions:
        item = {
            'transactionId': mp.transaction_id,
            'merchantId': mp.merchant_id,
            'referenceId': mp.reference_id,
            'type': mp.transaction_type,
            'status': mp.status,
            'paymentMethod': mp.payment_method,
            'createdAt': mp.created_at,
            'paidAt': mp.paid_at,
            'source': mp.source
        }

        pg_transaction = next((
            pg for pg in pgdb_transactions
            if pg.external_transaction_id == mp.transaction_id and pg.merchant_code == mp.merchant_id
        ), None)
        item['pg_transaction_id'] = pg_transaction.transaction_id if pg_transaction else 0

        data.append(item)
        key = f'{mp.merchant_id}/{mp.transaction_id}/{mp.reference_id}'

        if args.enable_pubsub:
            redis_client.publish('etl', f'{mp.transaction_id},dashboard-tools,compare')
            time.sleep(4 if mp.transaction_type == 'enrollment' else 0.5)

        print(f'{datetime.now()} - {key}')

    df = pd.DataFrame(data)
    df.to_csv('transactions.csv')


start()
