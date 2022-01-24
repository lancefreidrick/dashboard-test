"""
account_controller.py
"""
from flask import Blueprint, jsonify, abort, request, g
from server.models.person_model import Roles
from server.config.authentication import authentication
from server.repositories import person_repository, merchant_member_repository
from server.utilities import garnish, emails


account_blueprint = Blueprint('account', __name__)

@account_blueprint.route('/account/info', methods=['GET'])
@authentication.jwt_required
def get_account_info():
    current_user = g.user

    person = person_repository.find_person_by_id(current_user.id)
    if not person:
        abort(400, {'message': 'Unable to find the account information'})

    if person.system_role[0] == Roles.USER[0]:
        merchant_roles = merchant_member_repository.get_merchant_member_roles(person)
        person.merchant_roles = merchant_roles

    return jsonify(person.serialize()), 200

@account_blueprint.route('/account/info', methods=['POST'])
@authentication.jwt_required
@garnish.require_json_body(['firstname', 'lastname', 'email'])
def update_account_info():
    current_user = g.user
    form = request.get_json()

    person = person_repository.find_person_by_id(current_user.id)

    person.first_name = form.get('firstname')
    person.last_name = form.get('lastname')
    person.email = form.get('email')

    (is_updated, message) = person_repository.update_account_info_by_id(person)
    if not is_updated:
        abort(400, {'message': 'Unable to update the account information'})

    return jsonify({
        'message': message,
        'person': person.serialize()
    }), 200

@account_blueprint.route('/account/password', methods=['POST'])
@authentication.jwt_required
@garnish.require_json_body(['currentPassword', 'newPassword'])
@authentication.validate_password_strength('newPassword')
def update_account_password():
    current_user = g.user
    form = request.get_json()
    current_password = form.get('currentPassword')
    new_password = form.get('newPassword')
    person = person_repository.find_person_by_id(current_user.id)

    is_password_correct = person.check_password(current_password)
    if not is_password_correct:
        abort(401, {'message': 'Your current password is incorrect.'})

    (is_updated, message) = person_repository.update_account_password(current_user.id, new_password)
    if not is_updated:
        abort(400, {'message': 'Unable to update the account password'})

    emails.send_password_changed_confirmation_email(person.first_name, person.email)
    return jsonify({'message': message}), 200

@account_blueprint.route('/account/notif', methods=['POST'])
@authentication.jwt_required
@garnish.require_json_body(['can_receive_daily_transaction_emails', 'can_receive_settlement_emails'])
def update_account_notifications():
    current_user = g.user
    form = request.get_json()

    person = person_repository.find_person_by_id(current_user.id)

    person.can_receive_daily_transaction_emails = form.get('can_receive_daily_transaction_emails')
    person.can_receive_settlement_emails = form.get('can_receive_settlement_emails')

    (is_updated, message) = person_repository.update_account_notifications_by_id(person)

    if not is_updated:
        abort(400, {'message': 'Unable to update the account information'})

    return jsonify({
        'message': message
    }), 200
