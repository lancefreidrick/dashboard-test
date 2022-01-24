from typing import Tuple
from server.config import database
from server.models.merchant_model import Merchant
from server.models.merchant_member_model import Member
from server.models.person_model import MerchantMemberRole


def add_merchant_member(merchant: Merchant, member: Member) -> Tuple[bool, str]:
    params = [
        member.email_address,
        member.first_name,
        member.last_name,
        merchant.merchant_id,
        member.merchant_role_id
    ]
    rows = database.func('directory.add_merchant_member', params)
    if not rows:
        return False, 'Member was not added in the merchant account'

    return rows[0]['status'] == 'success', rows[0]['message']


def get_merchant_member_roles(member: Member) -> list:
    params = [
        member.id
    ]
    rows = database.func('directory.get_merchant_member_roles', params)

    return [MerchantMemberRole.map(mmr) for mmr in rows]
