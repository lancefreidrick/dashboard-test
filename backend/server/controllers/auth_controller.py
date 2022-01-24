# pylint: disable=unused-argument

from flask import request, jsonify, abort, Blueprint, g
from server.config import signing
from server.config.authentication import authentication
from server.config.logger import log
from server.repositories import (
    auth_repository, merchant_repository, person_repository,
)
from server.utilities import emails, garnish, passwords
from server.models.person_model import Roles, MerchantRoles, Person
from server.utilities.context_manager import open_transaction_context, ContextStatus


auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login', methods=['OPTIONS', 'POST'])
def log_in():
    fn = 'log_in'
    is_valid, data_or_err = Person.validate_login(request.get_json())
    if not is_valid:
        log.error(f'{fn}: Log in has missing credential on body: {data_or_err}')
        abort(401, {'message': 'Missing credentials'})

    email_address = data_or_err.get('email')
    user_password = data_or_err.get('password')
    client_id = data_or_err.get('client_id')
    person = person_repository.find_person_by_email(email_address)
    if person is None:
        abort(404, {'message': 'User does not exist'})

    with open_transaction_context(user=person, source='auth') as context:
        context.propset(
            action='Log In',
            metadata={
                'ipAddress': request.headers.get('HTTP_X_FORWARDED_FOR') or request.remote_addr,
                'userAgent': request.headers.get('User-Agent'),
                'path': f'{request.method} {request.path}'
            })

        if not person.is_enabled:
            context.propset(
                status=ContextStatus.ERROR,
                description='User is not enabled')
            abort(401, {'message': 'User is deactivated. Please contact administrators'})

        if not Roles.is_allowed(person.system_role, Roles.USER):
            context.propset(
                status=ContextStatus.ERROR,
                description='User role is not supported')
            abort(404, {'message': 'User does not exist'})

        if not person.check_password(user_password):
            context.propset(
                status=ContextStatus.ERROR,
                description='Incorrect email or password')
            abort(401, {'message': 'Invalid email or password'})

        # Refactor the log in because it is the one writing the session
        #  on the session table. It should be moved outside.
        jwt_token, refresh_token = authentication.login({
            'person': person,
            'client_id': client_id,
            'ip_address': request.headers.get('HTTP_X_FORWARDED_FOR') or request.remote_addr,
            'user_agent': request.headers.get('User-Agent')
        })

        auth_response = {
            'authenticationToken': jwt_token,
            'refreshToken': refresh_token,
        }

        # Add merchant to the log in payload for local storage
        if person.scopes:
            merchant = merchant_repository.find_merchant_by_code(person.scopes[0])
            auth_response['merchant'] = merchant.serialize() if merchant else None

        context.propset(
            status=ContextStatus.SUCCESS,
            description=f'{person.name} has logged in')
        return jsonify(auth_response), 200


@auth_blueprint.route('/logout', methods=['POST'])
@authentication.jwt_required
def logout():
    current_user = g.user
    client_id = request.headers.get('X-Client-Id')

    is_logout_success = authentication.logout(current_user, client_id)

    if not is_logout_success:
        abort(403, {'message': 'Not allowed to perform logout'})

    return jsonify({'message': 'Logout successful'}), 200


@auth_blueprint.route('/auth/export', methods=['POST'])
@authentication.jwt_required
def authenticate_export_action():
    current_user = g.user

    if not current_user.is_allowed(MerchantRoles.MERCHANT_ADMIN):
        abort(403, {'message': 'You are not allowed here'})

    # This jwt_token expires after 3 minutes to prevent reuse
    jwt_token = authentication.generate_export_token(current_user)
    return jsonify({'exportToken': jwt_token}), 200


