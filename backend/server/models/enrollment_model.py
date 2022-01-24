from datetime import datetime
from dateutil.relativedelta import relativedelta
from marshmallow import Schema, fields
from server.config.logger import log
from server.models.payment_method_model import PaymentMethod
from server.models.merchant_model import Merchant
from server.models.project_model import Project as MerchantProject
from server.utilities.code_generator import generate_ref_id
from server.utilities.helper import get_fields_as_dict, transform_dict_to_list

MAX_ALLOWED_MONTHS = 240

class CompactEnrollmentSchema(Schema):
    externalTransactionId = fields.Str(attribute='external_transaction_id')
    enrollmentReferenceId = fields.Str(attribute='transaction_reference_id')
    transactionId = fields.Str(attribute='transaction_id')
    transactionType = fields.Str(attribute='transaction_type.code')
    transactionStatus = fields.Str(attribute='transaction_status.code')
    paymentMode = fields.Str(attribute='payment_mode.code')
    paymentType = fields.Str(attribute='payment_type.code')
    paymentTypeName = fields.Str(attribute='payment_type.name')
    customerName = fields.Str(attribute='customer.name')
    customerEmail = fields.Str(attribute='customer.email')
    customerPhone = fields.Str(attribute='customer.phone')
    merchantId = fields.Int(attribute='merchant.merchant_id')
    merchantCode = fields.Str(attribute='merchant.merchant_code')
    merchantName = fields.Str(attribute='merchant.name')
    projectCode = fields.Str(attribute='project.project_code')
    projectId = fields.Str(attribute='project.project_id')
    projectName = fields.Str(attribute='project.name')
    projectCategory = fields.Str(attribute='project.category')
    baseAmount = fields.Function(lambda t: [t.base_currency, t.base_amount])
    enrollmentStartDate = fields.DateTime(attribute='enrollment_start_date')
    enrollmentEndDate = fields.Function(lambda e: e.end_date().isoformat() if e.end_date() else None)
    enrollmentMonths = fields.Int(attribute='enrollment_months')
    createdAt = fields.DateTime(attribute='transaction_created_at', format='iso')


class EnrollmentSchema(Schema):
    externalTransactionId = fields.Str(attribute='external_transaction_id')
    enrollmentReferenceId = fields.Str(attribute='transaction_reference_id')
    transactionId = fields.Str(attribute='transaction_id')
    transactionType = fields.Str(attribute='transaction_type.code')
    transactionStatus = fields.Str(attribute='transaction_status.code')
    status = fields.Str(attribute='payment_status.code')
    paymentMode = fields.Str(attribute='payment_mode.code')
    paymentType = fields.Str(attribute='payment_type.code')
    paymentTypeName = fields.Str(attribute='payment_type.name')
    customerName = fields.Str(attribute='customer.name')
    customerEmail = fields.Str(attribute='customer.email')
    customerPhone = fields.Str(attribute='customer.phone')
    merchantId = fields.Int(attribute='merchant.merchant_id')
    merchantCode = fields.Str(attribute='merchant.merchant_code')
    merchantName = fields.Str(attribute='merchant.name')
    projectCode = fields.Str(attribute='project.project_code')
    projectName = fields.Str(attribute='project.name')
    projectCategory = fields.Str(attribute='project.category')
    customFields = fields.Function(lambda t: get_fields_as_dict(t.custom_fields))
    baseAmount = fields.Function(lambda t: [t.base_currency, t.base_amount])
    paymentMethodId = fields.Int(attribute='payment_method.payment_method_id')
    paymentMethodName = fields.Str(attribute='payment_method.payment_method_name')
    paymentMethodProcessor = fields.Str(attribute='payment_method.payment_method_processor')
    paymentMethodType = fields.Str(attribute='payment_method.payment_method_type')
    paymentMethodStatus = fields.Str(attribute='payment_method.status')
    paymentMethodProvider = fields.Str(attribute='payment_method.provider')
    paymentMethodExpiry = fields.Str(attribute='payment_method.expiry')
    paymentMethodOrigin = fields.Str(attribute='payment_method.origin')
    paymentMethodIssuer = fields.Str(attribute='payment_method.issuer')
    paymentMethodProcessorId = fields.Function(
        lambda t: t.payment_method.processor_id())
    paymentMethodCardLastFour = fields.Function(
        lambda t: t.payment_method.card_last_four())
    paymentMethodCustomerName = fields.Function(
        lambda t: t.payment_method.payment_method_full_name())
    paymentMethodBillingAddress = fields.Function(
        lambda t: t.payment_method.billing_address())
    enrollmentStartDate = fields.DateTime(attribute='enrollment_start_date')
    enrollmentEndDate = fields.Function(lambda e: e.end_date().isoformat() if e.end_date() else None)
    enrollmentMonths = fields.Int(attribute='enrollment_months')
    enrollmentComment = fields.Str(attribute='enrollment_comment')
    createdAt = fields.DateTime(attribute='transaction_created_at', format='iso')


