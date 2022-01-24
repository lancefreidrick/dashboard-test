""" user_controller.py """
# pylint: disable=unused-argument
from flask import request, jsonify, Blueprint, g, abort
from server.config.authentication import authentication
from server.config.signing import sign_invite
from server.models.person_model import Roles, MerchantRoles
from server.models.search_option_model import SearchOption
from server.repositories import person_repository, merchant_repository, merchant_member_repository
from server.utilities import emails, garnish, helper
from server.models.person_model import Person

user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/users', methods=['GET'])
@authentication.jwt_required
@authentication.min_system_access_role(Roles.CUSTOMERSUPPORT)
def get_users():
    search_option = SearchOption.map_from_query(request.args)
    (users, total_count) = person_repository.search_people(g.user, search_option)
    serialized_users = [p.serialize() for p in users]
    return jsonify({
        'users': serialized_users,
        'totalCount': total_count,
        'page': search_option.page,
        'size': search_option.size,
    }), 200


@user_blueprint.route('/users/<user_id>', methods=['GET'])
@authentication.jwt_required
@authentication.min_system_access_role(Roles.CUSTOMERSUPPORT)
def get_user_by_id(user_id: str):
    valid_id = helper.get_id_as_int(user_id)
    if not valid_id or valid_id <= 0:
        abort(404, {'message': 'User does not exist'})

    current_user = g.user
    person = person_repository.find_person_by_id(user_id)

    if not person:
        abort(404, {'message': 'User does not exist'})

    if person.system_role[0] == Roles.USER[0]:
        merchant_roles = merchant_member_repository.get_merchant_member_roles(person)
        person.merchant_roles = merchant_roles
        if merchant_roles:
            person.merchant_role = merchant_roles[0].merchant_role

    if not current_user.is_internal():
        abort(403, {'message': 'Not allowed to get user'})

    serialized_person = person.serialize()
    return jsonify(serialized_person), 200


@user_blueprint.route('/users', methods=['POST'])
@authentication.jwt_required
@authentication.min_access_role(Roles.USER, MerchantRoles.MERCHANT_ADMIN)
@garnish.require_json_body(['email', 'firstname', 'lastname', 'systemrole'])
def create_user():
    current_user = g.user
    form = request.get_json()
    merchants = form.get('merchants')
    system_role = Roles.get_role_by_id(form.get('systemrole'))
    merchant_role = MerchantRoles.get_role_by_id(form.get('merchantrole'))
    email = form.get('email')

    if system_role[0] == Roles.RESTRICTED[0]:
        abort(400, {'message': 'The user has an invalid role'})
    if current_user.system_role[0] >= Roles.AUDITOR[0]:
        abort(403, {'message': 'Lower role users cannot create higher role users'})

    user_with_same_email = person_repository.find_person_by_email(email)
    if user_with_same_email:
        abort(400, {'message': 'User with email {} already exists'.format(email)})

    new_user = Person()
    new_user.first_name = form.get('firstname')
    new_user.last_name = form.get('lastname')
    new_user.email = email
    new_user.system_role = system_role
    new_user.merchant_role = merchant_role if merchant_role else None
    matched_merchants = []

    if merchants:
        # ADMIN and STAFF role cannot have merchant scopes
        if new_user.system_role[0] <= Roles.CUSTOMERSUPPORT[0]:
            abort(403, {'message': 'Not allowed to select merchants'})

        # If merchants is a string, convert it to a list, else it should be a list of strings.
        # This is to potentially allow multiple merchants to a user.
        if isinstance(merchants, str):
            merchants = [merchants]

        all_merchants, _ = merchant_repository.get_all_merchants()
        matched_merchants = [m.merchant_code for m in all_merchants if m.merchant_code in merchants]

        if len(matched_merchants) != len(merchants):
            abort(400, {'message': 'The merchant scopes have invalid value'})

    new_user.scopes = matched_merchants

    is_created = person_repository.create_person(new_user)
    if not is_created:
        abort(400, {'message': 'Unable to create a new user.'})

    new_person = person_repository.find_person_by_email(email)
    return jsonify({
        'person': new_person.serialize(),
        'message': 'New user {} created'.format(email)
    }), 201


