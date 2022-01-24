from flask import Blueprint, request, jsonify, abort, g
from server.config.logger import log
from server.config.authentication import authentication
from server.models.search_option_model import SearchOption
from server.models.person_model import Roles, MerchantRoles
from server.models.transaction_log_model import TransactionLog
from server.repositories import (
    transaction_log_repository,
    enrollment_repository,
    payment_repository
)

log_blueprint = Blueprint('log', __name__)


@log_blueprint.route('/logs/<transaction_id>', defaults={'invoice_id': None}, methods=['GET'])
@log_blueprint.route('/logs/<transaction_id>/invoices/<invoice_id>', methods=['GET'])
@authentication.jwt_required
@authentication.min_system_access_role(Roles.USER)
def get_logs(transaction_id: str, invoice_id: str):
    current_user = g.user
    i_transaction_id = int(transaction_id)
    i_invoice_id = int(invoice_id) if invoice_id else None

    if not invoice_id:
        enrollment = enrollment_repository.find_enrollment_by_transaction_id(i_transaction_id)
        if not g.user.is_internal() and enrollment.merchant.merchant_code not in g.user.scopes:
            abort(403, {'message': 'You are not allowed to get on this method'})

    else:
        payment = payment_repository.find_payment_by_invoice_id(i_invoice_id)
        if not g.user.is_internal() and payment.merchant.merchant_code not in g.user.scopes:
            abort(403, {'message': 'You are not allowed to get on this method'})

    search_option = SearchOption.map_from_query(request.args)
    logs, total_count = transaction_log_repository.get_logs(
        transaction_id=i_transaction_id,
        invoice_id=i_invoice_id,
        search_option=search_option)

    serialized_logs = [
        log.serialize(show_metadata=current_user.is_internal()) for log in logs
    ]

    return jsonify({
        'logs': serialized_logs,
        'totalCount': total_count
    }), 200


@log_blueprint.route('/logs/<transaction_id>', defaults={'invoice_id': None}, methods=['POST'])
@log_blueprint.route('/logs/<transaction_id>/invoices/<invoice_id>', methods=['POST'])
@authentication.jwt_required
@authentication.min_system_access_role(Roles.USER)
def submit_log(transaction_id: str, invoice_id: str):
    current_user = g.user
    fn = 'submit_log'
    try:
        i_transaction_id = int(transaction_id)
        i_invoice_id = int(invoice_id) if invoice_id else None

        if not invoice_id:
            enrollment = enrollment_repository.find_enrollment_by_transaction_id(i_transaction_id)
            if not g.user.is_internal() and enrollment.merchant.merchant_code not in g.user.scopes:
                abort(403, {'message': 'You are not allowed to get on this method'})

        else:
            payment = payment_repository.find_payment_by_invoice_id(i_invoice_id)
            if not g.user.is_internal() and payment.merchant.merchant_code not in g.user.scopes:
                abort(403, {'message': 'You are not allowed to get on this method'})

        is_loaded, submitted_log = TransactionLog.validate_submitted_log(request.json)
        if not is_loaded:
            log.error(f'{fn}: Validation error: {submitted_log}')
            abort(400, {'message': 'Submitted log contains missing or invalid required values'})

        is_added, message = transaction_log_repository.submit_log(
            transaction_id=i_transaction_id,
            invoice_id=i_invoice_id,
            submitted_log=submitted_log,
            submitted_by=current_user)
        if not is_added:
            log.error(f'{fn}: Log was not recorded > "{message}"')
            abort(400, {'message': 'Submitted log was not saved in the records. Please try again later.'})

        return jsonify({'message': 'Submitted log has been saved'}), 201
    except TypeError as type_error:
        log.error(f'{fn}: Type error on arguments upon submit: {type_error}')
        abort(400, {'message': 'Submitted transaction log is not valid.'})


@log_blueprint.route('/logs/<transaction_id>/logs/<log_id>', defaults={'invoice_id': None}, methods=['DELETE'])
@log_blueprint.route('/logs/<transaction_id>/invoices/<invoice_id>/logs/<log_id>', methods=['DELETE'])
@authentication.jwt_required
@authentication.min_system_access_role(Roles.USER)
def remove_log(transaction_id: str, invoice_id: str, log_id: str):
    current_user = g.user
    fn = 'remove_log'
    try:
        i_transaction_id = int(transaction_id)
        i_invoice_id = int(invoice_id) if invoice_id else None

        if not invoice_id:
            enrollment = enrollment_repository.find_enrollment_by_transaction_id(i_transaction_id)
            if not g.user.is_internal() and enrollment.merchant.merchant_code not in g.user.scopes:
                abort(403, {'message': 'You are not allowed to get on this method'})

        else:
            payment = payment_repository.find_payment_by_invoice_id(i_invoice_id)
            if not g.user.is_internal() and payment.merchant.merchant_code not in g.user.scopes:
                abort(403, {'message': 'You are not allowed to get on this method'})

        log_id_as_int = int(log_id)
        search_option = SearchOption.map_from_query({'page': 1, 'size': 1000})
        logs, _ = transaction_log_repository.get_logs(
            transaction_id=i_transaction_id,
            invoice_id=i_invoice_id,
            search_option=search_option)

        found_log = next((log for log in logs if log.log_id == log_id_as_int), None)
        if not found_log:
            log.error(f'{fn}: Log does not exist')
            abort(404, {'message': 'Transaction log does not exist'})

        if not current_user.is_internal() and found_log.created_by_id != current_user.id:
            log.error(f'{fn}: User {current_user} attempts to remove this log: {log}')
            abort(403, {'message': 'You are not allowed to remove this log'})

        # System logs should not be removed.
        if found_log.action_name or found_log.action_status:
            log.error(f'{fn}: User {current_user} attempts to remove system log: {log}')
            abort(403, {'message': 'You are not allowed to remove this log'})

        is_removed, message = transaction_log_repository.remove_log(found_log, current_user)
        if not is_removed:
            log.error(f'{fn}: Log #{log_id} was not removed > "{message}"')
            abort(400, {'message': 'Log was not removed in the records. Please try again later.'})

        return jsonify({'message': 'Log has been removed'}), 200

    except TypeError as terr:
        log.error(f'{fn}: Log #{log_id} was not removed > Exception "{terr}"')
        abort(400, {'message': 'Log was not removed in the records.'})
