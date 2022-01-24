""" merchant_payment_method_controller.py """
# pylint: disable=unused-argument
from flask import Blueprint, abort, jsonify, g
from server.config.logger import log
from server.config.authentication import authentication
from server.models.person_model import MerchantRoles, Roles
from server.repositories import merchant_payment_method_repository


merchant_payment_method_blueprint = Blueprint('merchant_payment_method', __name__)
base_url = '/merchants/<int:merchant_id>/payment-methods'


@merchant_payment_method_blueprint.route(
    base_url,
    methods=['GET'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_ADMIN)
def get_merchant_payment_methods(merchant_id: int):
    merchant = g.merchant

    methods = merchant_payment_method_repository.get_merchant_payment_methods(merchant)
    serialized_methods = [m.serialize() for m in methods]
    return jsonify(serialized_methods), 200


@merchant_payment_method_blueprint.route(
    f'{base_url}/<int:payment_method_id>/activate',
    methods=['POST'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_ADMIN)
def activate_payment_method(merchant_id: int, payment_method_id: int):
    fn = 'activate_payment_method'
    current_user = g.user
    merchant = g.merchant

    methods = merchant_payment_method_repository.get_merchant_payment_methods(merchant)
    payment_method = next((m for m in methods if m.is_match(payment_method_id)), None)
    if not payment_method:
        log.error(f'{fn}: Payment method does not exist')
        abort(404, {'message': 'Payment method does not exist'})

    if payment_method.is_enabled:
        log.error(f'{fn}: Payment method is already active')
        abort(400, {'message': 'Payment method is already active'})

    is_success, message = merchant_payment_method_repository.activate_payment_method(
        merchant=merchant,
        method=payment_method,
        activated_by=current_user)
    if not is_success:
        log.error(f'{fn}: Payment method error message: {message}')
        abort(400, {'message': 'We are not able to activate this payment method'})

    return jsonify({'message': 'Payment method has been activated'}), 200


@merchant_payment_method_blueprint.route(
    f'{base_url}/<int:payment_method_id>/disable',
    methods=['POST'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_ADMIN)
def disable_payment_method(merchant_id: int, payment_method_id: int):
    fn = 'disable_payment_method'
    current_user = g.user
    merchant = g.merchant

    methods = merchant_payment_method_repository.get_merchant_payment_methods(merchant)
    payment_method = next((m for m in methods if m.is_match(payment_method_id)), None)
    if not payment_method:
        log.error(f'{fn}: Payment method does not exist')
        abort(404, {'message': 'Payment method does not exist'})

    if payment_method.method_code == 'card':
        log.error(f'{fn}: {payment_method} cannot be disabled')
        abort(403, {'message': 'You are not allowed to disable card payments'})

    if not payment_method.is_enabled:
        log.error(f'{fn}: Payment method is already disabled')
        abort(400, {'message': 'Payment method is already disabled'})

    is_success, message = merchant_payment_method_repository.disable_payment_method(
        merchant=merchant,
        method=payment_method,
        disabled_by=current_user)
    if not is_success:
        log.error(f'{fn}: Payment method error message: {message}')
        abort(400, {'message': 'We are not able to disable this payment method'})

    return jsonify({'message': 'Payment method has been disabled'}), 200
