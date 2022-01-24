import datetime
from dateutil import parser
from marshmallow import Schema, fields, post_dump
from server.models.payment_method_model import PaymentMethod
from server.models.merchant_model import Merchant
from server.models.project_model import Project as MerchantProject
from server.utilities.helper import get_fields_as_dict
from server.utilities.auth import digest
class CompactTransactionSchema(Schema):
    transactionId = fields.Int(attribute='transaction_id')
    externalTransactionId = fields.Str(attribute='external_transaction_id')
    referenceId = fields.Str(attribute='reference_id')
    transactionType = fields.Str(attribute='transaction_type.code')
    transactionStatus = fields.Str(attribute='transaction_status.code')
    invoiceStatus = fields.Str(attribute='invoice_status.code')
    paymentMode = fields.Str(attribute='payment_mode.code')
    paymentType = fields.Str(attribute='payment_type.code')
    paymentTypeName = fields.Str(attribute='payment_type.name')
    paymentMethodName = fields.Str(attribute='payment_method.payment_method_name')
    customerName = fields.Str(attribute='customer.name')
    customerEmail = fields.Str(attribute='customer.email')
    customerPhone = fields.Str(attribute='customer.phone')
    merchantId = fields.Int(attribute='merchant.merchant_id')
    merchantCode = fields.Str(attribute='merchant.merchant_code')
    merchantName = fields.Str(attribute='merchant.name')
    projectId = fields.Str(attribute='project.project_id')
    projectCode = fields.Str(attribute='project.project_code')
    projectKey = fields.Str(attribute='project.project_key')
    projectName = fields.Str(attribute='project.name')
    projectCategory = fields.Str(attribute='project.category')
    transactionSource = fields.Str(attribute='transaction_source')
    baseAmount = fields.Function(lambda t: list(t.base_amount))
    createdAt = fields.DateTime(attribute='created_at', format='iso')
    expiresat = fields.DateTime(attribute='expires_at', format='iso')
    submittedAt = fields.DateTime(attribute='submitted_at', format='iso')
    paidAt = fields.DateTime(attribute='paid_at', format='iso')
    updatedAt = fields.DateTime(attribute='updated_at', format='iso')


class TransactionSchema(Schema):
    transactionId = fields.Int(attribute='transaction_id')
    externalTransactionId = fields.Str(attribute='external_transaction_id')
    referenceId = fields.Str(attribute='reference_id')
    transactionType = fields.Str(attribute='transaction_type.code')
    transactionStatus = fields.Str(attribute='transaction_status.code')
    paymentMode = fields.Str(attribute='payment_mode.code')
    paymentType = fields.Str(attribute='payment_type.code')
    paymentTypeName = fields.Str(attribute='payment_type.name')
    paymentMethodName = fields.Str(attribute='payment_method.payment_method_name')
    customerName = fields.Str(attribute='customer.name')
    customerEmail = fields.Str(attribute='customer.email')
    customerPhone = fields.Str(attribute='customer.phone')
    merchantId = fields.Int(attribute='merchant.merchant_id')
    merchantCode = fields.Str(attribute='merchant.merchant_code')
    merchantName = fields.Str(attribute='merchant.name')
    projectId = fields.Str(attribute='project.project_id')
    projectCode = fields.Str(attribute='project.project_code')
    projectKey = fields.Str(attribute='project.project_key')
    projectName = fields.Str(attribute='project.name')
    projectCategory = fields.Str(attribute='project.category')
    customFields = fields.Function(lambda t: get_fields_as_dict(t.custom_fields))
    # transactionHistory = fields.List(fields.Dict, attribute='transaction_history')
    transactionSource = fields.Str(attribute='transaction_source')
    adminNotes = fields.Str(attribute='admin_notes')
    clientNotes = fields.Str(attribute='client_notes')
    baseAmount = fields.Function(lambda t: list(t.base_amount))
    billBaseAmount = fields.Function(lambda t: list(t.bill_base_amount))
    createdAt = fields.DateTime(attribute='created_at', format='iso')
    expiresat = fields.DateTime(attribute='expires_at', format='iso')
    submittedAt = fields.DateTime(attribute='submitted_at', format='iso')
    paidAt = fields.DateTime(attribute='paid_at', format='iso')
    updatedAt = fields.DateTime(attribute='updated_at', format='iso')


############################################################


