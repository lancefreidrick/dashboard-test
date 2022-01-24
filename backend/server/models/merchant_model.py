"""
merchant_model.py
"""
from typing import List, Tuple

from pytz import all_timezones
from marshmallow import Schema, fields, ValidationError, validate


class MerchantStatus:
    ACTIVE = (
        10,
        'active',
        'Active',
        'Merchant is active.'
    )
    INACTIVE = (
        20,
        'inactive',
        'Inctive',
        'Merchant is inactive.'
    )
    SUSPENDED = (
        30,
        'suspended',
        'Suspended',
        'Merchant is suspended.'
    )
    CLOSED = (
        40,
        'closed',
        'Closed',
        'Merchant is closed.'
    )

    @staticmethod
    def as_list() -> list:
        return [
            {'key': r[0], 'code': r[1], 'label': r[2], 'description': r[3]}
            for r in [
                MerchantStatus.ACTIVE, MerchantStatus.INACTIVE, MerchantStatus.SUSPENDED, MerchantStatus.CLOSED
            ]
        ]

    @staticmethod
    def get_merchant_status_by_id(merchant_status_id: int) -> tuple:
        return {
            10: MerchantStatus.ACTIVE,
            20: MerchantStatus.INACTIVE,
            30: MerchantStatus.SUSPENDED,
            40: MerchantStatus.CLOSED
        }.get(merchant_status_id) or MerchantStatus.ACTIVE

    @staticmethod
    def get_merchant_status_by_code(merchant_status_code: str) -> tuple:
        return {
            'active': MerchantStatus.ACTIVE,
            'inactive': MerchantStatus.INACTIVE,
            'suspended': MerchantStatus.SUSPENDED,
            'closed': MerchantStatus.CLOSED
        }.get(merchant_status_code) or MerchantStatus.ACTIVE


class MerchantSchema(Schema):
    id = fields.Int(attribute='merchant_id')
    code = fields.Str(attribute='merchant_code')
    name = fields.Str()
    timezone = fields.Str(attribute='timezone')
    invoicingMode = fields.Str(attribute='invoicing_mode')
    isActive = fields.Bool(attribute='is_active')
    isPublic = fields.Bool(attribute='is_public')
    canManageProjects = fields.Bool(attribute='can_manage_projects')
    canManagePaymentMethods = fields.Bool(attribute='can_manage_payment_methods')
    canAccessReports = fields.Bool(attribute='can_access_reports')
    canCopySalesAgents = fields.Bool(attribute='can_copy_sales_agents')
    canManagePaymentLinks = fields.Bool(attribute='can_manage_payment_links')
    canManageNotificationSettings = fields.Bool(attribute='can_manage_notification_settings')
    address = fields.Dict()
    categoryId = fields.Int(attribute='category_id')
    categoryName = fields.Str(attribute='category_name')
    categoryDescription = fields.Str(attribute='category_description')
    projects = fields.List(fields.Dict())
    logo = fields.Str()
    isPortals3Configured = fields.Bool(attribute='is_portals3_configured')
    ownerId = fields.Int(attribute='owner.owner_id')
    ownerName = fields.Str(attribute='owner.name')
    status = fields.Function(lambda m: list(m.merchant_status))

    class Meta:
        fields = (
            'id', 'code', 'name', 'invoicingMode', 'isActive', 'isPublic',
            'categoryId', 'categoryName', 'categoryDescription', 'canManageProjects',
            'canManagePaymentMethods', 'canAccessReports', 'canCopySalesAgents', 'canManagePaymentLinks',
            'canManageNotificationSettings','address', 'paymentTypes', 'paymentModes', 'projects', 'logo',
            'isPortals3Configured', 'timezone', 'ownerId', 'ownerName', 'status'
        )
        ordered = True


class CompactMerchantSchema(Schema):
    id = fields.Str(attribute='merchant_id')
    code = fields.Str(attribute='merchant_code')
    name = fields.Str()
    invoicingMode = fields.Str(attribute='invoicing_mode')
    isActive = fields.Bool(attribute='is_active')
    isPublic = fields.Bool(attribute='is_public')
    categoryId = fields.Str(attribute='category_id')
    categoryName = fields.Str(attribute='category_name')
    categoryDescription = fields.Str(attribute='category_description')

    class Meta:
        fields = (
            'id', 'code', 'name', 'invoicingMode', 'isActive', 'isPublic',
            'categoryId', 'categoryName', 'categoryDescription'
        )
        ordered = True


