import sys
from os import getenv
from json import loads
from typing import List
import logging
from argparse import ArgumentParser
from datetime import datetime, timedelta

import psycopg2
from redis import Redis
from tenjin import Engine
from tenjin.html import *
from tenjin.helpers import *
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from server.models.email_task_model import EmailTask


load_dotenv()

description = 'Sends payment email to merchants using the payment reference ID'
script_usage = f'''
    python ./portals-payment-emails.py
        [-e, --email={{EMAIL}}]
        [-m, --merchant={{MERCHANT_CODE}}]
        [-p, --pay={{PAYMENT_REFERENCE_ID}}]
'''

main_parser = ArgumentParser(description=description, usage=script_usage)

main_parser.add_argument('--email',
                         '-e',
                         help='Recipient email')

main_parser.add_argument('--merchant',
                         '-m',
                         help='Merchant Code')

main_parser.add_argument('--pay',
                         '-p',
                         help='Payment Reference ID')

args = main_parser.parse_args()

log = logging.getLogger('portals-payment-emails')
log.setLevel(level=logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handle = logging.FileHandler('portals-payment-emails.log', mode='a+', encoding='utf-8')
file_handle.setLevel(level=logging.INFO)
file_handle.setFormatter(formatter)

log_stream = logging.StreamHandler(sys.stdout)
log_stream.setLevel(level=logging.DEBUG)
log_stream.setFormatter(formatter)

log.addHandler(file_handle)
log.addHandler(log_stream)

LIST_KEY = 'aqw-email-queue'

tasks: List[EmailTask] = []
engine = Engine()
db = None
redis_client: Redis = None

def initialize_db():
    global log, db
    cursor = None
    connection_string = getenv('PG_CONNECTION_STRING')

    try:
        log.info('pgdb: Connecting to PSQL database (%s)...', connection_string.split('@')[1])
        db = psycopg2.connect(connection_string)
        cursor = db.cursor()
        cursor.execute('SELECT VERSION()')
        log.info('pgdb: Connected to %s', cursor.fetchone())

    except psycopg2.DatabaseError as error:
        log.error('pgdb: ERROR on database connection')
        log.error('pgdb: %s', error)

    finally:
        if cursor:
            cursor.close()


def initialize_redis():
    global redis_client

    try:
        redis_client = Redis(host=getenv('REDIS_HOST'),
                             port=int(getenv('REDIS_PORT', 0)),
                             password=getenv('REDIS_PASSWORD'))
        redis_client.ping()
    except Exception as e:
        log.error(f'Connection failed: {str(e)}')
        exit()


def execute_function(func_name, *params):
    global log, db

    log.debug('dbfunc: %s %s', func_name, str(*params))

    try:
        cursor = db.cursor()
        cursor.callproc(func_name, *params)
        data = cursor.fetchall()

        column_names = [d[0] for d in cursor.description]
        mapped_data = [dict(zip(column_names, list(values))) for values in data]

        db.commit()
        return mapped_data

    except (psycopg2.InterfaceError, psycopg2.OperationalError) as error:
        log.error("Db server connection error, restarting connection..")
        initialize_db()
        log.info("Server reconnected, retrying query..")

    except (psycopg2.ProgrammingError, psycopg2.DatabaseError) as error:
        db.rollback()
        log.error("Internal server error, rolling back..")
        raise error

    finally:
        cursor.close()


def queue_handler():
    global redis_client, tasks

    if args.merchant and args.pay and args.email:
        log.info('Skipping Redis task queue retrieval')
        tasks.append(EmailTask(**{
            'recipients': [args.email],
            'taskId': 'PORTALS_PAYMENT_NOTIFICATION',
            'source': 'manual_invoke',
            'args': {
                'merchantCode': args.merchant,
                'paymentReferenceId': args.pay
            }
        }))
        return

    log.info('Retrieving details from Redis queue')
    for_requeue: List[EmailTask] = []
    while True:
        msg = redis_client.lpop(LIST_KEY)
        if msg is None:
            break

        task = EmailTask(**loads(msg.decode('utf-8')))

        # Do not include task if not yet time to execute
        if not task.must_execute:
            log.info(f'Skipping {task} with retry count of {task.retries} '
                     f'and upcoming retry on {task.retry_timestamp.isoformat()}')
            for_requeue.append(task)
            continue

        # Greater than 3 retries means do not try again anymore
        if task.retries > 3:
            log.info(f'{task} has exceeded maximum retries, dropping task')
            continue

        tasks.append(task)

    if for_requeue:
        redis_client.rpush(LIST_KEY, *[r.json() for r in for_requeue])


def main(email_task: EmailTask):
    global redis_client, engine

    merchant = email_task.args.get('merchantCode')
    payment_reference_id = email_task.args.get('paymentReferenceId')
    key = f'{merchant}/{payment_reference_id}'

    _result = execute_function('invoicing.find_payment_by_reference_id', [merchant, payment_reference_id])
    if not _result:
        log.error(f'Payment {key} does not exist')
        email_task.retries += 1
        email_task.retry_timestamp = datetime.now() + timedelta(minutes=15)
        redis_client.rpush(LIST_KEY, email_task.json())
        return

    result = _result[0]
    empty_value = 'None provided'
    email_payload = {
        'merchant_name': result['merchant_name'] or empty_value,
        'merchant_project': result['project_name'] or empty_value,
        'base_payment': f"{result['bill_base_currency']} {result['bill_base_amount']:,.2f}",
        'net_payment': f"{result['net_currency']} {result['net_amount']:,.2f}",
        'customer_name': result['customer_name'] or empty_value,
        'customer_email': result['customer_email_address'] or empty_value,
        'payment_type': result['payment_type_name'] or empty_value,
        'payment_reference_id': payment_reference_id,
        'payment_url': f"{getenv('APP_CLIENT_URL')}/merchants/{merchant}/payments/{payment_reference_id}"
    }

    payload = engine.render('tools/emails/portals_payment.html', email_payload)
    mailer = SendGridAPIClient(api_key=getenv('SENDGRID_SECRET_KEY'))

    recipients = {
        'to': [{'email': email} for email in email_task.recipients],
        'cc': [{'email': email} for email in (email_task.cc or [])],
        'bcc': [{'email': email} for email in (email_task.bcc or [])],
    }

    response = mailer.client.mail.send.post(request_body={
        'personalizations': [{k: v for k, v in recipients.items() if v}],
        'subject': f"Payment {email_payload['payment_reference_id']} "
                   f"from {email_payload['customer_name']} for {email_payload['merchant_project']}",
        'from': {
            'email': getenv('SENDGRID_SENDER')
        },
        'content': [
            {
                'type': 'text/html',
                'value': payload
            }
        ]
    })

    if 200 <= response.status_code < 300:
        log.info(f'Payment receipt for {key} sent to {email_task.recipients}')

    else:
        log.error(f'Failed to send payment receipt for {key} to {email_task.recipients} after {email_task.retries}')
        new_task = email_task
        new_task.retries += 1
        new_task.retry_timestamp = datetime.now() + timedelta(minutes=15)

        redis_client.rpush(LIST_KEY, new_task.json())


if __name__ == '__main__':
    initialize_db()
    initialize_redis()
    queue_handler()

    for task in tasks:
        try:
            main(task)
        except Exception as e:
            log.error(f'Unknown error occurred, will requeue task: {str(e)}')
            task.retries += 1
            task.retry_timestamp = datetime.now() + timedelta(minutes=15)
            redis_client.rpush(LIST_KEY, task.json())