@auth_blueprint.route('/merchants/<int:merchant_id>/auth/export', methods=['POST'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_ADMIN)
def authenticate_merchant_export_action(merchant_id: int):
    current_user = g.user

    # This jwt_token expires after 3 minutes to prevent reuse
    jwt_token = authentication.generate_export_token(current_user)
    return jsonify({'exportToken': jwt_token}), 200


@auth_blueprint.route('/verify-signup-url', methods=['GET'])
@garnish.require_query_params(['data'])
def verify_signup_url():
    data = request.args.get('data')
    email, result = signing.unsign_invite(data)
    if not email:
        if result == signing.SIGNATURE_EXPIRED:
            abort(400, {'message': 'This signup link has already expired.'})
        abort(400, {'message': "Your sign up link does not exist or is invalid."})

    person = person_repository.find_person_by_email(email)

    if person.password_hash:
        return jsonify({
            'message': "This link has already been used.",
            'hasPassword': True,
            'person': person.serialize(),
        }), 400

    return jsonify({'person': person.serialize()}), 200


@auth_blueprint.route('/signup/<int:user_id>', methods=['POST'])
@authentication.validate_password_strength('password')
def signup(user_id: int):
    fn = 'signup'
    form = request.get_json()

    is_valid, data_or_err = Person.validate_signup(request.get_json())
    if not is_valid:
        log.error(f'{fn}: Sign up has missing credential on body: {data_or_err}')
        abort(401, {'message': 'Missing credentials'})

    encodedEmail = form.get('encodedEmail')

    email, result = signing.unsign_invite(encodedEmail)
    if not email:
        if result == signing.SIGNATURE_EXPIRED:
            abort(400, {'message': 'This signup link has already expired.'})
        abort(400, {'message': "Your sign up link does not exist or is invalid."})

    person = person_repository.find_person_by_id(user_id)
    if not person:
        abort(400, {'message': 'Unable to find the account information'})

    person.first_name = form.get('firstname')
    person.last_name = form.get('lastname')
    password = form.get('password')

    # Add validation on the user sign up's role here
    success, message = person_repository.update_account_signup_info_by_id(person, password)
    if not success:
        abort(400, {'message': "Your email {} doesn't seem to be in our system.".format(email)})

    # Only send a welcome email to USERs
    if person.system_role[0] == Roles.USER[0]:
        emails.send_user_welcome_email(email, person.first_name)

    return jsonify({'message': message}), 200


@auth_blueprint.route('/reset-token', methods=['POST'])
def request_reset_token():
    fn = 'request_reset_token'
    form = request.get_json()
    email = form.get('email')
    person = person_repository.find_person_by_email(email)

    success_message = 'The password reset request has been sent to your inbox'

    if not person:
        log.warning(f'{fn}: Accessing reset password for non-existing user')
        return jsonify({'message': success_message}), 200

    if not person.is_enabled:
        log.warning(f'{fn}: Disabled user accessing reset token')
        return jsonify({'message': success_message}), 200

    if not Roles.is_allowed(person.system_role, Roles.USER):
        log.warning(f'{fn}: Non-enterprise user accessing reset token')
        return jsonify({'message': success_message}), 200

    reset_id, token, token_hash = passwords.generate_password_reset_tokens()
    auth_repository.save_reset_token(reset_id, token_hash, person.id)

    emails.send_password_reset_email(person.first_name, person.email, reset_id, token)

    return jsonify({'message': success_message}), 200


@auth_blueprint.route('/password-reset/<reset_id>/verify', methods=['POST'])
@authentication.jwt_optional
@garnish.require_json_body(['token'])
def verify_reset_token(reset_id: str):
    current_user = g.user
    if current_user.id:
        abort(400, {'message': 'You are not supposed to be here.'})

    form = request.get_json()
    token = form.get('token')

    reset_token = auth_repository.find_reset_token(reset_id)

    if not reset_token:
        abort(400, {'message': "Something's wrong with your password reset link."})

    if not reset_token.check_token(token):
        abort(400, {'message': 'Your token is invalid.'})

    if reset_token.is_used:
        abort(400, {'message': 'Your token has been used. Please request a new one.'})

    if reset_token.is_expired:
        abort(400, {'message': 'Your token has expired. Please request a new one.'})

    person = person_repository.find_person_by_id(reset_token.user_id)
    return jsonify({'person': person.serialize()}), 200


@auth_blueprint.route('/password-reset/<reset_id>/reset', methods=['POST'])
@authentication.jwt_optional
@garnish.require_json_body(['token', 'new_password'])
@authentication.validate_password_strength('new_password')
def reset_password(reset_id: str):
    current_user = g.user
    if current_user.id:
        abort(400, {'message': 'You are not supposed to be here.'})

    form = request.get_json()
    token = form.get('token')
    new_password = form.get('new_password')

    if not new_password:
        abort(400, {'message': 'The password may not be blank.'})

    reset_token = auth_repository.find_reset_token(reset_id)
    if not reset_token:
        abort(400, {'message': "Something's wrong with your password reset link."})

    if not reset_token.check_token(token):
        abort(400, {'message': 'Your token is invalid.'})

    if reset_token.is_used:
        abort(400, {'message': 'Your token has been used. Please request a new one.'})

    if reset_token.is_expired:
        abort(400, {'message': 'Your token has expired. Please request a new one.'})

    (has_reset, message) = person_repository.update_account_password(reset_token.user_id, new_password)
    auth_repository.mark_reset_token_as_used(reset_token.id)

    if not has_reset:
        abort(400, {'message': 'Something went wrong!'})

    person = person_repository.find_person_by_id(reset_token.user_id)
    emails.send_password_changed_confirmation_email(person.first_name, person.email)

    return jsonify({'message': message}), 200