class SubmittedMerchantAddressSchema(Schema):
    address_one = fields.Str(data_key='addressOne', required=False)
    address_two = fields.Str(data_key='addressTwo', required=False)
    address_three = fields.Str(data_key='addressThree', required=False)


class SubmittedMerchantInformationSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    category = fields.Int(required=True)
    address = fields.Nested(SubmittedMerchantAddressSchema(), required=True)
    timezone = fields.Str(
        required=True,
        validate=validate.OneOf(all_timezones, error='Must be a valid timezone'))


class MerchantCategorySchema(Schema):
    id = fields.Int(attribute='category_id')
    name = fields.Str()
    description = fields.Str()

class MerchantPaymentTypeSchema(Schema):
    id = fields.Int(attribute='id')
    code = fields.Str()
    name = fields.Str()

############################################################


class MerchantCategory:
    def __init__(self):
        self.category_id: int = None
        self.name: str = None
        self.description: str = None

    def serialize(self):
        return MerchantCategorySchema().dump(self)

    @staticmethod
    def map(data: dict):
        if not data:
            return None

        category = MerchantCategory()
        category.category_id = data['merchant_category_id']
        category.name = data['merchant_category_name']
        category.description = data['merchant_category_description']
        return category

class MerchantPaymentType:
    def __init__(self):
        self.id: int = None
        self.code: str = None
        self.name: str = None

    @property
    def simple_code(self) -> str:
        return '_'.join(self.code.split('_')[1:])

    def serialize(self):
        return MerchantPaymentTypeSchema().dump(self)

    @staticmethod
    def map(data: dict):
        if not data:
            return None

        payment_type = MerchantPaymentType()
        payment_type.id = data['payment_type_id']
        payment_type.code = data['payment_type_code']
        payment_type.name = data['payment_type_name']

        return payment_type

