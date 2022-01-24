""" server.controllers.settlement_controller """
# pylint: disable=unused-argument
from flask import Blueprint, jsonify, abort, g, request

from dateutil import parser
from server.config import s3
from server.config.logger import log
from server.config.authentication import authentication
from server.repositories import settlement_repository, merchant_repository, person_repository, payment_repository
from server.models.settlement_model import SettlementFile, Settlement
from server.models.person_model import Roles, MerchantRoles
from server.models.search_option_model import SearchOption
from server.utilities import garnish, helper, emails

settlement_blueprint = Blueprint('settlement', __name__)

base_url = '/merchants/<int:merchant_id>/settlements'


@settlement_blueprint.route('/settlements', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_role(Roles.CUSTOMERSUPPORT)
def search_settlements():
    search_option = SearchOption.map_from_query(request.args)
    settlements, total_count = settlement_repository.search_settlements(search_option)

    serialized_settlements = [s.serialize() for s in settlements]
    return jsonify({
        'settlements': serialized_settlements,
        'totalCount': total_count
    }), 200


@settlement_blueprint.route('/settlements/<settlement_id>', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_role(Roles.CUSTOMERSUPPORT)
def find_settlement_by_id(settlement_id: str):
    fn = 'find_settlement_by_id'
    try:
        valid_settlement_id = int(settlement_id)
        settlement = settlement_repository.find_settlement_by_id(valid_settlement_id)

        if not settlement:
            abort(404, {'message': 'Settlement does not exist'})

        return jsonify(settlement.serialize()), 200

    except (ValueError, TypeError) as value_error:
        log.error(f'{fn}: {value_error} on settlement_id: {settlement_id}')
        abort(404, {'message': 'Settlement does not exist'})


@settlement_blueprint.route(base_url, methods=['GET'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_STAFF)
def get_settlements(merchant_id: int):
    merchant = g.merchant

    search_option = SearchOption.map_from_query(request.args)
    settlements, total_count = settlement_repository.get_merchant_settlements(merchant, search_option)

    serialized_settlements = [s.serialize() for s in settlements]
    return jsonify({
        'settlements': serialized_settlements,
        'totalCount': total_count
    }), 200

@settlement_blueprint.route(f'{base_url}/<settlement_reference_id>', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_STAFF)
def get_settlement(merchant_id: int, settlement_reference_id: str):
    merchant = g.merchant

    settlement = settlement_repository.find_settlement_by_reference_id(settlement_reference_id)
    if not settlement:
        abort(404, {'message': 'Settlement report not found.'})

    if merchant.merchant_id != settlement.merchant.merchant_id:
        abort(404, {'message': 'Settlement report not found.'})

    current_user = g.user
    if not current_user.is_internal() and settlement.merchant.merchant_code not in current_user.scopes:
        abort(403, {'message': 'You are not allowed to get settlements for this merchant.'})

    serialized_settlement = settlement.serialize()
    return jsonify(serialized_settlement), 200

@settlement_blueprint.route(base_url, methods=['POST'])
@authentication.jwt_required
@authentication.min_system_access_role(Roles.CUSTOMERSUPPORT)
def create_settlement(merchant_id: int):
    fn = 'create_settlement'
    current_user = g.user
    merchant = merchant_repository.find_merchant_by_id(merchant_id)
    if not merchant:
        abort(404, {'message': 'Merchant does not exist'})

    if not current_user.is_internal() and merchant.merchant_code not in current_user.scopes:
        abort(403, {'message': 'You are not allowed to create settlements for this merchant'})

    request_body = request.get_json()
    validation_error, settlement_data = Settlement.validate(request_body=request_body)
    if validation_error:
        log.error(f'{fn}: Settlement validation error => {validation_error}')
        abort(400, {'message': 'The submitted settlement is not valid'})

    if settlement_data.are_invoices_unique():
        log.error(f'{fn}: Settlement payments have duplicates {settlement_data.invoice_ids}')
        abort(400, {'message': 'The payments on the settlement report have duplicate items'})

    settlement_file = settlement_repository.find_settlement_file_by_id(
        merchant=merchant,
        settlement_file_id=settlement_data.settlement_file_id)
    if not settlement_file or settlement_file.deleted_at:
        abort(404, {'message': 'The submitted settlement file does not exist'})

    if settlement_file.merchant != merchant:
        abort(403, {'message': 'You are forbidden to use this settlement file'})

    is_created, message, settlement_id, reference_id = settlement_repository.create_settlement(
        merchant=merchant,
        settlement_data=settlement_data,
        settlement_file=settlement_file,
        settled_by=current_user)
    if not is_created:
        log.error(f'{fn}: Settlement report not created {str(current_user)} > {message}')
        abort(400, {'message': message})

    users, total_merchant_count = person_repository.get_merchant_admins_with_notifications_by_merchant_id(merchant)
    serialized_users = [p.serialize() for p in users]
    merchant_admins_emails = [item['email'] for item in serialized_users]

    payments, total_payment_count = payment_repository.get_settled_payments(merchant, reference_id)
    serialized_payments = [p.serialize(is_compact=True) for p in payments]

    for item in serialized_payments:
        parsed_created_at = parser.parse(item['createdAt'])
        item['createdAt'] = parsed_created_at.strftime("%b %d, %Y %I:%M:%S %p")

    emails.send_settlement_report_email(
        merchant_admins_emails,
        serialized_payments,
        total_payment_count,
        total_merchant_count)

    log.info(f'{fn}: Settlement #{settlement_id} - {reference_id} has been created by {str(current_user)}')
    return jsonify({
        'message': 'Settlement report has been created',
        'settlementId': settlement_id,
        'referenceId': reference_id
    }), 201

@settlement_blueprint.route(f'{base_url}/<settlement_reference_id>', methods=['DELETE'])
@authentication.jwt_required
@authentication.min_system_access_role(Roles.CUSTOMERSUPPORT)
def delete_settlement(merchant_id: int, settlement_reference_id: str):
    fn = 'delete_settlement'
    current_user = g.user
    merchant = merchant_repository.find_merchant_by_id(merchant_id)
    if not merchant:
        abort(404, {'message': 'Merchant does not exist'})

    if not current_user.is_internal() and merchant.merchant_code not in current_user.scopes:
        abort(403, {'message': 'You are not allowed to delete settlements for this merchant.'})

    settlement = settlement_repository.find_settlement_by_reference_id(
        reference_id=settlement_reference_id)
    if not settlement:
        abort(404, {'message': 'Settlement report does not exist'})

    if settlement.merchant.merchant_id != merchant.merchant_id:
        abort(403, {'message': 'Settlement report belongs to another merchant'})

    is_removed, message = settlement_repository.delete_settlement(
        settlement=settlement,
        deleted_by=current_user)
    if not is_removed:
        log.error(f'{fn}: Cannot remove the settlement [{settlement}]: {message}')
        abort(404, {'message': 'Settlement report has not been removed'})

    return jsonify(), 204

@settlement_blueprint.route(f'{base_url}/files/upload/presigned-url', methods=['POST'])
@authentication.jwt_required
@authentication.min_system_access_role(Roles.CUSTOMERSUPPORT)
@garnish.require_json_body(['filename', 'contentType', 'contentLength'])
def get_presigned_upload_url(merchant_id: int):
    merchant = merchant_repository.find_merchant_by_id(merchant_id)
    if not merchant:
        abort(404, {'message': 'Merchant does not exist'})

    request_body = request.get_json()
    presigned_data = s3.get_presigned_upload_url(
        merchant=merchant,
        filename=request_body.get('filename'),
        metadata={
            'contentType': request_body.get('contentType'),
            'contentLength': request_body.get('contentLength')
        })

    if not presigned_data:
        abort(400, {'message': 'The server presigned URL was not generated'})

    parsed_url = presigned_data.parse_url()
    file_url = f'{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}'
    return jsonify({
        'presignedUrl': presigned_data.url,
        'bucket': presigned_data.bucket_name,
        'directory': presigned_data.file_directory,
        'uniqueIdentifier': presigned_data.unique_identifier,
        'url': file_url,
        'scheme': parsed_url.scheme,
        'domain': parsed_url.netloc,
    }), 200


@settlement_blueprint.route(f'{base_url}/files/<settlement_file_id>/presigned-url', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_AGENT)
def get_presigned_download_url(merchant_id: int, settlement_file_id: str):
    fn = 'get_presigned_download_url'
    merchant = g.merchant

    sf_id = helper.get_id_as_int(settlement_file_id)
    if sf_id < 0:
        log.error(f'{fn}: Settlement file ID is not valid')
        abort(404, {'message': 'Settlement file does not exist'})

    settlement_file = settlement_repository.find_settlement_file_by_id(
        merchant=merchant,
        settlement_file_id=sf_id)
    if not settlement_file:
        log.error(f'{fn}: Settlement file does not exist')
        abort(404, {'message': 'Settlement file does not exist'})

    presigned_url = s3.get_presigned_download_url(file=settlement_file)
    if not presigned_url:
        log.error(f'{fn}: Presigned URL was not generated for {settlement_file}')
        abort(400, {'message': 'Presigned url is not generated for this file'})

    log.info(f'{fn}: Presigned URL generated for {settlement_file}')

    serialized_data = settlement_file.serialize(presigned_url.url)
    return jsonify(serialized_data), 200


@settlement_blueprint.route(f'{base_url}/files', methods=['POST'])
@authentication.jwt_required
@authentication.min_system_access_role(Roles.CUSTOMERSUPPORT)
def add_settlement_file(merchant_id: int):
    fn = 'add_settlement_file'
    merchant = merchant_repository.find_merchant_by_id(merchant_id)
    if not merchant:
        abort(404, {'message': 'Merchant does not exist'})

    request_body = request.get_json()
    validation_error, settlement_file = SettlementFile.validate(
        merchant=merchant,
        request_body=request_body)
    if validation_error:
        log.error(f'{fn}: Settlement file validation error {validation_error}')
        abort(400, {'message': 'Settlement file is not valid'})

    is_saved, save_message, settlement_file_id = settlement_repository.add_settlement_file(
        settlement_file=settlement_file)
    if not is_saved:
        log.error(f'{fn}: Cannot save settlement file for [{merchant}]: {save_message}')
        abort(400, {'message': 'Settlement file has not been saved'})

    return jsonify({
        'settlementFileId': settlement_file_id,
        'merchantCode': merchant.merchant_code,
        'uniqueIdentifier': settlement_file.unique_identifier,
        'fileUrl': settlement_file.s3_file_url,
        'message': 'Settlement file has been saved'
    }), 201
