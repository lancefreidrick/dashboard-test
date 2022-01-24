""" merchant_controller.py """
# pylint: disable=unused-argument
from flask import jsonify, abort, Blueprint, g, request

from server.config.logger import log
from server.config.authentication import authentication
from server.models.person_model import Roles, MerchantRoles
from server.models.search_option_model import SearchOption
from server.models.merchant_model import Merchant
from server.repositories import merchant_repository, person_repository


merchant_blueprint = Blueprint('merchant', __name__)


@merchant_blueprint.route('/merchants', methods=['GET'])
@authentication.jwt_required
@authentication.min_system_access_role(Roles.USER)
def get_merchants():
    current_user = g.user
    if not current_user.scopes and not current_user.is_internal():
        return jsonify([]), 200

    search_option = SearchOption.map_from_query(request.args)

    if current_user.is_internal():
        merchants, total_count = merchant_repository.get_all_merchants(search_option)
        return jsonify({
            'merchants': [m.serialize() for m in merchants],
            'totalCount': total_count,
        }), 200

    merchants = merchant_repository.get_user_merchants(current_user)
    return jsonify({
        'merchants': [m.serialize() for m in merchants],
        'totalCount': len(merchants),
    }), 200


@merchant_blueprint.route('/merchants/<int:merchant_id>/categories', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_ADMIN)
def get_merchant_categories(merchant_id: int):
    categories = merchant_repository.get_all_merchant_categories()
    serialized_categories = [c.serialize() for c in categories]
    return jsonify(serialized_categories), 200


