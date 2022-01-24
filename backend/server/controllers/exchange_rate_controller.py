""" server.controllers.exchange_rate_controller.py """
from flask import jsonify, Blueprint, abort
from server.config.authentication import authentication
from server.repositories import exchange_rate_repository
from server.models.person_model import Roles

exchange_rate_blueprint = Blueprint('exchange_rate', __name__)

@exchange_rate_blueprint.route('/xrates/latest', methods=['GET'])
@authentication.jwt_required
@authentication.min_system_access_role(Roles.CUSTOMERSUPPORT)
def get_latest_exchange_rate():
    exchange_rate = exchange_rate_repository.get_latest_exchange_rate()

    if not exchange_rate:
        abort(404, {'message': 'Exchange rate is not available'})

    return jsonify(exchange_rate.serialize()), 200
