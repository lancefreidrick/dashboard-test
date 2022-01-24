""" server.controllers.merchant_member_controller.py """
# pylint: disable=unused-argument
from flask import jsonify, abort, Blueprint, g, request

from server.config.logger import log
from server.config.signing import sign_invite
from server.config.authentication import authentication
from server.models.merchant_member_model import Member
from server.models.person_model import Roles, MerchantRoles
from server.models.search_option_model import SearchOption
from server.repositories import (
    person_repository,
    merchant_member_repository
)
from server.utilities import emails

# This is currently for beta purpose only.
# As we expand the AQWIRE B2B business, we will increase the maximum limit.
MAX_MERCHANT_MEMBERS_COUNT = 20

merchant_member_blueprint = Blueprint('merchant_member', __name__)


@merchant_member_blueprint.route('/merchants/<int:merchant_id>/members', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_ADMIN)
def get_members_by_merchant(merchant_id: int):
    current_user = g.user
    merchant = g.merchant
    search_option = SearchOption.map_from_query(request.args)

    if not current_user.is_internal() and merchant.merchant_code not in current_user.scopes:
        abort(403, {'message': 'You are not allowed to get this merchant'})

    members, total_count = person_repository.get_merchant_members(merchant, search_option)
    serialized_members = [p.serialize() for p in members]
    return jsonify({
        'members': serialized_members,
        'totalCount': total_count,
    }), 200