@merchant_blueprint.route('/merchants/<merchant_code>', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_role(Roles.USER, MerchantRoles.MERCHANT_AGENT)
def find_merchant_by_code(merchant_code: str):
    current_user = g.user
    merchant = merchant_repository.find_merchant_by_code(merchant_code)

    if not merchant:
        abort(404, {'message': 'Merchant does not exist'})

    if not current_user.is_internal() and merchant.merchant_code not in current_user.scopes:
        abort(403, {'message': 'You are not allowed to get this merchant'})

    serialized_merchant = merchant.serialize()
    return jsonify(serialized_merchant), 200


@merchant_blueprint.route('/merchants/<int:merchant_id>', methods=['POST'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_ADMIN)
def update_merchant_information(merchant_id: int):
    fn = 'update_merchant_information'
    merchant = g.merchant

    is_valid, validated_data = Merchant.validate_submitted_info(request.get_json())
    if not is_valid:
        log.error(f'{fn}: Validation error {validated_data}')
        abort(400, {
            'message': 'Submitted merchant has form validation errors',
            'fields': validated_data.messages
        })

    category_id = validated_data.get('category')
    merchant_category = merchant_repository.find_merchant_category_by_id(category_id)
    if not merchant_category:
        abort(400, {'message': 'Category does not exist'})

    # Add validation
    merchant.name = validated_data.get('name')
    merchant.category_id = validated_data.get('category')
    merchant.address = validated_data.get('address')
    merchant.timezone = validated_data.get('timezone')

    is_updated, message = merchant_repository.update_merchant_information(merchant)
    if not is_updated:
        log.error(f'{fn}: Merchant information was not saved: {message}')
        abort(400, {'message': 'Submitted merchant information has not been saved. Please try again later.'})

    log.info(f'{fn}: Merchant {merchant} account was updated')
    return jsonify({'message': 'Merchant account information has been saved'}), 200


@merchant_blueprint.route('/merchants/<int:merchant_id>/ownership', methods=['POST'])
@authentication.jwt_required
@authentication.min_system_access_role(Roles.SYSADMIN)
def set_merchant_owner(merchant_id: int):
    fn = 'set_merchant_owner'
    current_user = g.user

    form = request.get_json()
    user_id = int(form.get('userId'))

    merchant = merchant_repository.find_merchant_by_id(merchant_id)

    if not merchant:
        abort(404, {'message': 'Merchant does not exist'})

    person = person_repository.find_person_by_id(user_id)

    if not person:
        abort(404, {'message': 'User does not exist'})

    if not person.system_role[0] == Roles.USER[0]:
        abort(400, {'message': 'Unable to set user as the merchant owner'})

    if not current_user.is_internal() and merchant.merchant_code not in current_user.scopes:
        abort(403, {'message': 'You are not allowed to get this merchant'})

    is_updated, message = person_repository.update_merchant_owner(person, merchant)
    if not is_updated:
        abort(400, {'message': 'Unable to update merchant owner'})

    log.info(f'{fn}: Merchant {merchant} owner was has been updated')
    return jsonify({
        'message': message
    }), 200


@merchant_blueprint.route('/merchants/<int:merchant_id>/suspend', methods=['POST'])
@authentication.jwt_required
@authentication.min_system_access_role(Roles.SYSADMIN)
def suspend_merchant_account(merchant_id: int):
    fn = 'suspend_merchant_account'

    merchant = merchant_repository.find_merchant_by_id(merchant_id)
    if not merchant:
        abort(404, {'message': 'Merchant does not exist'})

    is_suspended, message = merchant_repository.suspend_merchant_account(merchant)
    if not is_suspended:
        log.error(f'{fn}: Merchant account was not suspended: {message}')
        abort(400, {'message': 'Merchant account was not suspended. Please try again later.'})

    log.info(f'{fn}: Merchant {merchant} account was suspended')
    return jsonify({'message': 'Merchant account has been suspended'}), 200


@merchant_blueprint.route('/merchants/<int:merchant_id>/close', methods=['POST'])
@authentication.jwt_required
@authentication.min_system_access_role(Roles.SYSADMIN)
def close_merchant_account(merchant_id: int):
    fn = 'close_merchant_account'

    merchant = merchant_repository.find_merchant_by_id(merchant_id)
    if not merchant:
        abort(404, {'message': 'Merchant does not exist'})

    is_closed, message = merchant_repository.close_merchant_account(merchant)
    if not is_closed:
        log.error(f'{fn}: Merchant account was not closed: {message}')
        abort(400, {'message': 'Merchant account was not closed. Please try again later.'})

    log.info(f'{fn}: Merchant {merchant} account was closed')
    return jsonify({'message': 'Merchant account has been closed'}), 200


@merchant_blueprint.route('/merchants/<int:merchant_id>/activate', methods=['POST'])
@authentication.jwt_required
@authentication.min_system_access_role(Roles.SYSADMIN)
def activate_merchant_account(merchant_id: int):
    fn = 'activate_merchant_account'

    merchant = merchant_repository.find_merchant_by_id(merchant_id)
    if not merchant:
        abort(404, {'message': 'Merchant does not exist'})

    is_activated, message = merchant_repository.activate_merchant_account(merchant)
    if not is_activated:
        log.error(f'{fn}: Merchant account was not activated: {message}')
        abort(400, {'message': 'Merchant account was not activated. Please try again later.'})

    log.info(f'{fn}: Merchant {merchant} account was activated')
    return jsonify({'message': 'Merchant account has been activated'}), 200


@merchant_blueprint.route('/merchants/<int:merchant_id>/category', methods=['POST'])
@authentication.jwt_required
@authentication.min_system_access_role(Roles.SYSADMIN)
def update_merchant_category(merchant_id: int):
    fn = 'update_merchant_category'

    form = request.get_json()
    merchant_category_id = int(form.get('merchantCategory'))

    if merchant_category_id not in [1, 2 ,3]:
        abort(400, {'message': 'Invalid merchant category.'})

    merchant = merchant_repository.find_merchant_by_id(merchant_id)
    if not merchant:
        abort(404, {'message': 'Merchant does not exist'})

    if merchant.merchant_status[0] == 40:
        abort(404, {'message': 'Merchant is closed.'})

    is_updated, message = merchant_repository.update_merchant_category(merchant, merchant_category_id)
    if not is_updated:
        log.error(f'{fn}: Merchant category was not updated: {message}')
        abort(400, {'message': 'Merchant category was not updated. Please try again later.'})

    log.info(f'{fn}: Merchant {merchant} category was update')
    return jsonify({'message': 'Merchant category has been updated'}), 200


@merchant_blueprint.route('/merchants/<int:merchant_id>/flags', methods=['POST'])
@authentication.jwt_required
@authentication.min_system_access_role(Roles.SYSADMIN)
def update_merchant_feature_flags(merchant_id: int):
    fn = 'update_merchant_feature_flags'

    merchant = merchant_repository.find_merchant_by_id(merchant_id)
    if not merchant:
        abort(404, {'message': 'Merchant does not exist'})

    is_valid, validated_data = Merchant.validate_feature_flags(request.get_json())

    if not is_valid:
        abort(400, {'message': 'Submitted flags were invalid'})

    merchant.can_manage_projects = validated_data.get('canManageProjects')
    merchant.can_manage_payment_methods = validated_data.get('canManagePaymentMethods')
    merchant.can_access_reports = validated_data.get('canAccessReports')
    merchant.can_copy_sales_agents = validated_data.get('canCopySalesAgents')
    merchant.can_manage_payment_links = validated_data.get('canManagePaymentLinks')
    merchant.can_manage_notification_settings = validated_data.get('canManageNotificationSettings')

    is_updated, message = merchant_repository.update_merchant_feature_flags(merchant)

    if not is_updated:
        log.error(f'{fn}: Merchant {merchant} feature flags was not updated: {message}')
        abort(400, {'message': 'Merchant feature flags were not updated. Please try again later'})

    log.info(f'{fn}: Merchant {merchant} account flags has been updated')
    return jsonify({'message': 'Merchant feature flags updated'}), 200


@merchant_blueprint.route('/merchants/<int:merchant_id>/payment-types', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_AGENT)
def get_payment_types(merchant_id: int):
    current_user = g.user
    merchant = g.merchant

    if not current_user.is_internal() and merchant.merchant_code not in current_user.scopes:
        abort(403, {'message': 'You are not allowed to get payment types'})

    payment_types = merchant_repository.get_merchant_payment_types(
        merchant=merchant)

    if 'purpose' in request.args and request.args.get('purpose') == 'pay':
        return jsonify({
            'paymentTypes': [
                pt.serialize() for pt in payment_types for mpt in merchant.payment_types
                if pt.code.endswith(mpt.code)
            ]
        }), 200

    return jsonify({
        'paymentTypes': [p.serialize() for p in payment_types]
    }), 200


@merchant_blueprint.route('/merchants/<int:merchant_id>/roles', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_ADMIN)
def get_roles(merchant_id: int):
    return jsonify({
        'merchantRoles': MerchantRoles.as_list()
    }), 200


@merchant_blueprint.route('/merchants/<int:merchant_id>/payment-currencies', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_AGENT)
def get_payment_currencies(merchant_id: int):
    current_user = g.user
    merchant = g.merchant

    if not current_user.is_internal() and merchant.merchant_code not in current_user.scopes:
        abort(403, {'message': 'You are not allowed to get payment currencies'})

    payment_currencies = merchant_repository.get_merchant_payment_currencies(merchant_id=merchant_id)
    return jsonify({
        'paymentCurrencies': payment_currencies
    }), 200