class Transaction:
    class LookupItem:
        def __init__(self, lookup_id: int, code: str, name: str):
            self.id: int = lookup_id
            self.code: str = code
            self.name: str = name

        def __str__(self):
            return f'Payment.LookupItem({self.id},{self.code},{self.name})'

        def __repr__(self):
            return f'Payment.LookupItem({self.id},{self.code},{self.name})'

    class Customer:
        def __init__(self, name, email, phone, country_prefix):
            self.name = name
            self.email = email
            self.phone = phone
            self.phone_country_prefix = country_prefix

    def __init__(self):
        self.transaction_id: int = None
        self.external_transaction_id: str = None
        self.reference_id: str = None
        self.invoice_reference_id: str = None
        self.payment_reference_id: str = None
        self.transaction_type: Transaction.LookupItem = None
        self.transaction_status: Transaction.LookupItem = None
        self.invoice_status: Transaction.LookupItem = None
        self.merchant: Merchant = None
        self.project: MerchantProject = None
        self.payment_mode: Transaction.LookupItem = None
        self.payment_type: Transaction.LookupItem = None
        self.payment_method: PaymentMethod = PaymentMethod()
        self.customer: Transaction.Customer = None
        self.custom_fields: list = []
        self.transaction_source: str = None
        self.transaction_ip_address: str = None
        self.transaction_history: list = []
        self.xsrf_key: str = None
        self.is_active: bool = False
        self.base_amount: tuple = ('PHP', 0)
        self.bill_base_amount: tuple = ('PHP', 0)

        self.admin_notes: str = None
        self.client_notes: str = None

        self.expires_at: datetime = None
        self.paid_at: datetime = None
        self.submitted_at: datetime = None
        self.created_at: datetime = None
        self.updated_at: datetime = None

    def serialize(self, is_compact=False):
        if is_compact:
            return CompactTransactionSchema().dump(self)
        return TransactionSchema().dump(self)

    def generate_hmac_signature(self, key):
        msg = PaymentTransactionHMACSchema().dumps(self)
        server_signature = digest(msg=msg, key=key)
        return server_signature

    @staticmethod
    def map_from_row(data: dict):
        if not data:
            return None

        transaction = Transaction()
        transaction.transaction_id = data.get('transaction_id')
        transaction.external_transaction_id = data.get('external_transaction_id')
        transaction.reference_id = data.get('reference_id')
        transaction.transaction_type = Transaction.LookupItem(
            lookup_id=data.get('transaction_type_id'),
            code=data.get('transaction_type_code'),
            name=data.get('transaction_type_name'))
        transaction.transaction_status = Transaction.LookupItem(
            lookup_id=data.get('transaction_status_id'),
            code=data.get('transaction_status_code'),
            name=data.get('transaction_status_name'))

        transaction.merchant = Merchant()
        transaction.merchant.merchant_id = data.get('merchant_id')
        transaction.merchant.merchant_code = data.get('merchant_code')
        transaction.merchant.name = data.get('merchant_name')
        transaction.merchant.invoicing_mode = data.get('invoicing_mode')

        transaction.customer = Transaction.Customer(
            name=data.get('customer_name'),
            email=data.get('customer_email_address'),
            phone=data.get('customer_phone_number'),
            country_prefix=data.get('customer_phone_number_prefix'))

        transaction.project = MerchantProject()
        transaction.project.project_id = data.get('merchant_project_id')
        transaction.project.project_key = data.get('project_key')
        transaction.project.name = data.get('project_name')
        transaction.project.project_code = data.get('project_code')
        transaction.project.category = data.get('project_category')

        transaction.payment_mode = Transaction.LookupItem(
            lookup_id=data.get('payment_mode_id'),
            code=data.get('payment_mode_code'),
            name=data.get('payment_mode_name'))
        transaction.payment_type = Transaction.LookupItem(
            lookup_id=data.get('payment_type_id'),
            code=data.get('payment_type_code'),
            name=data.get('payment_type_name'))

        transaction.payment_method = PaymentMethod.map_from_row(data)
        transaction.client_notes = data.get('client_notes')
        transaction.admin_notes = data.get('admin_notes')
        transaction.custom_fields = data.get('custom_fields')

        transaction.transaction_source = data.get('transaction_source')
        transaction.transaction_ip_address = data.get('transaction_ip_address')
        transaction.transaction_history = data.get('transaction_history')

        transaction.xsrf_key = data.get('xsrf_key')
        transaction.is_active = data.get('is_active')
        transaction.base_amount = (data.get('base_currency'), float(data.get('base_amount')))

        transaction.expires_at = data.get('transaction_expires_at')
        transaction.paid_at = data.get('invoice_paid_at')
        transaction.submitted_at = data.get('invoice_submitted_at')
        transaction.created_at = data.get('transaction_created_at')
        transaction.updated_at = data.get('transaction_updated_at')

        return transaction

class PaymentTransactionHMACSchema(Schema):
    billBaseAmount = fields.Function(lambda t: str(t.base_amount[1]))
    billBaseCurrency = fields.Function(lambda t: t.base_amount[0])
    createdAt = fields.DateTime(attribute='created_at')
    customerEmail = fields.Str(attribute='customer.email')
    customerName = fields.Str(attribute='customer.name')

    @post_dump
    def convertToUtc(self, data, **kwargs): # pylint: disable=unused-argument
        key = 'createdAt'
        value = data[key]
        orig_dt = parser.parse(value)
        utc_time_value = orig_dt - orig_dt.utcoffset()
        utc_dt = utc_time_value.replace(tzinfo=None)
        data[key] = utc_dt.strftime('%Y-%m-%d %H:%M:%S.%f')

        return data
    class Meta:
        ordered = True