@merchant_member_blueprint.route('/merchants/roles', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_role(Roles.USER, MerchantRoles.MERCHANT_ADMIN)
def get_roles():
    return jsonify({
        'systemRoles': Roles.as_list(),
        'merchantRoles': MerchantRoles.as_list()
    }), 200


@merchant_member_blueprint.route('/merchants/<int:merchant_id>/members/<int:user_id>/notifications',
                                 methods=['GET'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_STAFF)
def get_merchant_member_notification_settings(merchant_id: int, user_id: int):
    current_user = g.user
    merchant = g.merchant

    if current_user.id != user_id:
        abort(403, {'message': 'You are not allowed to get another user\'s information'})

    if not merchant.can_manage_notification_settings:
        abort(403, {'message': 'You are not allowed to manage notification settings'})

    notification_settings = person_repository.get_merchant_member_notification_settings(merchant, user_id)
    if not notification_settings:
        abort(400, {'message': 'User not found'})

    return jsonify({
        'canReceiveDailyTransactionEmails': notification_settings.can_receive_daily_transaction_emails,
        'canReceivePaymentEmails': notification_settings.can_receive_portals_payment_emails,
        'canReceiveSettlementEmails': notification_settings.can_receive_settlement_emails
    }), 200


@merchant_member_blueprint.route(
    '/merchants/<int:merchant_id>/members/<int:user_id>/roles/<int:role_id>',
    methods=['POST'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_ADMIN)
def update_merchant_member_role(merchant_id: int, user_id: int, role_id: int):
    current_user = g.user
    merchant = g.merchant

    if not current_user.is_internal() and merchant.merchant_code not in current_user.scopes:
        abort(403, {'message': 'You are not allowed to update roles of users from another merchant'})

    person = person_repository.find_person_by_id(user_id)
    if not person:
        abort(400, {'message': 'User not found'})

    if not person.is_enabled:
        abort(400, {'message': 'User not found'})

    if merchant.owner.owner_id == user_id:
        abort(400, {'message': 'You are not allowed to update the merchant account owner\'s role'})

    (is_updated, message) = person_repository.update_merchant_member_role(merchant, person, role_id)
    if not is_updated:
        abort(400, {'message': 'Unable to update user role'})

    return jsonify({
        'message': message
    }), 200


@merchant_member_blueprint.route('/merchants/<int:merchant_id>/member', methods=['POST'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_ADMIN)
def add_merchant_member(merchant_id: int):
    fn = 'add_merchant_member'
    current_user = g.user
    merchant = g.merchant

    if not current_user.is_internal() and merchant.merchant_code not in current_user.scopes:
        log.error(f'{fn}: {current_user} is not allowed to add members on {merchant}')
        abort(403, {'message': 'You are not allowed to add members'})

    search_option = SearchOption()
    _, total_count = person_repository.get_merchant_members(merchant, search_option)
    if total_count >= MAX_MERCHANT_MEMBERS_COUNT:
        log.error(f'{fn}: {merchant} members has already reached member limit.')
        abort(400, {'message': 'Maximum allowed member invites has been reacheded'})

    is_valid, validated_member_data = Member.validate_add_member(request.get_json())
    if not is_valid:
        log.error(f'{fn}: Missing fields from request.')
        abort(400, {
            'message': 'Added member has missing fields',
            'fields': validated_member_data.messages
        })

    member = Member()
    member.email_address = validated_member_data.get('email_address')
    member.first_name = ''
    member.last_name = ''
    member.merchant_role_id = validated_member_data.get('role_id')
    is_added, message = merchant_member_repository.add_merchant_member(
        merchant=merchant,
        member=member)
    if not is_added:
        log.error(f'{fn}: {merchant.merchant_code} Member {member.email_address} has not been added: {message}')
        abort(400, {
            'message': 'Member was not added in the merchant account.',
            'fields': validated_member_data.messages
        })

    added_user = person_repository.find_person_by_email(member.email_address)
    return jsonify({
        'person': added_user.serialize(),
        'message': 'New merchant member {} created'.format(member.email_address)
    }), 201


@merchant_member_blueprint.route('/merchants/<int:merchant_id>/members/<int:user_id>', methods=['DELETE'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_ADMIN)
def delete_merchant_member(merchant_id: int, user_id: int):
    current_user = g.user
    merchant = g.merchant

    if not current_user.is_internal() and merchant.merchant_code not in current_user.scopes:
        abort(403, {'message': 'You are not allowed to delete users from another merchant'})

    person = person_repository.find_person_by_id(user_id)
    if not person:
        abort(400, {'message': 'User not found'})

    if not person.is_enabled:
        abort(400, {'message': 'User not found'})

    if merchant.owner.owner_id == user_id:
        abort(400, {'message': 'You are not allowed to remove the merchant account owner'})

    is_deleted, message = person_repository.remove_merchant_member(person, merchant)
    if not is_deleted:
        abort(400, {'message': 'Unable to delete user'})

    return jsonify({
        'message': message
    }), 200


@merchant_member_blueprint.route('/merchants/<int:merchant_id>/notifications', methods=['POST'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_STAFF)
# @garnish.require_json_body(['can_receive_daily_transaction_emails', 'can_receive_settlement_emails'])
def update_merchant_member_notification_settings(merchant_id: int):
    current_user = g.user
    merchant = g.merchant
    form = request.get_json()

    if not merchant.can_manage_notification_settings:
        abort(403, {'message': 'You are not allowed to manage notifications'})

    member = person_repository.find_merchant_member_by_id(merchant, current_user.id)
    member.can_receive_daily_transaction_emails = form.get('canReceiveDailyTransactionEmails')
    member.can_receive_portals_payment_emails = form.get('canReceivePaymentEmails')
    member.can_receive_settlement_emails = form.get('canReceiveSettlementEmails')

    is_updated, message = person_repository.update_merchant_member_notification_settings(merchant, member)

    if not is_updated:
        abort(400, {'message': 'Unable to update the user notification settings'})

    return jsonify({
        'message': message
    }), 200


@merchant_member_blueprint.route('/merchants/<int:merchant_id>/members/<email>/invite', methods=['POST'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_ADMIN)
def send_merchant_member_invite(merchant_id: int, email: str):
    current_user = g.user
    merchant = g.merchant

    if not current_user.first_name or not current_user.last_name:
        abort(400, {'message': 'Update your profile with your name first, before sending invites'})

    if not current_user.is_internal() and merchant.merchant_code not in current_user.scopes:
        abort(403, {'message': 'You are not allowed to invite users for this merchant.'})

    person = person_repository.find_person_by_email(email)
    if not person:
        abort(400, {'message': 'No user with email {} found'.format(email)})

    if not person.is_internal() and merchant.merchant_code not in person.scopes:
        abort(403, {'message': 'You are not allowed to invite users from another merchant'})

    sender_name = '{} {}'.format(current_user.first_name, current_user.last_name)
    encoded_email = sign_invite(email)
    emails.send_user_invite_email(email, sender_name, encoded_email)

    return jsonify({'message': 'Invite sent!'}), 200


@merchant_member_blueprint.route('/merchants/<int:merchant_id>/members', methods=['POST'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_ADMIN)
def add_multiple_merchant_member(merchant_id: int):
    fn = 'add_multiple_merchant_member'
    current_user = g.user
    merchant = g.merchant

    if not current_user.is_internal() and merchant.merchant_code not in current_user.scopes:
        log.error(f'{fn}: {current_user} is not allowed to add members on {merchant}')
        abort(403, {'message': 'You are not allowed to add members'})

    search_option = SearchOption()
    search_option.size = MAX_MERCHANT_MEMBERS_COUNT
    members, total_count = person_repository.get_merchant_members(merchant, search_option)

    is_valid, validated_members_data = Member.validate_add_multiple_members(request.get_json())
    if not is_valid:
        log.error(f'{fn}: Missing fields from request.')
        abort(400, {
            'message': 'Added members has missing fields',
            'fields': validated_members_data.messages
        })

    if (total_count + len(validated_members_data)) >= MAX_MERCHANT_MEMBERS_COUNT:
        log.error(f'{fn}: {merchant} members has already reached member limit.')
        abort(400, {'message': 'Maximum allowed member invites has been reached'})

    email_list = validated_members_data.get('email_addresses')

    for email in email_list:
        member = Member()
        member.email_address = email
        member.first_name = ''
        member.last_name = ''
        member.merchant_role_id = validated_members_data.get('role_id')

        person = person_repository.find_person_by_email(member.email_address)

        if person and person in members:
            emails.send_user_welcome_email(email, person.first_name)

        else:
            is_added, message = merchant_member_repository.add_merchant_member(
                merchant=merchant,
                member=member)

            if is_added:
                sender_name = f'{current_user.first_name} {current_user.last_name}'
                encoded_email = sign_invite(email)
                emails.send_user_invite_email(email, sender_name, encoded_email)

            if not is_added:
                log.error(f'{fn}: {merchant.merchant_code} Member {member.email_address} has not been added: {message}')
                log.error(f'{fn}: Member was not added in the merchant account.')
                log.error(f'{fn}: {validated_members_data.messages}')

    return jsonify({
        'message': 'New members are added to your account.'
    }), 201
