from enum import Enum
from marshmallow import Schema, fields, ValidationError, validate
from server.models.person_model import Person

class MerchantRoles(Enum):
    ADMIN = 10
    STAFF = 20
    AGENT = 30


class AddMemberRequestSchema(Schema):
    email_address = fields.Str(data_key='email', required=True,
        validate=validate.Email())
    role_id = fields.Integer(data_key='merchantrole', required=True,
        validate=validate.OneOf([10, 20, 30]))

class AddMultipleMemberRequestSchema(Schema):
    email_addresses = fields.List(fields.Email, data_key='emails', required=True)
    role_id = fields.Integer(data_key='merchantrole', required=True,
        validate=validate.OneOf([10, 20, 30]))


class Member(Person):
    def __init__(self):
        self.merchant_role_id: int = MerchantRoles.AGENT.value
        self.can_receive_daily_transaction_emails = False
        self.can_receive_portals_payment_emails = False
        self.can_receive_settlement_emails = False

    def __str__(self) -> str:
        return f'Member {self.email_address}'

    def __repr__(self) -> str:
        return f'Member({self.email_address})'

    @staticmethod
    def validate_add_member(data: dict):
        try:
            add_member_data = AddMemberRequestSchema().load(data)
            return True, add_member_data
        except ValidationError as verr:
            return False, verr

    @staticmethod
    def validate_add_multiple_members(data: dict):
        try:
            add_member_data = AddMultipleMemberRequestSchema().load(data)
            return True, add_member_data
        except ValidationError as verr:
            return False, verr
