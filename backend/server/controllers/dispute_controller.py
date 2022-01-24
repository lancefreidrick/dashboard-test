from flask import jsonify, Blueprint, request, abort, g

from server.models.person_model import Roles
from server.models.dispute_model import Dispute
from server.repositories import dispute_repository
from server.config.logger import log
from server.config.authentication import authentication
from server.models.search_option_model import SearchOption


dispute_blueprint = Blueprint('dispute', __name__)


@dispute_blueprint.route('/disputes', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_role(Roles.CUSTOMERSUPPORT)
def search_disputes():
    search_option = SearchOption.map_from_query(request.args)
    disputes, total_count = dispute_repository.search_disputes(search_option=search_option)

    serialized_disputes = [d.serialize() for d in disputes]
    return jsonify({
        'disputes': serialized_disputes,
        'totalCount': total_count
    }), 200


@dispute_blueprint.route('/disputes/<int:dispute_id>', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_role(Roles.CUSTOMERSUPPORT)
def find_dispute_by_id(dispute_id: int):
    dispute = dispute_repository.find_dispute_by_id(dispute_id)

    if not dispute:
        abort(404, {'message': 'Could not find dispute'})

    return jsonify(dispute.serialize()), 200


@dispute_blueprint.route('/disputes/invoices/<int:invoice_id>', methods=['GET'])
@authentication.jwt_required
@authentication.min_system_access_role(Roles.USER)
def find_dispute_by_invoice_id(invoice_id: int):
    dispute = dispute_repository.find_dispute_by_invoice_id(invoice_id)

    if not dispute:
        abort(404, {'message': 'Could not find dispute'})

    return jsonify(dispute.serialize()), 200


@dispute_blueprint.route('/disputes/<int:dispute_id>', methods=['POST'])
@authentication.jwt_required
@authentication.min_access_role(Roles.CUSTOMERSUPPORT)
def update_dispute_by_id(dispute_id: int):
    fn = 'update_dispute_by_id'
    current_user = g.user

    dispute = dispute_repository.find_dispute_by_id(dispute_id)
    if not dispute:
        abort(404, {'message': 'Could not find dispute'})

    is_loaded, dispute_update = Dispute.validate_submitted_dispute_update(request.json)
    if not is_loaded:
        log.error(f'{fn}: Validation error on dispute status update: {dispute_update}')
        abort(400, {'message': 'Submitted request contains missing or invalid required values'})

    is_updated, message = dispute_repository.update_dispute_by_id(
        dispute=dispute,
        dispute_update=dispute_update,
        updated_by=current_user)

    if not is_updated:
        log.error(f'{fn}: Dispute was not updated > "{message}"')
        abort(400, {'message': 'Dispute cannot be updated as of the moment'})

    return jsonify({ 'message': message }), 200
