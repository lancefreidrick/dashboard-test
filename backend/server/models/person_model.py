from marshmallow import Schema, fields, ValidationError, validate
from server.utilities import passwords

class Roles:
    SYSADMIN = (
        10,
        'sysadmin',
        'System Admin',
        'Administrators have complete and unrestricted access to the system.'
    )
    ENGINEERING = (
        20,
        'engineering',
        'Engineering',
        'Full access to the financial records, merchants, diagnostic reports and technical logs.'
    )
    FINANCE = (
        30,
        'finance',
        'Finance',
        'Full access to the financial records, merchants and reports.'
    )
    CUSTOMERSUPPORT = (
        40,
        'customersupport',
        'Customer Support',
        'Limited access to the financial records and merchants.'
    )
    MANAGEMENT = (
        50,
        'management',
        'Management',
        'Limited access to the financial reports'
    )
    AUDITOR = (
        60,
        'auditor',
        'Auditor',
        'Limited access to the financial reports'
    )
    USER = (
        70,
        'user',
        'User',
        'Access to their assigned merchant account'
    )
    PAYER = (
        80,
        'payer',
        'Payer',
        'Access to their own financial records'
    )
    GUEST = (
        90,
        'guest',
        'Guest',
        'Restricted access to the system'
    )
    RESTRICTED = (
        100,
        'restricted',
        'Restricted',
        'No Access'
    )

    @staticmethod
    def is_allowed(user_role: tuple, min_access_role: tuple) -> bool:
        if not user_role or not isinstance(user_role, tuple):
            return False
        if not min_access_role or not isinstance(min_access_role, tuple):
            return False

        return user_role[0] <= min_access_role[0]

    @staticmethod
    def as_list() -> list:
        return [
            {'key': r[0], 'code': r[1], 'label': r[2], 'description': r[3]}
            for r in [
                Roles.SYSADMIN, Roles.ENGINEERING, Roles.FINANCE, Roles.CUSTOMERSUPPORT,
                Roles.MANAGEMENT, Roles.AUDITOR, Roles.USER, Roles.PAYER, Roles.GUEST
            ]
        ]

    @staticmethod
    def get_role_by_id(role_id: int) -> tuple:
        return {
            10: Roles.SYSADMIN,
            20: Roles.ENGINEERING,
            30: Roles.FINANCE,
            40: Roles.CUSTOMERSUPPORT,
            50: Roles.MANAGEMENT,
            60: Roles.AUDITOR,
            70: Roles.USER,
            80: Roles.PAYER,
            90: Roles.GUEST
        }.get(role_id) or Roles.RESTRICTED

    @staticmethod
    def get_role_by_code(system_role: str) -> tuple:
        return {
            'sysadmin': Roles.SYSADMIN,
            'engineering': Roles.ENGINEERING,
            'finance': Roles.FINANCE,
            'customersupport': Roles.CUSTOMERSUPPORT,
            'management': Roles.MANAGEMENT,
            'auditor': Roles.AUDITOR,
            'user': Roles.USER,
            'payer': Roles.PAYER,
            'guest': Roles.GUEST
        }.get(system_role) or Roles.RESTRICTED


class MerchantRoles:
    MERCHANT_ADMIN = (
        10, 'Admin',
        'Merchant administrator. Can manage all merchant information and transactions'
    )
    MERCHANT_STAFF = (
        20, 'Staff',
        'Can view specific merchant transactions'
    )
    MERCHANT_AGENT = (
        30, 'Agent',
        'Agents have very limited information access'
    )
    NO_ACCESS = (
        100, 'No Access',
        'Default access. Zero accessibility to the dashboard'
    )

    @staticmethod
    def get_role_by_id(role_id: int) -> tuple:
        return {
            10: MerchantRoles.MERCHANT_ADMIN,
            20: MerchantRoles.MERCHANT_STAFF,
            30: MerchantRoles.MERCHANT_AGENT
        }.get(role_id) or MerchantRoles.NO_ACCESS

    @staticmethod
    def as_list() -> list:
        return [
            {'key': r[0], 'label': r[1], 'description': r[2]}
            for r in [
                MerchantRoles.MERCHANT_ADMIN,
                MerchantRoles.MERCHANT_STAFF,
                MerchantRoles.MERCHANT_AGENT
            ]
        ]


class EncodedJWTPersonSchema(Schema):
    """
    Used for encoding JWT data
    """
    id = fields.Int()
    firstName = fields.Str(attribute='first_name')
    lastName = fields.Str(attribute='last_name')
    email = fields.Str()
    systemRole = fields.Function(lambda p: list(p.system_role))
    merchantRole = fields.Function(lambda p: list(p.merchant_role))

    class Meta:
        fields = ('id', 'firstName', 'lastName', 'email', 'systemRole', 'merchantRole')
        ordered = True


class MerchantMemberRoleSchema(Schema):
    """
    Used for returning JSON-structured values on the API endpoints
    """
    id = fields.Int()
    merchantCode = fields.Str(attribute='merchant_code')
    merchantRole = fields.Function(lambda p: list(p.merchant_role))

    class Meta:
        fields = (
            'id',
            'merchantCode',
            'merchantRole'
        )
        ordered = True