class Merchant:
    class Owner:
        def __init__(self, owner_id: int, name: str, email_address: str):
            self.owner_id = owner_id
            self.name = name
            self.email_address = email_address

    class AcceptedCurrency:
        def __init__(self, currency: str, min_amount: float, max_amount: float):
            self.currency = currency
            self.min_amount = min_amount
            self.max_amount = max_amount

    def __init__(self):
        self.merchant_id = None
        self.merchant_code = None
        self.name = None
        self.timezone = None
        self.invoicing_mode = None
        self.category_id = None
        self.category_name = None
        self.category_description = None
        self.address = None
        self.config = dict()
        self.portal_url = None
        self.is_public = False
        self.is_active = False
        self.payment_types = []
        self.can_manage_projects = False
        self.can_manage_payment_methods = False
        self.can_access_reports = False
        self.can_copy_sales_agents = False
        self.can_manage_payment_links = False
        self.can_manage_notification_settings = False
        self.projects = []
        self.payment_modes = []
        self.logo = None
        self.is_portals3_configured = False
        self.links_secret = None
        self.owner = Merchant.Owner(0, None, None)
        self.merchant_status: tuple = MerchantStatus.ACTIVE
        self.payment_form: List[dict] = []
        self.enrollment_form: List[dict] = []
        self.accepted_currencies: List[Merchant.AcceptedCurrency] = []

    def __eq__(self, other):
        if not isinstance(other, Merchant):
            return False
        return self.merchant_id == other.merchant_id

    def __lt__(self, other):
        if not isinstance(other, Merchant):
            return False
        return self.merchant_id < other.merchant_id

    def __hash__(self):
        return hash(self.merchant_id)

    def __str__(self):
        return f'#{self.merchant_id}: {self.merchant_code}'

    def __repr__(self):
        return f'Merchant({self.merchant_id}, {self.merchant_code})'

    def serialize(self, is_compact: bool = False) -> dict:
        """
        Serializes the merchant
        Keyword Arguments:
            is_compact {bool} -- Compacts the data only with essential properties (default: {False})
        Returns:
            dict
        """
        if is_compact:
            return CompactMerchantSchema().dump(self)
        return MerchantSchema().dump(self)

    @property
    def is_enabled(self):
        return self.merchant_status[1] != 'closed'

    @staticmethod
    def validate_submitted_info(data: dict):
        try:
            info = SubmittedMerchantInformationSchema().load(data)
            return True, info
        except ValidationError as verr:
            return False, verr

    @staticmethod
    def validate_feature_flags(data: dict) -> Tuple[bool, dict]:
        required_fields = ['canManageProjects',
                           'canManagePaymentMethods',
                           'canAccessReports',
                           'canCopySalesAgents',
                           'canManagePaymentLinks',
                           'canManageNotificationSettings']
        return all(True for k, v in data.items()
                   if v is not None and type(v) is bool and k in required_fields), data

    @staticmethod
    def map(data):
        if not data:
            return None

        merchant = Merchant()
        merchant.merchant_id = data.get('merchant_id')
        merchant.merchant_code = data.get('merchant_code')
        merchant.name = data.get('merchant_name')
        merchant.logo = data.get('merchant_logo_url')
        merchant.timezone = data.get('merchant_timezone')
        merchant.invoicing_mode = data.get('invoicing_mode')
        merchant.category_id = data.get('merchant_category_id')
        merchant.category_name = data.get('merchant_category_name')
        merchant.category_description = data.get('merchant_category_description')
        merchant.address = {
            'address_one': data.get('address_one'),
            'address_two': data.get('address_two'),
            'address_three': data.get('address_three')
        }
        merchant.portal_url = data.get('portal_url')
        merchant.is_public = data.get('is_public')
        merchant.is_active = data.get('is_active')
        merchant.can_manage_projects = data.get('can_manage_projects')
        merchant.can_manage_payment_methods = data.get('can_manage_payment_methods')
        merchant.can_access_reports = data.get('can_access_reports')
        merchant.can_copy_sales_agents = data.get('can_copy_sales_agents')
        merchant.can_manage_payment_links = data.get('can_manage_payment_links')
        merchant.can_manage_notification_settings = data.get('can_manage_notification_settings')
        merchant.projects = (data.get('project_id') if data.get('project_id') else [])

        merchant.is_portals3_configured = bool(data.get('portal3_config'))
        if 'portal3_config' in data:
            portal3_config = data.get('portal3_config')
            if 'secrets' in portal3_config:
                secrets = portal3_config.get('secrets')
                merchant.links_secret = secrets.get('paymentLinks')

            if 'paymentTypes' in portal3_config:
                # This is a workaround to limit create payment link's available payment types.
                # Get the configured payment types for Portals 3 and filter out the list
                p3_ptypes = portal3_config.get('paymentTypes') or {}
                merchant.payment_types = [
                    MerchantPaymentType.map({
                        'payment_type_id': 0,
                        'payment_type_code': key,
                        'payment_type_name': p3_ptypes[key]['name']\
                            if isinstance(p3_ptypes[key], dict) else p3_ptypes[key],
                    })
                    for key in p3_ptypes
                ]
            if 'forms' in portal3_config:
                forms = portal3_config.get('forms')
                merchant.payment_form = _map_form_fields(forms, 'payment')
                merchant.enrollment_form = _map_form_fields(forms, 'enrollment')

            if 'paymentCurrencies' in portal3_config and isinstance(portal3_config['paymentCurrencies'], list):
                merchant.accepted_currencies = []
                for pc in portal3_config['paymentCurrencies']:
                    min_amount = 100 if pc['currency'] == 'PHP' else 1
                    merchant.accepted_currencies.append(Merchant.AcceptedCurrency(
                        currency=pc['currency'],
                        min_amount=min_amount,
                        max_amount=pc['amount']))

        merchant.owner = Merchant.Owner(
            data.get('owner_id'),
            data.get('owner_name'),
            data.get('owner_email_address'))
        merchant.merchant_status = MerchantStatus.get_merchant_status_by_code(data.get('merchant_status', 'active'))

        return merchant


def _map_form_fields(forms: dict, key: str) -> List[dict]:
    """
    Maps the payment/enrollment form.
    """
    form_fields = forms.get(key, {})

    if isinstance(form_fields, list):
        return _flatten_form_fields(form_fields, [])
    if isinstance(form_fields, dict) and isinstance(form_fields.get('fields'), list):
        return _flatten_form_fields(form_fields.get('fields'), [])

    return []


def _flatten_form_fields(form_fields: list, listed_fields: list = []):
    """
    Inspired by server.models.form_fields

    Uses recursion to flatten the hierarchical fields in the payment/enrollment forms
    """
    for field in form_fields:
        if field['fieldType'] == 'row':
            fields = _flatten_form_fields(field['fields'], listed_fields)
            listed_fields = listed_fields + fields
        else:
            listed_fields.append(field)

    return listed_fields