@user_blueprint.route('/users/<user_id>', methods=['POST'])
@authentication.jwt_required
@authentication.min_system_access_role(Roles.CUSTOMERSUPPORT)
@garnish.require_json_body(['firstname', 'lastname', 'systemrole'])
def update_user(user_id: str):
    current_user = g.user
    form = request.get_json()
    merchants = form.get('merchants')
    system_role = Roles.get_role_by_id(form.get('systemrole'))
    merchant_role = MerchantRoles.get_role_by_id(form.get('merchantrole'))

    person = person_repository.find_person_by_id(user_id)
    if not person:
        abort(404, {'message': 'User does not exist'})

    if system_role[0] == Roles.RESTRICTED[0]:
        abort(400, {'message': 'The user has an invalid role'})
    if current_user.system_role[0] >= Roles.AUDITOR[0]:
        abort(403, {'message': 'Not allowed to update users on high level role'})

    person.first_name = form.get('firstname')
    person.last_name = form.get('lastname')
    person.system_role = system_role
    person.merchant_role = merchant_role if merchant_role else None
    matched_merchants = []

    if merchants:
        # ADMIN and STAFF role cannot have merchant scopes
        if person.system_role[0] < Roles.CUSTOMERSUPPORT[0]:
            abort(403, {'message': 'Not allowed to select merchants'})

        # If merchants is a string, convert it to a list, else it should be a list of strings.
        # This is to potentially allow multiple merchants to a user.
        if isinstance(merchants, str):
            merchants = [merchants]

        all_merchants, _ = merchant_repository.get_all_merchants()
        matched_merchants = [m.merchant_code for m in all_merchants if m.merchant_code in merchants]

        if len(matched_merchants) != len(merchants):
            abort(400, {'message': 'The merchant scopes have invalid value'})

    person.scopes = matched_merchants

    if person.system_role[0] == Roles.RESTRICTED[0]:
        abort(400, {'message': 'The user has an invalid role'})

    (is_updated, message) = person_repository.update_person_by_id(person)
    if not is_updated:
        abort(400, {'message': 'Unable to update the user'})

    if person.system_role[0] == Roles.USER[0]:
        merchant_roles = merchant_member_repository.get_merchant_member_roles(person)
        person.merchant_roles = merchant_roles

    if not current_user.is_internal():
        abort(403, {'message': 'Not allowed to update user'})

    return jsonify({
        'message': message,
        'person': person.serialize()
    }), 200


@user_blueprint.route('/users/<email>/invite', methods=['POST'])
@authentication.jwt_required
@authentication.min_system_access_role(Roles.FINANCE)
def send_invite(email: str):
    current_user = g.user
    if not current_user.first_name or not current_user.last_name:
        abort(400, {'message': 'Update your profile with your name first, before sending invites'})

    person = person_repository.find_person_by_email(email)
    if not person:
        abort(400, {'message': 'No user with email {} found'.format(email)})

    sender_name = '{} {}'.format(current_user.first_name, current_user.last_name)
    encoded_email = sign_invite(email)
    emails.send_user_invite_email(email, sender_name, encoded_email)

    return jsonify({'message': 'Invite sent!'}), 200


@user_blueprint.route('/users/<email>', methods=['DELETE'])
@authentication.jwt_required
@authentication.min_system_access_role(Roles.SYSADMIN)
def deactivate_user(email: str):
    current_user = g.user
    if not current_user.first_name or not current_user.last_name:
        abort(400, {'message': 'Update your profile with your name first, before deactivating'})

    person = person_repository.find_person_by_email(email)
    if not person:
        abort(400, {'message': 'No user with email {} found'.format(email)})

    if not person.is_enabled:
        abort(400, {'message': 'User already deactivated'})

    if not person.is_account_confirmed:
        abort(400, {'message': 'Profile must be confirmed first before deactivating'})

    is_deactivated = person_repository.deactivate_person(person)
    if not is_deactivated:
        abort(400, {'message': 'Unable to deactivate user'})

    person = person_repository.find_person_by_email(email)
    return jsonify({
        'person': person.serialize(),
        'message': 'User {} deactivated'.format(email)
    }), 200