class PersonSchema(Schema):
    """
    Used for returning JSON-structured values on the API endpoints
    """
    id = fields.Int()
    firstName = fields.Str(attribute='first_name')
    lastName = fields.Str(attribute='last_name')
    email = fields.Str()
    scopes = fields.List(fields.Str())
    systemRole = fields.Function(lambda p: list(p.system_role))
    merchantRole = fields.Function(lambda p: list(p.merchant_role))
    merchantRoles = fields.List(fields.Nested(MerchantMemberRoleSchema), attribute='merchant_roles')
    profilePicture = fields.Str(attribute='profile_picture')
    isEnabled = fields.Boolean(attribute='is_enabled')
    canReceiveDailyTransactionEmails = fields.Boolean(attribute='can_receive_daily_transaction_emails')
    canReceivePortalsPaymentEmails = fields.Boolean(attribute='can_receive_portals_payment_emails')
    canReceiveSettlementEmails = fields.Boolean(attribute='can_receive_settlement_emails')
    isAccountConfirmed = fields.Boolean(attribute='is_account_confirmed')

    class Meta:
        fields = (
            'id',
            'firstName',
            'lastName',
            'email',
            'scopes',
            'systemRole',
            'merchantRole',
            'merchantRoles',
            'profilePicture',
            'isEnabled',
            'canReceiveDailyTransactionEmails',
            'canReceiveSettlementEmails',
            'isAccountConfirmed'
        )
        ordered = True


class LoginRequestSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    client_id = fields.Str(required=True, data_key='clientId')


class SignUpRequestSchema(Schema):
    encoded_email = fields.Str(data_key='encodedEmail', required=True)
    first_name = fields.Str(data_key='firstname', required=True, validate=validate.Length(max=50))
    last_name = fields.Str(data_key='lastname', required=True, validate=validate.Length(max=50))
    password = fields.Str(required=True)


class MerchantMemberRole:
    def __init__(self):
        self.merchant_id = None
        self.merchant_code = None
        self.merchant_role: tuple = MerchantRoles.NO_ACCESS

    def serialize(self):
        return MerchantMemberRoleSchema().dump(self)

    @staticmethod
    def map(data: dict):
        """
        @returns MerchantMemberRole
        """
        if not data:
            return None

        member_role = MerchantMemberRole()
        member_role.merchant_id = data.get('merchant_id')
        member_role.merchant_code = data.get('merchant_code')
        member_role.merchant_role = MerchantRoles.get_role_by_id(data.get('merchant_role_id', 100))

        return member_role

class NotificationSettings:
    def __init__(self):
        self.can_receive_daily_transaction_emails = False
        self.can_receive_portals_payment_emails = False
        self.can_receive_settlement_emails = False

    @staticmethod
    def map(data: dict):
        """
        @returns NotificationSettings
        """
        if not data:
            return None

        notification_settings = NotificationSettings()
        notification_settings.can_receive_daily_transaction_emails = data.get('can_receive_daily_transaction_emails')
        notification_settings.can_receive_portals_payment_emails = data.get('can_receive_portals_payment_emails')
        notification_settings.can_receive_settlement_emails = data.get('can_receive_settlement_emails')

        return notification_settings


class Person:
    def __init__(self):
        self.id = None
        self.first_name = None
        self.last_name = None
        self.email = None
        self.system_role: tuple = Roles.RESTRICTED
        self.merchant_role: tuple = MerchantRoles.NO_ACCESS
        self.merchant_roles = []
        self.password_hash = None
        self.profile_picture = None
        self.scopes = []
        self.is_enabled = True
        self.is_account_confirmed = False

    def serialize(self):
        return PersonSchema().dump(self)

    def get_jwt_serialized_person(self):
        return EncodedJWTPersonSchema().dump(self)

    def check_password(self, password: str) -> bool:
        return passwords.check_password(password, self.password_hash)

    def is_internal(self) -> bool:
        """
        Checks if the user is within the internal role

        Returns:
            bool
        """
        return self.system_role[0] <= Roles.CUSTOMERSUPPORT[0]

    def is_allowed(self, merchant_role) -> bool:
        if self.system_role[0] == Roles.USER[0]:
            return self.merchant_role and self.merchant_role[0] <= merchant_role[0]

        return self.system_role[0] <= Roles.AUDITOR[0]

    def __str__(self):
        return f'[{self.id}] {self.name} ({self.email})'

    def __repr__(self):
        return f'Person({self.id}, {self.name}, {self.email})'

    def __eq__(self, other):
        return self.id == other.id

    @property
    def name(self) -> str:
        return '{} {}'.format(self.first_name, self.last_name)

    @staticmethod
    def validate_signup(request_body: dict):
        try:
            validated_data = SignUpRequestSchema().load(request_body)
            return True, validated_data
        except ValidationError as verr:
            return False, verr

    @staticmethod
    def validate_login(request_body: dict):
        try:
            validated_data = LoginRequestSchema().load(request_body)
            return True, validated_data
        except ValidationError as verr:
            return False, verr

    @staticmethod
    def map(data: dict):
        """
        @returns Person
        """
        if not data:
            return None

        person = Person()
        person.id = data.get('person_id')
        person.email = data.get('email_address')
        person.scopes = (data.get('scopes') if data.get('scopes') else [])
        person.first_name = data.get('first_name')
        person.last_name = data.get('last_name')
        person.system_role = Roles.get_role_by_code(data.get('system_role', 'user'))
        person.merchant_role = MerchantRoles.get_role_by_id(data.get('merchant_role_id', 100))
        person.password_hash = data.get('hashed_password')
        person.is_account_confirmed = data.get('is_account_confirmed')
        person.is_enabled = data.get('is_enabled')
        person.profile_picture = str(data.get('profile_picture') or '')

        return person

    @staticmethod
    def create_anonymous_user():
        return Person.map({'person_id': 0, 'system_role': 'user'})