class ExportEnrollmentSchema(Schema):
    externalTransactionId = fields.Str(attribute='external_transaction_id')
    enrollmentReferenceId = fields.Str(attribute='transaction_reference_id')
    transactionId = fields.Str(attribute='transaction_id')
    transactionType = fields.Str(attribute='transaction_type.code')
    transactionStatus = fields.Str(attribute='transaction_status.code')
    paymentType = fields.Str(attribute='payment_type.name')
    customerName = fields.Str(attribute='customer.name')
    customerEmail = fields.Str(attribute='customer.email')
    customerPhone = fields.Str(attribute='customer.phone')
    merchantId = fields.Int(attribute='merchant.merchant_id')
    merchantCode = fields.Str(attribute='merchant.merchant_code')
    merchantName = fields.Str(attribute='merchant.name')
    projectCode = fields.Str(attribute='project.project_code')
    projectName = fields.Str(attribute='project.name')
    projectCategory = fields.Str(attribute='project.category')
    baseAmount = fields.Float(attribute='base_amount')
    baseCurrency = fields.Str(attribute='base_currency')
    paymentMethodId = fields.Int(attribute='payment_method.payment_method_id')
    paymentMethodName = fields.Str(attribute='payment_method.payment_method_name')
    paymentMethodProcessor = fields.Str(attribute='payment_method.payment_method_processor')
    paymentMethodType = fields.Str(attribute='payment_method.payment_method_type')
    paymentMethodStatus = fields.Str(attribute='payment_method.status')
    paymentMethodProvider = fields.Str(attribute='payment_method.provider')
    paymentMethodExpiry = fields.Function(lambda t: t.payment_method.payment_method_expiry())
    paymentMethodOrigin = fields.Str(attribute='payment_method.origin')
    paymentMethodIssuer = fields.Str(attribute='payment_method.issuer')
    paymentMethodCustomerName = fields.Function(lambda t: t.payment_method.payment_method_full_name())
    enrollmentStartDate = fields.DateTime(attribute='enrollment_start_date')
    enrollmentEndDate = fields.Function(lambda e: e.end_date().isoformat() if e.end_date() else None)
    enrollmentMonths = fields.Str(attribute='enrollment_months')
    transactionSource = fields.Str(attribute='friendly_source_name')
    createdAt = fields.DateTime(attribute='transaction_created_at', format='iso')


