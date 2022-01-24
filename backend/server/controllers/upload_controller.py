from flask import request, jsonify, Blueprint, abort
from server.config import s3
from server.config.authentication import authentication
from server.repositories import file_upload_repository
from server.models.person_model import Roles, MerchantRoles
from server.utilities import garnish

upload_blueprint = Blueprint('upload', __name__)


@upload_blueprint.route('/files/presigned-url/upload', methods=['GET'])
@authentication.jwt_required
@authentication.min_system_access_role(Roles.CUSTOMERSUPPORT)
@garnish.require_query_params(['directory', 'filename', 'content_type'])
def get_presigned_upload_url():
    directory = request.args.get('directory')
    filename = request.args.get('filename')
    content_type = request.args.get('content_type')

    presigned_url = s3.get_presigned_upload_url(directory, filename, content_type)
    return jsonify({'presigned_url': presigned_url}), 200


@upload_blueprint.route('/files', methods=['POST'])
@authentication.jwt_required
@authentication.min_system_access_role(Roles.CUSTOMERSUPPORT)
@garnish.require_json_body(['directory', 'filename', 'content_type'])
def record_file_upload():
    form = request.get_json()
    directory = form.get('directory')
    filename = form.get('filename')
    content_type = form.get('content_type')
    settlement_id = form.get('settlement_id')

    (is_uploaded, result) = file_upload_repository.create_settlement_file(
        directory,
        filename,
        content_type,
        int(settlement_id)
    )
    if not is_uploaded:
        abort(400, {'message': result})

    file_upload = file_upload_repository.find_settlement_file_by_id(int(result))
    presigned_url = s3.get_presigned_download_url(directory, filename)

    return jsonify({'presigned_download_url': presigned_url, 'file_upload': file_upload.serialize()}), 200


@upload_blueprint.route('/files/presigned-url/download/<settlement_file_id>', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_role(Roles.USER, MerchantRoles.MERCHANT_ADMIN)
def get_presigned_download_url(settlement_file_id: str):
    f = file_upload_repository.find_settlement_file_by_id(int(settlement_file_id))
    presigned_url = s3.get_presigned_download_url(f.directory, f.filename)

    return jsonify({'presigned_url': presigned_url, 'file_upload': f.serialize()}), 200


@upload_blueprint.route('/files/<settlement_file_id>', methods=['DELETE'])
@authentication.jwt_required
@authentication.min_system_access_role(Roles.CUSTOMERSUPPORT)
def delete_file_reference(settlement_file_id: str):
    (is_removed, message) = file_upload_repository.delete_settlement_file_by_id(int(settlement_file_id))
    if not is_removed:
        abort(404, {'message': 'Unable to delete settlement file.'})

    return jsonify({'message': message}), 200
