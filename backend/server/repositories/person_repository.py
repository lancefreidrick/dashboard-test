from typing import Tuple
from server.config import database
from server.models.search_option_model import SearchOption
from server.models.person_model import NotificationSettings, Person
from server.models.merchant_member_model import Member
from server.models.merchant_model import Merchant
from server.utilities import passwords


def search_people(requested_by: Person, search_option: SearchOption) -> Tuple[list, int]:
    db_params = [
        requested_by.system_role[0],
        search_option.merchant_code or None,
        search_option.system_role or None,
        search_option.is_enabled,
        search_option.search_term or None,
        search_option.size,
        search_option.skip()
    ]
    processed_data = database.func('directory.search_people', db_params)
    users = [Person.map(p) for p in processed_data]
    if not users:
        return [], 0
    return users, processed_data[0]['full_count']


def find_person_by_id(user_id: int) -> Person:
    db_params = [user_id]
    found_user = database.func('directory.find_person_by_id', db_params)
    if not found_user:
        return None
    return Person.map(found_user[0])


def find_person_by_email(email: str) -> Person:
    db_params = [email]
    found_user = database.func('directory.find_person_by_email', db_params)
    if not found_user:
        return None
    return Person.map(found_user[0])


def update_account_password(user_id: str, password: str) -> Tuple[bool, str]:
    db_params = [
        int(user_id),
        passwords.hash_password(password)
    ]
    result = database.func('directory.update_account_password', db_params)
    return result[0]['status'] == 'success', result[0]['message']


def create_person(person: Person) -> bool:
    db_params = [
        person.email,
        person.first_name,
        person.last_name,
        person.system_role[1],
        person.merchant_role[0],
        person.scopes
    ]
    result = database.func('directory.create_person', db_params)
    return result[0]['status'] == 'success'


def deactivate_person(person: Person) -> bool:
    db_params = [person.email]
    result = database.func('directory.deactivate_person', db_params)
    return result[0]['status'] == 'success'


def update_person_by_id(person: Person) -> Tuple[bool, str]:
    db_params = [
        person.id,
        person.first_name,
        person.last_name,
        person.system_role[1],
        person.merchant_role[0],
        person.scopes
    ]
    result = database.func('directory.update_person_by_id', db_params)
    return result[0]['status'] == 'success', result[0]['message']


def update_account_info_by_id(person: Person) -> Tuple[bool, str]:
    db_params = [
        person.id,
        person.first_name,
        person.last_name,
        person.email
    ]
    result = database.func('directory.update_account_info_by_id', db_params)
    return result[0]['status'] == 'success', result[0]['message']


def update_account_signup_info_by_id(person: Person, password: str) -> Tuple[bool, str]:
    db_params = [
        person.id,
        person.first_name,
        person.last_name,
        passwords.hash_password(password)
    ]
    result = database.func('directory.update_account_signup_info_by_id', db_params)
    return result[0]['status'] == 'success', result[0]['message']


def get_people_by_merchant_id(merchant: Merchant, search_option: SearchOption) -> Tuple[list, int]:
    db_params = [
        merchant.merchant_id,
        search_option.system_role or None,
        search_option.merchant_role or None,
        search_option.search_term or None,
        search_option.size,
        search_option.skip()
    ]
    queried_users = database.func('directory.get_people_by_merchant_id', db_params)
    if not queried_users:
        return ([], 0)
    users = [Person.map(p) for p in queried_users]

    return users, queried_users[0]['full_count']


def update_account_notifications_by_id(person: Person) -> Tuple[bool, str]:
    db_params = [
        person.id,
        person.can_receive_daily_transaction_emails,
        person.can_receive_settlement_emails
    ]
    result = database.func('directory.update_account_notifications_by_id', db_params)
    return result[0]['status'] == 'success', result[0]['message']


def get_merchant_members(merchant: Merchant, search_option: SearchOption) -> Tuple[list, int]:
    db_params = [
        merchant.merchant_id,
        search_option.size,
        search_option.skip()
    ]
    queried_members = database.func('directory.get_merchant_members', db_params)
    if not queried_members:
        return ([], 0)
    users = [Member.map(p) for p in queried_members]

    return users, queried_members[0]['full_count']


def get_merchant_admins_with_notifications_by_merchant_id(merchant: Merchant) -> Tuple[list, int]:
    db_params = [merchant.merchant_id]
    queried_merchant_admins = database.func(
        'directory.get_merchant_admins_with_notifications_by_merchant_id',
        db_params)
    if not queried_merchant_admins:
        return ([], 0)

    merchant_admins = [Person.map(p) for p in queried_merchant_admins]

    return merchant_admins, queried_merchant_admins[0]['full_count']


def remove_merchant_member(user: Person, merchant: Merchant) -> Tuple[bool, str]:
    params = [
        merchant.merchant_id,
        user.id
    ]
    rows = database.func('directory.remove_merchant_member', params)
    if not rows:
        return False, 'Merchant has not been removed'
    return rows[0]['status'] == 'success', rows[0]['message']


def find_merchant_member_by_id(merchant: Merchant, user_id: int) -> Member:
    db_params = [
        merchant.merchant_id,
        user_id
    ]

    found_user = database.func('directory.find_merchant_member_by_id', db_params)

    if not found_user:
        return None
    return Member.map(found_user[0])


def get_merchant_member_notification_settings(merchant: Merchant, user_id: int) -> NotificationSettings:
    db_params = [
        merchant.merchant_id,
        user_id
    ]

    notification_settings = database.func('directory.find_merchant_member_by_id', db_params)

    return NotificationSettings.map(notification_settings[0])


def update_merchant_member_notification_settings(merchant: Merchant, member: Member) -> Tuple[bool, str]:
    db_params = [
        member.id,
        merchant.merchant_id,
        member.can_receive_daily_transaction_emails,
        member.can_receive_portals_payment_emails,
        member.can_receive_settlement_emails
    ]
    result = database.func('directory.update_merchant_member_notification_settings', db_params)
    return result[0]['status'] == 'success', result[0]['message']


def update_merchant_member_role(merchant: Merchant, person: Person, role_id: int) -> Tuple[bool, str]:
    db_params = [
        person.id,
        merchant.merchant_id,
        role_id
    ]
    result = database.func('directory.update_merchant_member_role', db_params)
    return result[0]['status'] == 'success', result[0]['message']


def update_merchant_owner(user: Person, merchant: Merchant) -> Tuple[bool, str]:
    params = [
        merchant.merchant_id,
        user.id
    ]
    rows = database.func('directory.update_merchant_owner', params)
    if not rows:
        return False, 'Merchant owner has not been changed'
    return rows[0]['status'] == 'success', rows[0]['message']
