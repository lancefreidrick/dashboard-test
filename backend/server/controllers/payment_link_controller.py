""" project_controller.py """
# pylint: disable=unused-argument
from flask import Blueprint, abort, jsonify, g, request
from marshmallow import ValidationError

from server.config.logger import log
from server.config.authentication import authentication
from server.models.person_model import Person, Roles, MerchantRoles
from server.models.merchant_model import Merchant
from server.models.payment_model import Payment, validate_payment_link
from server.config.environment import config
from server.repositories import (
    project_repository, payment_repository, transaction_repository, merchant_repository
)
from server.utilities import emails
from server.services import apocalypse_service

"""
Call to the apocalypse endpoints where the main logic happens. This is because the mongoDB
counterpart of the transaction must be created first:
1. create_payment_link() is called
2. apocalypse is called, the transaction is created in both MongoDB and Postgres (double write)
3. apocalypse sends a success response to the caller (dashboards-api), dashboards-api then sends a
   success response to black-widow
4. black-widow redirects the page with the created/updated payment page, knowing that the
   double db write is successful.

This is the structure for now as long as the two DBs exist; ought to be changed later on once the
data is fully migrated to Postgres, in which the main logic should now happen in dashboards-api:
1. create_payment_link() is called
2. dashboards-api writes to Postgres
3. dashboards-api then sends a success response to black-widow
4. black-widow redirects the page with the created/updated payment page
"""

payment_link_blueprint = Blueprint('payment_link', __name__)
BASE_URL = '/merchants/<int:merchant_id>/payment-links'


@payment_link_blueprint.route(BASE_URL, methods=['GET'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_STAFF)
def get_payment_link_form(merchant_id: int):
    current_user: Person = g.user
    merchant: Merchant = g.merchant

    if not current_user.is_internal() and merchant.merchant_code not in current_user.scopes:
        abort(403, {'message': 'You are not allowed to get this merchant payment'})

    if not merchant.can_manage_payment_links:
        abort(403, {'message': 'You are not allowed to create payment links'})

    return jsonify(merchant.payment_form), 200


@payment_link_blueprint.route(BASE_URL, methods=['POST'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_STAFF)
def create_payment_link(merchant_id: int):
    fn = 'create_payment_link'
    current_user: Person = g.user
    merchant: Merchant = g.merchant

    if not current_user.is_internal() and merchant.merchant_code not in current_user.scopes:
        abort(403, {'message': 'You are not allowed to create a payment link'})

    if not merchant.can_manage_payment_links:
        abort(403, {'message': 'You are not allowed to create payment links'})

    request_body = request.get_json()
    validation_error, payment_link = validate_payment_link(
        data=request_body,
        merchant=merchant)
    if validation_error:
        abort(400, {
            'message': 'There are errors in your submitted payment link',
            'errors': validation_error.normalized_messages()
        })

    # NOTE: .endswith throws an error if it is empty.
    type_code = payment_link.payment_type_code
    payment_types = merchant_repository.get_merchant_payment_types(merchant)
    payment_type = next((pt for pt in payment_types if pt.code.endswith(type_code)), None)\
        if type_code else None
    if not payment_type:
        payment_type = next((pt for pt in payment_types if pt.code.endswith('DTP')), None)

    project = project_repository.find_merchant_project_by_project_id(merchant, payment_link.project_id)

    is_payment_link_created, data, field_errors = apocalypse_service.create_payment_link(
        merchant=merchant,
        payment_link=payment_link,
        created_by=current_user,
        project=project,
        payment_type=payment_type)
    if not is_payment_link_created:
        log.error(f'{fn}: Payment link was not created with the following data')
        if field_errors:
            abort(400, {
                'message': 'There are errors in your submitted payment link',
                'errors': field_errors
            })

        abort(400, {
            'message': 'We are not able to create the payment link. Please try again later.'
        })

    return jsonify({
        'externalTransactionId': data['externalTransactionId'],
        'transactionId': data['transactionId'],
        'invoiceId': data['invoiceId'],
        'paymentUrl': data['paymentUrl'],
        'message': data['message'],
    }), 201


@payment_link_blueprint.route(
    f'{BASE_URL}/<int:invoice_id>/cancel',
    methods=['POST'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_STAFF)
def cancel_payment_link(merchant_id: int, invoice_id: int):
    fn = 'cancel_payment_link'
    current_user: Person = g.user
    merchant: Merchant = g.merchant

    if not current_user.is_internal() and merchant.merchant_code not in current_user.scopes:
        abort(403, {'message': 'You are not allowed to cancel this payment link'})

    if not merchant.can_manage_payment_links:
        abort(403, {'message': 'You are not allowed to create payment links'})

    payment = payment_repository.find_payment_by_invoice_id(invoice_id)
    if not payment:
        log.error(f'{fn}: Payment does not exist')
        abort(404, {'message': 'Payment does not exist'})

    # Checks, if not INC and PENDING
    if payment.transaction_status.id != 1: # INCOMPLETE
        log.error(f'{fn}: Invalid invoice status (Not INC)')
        abort(404, {'message': 'Cancel link failed. Payment transaction is not INC status'})

    if payment.payment_status.id != 7: # PENDING
        log.error(f'{fn}: Invalid invoice status (Not PENDING)')
        abort(404, {'message': 'Cancel link failed. Payment invoice is not PENDING status'})

    is_payment_link_cancelled, message = apocalypse_service.cancel_payment_link(
        merchant=merchant,
        cancelled_by=current_user,
        payment=payment)

    if not is_payment_link_cancelled:
        log.error(f'{fn}: {message}')
        abort(404, {'message': message})

    return jsonify({
        'message': 'Cancel Link successful',
    }), 200


@payment_link_blueprint.route(
    f'{BASE_URL}/<int:invoice_id>/send-email',
    methods=['POST'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_STAFF)
def send_payment_link_email(merchant_id, invoice_id):
    fn = 'send_payment_link_email'
    merchant: Merchant = g.merchant
    email: str = request.json['email']

    if not email:
        log.error(f'{fn}: No email address provided')
        abort(400, {'message': 'No email address provided'})

    payment: Payment = payment_repository.find_payment_by_invoice_id(invoice_id)
    if not payment:
        abort(404, {'message': 'Payment does not exist'})

    if payment.merchant.merchant_id != merchant.merchant_id:
        abort(404, {'message': 'Payment does not exist'})

    transaction = transaction_repository.find_transaction_by_external_transaction_id(
        transaction_id=payment.external_transaction_id,
        merchant=merchant)
    signature = transaction.generate_hmac_signature(merchant.links_secret)
    payment_link = (
        f'{config.portals_url}/{merchant.merchant_code}/links/'
        f'{transaction.external_transaction_id}/{signature}'
    )

    send_result = emails.send_payment_link_email(email, transaction, payment_link)
    if not send_result.is_sent:
        log.error(f'{fn}: failed to send email to {email}')
        abort(503, {'message': 'Failed to send payment link'})

    log.info(f'{fn}: email sent to {email}')
    return jsonify({'message': 'Payment link email has been sent'}), 200
