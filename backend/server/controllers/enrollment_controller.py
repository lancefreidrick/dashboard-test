""" server.controllers.enrollment_controller """
# pylint: disable=unused-argument
from io import StringIO
from datetime import datetime
import pandas as pd
from flask import Blueprint, jsonify, abort, g, request, Response
from server.config.logger import log
from server.config.authentication import authentication
from server.models.search_option_model import SearchOption
from server.models.person_model import Roles, MerchantRoles
from server.utilities.context_manager import open_transaction_context, ContextStatus
from server.repositories import merchant_repository, enrollment_repository
from server.utilities import garnish


enrollment_blueprint = Blueprint('enrollment', __name__)


@enrollment_blueprint.route('/enrollments', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_role(Roles.CUSTOMERSUPPORT)
def search_enrollments():
    search_option = SearchOption.map_from_query(request.args)
    enrollments, total_count = enrollment_repository.search_enrollments(search_option)

    serialized_enrollments = [p.serialize(is_compact=True) for p in enrollments]
    return jsonify({
        'enrollments': serialized_enrollments,
        'totalCount': total_count,
        'page': search_option.page,
        'size': search_option.size
    }), 200


@enrollment_blueprint.route('/enrollments/export', methods=['GET'])
def export_enrollments():
    export_token = request.args.get('token')
    is_success, current_user = authentication.validate_export_token(export_token)
    if not is_success:
        abort(401, {'message': 'Unauthorized to export enrollments'})

    if not current_user.is_internal():
        abort(403, {'message': 'You are not allowed to export these payments'})

    # The current export limit is 10,000 records
    search_option = SearchOption.map_from_query(request.args)
    search_option.page = 1
    search_option.size = 10000

    with open_transaction_context(user=current_user, source='enrollments') as context:
        context.propset(action='Export')
        enrollments, total_count = enrollment_repository.search_enrollments(search_option)

        csv_content = _build_csv_on_enrollments(enrollments, True)
        filename = 'enrollments-{}.csv'.format(datetime.now().strftime('%Y-%m-%d'))

        context.propset(
            status=ContextStatus.SUCCESS,
            description='Exported enrollments',
            metadata={
                'page': search_option.page,
                'size': search_option.size,
                'status': search_option.status,
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
        response.headers['Content-Disposition'] = f'filename="{filename}"'
        return response


@enrollment_blueprint.route('/enrollments/<transaction_id>', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_role(Roles.CUSTOMERSUPPORT)
def get_enrollment_by_transaction_id(transaction_id: str):
    fn = 'get_enrollment_by_transaction_id'
    try:
        enrollment_transaction_id = int(transaction_id)
        payment = enrollment_repository.find_enrollment_by_transaction_id(enrollment_transaction_id)

        if not payment:
            abort(404, {'message': 'Enrollment does not exist'})

        return jsonify(payment.serialize(with_custom_fields=True)), 200
    except ValueError as value_error:
        log.error(f'{fn}: {value_error} on transaction_id: {transaction_id}')
        abort(404, {'message': 'Enrollment does not exist'})
    except TypeError as type_error:
        log.error(f'{fn}: {type_error} on transaction_id: {transaction_id}')
        abort(404, {'message': 'Enrollment does not exist'})


@enrollment_blueprint.route('/merchants/<int:merchant_id>/enrollments', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_AGENT)
def get_merchant_enrollments(merchant_id: int):
    merchant = g.merchant

    search_option = SearchOption.map_from_query(request.args)
    enrollments, total_count = enrollment_repository.get_merchant_enrollments(merchant, search_option)

    serialized_enrollments = [e.serialize(is_compact=True) for e in enrollments]
    return jsonify({
        'enrollments': serialized_enrollments,
        'totalCount': total_count,
        'page': search_option.page,
        'size': search_option.size
    }), 200


@enrollment_blueprint.route('/merchants/<int:merchant_id>/enrollments/<external_transaction_id>', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_AGENT)
def get_merchant_enrollment_by_external_transaction_id(merchant_id: int, external_transaction_id: str):
    merchant = g.merchant

    enrollment = enrollment_repository.find_merchant_enrollment_by_external_transaction_id(external_transaction_id,
                                                                                           merchant)
    if not enrollment:
        abort(404, {'message': 'Enrollment does not exist'})

    return jsonify(enrollment.serialize()), 200


@enrollment_blueprint.route(
    '/merchants/<int:merchant_id>/enrollments/<enrollment_reference_id>/invoices', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_AGENT)
def get_enrollment_invoices(merchant_id: int, enrollment_reference_id: str):
    merchant = g.merchant

    enrollment = enrollment_repository.find_enrollment_by_reference_id(enrollment_reference_id, merchant)
    if not enrollment:
        abort(404, {'message': 'Enrollment does not exist'})

    search_option = SearchOption.map_from_query(request.args)
    (invoices, total_count) = enrollment_repository.get_enrollment_invoices(enrollment, search_option)
    serialized_invoices = [i.serialize() for i in invoices]
    return jsonify({
        'invoices': serialized_invoices,
        'totalCount': total_count,
    }), 200


@enrollment_blueprint.route('/merchants/<merchant_code>/enrollments/export', methods=['GET'])
def export_merchant_enrollments(merchant_code: str):
    export_token = request.args.get('token')
    merchant = merchant_repository.find_merchant_by_code(merchant_code)
    if not merchant:
        abort(404, {'message': 'Merchant does not exist'})

    is_success, current_user = authentication.validate_export_token(export_token)
    if not is_success:
        abort(401, {'message': 'Unauthorized to export enrollments'})

    if not current_user.is_internal() and merchant.merchant_code not in current_user.scopes:
        abort(403, {'message': 'You are not allowed to export enrollments'})

    # The current export limit is 10,000 records
    search_option = SearchOption.map_from_query(request.args)
    search_option.page = 1
    search_option.size = 10000

    with open_transaction_context(user=current_user, source='enrollments') as context:
        context.propset(action='Export')
        enrollments, total_count = enrollment_repository.get_merchant_enrollments(merchant, search_option)

        csv_content = _build_csv_on_enrollments(enrollments, False)
        filename = 'enrollments-{}.csv'.format(datetime.now().strftime('%Y-%m-%d'))

        context.propset(
            status=ContextStatus.SUCCESS,
            description=f'Exported enrollments from {merchant.merchant_code}',
            metadata={
                'merchant': merchant.merchant_code,
                'page': search_option.page,
                'size': search_option.size,
                'status': search_option.status,
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
        response.headers['Content-Disposition'] = f'filename="{filename}"'
        return response


@enrollment_blueprint.route(
    '/merchants/<int:merchant_id>/enrollments/<enrollment_reference_id>/approve', methods=['POST'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_ADMIN)
def approve_enrollment(merchant_id: int, enrollment_reference_id: str):
    fn = 'approve_enrollment'
    current_user = g.user
    merchant = g.merchant

    with open_transaction_context(user=current_user, source='enrollments') as context:
        context.propset(action='Approve enrollment')
        enrollment = enrollment_repository.find_enrollment_by_reference_id(
            enrollment_reference_id=enrollment_reference_id,
            merchant=merchant)
        if not enrollment:
            context.propset(
                status=ContextStatus.ERROR,
                description='Failed to approve enrollment. It does not exist',
                metadata={'merchant': merchant.merchant_code})
            abort(404, {'message': 'Enrollment does not exist'})

        if enrollment.transaction_status.code != 'FOR REVIEW':
            context.propset(
                status=ContextStatus.ERROR,
                description=f'Failed to approve {enrollment}. Status is not FOR REVIEW',
                metadata={
                    'merchant': merchant.merchant_code,
                    'status': enrollment.transaction_status.code,
                    'externalTransactionId': enrollment.external_transaction_id,
                    'referenceId': enrollment.transaction_reference_id
                })
            abort(400, {'message': 'Enrollment status is not for review'})

        is_approved, message = enrollment_repository.approve_enrollment(
            enrollment=enrollment,
            approved_by=current_user,
            merchant=merchant)
        if not is_approved:
            log.error(f'{fn}: Approving {enrollment} has failed => {message}')
            context.propset(
                status=ContextStatus.ERROR,
                description=f'Failed to approve {enrollment}: {message}',
                metadata={
                    'merchant': merchant.merchant_code,
                    'status': enrollment.transaction_status.code,
                    'externalTransactionId': enrollment.external_transaction_id,
                    'referenceId': enrollment.transaction_reference_id
                })
            return abort(400, {'message': 'Enrollment has not been approved'})

        context.propset(
            status=ContextStatus.SUCCESS,
            description=f'{enrollment} has been approved',
            metadata={
                'merchant': merchant.merchant_code,
                'status': enrollment.transaction_status.code,
                'externalTransactionId': enrollment.external_transaction_id,
                'referenceId': enrollment.transaction_reference_id
            })
        log.info(f'{fn}: {enrollment} has been approved')
        return jsonify({'message': 'Enrollment has been approved'}), 200


@enrollment_blueprint.route(
    '/merchants/<int:merchant_id>/enrollments/<enrollment_reference_id>/decline', methods=['POST'])
@garnish.require_json_body(['comment'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_ADMIN)
def decline_enrollment(merchant_id: int, enrollment_reference_id: str):
    fn = 'decline_enrollment'
    current_user = g.user
    merchant = g.merchant
    with open_transaction_context(user=current_user, source='enrollments') as context:
        context.propset(action='Decline enrollment')
        enrollment = enrollment_repository.find_enrollment_by_reference_id(
            enrollment_reference_id=enrollment_reference_id,
            merchant=merchant)
        if not enrollment:
            context.propset(
                status=ContextStatus.ERROR,
                description='Failed to decline enrollment. It does not exist',
                metadata={'merchant': merchant.merchant_code})
            abort(404, {'message': 'Enrollment does not exist'})

        if enrollment.transaction_status.code != 'FOR REVIEW':
            context.propset(
                status=ContextStatus.ERROR,
                description=f'Failed to decline {enrollment}. Status is not FOR REVIEW',
                metadata={
                    'merchant': merchant.merchant_code,
                    'status': enrollment.transaction_status.code,
                    'externalTransactionId': enrollment.external_transaction_id,
                    'referenceId': enrollment.transaction_reference_id
                })
            abort(400, {'message': 'Enrollment status is not for review'})

        form = request.get_json()
        is_declined, message = enrollment_repository.decline_enrollment(
            enrollment=enrollment,
            merchant=merchant,
            declined_by=current_user,
            comment=form.get('comment'))
        if not is_declined:
            log.error(f'{fn}: Failed to decline {enrollment}: {message}')
            context.propset(
                status=ContextStatus.ERROR,
                description=f'Failed to decline {enrollment}: {message}',
                metadata={
                    'merchant': merchant.merchant_code,
                    'status': enrollment.transaction_status.code,
                    'externalTransactionId': enrollment.external_transaction_id,
                    'referenceId': enrollment.transaction_reference_id
                })
            return abort(400, {'message': 'Enrollment has not been declined'})

        context.propset(
            status=ContextStatus.SUCCESS,
            description=f'{enrollment} has been declined',
            metadata={
                'merchant': merchant.merchant_code,
                'status': enrollment.transaction_status.code,
                'externalTransactionId': enrollment.external_transaction_id,
                'referenceId': enrollment.transaction_reference_id
            })
        log.info(f'{fn}: {enrollment} has been declined')
        return jsonify({'message': 'Enrollment has been declined'}), 200


@enrollment_blueprint.route(
    '/merchants/<int:merchant_id>/enrollments/<enrollment_reference_id>/cancel', methods=['POST'])
@garnish.require_json_body(['comment'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_ADMIN)
def cancel_enrollment(merchant_id: int, enrollment_reference_id: str):
    fn = 'cancel_enrollment'
    current_user = g.user
    merchant = g.merchant

    with open_transaction_context(user=current_user, source='enrollments') as context:
        context.propset(action='Cancel enrollment')
        enrollment = enrollment_repository.find_enrollment_by_reference_id(
            enrollment_reference_id=enrollment_reference_id,
            merchant=merchant)
        if not enrollment:
            context.propset(
                status=ContextStatus.ERROR,
                description='Failed to cancel enrollment. It does not exist',
                metadata={'merchant': merchant.merchant_code})
            abort(404, {'message': 'Enrollment does not exist'})

        if enrollment.transaction_status.code != 'ONGOING':
            context.propset(
                status=ContextStatus.ERROR,
                description=f'Failed to cancel {enrollment}. Status is not ONGOING',
                metadata={
                    'merchant': merchant.merchant_code,
                    'status': enrollment.transaction_status.code,
                    'externalTransactionId': enrollment.external_transaction_id,
                    'referenceId': enrollment.transaction_reference_id
                })
            abort(400, {'message': 'Enrollment is already completed or terminated'})

        form = request.get_json()
        is_canceled, message = enrollment_repository.cancel_enrollment(
            enrollment=enrollment,
            merchant=merchant,
            cancelled_by=current_user,
            comment=form.get('comment'))
        if not is_canceled:
            log.error(f'{fn}: Cancelling {enrollment} has failed => {message}')
            context.propset(
                status=ContextStatus.ERROR,
                description=f'Failed to cancel {enrollment}: {message}',
                metadata={
                    'merchant': merchant.merchant_code,
                    'status': enrollment.transaction_status.code,
                    'externalTransactionId': enrollment.external_transaction_id,
                    'referenceId': enrollment.transaction_reference_id
                })
            return abort(400, {'message': 'Enrollment has not been cancelled'})

        context.propset(
            status=ContextStatus.SUCCESS,
            description=f'{enrollment} has been cancelled',
            metadata={
                'merchant': merchant.merchant_code,
                'status': enrollment.transaction_status.code,
                'externalTransactionId': enrollment.external_transaction_id,
                'referenceId': enrollment.transaction_reference_id
            })
        log.info(f'{fn}: {enrollment} has been cancelled')
        return jsonify({'message': 'Enrollment has been cancelled'}), 200


def _build_csv_on_enrollments(enrollments: list, show_all=False) -> str:
    allowed_headers = [
        {'name': 'externalTransactionId', 'show_on_default': True},
        {'name': 'enrollmentReferenceId', 'show_on_default': True},
        {'name': 'transactionType', 'show_on_default': True},
        {'name': 'transactionStatus', 'show_on_default': True},
        {'name': 'merchantCode', 'show_on_default': False},
        {'name': 'merchantName', 'show_on_default': False},
        {'name': 'projectName', 'show_on_default': True},
        {'name': 'baseAmount', 'show_on_default': True},
        {'name': 'baseCurrency', 'show_on_default': True},
        {'name': 'paymentType', 'show_on_default': True},
        {'name': 'customerName', 'show_on_default': True},
        {'name': 'customerEmail', 'show_on_default': True},
        {'name': 'customerPhone', 'show_on_default': True},
        {'name': 'paymentMethodType', 'show_on_default': True},
        {'name': 'paymentMethodName', 'show_on_default': True},
        {'name': 'paymentMethodStatus', 'show_on_default': False},
        {'name': 'paymentMethodProvider', 'show_on_default': False},
        {'name': 'paymentMethodProcessor', 'show_on_default': False},
        {'name': 'paymentMethodExpiry', 'show_on_default': False},
        {'name': 'paymentMethodOrigin', 'show_on_default': False},
        {'name': 'paymentMethodIssuer', 'show_on_default': False},
        {'name': 'transactionSource', 'show_on_default': True},
        {'name': 'enrollmentMonths', 'show_on_default': True},
        {'name': 'enrollmentStartDate', 'show_on_default': True},
        {'name': 'enrollmentEndDate', 'show_on_default': True},
        {'name': 'createdAt', 'show_on_default': True}
    ]
    custom_field_headers = list(set([
       cf['name'] for e in enrollments for cf in e.custom_fields_list()
    ]))
    headers = [
        h['name'] for h in allowed_headers if show_all or h['show_on_default']
    ] + custom_field_headers

    serialized_data = [e.serialize(is_export=True, with_custom_fields=True) for e in enrollments]
    df = pd.DataFrame(serialized_data, columns=headers)

    # Uses buffer instead of file on to_csv
    #   pandas has good built-in escape for exporting CSV
    buf = StringIO()
    df.to_csv(path_or_buf=buf, index=False)
    value = buf.getvalue()
    buf.close()
    return value
