# Though this hurts me, this is how tenjin does things:
from contextlib import suppress
from server.models.transaction_model import Transaction
from dateutil.parser import isoparse
from tenjin.helpers import *  # pylint: disable=wildcard-import,import-error

from server.config import environment
from server.config import tenjin_templater
from server.config.mailer import send_email
from server.models.payment_model import Payment
from server.models.invoice_model import Invoice

config = environment.config


def send_user_invite_email(recipient_email, sender_name, encoded_email):
    templater = tenjin_templater.get_templater()

    invite_url = '{}/signup/{}'.format(config.client_url, encoded_email)

    context = {
        'sender_name': sender_name,
        'invite_url': invite_url,
        'days_before_expiration': '{0:.0f}'.format(config.signup_link_max_age / 24 / 60 / 60),
    }

    html = templater.render('user_invite.pyhtml', context)

    return send_email(recipient_email, "You've been invited to AQWIRE's dashboard!", html)


def send_password_reset_email(recipient_name, recipient_email, reset_id, token):
    templater = tenjin_templater.get_templater()

    reset_url = '{}/password-reset/{}/{}'.format(config.client_url, reset_id, token)

    context = {
        'recipient_name': recipient_name,
        'reset_url': reset_url,
        'hours_before_expiration': '{0:.0f}'.format(config.reset_token_life),
    }

    html = templater.render('password_reset.pyhtml', context)

    return send_email(recipient_email, 'Reset your password', html)


def send_password_changed_confirmation_email(recipient_name, recipient_email):
    templater = tenjin_templater.get_templater()

    context = {
        'recipient_name': recipient_name,
    }

    html = templater.render('password_changed_confirmation.pyhtml', context)

    return send_email(recipient_email, 'Your AQWIRE dashboard password has been changed', html)


def send_settlement_report_email(recipient_emails, payments, total_payments, total_merchants):
    templater = tenjin_templater.get_templater()

    context = {
        'payments': payments,
        'total_payments': total_payments,
        'total_merchants': total_merchants
    }

    html = templater.render('settlement_report.pyhtml', context)

    return send_email(recipient_emails, 'Settlement Report', html)


