""" payment_controller.py """
# pylint: disable=unused-argument
from io import StringIO
from datetime import datetime
from flask import Blueprint, request, jsonify, abort, Response, g
import pandas as pd
from server.config.logger import log
from server.config.authentication import authentication
from server.config.environment import config
from server.models.search_option_model import SearchOption
from server.models.person_model import Roles, MerchantRoles
from server.models.transaction_log_model import TransactionLog
from server.models.dispute_model import Dispute
from server.utilities.context_manager import open_transaction_context, ContextStatus
from server.utilities.emails import send_payment_receipt
from server.utilities.code_generator import generate_dispute_ref_id
from server.repositories import (
    merchant_repository, payment_repository, transaction_repository, transaction_log_repository, dispute_repository
)

payment_blueprint = Blueprint('payment', __name__)


@payment_blueprint.route('/payments', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_role(Roles.CUSTOMERSUPPORT)
def search_payments():
    search_option = SearchOption.map_from_query(request.args)
    payments, total_count = payment_repository.search_payments(search_option)

    serialized_payments = [p.serialize(is_compact=True) for p in payments]
    return jsonify({
        'payments': serialized_payments,
        'totalCount': total_count,
        'page': search_option.page,
        'size': search_option.size
    }), 200


@payment_blueprint.route('/payments/<int:invoice_id>', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_role(Roles.CUSTOMERSUPPORT)
def get_payment_by_invoice_id(invoice_id: int):
    payment = payment_repository.find_payment_by_invoice_id(invoice_id)
    if not payment:
        abort(404, {'message': 'Payment does not exist'})

    return jsonify(payment.serialize(with_custom_fields=True)), 200


@payment_blueprint.route('/merchants/<int:merchant_id>/payments', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_AGENT)
def get_merchant_payments(merchant_id: int):
    merchant = g.merchant

    search_option = SearchOption.map_from_query(request.args)
    payments, total_count = payment_repository.get_merchant_payments(merchant, search_option)

    serialized_payments = [p.serialize(is_compact=True) for p in payments]
    return jsonify({
        'payments': serialized_payments,
        'totalCount': total_count,
        'page': search_option.page,
        'size': search_option.size
    }), 200


@payment_blueprint.route('/merchants/<merchant_id>/payments/export', methods=['GET'])
def export_merchant_payments(merchant_id: str):
    export_token = request.args.get('token')
    merchant = merchant_repository.find_merchant_by_code(merchant_id)
    if not merchant:
        abort(404, {'message': 'Merchant does not exist'})

    is_success, current_user = authentication.validate_export_token(export_token)
    if not is_success:
        abort(401, {'message': 'Unauthorized to export payments'})

    if not current_user.is_internal() and merchant.merchant_code not in current_user.scopes:
        abort(403, {'message': 'You are not allowed to export payments'})

    # The current export limit is 10,000 records
    search_option = SearchOption.map_from_query(request.args)
    search_option.page = 1
    search_option.size = 10000

    with open_transaction_context(user=current_user, source='payments') as context:
        context.propset(action='Export')
        payments, total_count = payment_repository.get_merchant_payments(merchant, search_option)

        csv_content = _build_csv_on_payments(payments, merchant.timezone, False)
        filename = f'payments-{datetime.now().strftime("%Y-%m-%d")}.csv'

        context.propset(
            status=ContextStatus.SUCCESS,
            description=f'Exported payments from {merchant.merchant_code}',
            metadata={
                'merchant': merchant.merchant_code,
                'page': search_option.page,
                'size': search_option.size,
                'status': search_option.status,
                'paymentMethod': search_option.payment_method,
                'project': search_option.project,
                'paymentType': search_option.payment_type,
                'startdate': str(search_option.start_date),
                'enddate': str(search_option.end_date),
                'query': search_option.search_term,
                'filename': filename,
                'totalCount': total_count
            })
        response = Response(csv_content, 200)
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'filename="{}"'.format(filename)
        return response


@payment_blueprint.route('/payments/export', methods=['GET'])
def export_payments():
    export_token = request.args.get('token')
    is_success, current_user = authentication.validate_export_token(export_token)
    if not is_success:
        abort(401, {'message': 'Unauthorized to export payments'})

    if not current_user.is_internal():
        abort(403, {'message': 'You are not allowed to export these payments'})

    # The current export limit is 10,000 records
    search_option = SearchOption.map_from_query(request.args)
    search_option.page = 1
    search_option.size = 10000

    with open_transaction_context(user=current_user, source='payments') as context:
        context.propset(action='Export')
        payments, total_count = payment_repository.search_payments(search_option)

        # Default timezone of Asia/Manila since QW is in PH
        csv_content = _build_csv_on_payments(payments, 'Asia/Manila', True)
        filename = f'payments-{datetime.now().strftime("%Y-%m-%d")}.csv'

        context.propset(
            status=ContextStatus.SUCCESS,
            description='Exported payments',
            metadata={
                'page': search_option.page,
                'size': search_option.size,
                'status': search_option.status,
                'paymentMethod': search_option.payment_method,
                'project': search_option.project,
                'paymentType': search_option.payment_type,
                'reportAt': str(search_option.reporting_date),
                'dueAt': str(search_option.due_date),
                'startdate': str(search_option.start_date),
                'enddate': str(search_option.end_date),
                'query': search_option.search_term,
                'filename': filename,
                'totalCount': total_count
            })
        response = Response(csv_content, 200)
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'filename="{}"'.format(filename)
        return response


@payment_blueprint.route('/merchants/<merchant_code>/payments/<payment_reference_id>', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_role(Roles.USER, MerchantRoles.MERCHANT_AGENT)
def find_payment_by_reference_id(merchant_code: str, payment_reference_id: str):
    current_user = g.user
    merchant = merchant_repository.find_merchant_by_code(merchant_code)
    if not merchant:
        abort(404, {'message': 'Merchant does not exist'})

    if not current_user.is_internal() and merchant.merchant_code not in current_user.scopes:
        abort(403, {'message': 'You are not allowed to get this merchant payment'})

    payment = payment_repository.find_payment_by_reference_id(payment_reference_id, merchant)
    if not payment:
        abort(404, {'message': 'Payment does not exist'})

    return jsonify(payment.serialize()), 200


@payment_blueprint.route('/merchants/<int:merchant_id>/payments/<external_transaction_id>/<int:invoice_id>',
                         methods=['GET'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_AGENT)
def find_payment_by_external_transaction_id_invoice_id(merchant_id: int, external_transaction_id: str,
                                                       invoice_id: int):
    current_user = g.user
    merchant = g.merchant

    if not current_user.is_internal() and merchant.merchant_code not in current_user.scopes:
        abort(403, {'message': 'You are not allowed to get this merchant payment'})

    payment = payment_repository.find_payment_by_multiple_ids(invoice_id, external_transaction_id, merchant)
    if not payment:
        abort(404, {'message': 'Payment does not exist'})

    data = payment.serialize()

    if payment.transaction_source == 'payment-link':
        transaction = transaction_repository.find_transaction_by_external_transaction_id(external_transaction_id,
                                                                                         merchant)
        hmacSignature = transaction.generate_hmac_signature(merchant.links_secret)
        data['paymentLink'] = f'{config.portals_url}/{merchant.merchant_code}/links/' \
            f'{external_transaction_id}/{hmacSignature}'

    return jsonify(data), 200


@payment_blueprint.route(
    '/merchants/<merchant_code>/payments/<payment_reference_id>/refund',
    methods=['POST'])
@authentication.jwt_required
@authentication.min_access_role(Roles.CUSTOMERSUPPORT)
def refund_payment(merchant_code: str, payment_reference_id: str):
    fn = 'refund payment'
    current_user = g.user

    merchant = merchant_repository.find_merchant_by_code(merchant_code)
    if not merchant:
        abort(404, {'message': 'Merchant does not exist'})

    payment = payment_repository.find_payment_by_reference_id(payment_reference_id, merchant)
    if not payment:
        abort(404, {'message': 'Payment does not exist'})

    is_loaded, validation_error = payment.validate_refund(request.json)
    if not is_loaded or validation_error:
        log.error(f'{fn}: Validation error on refund: {validation_error}')
        abort(400, {'message': 'Submitted refund request contains missing or invalid required values'})

    is_saved, message = payment_repository.refund_payment(payment, current_user)
    if not is_saved:
        log.error(f'{fn}: Failed to refund {payment}: {message}')
        abort(400, {'message': 'Unable to update payment status to refunded'})

    log.info(f'{fn}: Payment {payment} has been refunded')
    return jsonify({ 'message': message }), 200


@payment_blueprint.route(
    '/merchants/<merchant_code>/payments/<payment_reference_id>/offline',
    methods=['POST'])
@authentication.jwt_required
@authentication.min_access_role(Roles.CUSTOMERSUPPORT)
def update_offline_payment(merchant_code: str, payment_reference_id: str):
    fn = 'update_offline_payment'
    current_user = g.user

    merchant = merchant_repository.find_merchant_by_code(merchant_code)
    if not merchant:
        abort(404, {'message': 'Merchant does not exist'})

    payment = payment_repository.find_payment_by_reference_id(payment_reference_id, merchant)
    if not payment:
        abort(404, {'message': 'Payment does not exist'})

    if payment.payment_method.payment_method_name != 'offline':
        log.error(f'{fn}: Payment method mismatch: {payment.payment_method.payment_method_name}')
        abort(404, {'message': 'Payment method is not offline and cannot be completed'})

    if payment.payment_status.id != 7: # PENDING
        log.error(f'{fn}: Payment status mismatch: {payment.payment_status.name}')
        abort(404, {'message': 'Payment cannot be completed due to incorrect status'})

    is_loaded, validation_error = payment.validate_submitted_payment_request(request.json)
    if not is_loaded or validation_error:
        log.error(f'{fn}: Validation error on complete offline payment: {validation_error}')
        abort(400, {'message': 'Submitted request contains missing or invalid required values'})

    is_successful, message = payment_repository.update_offline_payment(payment, current_user)
    if not is_successful:
        log.error(f'{fn}: Failed to complete {payment}: {message}')
        abort(400, {'message': 'Offline payment failed to process'})

    response = send_payment_receipt(payment.customer.email, payment)

    if not response.is_sent:
        log.error(f'{fn}: Receipt failed to send: {response.message} ({response.response or response.error})')
        abort(400, {'message': 'Payment receipt failed to send'})

    log.info(f'{fn}: Payment {payment} has been updated to PAID')
    return jsonify({'message': message}), 200


@payment_blueprint.route(
    '/merchants/<merchant_code>/payments/<payment_reference_id>/receipt/send',
    methods=['POST']
)
@authentication.jwt_required
@authentication.min_access_role(Roles.CUSTOMERSUPPORT)
def send_customer_payment_receipt(merchant_code: str, payment_reference_id: str):
    fn = 'send_customer_payment_receipt'
    current_user = g.user
    email = request.json['email']

    merchant = merchant_repository.find_merchant_by_code(merchant_code)
    if not merchant:
        abort(404, {'message': 'Merchant does not exist'})

    payment = payment_repository.find_payment_by_reference_id(payment_reference_id, merchant)
    if not payment:
        abort(404, {'message': 'Payment does not exist'})

    if payment.payment_status.id not in (1, 5):  # Indicates that transaction is not 'PAID' or 'SETTLED'
        log.error(f'{fn}: Payment status mismatch: {payment.payment_status.name}')
        abort(400, {'message': 'Payment cannot be completed due to incorrect status'})

    if not email:
        log.error(f'{fn}: No email address provided')
        abort(400, {'message': 'No email address provided'})

    # Get next scheduled invoice if the transaction type of the payment is ENROLLMENT
    next_invoice, remaining_months = payment_repository.get_next_scheduled_invoice(
        payment=payment) if payment.transaction_type.id == 20 else (None, 0)
    response = send_payment_receipt(email, payment, next_invoice, remaining_months)
    if not response.is_sent:
        log.error(f'{fn}: Receipt failed to send: {response.message} ({response.response or response.error})')
        abort(400, {'message': 'Payment receipt failed to send'})

    is_loaded, submitted_log = TransactionLog.validate_submitted_log({'content': f'Payment receipt sent to {email}'})
    if not is_loaded:
        log.error(f'{fn}: Validation error: {submitted_log}')
        abort(400, {'message': 'Submitted log contains missing or invalid required values'})

    is_added, message = transaction_log_repository.submit_log(
        transaction_id=payment.transaction_id,
        invoice_id=payment.invoice_id,
        submitted_log=submitted_log,
        submitted_by=current_user)

    if not is_added:
        log.error(f'{fn}: Log was not recorded > "{message}"')
        abort(400, {'message': 'Submitted log was not saved in the records. Please try again later.'})

    return jsonify({'message': 'Payment receipt sent successfully'}), 200


@payment_blueprint.route(
    '/merchants/<merchant_code>/payments/<payment_reference_id>/dispute',
    methods=['POST'])
@authentication.jwt_required
@authentication.min_access_role(Roles.CUSTOMERSUPPORT)
def dispute_payment(merchant_code: str, payment_reference_id: str):
    fn = 'dispute_payment'
    current_user = g.user

    merchant = merchant_repository.find_merchant_by_code(merchant_code)
    if not merchant:
        abort(404, {'message': 'Merchant does not exist'})

    payment = payment_repository.find_payment_by_reference_id(payment_reference_id, merchant)
    if not payment:
        abort(404, {'message': 'Payment does not exist'})

    if payment.payment_status.code not in ('PAID', 'SETTLED'):
        abort(400, {'message': 'Payment cannot be disputed'})

    dispute = dispute_repository.find_dispute_by_invoice_id(payment.invoice_id)
    if dispute:
        abort(400, {'message': 'Payment has an ongoing dispute'})

    new_dispute = Dispute()
    new_dispute.reference_id = generate_dispute_ref_id()
    new_dispute.invoice_id = payment.invoice_id
    new_dispute.reason = request.json['reason']

    dispute_id, is_disputed, message = dispute_repository.dispute_payment(
        dispute=new_dispute,
        payment=payment,
        disputed_by=current_user)
    if not is_disputed:
        log.error(f'{fn}: Failed to dispute {payment}: {message}')
        abort(400, {'message': 'Unable to dispute payment'})

    log.info(f'{fn}: Payment {payment} has been disputed')
    return jsonify({ 'message': message, 'disputeId': dispute_id }), 200


def _build_csv_on_payments(payments: list, tz_info: str, show_all=False) -> str:
    allowed_headers = [
        {'name': 'externalTransactionId', 'show_on_default': True},
        {'name': 'paymentReferenceId', 'show_on_default': True},
        {'name': 'invoiceReferenceId', 'show_on_default': True},
        {'name': 'enrollmentReferenceId', 'show_on_default': True},
        {'name': 'settlementReferenceId', 'show_on_default': True},
        {'name': 'merchantCode', 'show_on_default': False},
        {'name': 'merchantName', 'show_on_default': False},
        {'name': 'transactionStatus', 'show_on_default': True},
        {'name': 'paymentStatus', 'show_on_default': True},
        {'name': 'transactionType', 'show_on_default': True},
        {'name': 'customerName', 'show_on_default': True},
        {'name': 'customerEmail', 'show_on_default': True},
        {'name': 'customerPhone', 'show_on_default': True},
        {'name': 'clientNotes', 'show_on_default': True},
        {'name': 'projectName', 'show_on_default': True},
        {'name': 'projectCategory', 'show_on_default': True},
        {'name': 'baseCurrency', 'show_on_default': True},
        {'name': 'baseAmount', 'show_on_default': True},
        {'name': 'convertedCurrency', 'show_on_default': True},
        {'name': 'convertedAmount', 'show_on_default': True},
        {'name': 'feeCurrency', 'show_on_default': True},
        {'name': 'feeAmount', 'show_on_default': True},
        {'name': 'totalCurrency', 'show_on_default': True},
        {'name': 'totalAmount', 'show_on_default': True},
        {'name': 'waivedFeeCurrency', 'show_on_default': True},
        {'name': 'waivedFeeAmount', 'show_on_default': True},
        {'name': 'netCurrency', 'show_on_default': True},
        {'name': 'netAmount', 'show_on_default': True},
        {'name': 'paymentType', 'show_on_default': True},
        {'name': 'paymentMethodType', 'show_on_default': True},
        {'name': 'paymentMethodName', 'show_on_default': True},
        {'name': 'paymentMethodStatus', 'show_on_default': False},
        {'name': 'paymentMethodProvider', 'show_on_default': False},
        {'name': 'paymentMethodProcessor', 'show_on_default': False},
        {'name': 'paymentMethodExpiry', 'show_on_default': False},
        {'name': 'paymentMethodOrigin', 'show_on_default': False},
        {'name': 'paymentMethodIssuer', 'show_on_default': False},
        {'name': 'transactionSource', 'show_on_default': True},
        {'name': 'settledDate', 'show_on_default': True},
        {'name': 'createdAt', 'show_on_default': True},
        {'name': 'paidAt', 'show_on_default': True},
        {'name': 'dueAt', 'show_on_default': True},
        {'name': 'reportAt', 'show_on_default': True},
    ]
    custom_field_headers = list(set([
        cf['name'] for p in payments for cf in p.custom_fields_list()
    ]))
    headers = [
        h['name'] for h in allowed_headers if show_all or h['show_on_default']
    ] + custom_field_headers

    serialized_data = [p.serialize(is_export=True, with_custom_fields=True, tz_info=tz_info) for p in payments]
    df = pd.DataFrame(serialized_data, columns=headers)

    # Uses buffer instead of file on to_csv
    #   pandas has good built-in escape for exporting CSV
    buf = StringIO()
    df.to_csv(path_or_buf=buf, index=False)
    value = buf.getvalue()
    buf.close()
    return value