class Enrollment:
    class LookupItem:
        def __init__(self, item_id: int, code: str, name: str):
            self.id: int = item_id
            self.code: str = code
            self.name: str = name

        def __str__(self):
            return f'Payment.LookupItem({self.id},{self.code},{self.name})'

        def __repr__(self):
            return f'Payment.LookupItem({self.id},{self.code},{self.name})'

    class Bill:
        def __init__(self):
            self.total = ('PHP', 0)
            self.base = ('PHP', 0)
            self.fee = ('PHP', 0)
            self.converted = ('PHP', 0)
            # base, target, amount
            self.qwx_rate = ('USD', 'PHP', 0)
            self.ox_rate = ('USD', 'PHP', 0)

    class Customer:
        def __init__(self, name: str, email: str, phone: str, country_prefix: str):
            self.name = name
            self.email = email
            self.phone = phone
            self.phone_country_prefix = country_prefix

    def __init__(self):
        self.transaction_id: int = 0
        self.merchant: Merchant = None

        self.external_transaction_id: str = None
        self.transaction_reference_id: str = None

        self.transaction_type: Enrollment.LookupItem = None
        self.transaction_status: Enrollment.LookupItem = None
        self.payment_type: Enrollment.LookupItem = None
        self.payment_mode: Enrollment.LookupItem = None

        self.customer: Enrollment.Customer = None
        self.project: MerchantProject = None
        self.payment_method: PaymentMethod = None
        self.custom_fields: dict = {}

        self.client_notes: str = None
        self.admin_notes: str = None
        self.transaction_source: str = None
        self.transaction_ip_address: str = None
        self.transaction_history: list = []
        self.xsrf_key: str = None
        self.is_active: bool = False

        self.base_currency: str = 'USD'
        self.base_amount: float = 0
        self.enrollment_months: int = 0
        self.enrollment_start_date: datetime = None
        self.enrollment_is_processing = False
        self.enrollment_comment: str = None
        self.enrollment_status_updated_at: datetime = None

        self.transaction_expires_at: datetime = None
        self.transaction_created_at: datetime = None
        self.transaction_updated_at: datetime = None

    @property
    def friendly_source_name(self) -> str:
        sources = {
            'merchant-portal': 'Payment Portals v2',
            'portal3': 'Payment Portals v3',
        }
        return sources.get(self.transaction_source) or 'Others'

    def serialize(self, is_compact=False, is_export=False, with_custom_fields=False):
        """
        Serializes the enrollment transactions
        """
        payment = self
        data = CompactEnrollmentSchema().dump(payment) if is_compact\
            else ExportEnrollmentSchema().dump(payment) if is_export\
                else EnrollmentSchema().dump(payment)

        if with_custom_fields:
            custom_fields = self.custom_fields_list()
            for custom_field in custom_fields:
                data[custom_field.get('name')] = custom_field.get('value')
        return data

    def end_date(self) -> datetime:
        try:
            if not (self.enrollment_start_date and self.enrollment_months):
                return None
            if self.enrollment_months > MAX_ALLOWED_MONTHS:
                return None
            # Please note that the -1 month is because the start date is inclusive of the total months
            return self.enrollment_start_date + relativedelta(months=self.enrollment_months - 1)
        except ValueError:
            return None

    def custom_fields_list(self):
        tx_fields = self.custom_fields.get('transaction', []) + self.custom_fields.get('project', [])
        contract = self.custom_fields.get('contract', {})
        qwikpay = self.custom_fields.get('qwikpay', {})
        metadata = self.custom_fields.get('metadata', {})
        project_fields = self.project.project_fields.get('fields', [])\
            if self.project and self.project.project_fields else []
        return (
            transform_dict_to_list(qwikpay) +
            transform_dict_to_list(contract) +
            transform_dict_to_list(metadata) +
            [
                {'value': f.get('value'), 'name': f.get('name'), 'text': f.get('text')}
                for f in project_fields if 'text' in f
            ] +
            [
                {'value': f.get('value'), 'name': f.get('name'), 'text': f.get('text')}
                for f in tx_fields if 'text' in f
            ]
        )

    def generate_scheduled_invoices(self) -> list:
        ref_id = self.transaction_reference_id
        try:
            month_span = int(self.enrollment_months)
            # if the months are below 1 and greater than 20 years, return []
            if month_span > MAX_ALLOWED_MONTHS or month_span <= 0:
                return []

            return [
                {
                    'referenceId': generate_ref_id('Invoice'),
                    'description': '{} Auto Debit Enrollment ID: {} - Payment #{}'.format(
                        self.merchant.name,
                        ref_id,
                        index + 1
                    ),
                    'dueAt': self.enrollment_start_date + relativedelta(months=index)
                }
                for index in list(range(0, month_span))
            ]
        except ValueError as value_err:
            log.error(f'Generate scheduled invoices {ref_id} value error: {value_err}')
            return []
        except AttributeError as attr_err:
            log.error(f'Generate scheduled invoices {ref_id} attribute error: {attr_err}')
            return []
        except TypeError as type_err:
            log.error(f'Generate scheduled invoices {ref_id} attribute error: {type_err}')
            return []

    def __str__(self):
        tx_id = self.transaction_id
        ex_tx_id = self.external_transaction_id
        ref_id = self.external_transaction_id
        merchant = self.merchant.merchant_code
        status = self.transaction_status.code
        return f'Enrollment: [{status}] {tx_id} - {merchant}/{ex_tx_id}/{ref_id}]'

    def __repr__(self):
        tx_id = self.transaction_id
        ex_tx_id = self.external_transaction_id
        merchant = self.merchant.merchant_code
        return f'Enrollment({tx_id}, {merchant}, {ex_tx_id}'

    @staticmethod
    def map(data: dict):
        if not data:
            return None

        enrollment = Enrollment()
        enrollment.transaction_id = data.get('transaction_id')
        enrollment.external_transaction_id = data.get('external_transaction_id')
        enrollment.transaction_reference_id = data.get('reference_id')

        enrollment.transaction_type = Enrollment.LookupItem(
            item_id=data.get('transaction_type_id'),
            code=data.get('transaction_type_code'),
            name=data.get('transaction_type_name'))
        enrollment.transaction_status = Enrollment.LookupItem(
            item_id=data.get('transaction_status_id'),
            code=data.get('transaction_status_code'),
            name=data.get('transaction_status_name'))

        enrollment.merchant = Merchant()
        enrollment.merchant.merchant_id = data.get('merchant_id')
        enrollment.merchant.merchant_code = data.get('merchant_code')
        enrollment.merchant.name = data.get('merchant_name')
        enrollment.merchant.invoicing_mode = data.get('invoicing_mode')

        enrollment.customer = Enrollment.Customer(
            name=data.get('customer_name'),
            email=data.get('customer_email_address'),
            phone=data.get('customer_phone_number'),
            country_prefix=data.get('customer_phone_number_prefix'))

        enrollment.project = MerchantProject()
        enrollment.project.project_id = data.get('merchant_project_id')
        enrollment.project.project_key = data.get('project_key')
        enrollment.project.name = data.get('project_name')
        enrollment.project.project_code = data.get('project_code')
        enrollment.project.category = data.get('project_category')
        enrollment.project.description = data.get('project_description')
        enrollment.project.source = data.get('project_source')
        enrollment.project.project_fields = data.get('project_fields')

        enrollment.payment_mode = Enrollment.LookupItem(
            item_id=data.get('payment_mode_id'),
            code=data.get('payment_mode_code'),
            name=data.get('payment_mode_name'))
        enrollment.payment_type = Enrollment.LookupItem(
            item_id=data.get('payment_type_id'),
            code=data.get('payment_type_code'),
            name=data.get('payment_type_name'))
        enrollment.payment_method = PaymentMethod.map_from_row(data)

        enrollment.custom_fields = data.get('custom_fields')
        enrollment.admin_notes = data.get('admin_notes')
        enrollment.client_notes = data.get('client_notes')
        enrollment.transaction_source = data.get('transaction_source')
        enrollment.transaction_ip_address = data.get('transaction_ip_address')
        enrollment.transaction_history = data.get('transaction_history')
        enrollment.xsrf_key = data.get('xsrf_key')
        enrollment.is_active = data.get('is_active')

        enrollment.base_currency = data.get('base_currency')
        enrollment.base_amount = float(data.get('base_amount'))
        enrollment.enrollment_months = data.get('enrollment_months')
        enrollment.enrollment_start_date = data.get('enrollment_start_date')
        enrollment.enrollment_is_processing = data.get('enrollment_is_processing')
        enrollment.enrollment_comment = data.get('enrollment_comment')
        enrollment.enrollment_status_updated_at = data.get('enrollment_status_updated_at')

        enrollment.transaction_expires_at = data.get('transaction_expires_at')
        enrollment.transaction_created_at = data.get('transaction_created_at')
        enrollment.transaction_updated_at = data.get('transaction_updated_at')

        return enrollment