def send_payment_receipt(
        recipient_email,
        payment: Payment,
        next_invoice: Invoice = None,
        remaining_months: int = 0):
    templater = tenjin_templater.get_templater()

    payment_method = payment.payment_method.payment_method_type \
        if payment.payment_method.payment_method_name != 'cc' \
        else f'**** **** **** {payment.payment_method.card_last_four()}'

    context = {
        'merchant_name': payment.merchant.name,
        'customer_name': payment.customer.name,
        'customer_email': payment.customer.email,
        'customer_phone_number': f'''{payment.customer.phone or ''}''',
        'transaction_status': {
            'PROCESSED': 'PENDING',
            'PAID': 'SUCCESS',
            'SETTLED': 'SUCCESS',
        }.get(payment.payment_status.code, 'SUCCESS'),
        'receipt_id': payment.payment_reference_id,
        'receipt_date': payment.invoice_paid_at.strftime('%b. %d, %Y'),
        'transaction_action_name': {
            # FIXME: What should be the other stuff here?
            'processed': 'PENDING',
            'paid': 'SUCCESS',
            'SETTLED': 'SUCCESS',
        }.get(payment.transaction_status.name, 'completed'),
        'payment_type': payment.payment_type.name,
        'project': payment.project.displayed_name,
        'payment_method': payment_method,
        'amount_due': f'{payment.bill.base[0]} {payment.bill.base[1]:,.2f}',
        'amount_in_usd': f'{payment.bill.converted[0]} {payment.bill.converted[1]:,.2f}',
        'convenience_fee': f'{payment.bill.fee[0]} {payment.bill.fee[1]:,.2f}',
        'total_amount': f'{payment.bill.total[0]} {payment.bill.total[1]:,.2f}',
        'qw_rates': f'{payment.bill.qwx_rate[0]} 1 = {payment.bill.qwx_rate[1]} {payment.bill.qwx_rate[2]:,.4f}',
        'client_notes': payment.client_notes or 'You have not entered any notes',
        'project_aggregated_fields': __aggregate_paid_to_fields_as_key_value_tuple(payment),
        'show_amount_in_usd': payment.bill.qwx_rate[2] > 0,
        'copyright_year': payment.transaction_created_at.strftime('%Y'),
    }

    html = templater.render('payment_successful.html', context)

    if payment.transaction_type.id == 20:
        if payment.bill.converted:
            converted_amount = payment.bill.converted[1]
            converted_currency = payment.bill.converted[0]
            conversion = payment.bill.base[1] / converted_amount
            conversion_rate = f'{converted_currency} 1 ≈ {payment.bill.base[0]} {conversion:.3g}'
        else:
            converted_amount = None

        context.update({
            'enrollment_id': payment.transaction_reference_id,
            'description': payment.invoice_description,
            'base_currency': payment.bill.base[0],
            'base_amount': f'{payment.bill.base[1]:,.2f}',
            'converted_amount': f'{converted_amount:,.2f}',
            'converted_currency': converted_currency,
            'fee_currency': payment.bill.fee[0],
            'fee_amount': f'{payment.bill.fee[1]:,.2f}',
            'total_currency': payment.bill.total[0],
            'total_amount': f'{payment.bill.total[1]:,.2f}',
            'conversion_rate': conversion_rate
        })

        if next_invoice:
            context.update({
                'enrollment_id': payment.transaction_reference_id,
                'description': payment.invoice_description,
                'next_invoice': next_invoice,
                'next_invoice_date': next_invoice.due_at.strftime('%B %d, %Y'),
                'next_invoice_amount': f'{next_invoice.bill.base[0]} {next_invoice.bill.base[1]:,.2f}'
            })

        if remaining_months > 0:
            context.update({
                'remaining_months': remaining_months,
            })

        html = templater.render('payment_receipt_ma.html', context)

    return send_email(recipient_email, f'{payment.merchant.name} payment via AQWIRE', html)



def send_payment_link_email(recepient_email: str, transaction: Transaction, payment_link):
    templater = tenjin_templater.get_templater()

    context = {
        'merchant_name': transaction.merchant.name,
        'transaction_id': transaction.external_transaction_id,
        'customer_name': transaction.customer.name,
        'project_name': transaction.project.name,
        'payment_type': transaction.payment_type.name,
        'client_notes': transaction.client_notes,
        'amount_currency': transaction.base_amount[0],
        'amount_due': f'{transaction.base_amount[1]:.2f}',
        'payment_link': payment_link,
        'support_email': 'support@aqwire.io',
        'copyright_year': '2021'
    }

    html = templater.render('payment-link.html', context)
    return send_email(recepient_email, f'{transaction.merchant.name} payment link via AQWIRE', html)


def send_user_welcome_email(recipient_email, recipient_name):
    templater = tenjin_templater.get_templater()

    login_url = '{}/login'.format(config.client_url)

    context = {
        'recipient_name': recipient_name,
        'login_url': login_url,
    }

    html = templater.render('user_welcome.html', context)

    return send_email(recipient_email, "Welcome to the AQWIRE Enterprise Dashboard", html)


def __parse_datetime_string(value) -> str:
    if isinstance(value, str) and value.isdigit():
        return value

    # Ignores these errors as they correspond to invalid datetime strings
    with suppress(ValueError, TypeError):
        dt_string = isoparse(value)
        return dt_string.strftime('%b %d, %Y')

    return value


def __aggregate_paid_to_fields_as_key_value_tuple(payment: Payment):
    project_values = []

    for field in payment.custom_fields_list():
        if field.get('value'):
            # remove colon as last character
            key_text = field.get('text')
            is_colon_present = key_text[-1] == ':'
            key_text = key_text[:-1] if is_colon_present else key_text
            project_values.append((key_text, str(__parse_datetime_string(field.get('value')))))

    return project_values
