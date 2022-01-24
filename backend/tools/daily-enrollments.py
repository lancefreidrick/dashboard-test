import logging
from os import getenv
from datetime import datetime
from argparse import ArgumentParser
from collections import defaultdict

import psycopg2
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient


load_dotenv()

description = 'Sends daily enrollment and payment reports'
script_usage = f'''
    python ./daily-enrollment-payment-reports.py
        [-H, --hour={{NOW,0-23}}]
'''

main_parser = ArgumentParser(description=description, usage=script_usage)

main_parser.add_argument('--hour',
                         '-H',
                         help=(
                             'Sets the hour for which the script will run. '
                             'Default value is value of environment variable \'CRON_DAILY_TRANSACTION_HOUR\'. '
                             'Using the keyword \'NOW\' uses the hour of execution time.'
                         ),
                         default=getenv('CRON_DAILY_TRANSACTION_HOUR'))

main_parser.add_argument('--verbose',
                         '-v',
                         help='Allows the script to display debug messages',
                         action='store_true')

args = main_parser.parse_args()

if args.hour == 'NOW':
    args.hour = str(datetime.now().hour)

if args.hour.isdigit():
    args.hour = int(args.hour)

else:
    print('Hour is not a digit')
    exit()

log = logging.getLogger('daily-enroll-pay-report-job')
log.setLevel(level=logging.DEBUG if args.verbose else logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handle = logging.FileHandler('daily-enroll-pay-report-job.log', mode='a+', encoding='utf-8')
file_handle.setLevel(level=logging.DEBUG if args.verbose else logging.INFO)
file_handle.setFormatter(formatter)

log.addHandler(file_handle)

with open('tools/emails/daily-enrollments.html', mode='r') as f:
    template = f.read()

db = None


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


def main():
    global log, template

    initialize_db()

    mailer = SendGridAPIClient(api_key=getenv('SENDGRID_SECRET_KEY'))

    tmp = execute_function('directory.get_merchant_members_to_be_notified_by_hour',
                           [args.hour])

    merchant_members_to_be_notified = {}
    log.info(f'Preparing notifications for {len(tmp)} merchant admins')

    for item in tmp:
        if item['merchant_name'] in merchant_members_to_be_notified:
            merchant_members_to_be_notified[item['merchant_name']].append(item['email_address'])

        merchant_members_to_be_notified[item['merchant_name']] = [item['email_address']]

    for merchant, admins in merchant_members_to_be_notified.items():
        results = execute_function('invoicing.get_success_or_failed_transactions_today', [merchant])
        log.info(f'Processing {len(admins)} merchant admin(s) for {merchant} with {len(results)} transactions')

        transactions = ''

        summary_count = 0

        projects = defaultdict(list)

        for r in results:
            projects[r['project_name']].append(r)

        projects = list(projects.values())

        for project in projects:
            transactions += f'''<h2 style="color: #000">Project: <strong>{project[0]['project_name']}</strong></h2>'''

            customers = defaultdict(list)

            for p in project:
                customers[p['customer_name']].append(p)

            customers = list(customers.values())

            for customer in customers:
                transactions += (
                    f'''<h3 style="color: #000">Customer: <strong>{customer[0]['customer_name']}</strong></h3>'''
                    '<table width="100%" border="1" cellpadding="10" cellspacing="0">'
                    '<thead style="font-weight: 700;">'
                    '<td>Reference ID</td>'
                    '<td>Transaction Type</td>'
                    '<td>Transaction Status</td>'
                    '<td>Payment Type</td>'
                    '<td>Created At</td>'
                    '</thead>'
                )

                for record in customer:
                    summary_count += 1
                    formatted_date = record['created_at'].strftime('%B %d, %Y %I:%M:%S %p')

                    transactions += (
                        '<tr>'
                        f'''<td>{record['reference_id']}</td>'''
                        f'''<td>{record['transaction_type_name']}</td>'''
                        f'''<td>{record['transaction_status_name']}</td>'''
                        f'''<td>{record['payment_type_name']}</td>'''
                        f'<td>{formatted_date}</td>'
                        '</tr>'
                    )

                transactions += '</table><br><br>'

        transactions += f'<h3 style="color: #000">Total number of transactions: {summary_count}</h3>'

        html = template \
            .replace('{{ date }}', datetime.now().date().strftime('%B %d, %Y')) \
            .replace('{{ merchant }}', merchant) \
            .replace('{{ transactions }}', transactions)

        response = mailer.client.mail.send.post(request_body={
            'personalizations': [
                {
                    'to': [{'email': x} for x in admins],
                    'subject': 'Daily Enrollment And Payments Report'
                }
            ],
            'from': {
                'email': getenv('SENDGRID_SENDER')
            },
            'content': [
                {
                    'type': 'text/html',
                    'value': html
                }
            ]
        })

        if 200 <= response.status_code < 300:
            log.info((f'''Email sent to {len(admins)} merchant '''
                      f'''admins ({', '.join(admins)}) with status code {response.status_code}'''))

        else:
            log.warning((
                f'''Email failed to send to {len(admins)} merchant '''
                f'''admins ({', '.join(admins)}) with status code {response.status_code}'''
            ))


if __name__ == '__main__':
    main()
