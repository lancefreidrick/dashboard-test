from typing import Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from pytz import timezone
import pytz
from marshmallow import Schema, fields, ValidationError, validate
from server.models.payment_method_model import PaymentMethod
from server.models.merchant_model import Merchant
from server.models.project_model import Project as MerchantProject
from server.utilities.helper import get_fields_as_dict, transform_dict_to_list


class PaymentSchema(Schema):
    invoiceId = fields.Str(attribute='invoice_id')
    transactionId = fields.Str(attribute='transaction_id')
    externalTransactionId = fields.Str(attribute='external_transaction_id')
    paymentReferenceId = fields.Str(attribute='payment_reference_id')
    invoiceReferenceId = fields.Str(attribute='invoice_reference_id')
    transactionReferenceId = fields.Str(attribute='transaction_reference_id')
    settlementReferenceId = fields.Str(attribute='settlement_reference_id')
    settlementId = fields.Int(attribute='settlement_id')
    transactionType = fields.Str(attribute='transaction_type.code')
    transactionStatus = fields.Str(attribute='transaction_status.code')
    paymentStatus = fields.Str(attribute='payment_status.code')
    paymentMode = fields.Str(attribute='payment_mode.code')
    paymentType = fields.Str(attribute='payment_type.code')
    paymentTypeName = fields.Str(attribute='payment_type.name')
    customerName = fields.Str(attribute='customer.name')
    customerEmail = fields.Str(attribute='customer.email')
    customerPhone = fields.Str(attribute='customer.phone')
    merchantId = fields.Int(attribute='merchant.merchant_id')
    merchantCode = fields.Str(attribute='merchant.merchant_code')
    merchantName = fields.Str(attribute='merchant.name')
    projectId = fields.Int(attribute='project.project_id')
    projectCode = fields.Str(attribute='project.project_code')
    projectName = fields.Str(attribute='project.name')
    projectCategory = fields.Str(attribute='project.category')
    billBase = fields.Function(lambda t: list(t.bill.base))
    billConverted = fields.Function(lambda t: list(t.bill.converted))
    billFee = fields.Function(lambda t: list(t.bill.fee))
    billTotal = fields.Function(lambda t: list(t.bill.total))
    refundTotal = fields.Function(lambda t: list(t.bill.refund))
    waivedFee = fields.Function(lambda t: list(t.bill.waived_fee))
    net = fields.Function(lambda t: list(t.bill.net))
    qwxRate = fields.Function(lambda t: list(t.bill.qwx_rate))
    oxRate = fields.Function(lambda t: list(t.bill.ox_rate))
    customFields = fields.Function(lambda t: get_fields_as_dict(t.custom_fields))
    clientNotes = fields.Str(attribute='client_notes')
    adminNotes = fields.Str(attribute='admin_notes')
    refundReason = fields.Str(attribute='refund_reason')
    retryAttemptCount = fields.Int(attribute='retry_attempt_count')
    paymentMethodId = fields.Int(attribute='payment_method.payment_method_id')
    paymentMethodName = fields.Str(attribute='payment_method.payment_method_name')
    paymentMethodProcessor = fields.Str(attribute='payment_method.payment_method_processor')
    paymentMethodType = fields.Str(attribute='payment_method.payment_method_type')
    paymentMethodStatus = fields.Str(attribute='payment_method.status')
    paymentMethodProvider = fields.Str(attribute='payment_method.provider')
    paymentMethodExpiry = fields.Function(lambda t: t.payment_method.payment_method_expiry())
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
    transactionSource = fields.Str(attribute='transaction_source')
    expiresAt = fields.DateTime(attribute='transaction_expires_at', format='iso')
    createdAt = fields.DateTime(attribute='transaction_created_at', format='iso')
    updatedAt = fields.DateTime(attribute='transaction_updated_at', format='iso')
    paidAt = fields.DateTime(attribute='invoice_paid_at', format='iso')
    submittedAt = fields.DateTime(attribute='invoice_submitted_at', format='iso')
    dueAt = fields.DateTime(attribute='invoice_due_at', format='iso')
    invoiceCreatedAt = fields.DateTime(attribute='invoice_created_at', format='iso')
    invoiceUpdatedAt = fields.DateTime(attribute='invoice_updated_at', format='iso')
    settledDate = fields.DateTime(attribute='settled_date', format='iso')


class CompactPaymentSchema(Schema):
    invoiceId = fields.Str(attribute='invoice_id')
    transactionId = fields.Str(attribute='transaction_id')
    externalTransactionId = fields.Str(attribute='external_transaction_id')
    paymentReferenceId = fields.Str(attribute='payment_reference_id')
    invoiceReferenceId = fields.Str(attribute='invoice_reference_id')
    transactionReferenceId = fields.Str(attribute='transaction_reference_id')
    settlementReferenceId = fields.Str(attribute='settlement_reference_id')
    transactionType = fields.Str(attribute='transaction_type.code')
    transactionStatus = fields.Str(attribute='transaction_status.code')
    paymentStatus = fields.Str(attribute='payment_status.code')
    paymentMode = fields.Str(attribute='payment_mode.code')
    paymentType = fields.Str(attribute='payment_type.code')
    paymentTypeName = fields.Str(attribute='payment_type.name')
    customerName = fields.Str(attribute='customer.name')
    customerEmail = fields.Str(attribute='customer.email')
    customerPhone = fields.Str(attribute='customer.phone')
    merchantCode = fields.Str(attribute='merchant.merchant_code')
    merchantName = fields.Str(attribute='merchant.name')
    projectId = fields.Int(attribute='project.project_id')
    projectCode = fields.Str(attribute='project.project_code')
    projectName = fields.Str(attribute='project.name')
    projectCategory = fields.Str(attribute='project.category')
    billBase = fields.Function(lambda t: list(t.bill.base))
    billConverted = fields.Function(lambda t: list(t.bill.converted))
    billFee = fields.Function(lambda t: list(t.bill.fee))
    billTotal = fields.Function(lambda t: list(t.bill.total))
    waivedFee = fields.Function(lambda t: list(t.bill.waived_fee))
    net = fields.Function(lambda t: list(t.bill.net))
    qwxRate = fields.Function(lambda t: list(t.bill.qwx_rate))
    oxRate = fields.Function(lambda t: list(t.bill.ox_rate))
    transactionSource = fields.Str(attribute='transaction_source')
    paymentMethodName = fields.Str(attribute='payment_method.payment_method_name')
    expiresAt = fields.DateTime(attribute='transaction_expires_at', format='iso')
    createdAt = fields.DateTime(attribute='transaction_created_at', format='iso')
    updatedAt = fields.DateTime(attribute='transaction_updated_at', format='iso')
    paidAt = fields.DateTime(attribute='invoice_paid_at', format='iso')
    submittedAt = fields.DateTime(attribute='invoice_submitted_at', format='iso')
    dueAt = fields.DateTime(attribute='invoice_due_at', format='iso')
    invoiceCreatedAt = fields.DateTime(attribute='invoice_created_at', format='iso')
    invoiceUpdatedAt = fields.DateTime(attribute='invoice_updated_at', format='iso')


class ExportPaymentSchema(Schema):
    invoiceId = fields.Str(attribute='invoice_id')
    transactionId = fields.Str(attribute='transaction_id')
    externalTransactionId = fields.Str(attribute='external_transaction_id')
    paymentReferenceId = fields.Str(attribute='payment_reference_id')
    invoiceReferenceId = fields.Str(attribute='invoice_reference_id')
    transactionReferenceId = fields.Str(attribute='transaction_reference_id')
    settlementReferenceId = fields.Str(attribute='settlement_reference_id')
    transactionType = fields.Str(attribute='transaction_type.code')
    transactionStatus = fields.Str(attribute='transaction_status.code')
    paymentStatus = fields.Str(attribute='payment_status.code')
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
    baseCurrency = fields.Function(lambda t: t.bill.base[0] if t.bill and t.bill.base else None)
    baseAmount = fields.Function(lambda t: t.bill.base[1] if t.bill and t.bill.base else None)
    convertedCurrency = fields.Function(lambda t: t.bill.converted[0] if t.bill and t.bill.converted else None)
    convertedAmount = fields.Function(lambda t: t.bill.converted[1] if t.bill and t.bill.converted else None)
    feeCurrency = fields.Function(lambda t: t.bill.fee[0] if t.bill and t.bill.fee else None)
    feeAmount = fields.Function(lambda t: t.bill.fee[1] if t.bill and t.bill.fee else None)
    totalCurrency = fields.Function(lambda t: t.bill.total[0] if t.bill and t.bill.total else None)
    totalAmount = fields.Function(lambda t: t.bill.total[1] if t.bill and t.bill.total else None)
    waivedFeeCurrency = fields.Function(
        lambda t: t.bill.waived_fee[0] if t.bill and t.bill.waived_fee else None)
    waivedFeeAmount = fields.Function(
        lambda t: t.bill.waived_fee[1] if t.bill and t.bill.waived_fee else None)
    netCurrency = fields.Function(
        lambda t: t.bill.net[0] if t.bill and t.bill.net else None)
    netAmount = fields.Function(
        lambda t: t.bill.net[1] if t.bill and t.bill.net else None)
    qwxRate = fields.Function(lambda t: list(t.bill.qwx_rate))
    oxRate = fields.Function(lambda t: list(t.bill.ox_rate))
    clientNotes = fields.Str(attribute='client_notes')
    adminNotes = fields.Str(attribute='admin_notes')
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
    transactionSource = fields.Str(attribute='friendly_source_name')
    settledDate = fields.DateTime(attribute='settled_date', format='iso')
    expiresAt = fields.DateTime(attribute='transaction_expires_at', format='iso')
    createdAt = fields.DateTime(attribute='transaction_created_at', format='iso')
    updatedAt = fields.DateTime(attribute='transaction_updated_at', format='iso')
    paidAt = fields.DateTime(attribute='invoice_paid_at', format='iso')
    submittedAt = fields.DateTime(attribute='invoice_submitted_at', format='iso')
    dueAt = fields.DateTime(attribute='invoice_due_at', format='iso')
    reportAt = fields.Str(attribute='report_at')
    invoiceCreatedAt = fields.DateTime(attribute='invoice_created_at', format='iso')
    invoiceUpdatedAt = fields.DateTime(attribute='invoice_updated_at', format='iso')


class SubmittedRefundRequest(Schema):
    currency = fields.Str(required=True, data_key='refundTotalCurrency')
    amount = fields.Float(required=True, data_key='refundTotalAmount')
    reason = fields.Str(required=True, data_key='refundReason')
    notes = fields.Str(required=False, data_key='refundNotes')


class SubmittedPaymentRequest(Schema):
    total_currency = fields.Str(required=True, data_key='billTotalCurrency')
    total_amount = fields.Float(required=True, data_key='billTotalAmount')
    fee_currency = fields.Str(required=True, data_key='billFeeCurrency')
    fee_amount = fields.Float(required=True, data_key='billFeeAmount')
    converted_currency = fields.Str(required=True, data_key='convertedCurrency')
    converted_amount = fields.Float(required=True, data_key='convertedAmount')
    qwx_rate_base_currency = fields.Str(required=True, data_key='exchangeRateBaseCurrency')
    qwx_rate_target_currency = fields.Str(required=True, data_key='exchangeRateConvertedCurrency')
    qwx_rate_amount = fields.Float(required=True, data_key='exchangeRateAmount')
    source = fields.Str(required=True, data_key='paymentMethodSource')
    origin = fields.Str(required=True, data_key='paymentMethodOrigin')
    notes = fields.Str(required=False, data_key='paymentMethodNotes')


class BasePaymentLinkRequest(Schema):
    project_id = fields.Int(required=False, allow_none=True, data_key='project')
    payment_type_code = fields.Str(required=False, allow_none=True, data_key='paymentType')
    customer_name = fields.Str(required=True, data_key='customerName',
        validate=validate.Length(min=3, max=100))
    customer_email = fields.Email(required=True, data_key='customerEmail')
    mobile_number = fields.Str(required=True, data_key='mobileNumber')
    mobile_number_country_code = fields.Str(required=True, data_key='mobileNumberCountryCode')
    mobile_number_dial_code = fields.Str(required=True, data_key='mobileNumberDialCode')
    expire_time_in_hrs = fields.Int(required=True, data_key='expireTime',
        validate=validate.OneOf([3, 6, 12, 24, 48, 72, 96, 120, 144, 168]))
    client_notes = fields.Str(required=True, allow_none=True, data_key='clientNotes',
        validate=validate.Length(min=0, max=500))
    external_transaction_id = fields.Str(required=False, data_key='externalTransactionId', allow_none=True,
        validate=validate.Length(max=18))


class Payment:
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
            self.refund = ('PHP', 0)
            self.waived_fee = ('PHP', 0)
            self.net = ('PHP', 0)
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
        self.invoice_id: int = 0
        self.transaction_id: int = 0
        self.merchant: Merchant = None

        self.external_transaction_id: str = None
        self.transaction_reference_id: str = None
        self.payment_reference_id: str = None
        self.invoice_reference_id: str = None
        self.settlement_reference_id: str = None
        self.settlement_id: int = None

        self.transaction_type: Payment.LookupItem = None
        self.payment_status: Payment.LookupItem = None
        self.transaction_status: Payment.LookupItem = None
        self.payment_type: Payment.LookupItem = None
        self.payment_mode: Payment.LookupItem = None

        self.customer: Payment.Customer = None
        self.project: MerchantProject = None
        self.payment_method: PaymentMethod = None
        self.bill: Payment.Bill = Payment.Bill()
        self.custom_fields: list = []

        self.refund_reason: str = None
        self.client_notes: str = None
        self.admin_notes: str = None
        self.transaction_source: str = None
        self.transaction_ip_address: str = None
        self.transaction_history: list = []
        self.xsrf_key: str = None
        self.is_active: bool = False
        self.processor_code: str = None
        self.processor_data: dict = {}
        self.invoice_description: str = None
        self.invoice_breakdown: str = None
        self.retry_attempt_count: int = 0
        self.is_posted: bool = False
        self.posted_to: str = None

        self.transaction_expires_at: datetime = None
        self.transaction_created_at: datetime = None
        self.transaction_updated_at: datetime = None
        self.invoice_due_at: datetime = None
        self.invoice_submitted_at: datetime = None
        self.invoice_paid_at: datetime = None
        self.invoice_created_at: datetime = None
        self.invoice_updated_at: datetime = None

        self.settlement_id: int = 0
        self.settlement_reference_id: str = None
        self.settled_date: datetime = None

        # Temporary variables for now
        self.refund_notes: str = None
        self.complete_notes: str = None

    def __str__(self):
        return (
            f'{self.merchant.merchant_code}/{self.transaction_id} {self.payment_reference_id} '
            f'[{self.transaction_status.code}] {self.transaction_source}'
        )

    def serialize(self, is_compact=False, is_export=False, with_custom_fields=False, tz_info='Asia/Manila'):
        """
        Serializes the payment transactions
        """
        payment = self
        data = CompactPaymentSchema().dump(payment) if is_compact\
            else ExportPaymentSchema().dump(payment) if is_export\
                else PaymentSchema().dump(payment)

        # Change the timestamp based on the timezone for the four fields only.
        if is_export:
            date_fields = ['createdAt', 'paidAt', 'settledDate', 'dueAt']
            for dtf in date_fields:
                if data[dtf]:
                    timestamp_value = datetime.fromisoformat(data[dtf])
                    data[dtf] = timestamp_value.astimezone(timezone(tz_info))

        if with_custom_fields:
            custom_fields = self.custom_fields_list()
            for custom_field in custom_fields:
                data[custom_field.get('name')] = custom_field.get('value')
        return data

    def custom_fields_list(self):
        tx_fields = self.custom_fields.get('transaction', []) or [] + \
            self.custom_fields.get('project', []) or []
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

    @property
    def friendly_source_name(self) -> str:
        sources = {
            'merchant-portal': 'Payment Portals v2',
            'portal3': 'Payment Portals v3',
            'api': 'Access API',
            'payment-link': 'Payment Links',
        }
        return sources.get(self.transaction_source) or 'Others'

    @property
    def report_at(self) -> str:
        iso_date_format = '%Y-%m-%d'
        if self.payment_status.code not in ['PAID', 'SETTLED']:
            return None

        # e.g. August 10 is (August 9, 4:01pm - August 10, 4:00pm)
        base_date = self.invoice_paid_at or self.invoice_created_at
        threshold_date = base_date.replace(
            hour=16, minute=0, second=0, microsecond=0,
            tzinfo=pytz.timezone(self.merchant.timezone or 'Asia/Manila'))

        if base_date < threshold_date:
            return threshold_date.strftime(iso_date_format)

        next_day = threshold_date + timedelta(days=1)
        return next_day.strftime(iso_date_format)

    @property
    def is_refund_valid(self):
        return (
            self.bill.refund[0] == self.bill.total[0]
            and self.bill.refund[1] >= 1
            and self.bill.refund[1] <= self.bill.converted[1]
        )

    def validate_refund(self, data: dict):
        try:
            refund_request = SubmittedRefundRequest().load(data)
            self.bill.refund = [refund_request.get('currency'), refund_request.get('amount')]
            self.refund_reason = refund_request.get('reason')

            self.refund_notes = (
                refund_request.get('notes') or
                f'Payment has been refunded with a reason: {self.refund_reason}'
            )

            if not self.is_refund_valid:
                raise ValidationError('Refund amount has exceeded the total amount')

            return True, None
        except ValidationError as verr:
            return False, verr

    def validate_submitted_payment_request(self, data: dict):
        try:
            payment_request = SubmittedPaymentRequest().load(data)
            self.bill.total = [
                payment_request.get('total_currency'),
                payment_request.get('total_amount')
            ]
            self.bill.fee = [
                payment_request.get('fee_currency'),
                payment_request.get('fee_amount')
            ]
            self.bill.qwx_rate = [
                payment_request.get('qwx_rate_base_currency'),
                payment_request.get('qwx_rate_target_currency'),
                payment_request.get('qwx_rate_amount')
            ]
            self.bill.converted = [
                payment_request.get('converted_currency'),
                payment_request.get('converted_amount')
            ]
            self.complete_notes = payment_request.get('notes')
            self.payment_method.origin = payment_request.get('origin')
            self.payment_method.issuer = payment_request.get('source')

            return True, None
        except ValidationError as verr:
            return False, verr

    @staticmethod
    def map(data: dict):
        if not data:
            return None

        payment = Payment()
        payment.invoice_id = data.get('invoice_id')
        payment.transaction_id = data.get('transaction_id')
        payment.external_transaction_id = data.get('external_transaction_id')
        payment.transaction_reference_id = data.get('reference_id')
        payment.invoice_reference_id = data.get('invoice_reference_id')
        payment.payment_reference_id = data.get('payment_reference_id')
        payment.settlement_id = data.get('settlement_id')

        payment.transaction_type = Payment.LookupItem(
            item_id=data.get('transaction_type_id'),
            code=data.get('transaction_type_code') or {
                10: 'PAYMENT',
                20: 'ENROLLMENT',
                30: 'LOAN'
            }.get(data.get('transaction_type_id')) or 'NONE',
            name=data.get('transaction_type_name') or {
                10: 'Payment',
                20: 'Enrollment',
                30: 'Loan'
            }.get(data.get('transaction_type_id')) or 'None')
        payment.transaction_status = Payment.LookupItem(
            item_id=data.get('transaction_status_id'),
            code=data.get('transaction_status_code') or {
                1: 'INC',
                2: 'SUCCESS',
                3: 'FAIL',
                4: 'ONGOING',
                5: 'FOR REVIEW',
                6: 'DECLINED',
                7: 'CANCELLED',
                8: 'DONE',
                9: 'PENDING'
            }.get(data.get('transaction_status_id')) or 'NONE',
            name=data.get('transaction_status_name') or {
                1: 'Incomplete',
                2: 'Successful',
                3: 'Failed',
                4: 'Ongoing',
                5: 'For Review',
                6: 'Declined',
                7: 'Cancelled',
                8: 'Done',
                9: 'Pending'
            }.get(data.get('transaction_status_id')) or 'NONE')
        payment.payment_status = Payment.LookupItem(
            item_id=data.get('invoice_status_id'),
            code=data.get('invoice_status_code') or {
                1: 'PAID',
                2: 'SCHED',
                3: 'FAIL',
                4: 'CANCELLED',
                5: 'SETTLED',
                6: 'REFUNDED',
                7: 'PENDING',
                8: 'DISPUTED'
            }.get(data.get('invoice_status_id')) or 'NONE',
            name=data.get('invoice_status_name') or {
                1: 'Paid',
                2: 'Scheduled',
                3: 'Failed',
                4: 'Cancelled',
                5: 'Settled',
                6: 'Refunded',
                7: 'Pending',
                8: 'Disputed'
            }.get(data.get('invoice_status_id')) or 'None')

        payment.merchant = Merchant()
        payment.merchant.merchant_id = data.get('merchant_id')
        payment.merchant.merchant_code = data.get('merchant_code')
        payment.merchant.name = data.get('merchant_name')
        payment.merchant.invoicing_mode = data.get('invoicing_mode')

        payment.customer = Payment.Customer(
            name=data.get('customer_name'),
            email=data.get('customer_email_address'),
            phone=data.get('customer_phone_number'),
            country_prefix=data.get('customer_phone_number_prefix'))

        payment.project = MerchantProject()
        payment.project.project_id = data.get('merchant_project_id')
        payment.project.project_key = data.get('project_key')
        payment.project.name = data.get('project_name')
        payment.project.project_code = data.get('project_code')
        payment.project.category = data.get('project_category')
        payment.project.description = data.get('project_description')
        payment.project.source = data.get('project_description')
        payment.project.project_fields = data.get('project_fields')

        payment.payment_mode = Payment.LookupItem(
            item_id=data.get('payment_mode_id'),
            code=data.get('payment_mode_code'),
            name=data.get('payment_mode_name'))
        payment.payment_type = Payment.LookupItem(
            item_id=data.get('payment_type_id'),
            code=data.get('payment_type_code'),
            name=data.get('payment_type_name'))
        payment.payment_method = PaymentMethod.map_from_row(data)

        payment.custom_fields = data.get('custom_fields')
        payment.admin_notes = data.get('admin_notes')
        payment.client_notes = data.get('client_notes')
        payment.refund_reason = data.get('refund_reason')
        payment.transaction_source = data.get('transaction_source')
        payment.transaction_ip_address = data.get('transaction_ip_address')
        payment.transaction_history = data.get('transaction_history')
        payment.xsrf_key = data.get('xsrf_key')
        payment.is_active = data.get('is_active')

        payment.bill = Payment.Bill()
        payment.bill.base = (
            data.get('bill_base_currency'),
            float(data.get('bill_base_amount')))
        payment.bill.converted = (
            data.get('bill_converted_currency'),
            float(data.get('bill_converted_amount')))
        payment.bill.fee = (
            data.get('bill_fee_currency'),
            float(data.get('bill_fee_amount')))
        payment.bill.total = (
            data.get('bill_total_currency'),
            float(data.get('bill_total_amount')))
        payment.bill.refund = (
            data.get('refund_total_currency', 'PHP'),
            float(data.get('refund_total_amount', 0)))
        payment.bill.waived_fee = (
            data.get('waived_fee_currency', 'PHP'),
            float(data.get('waived_fee_amount') or 0))
        payment.bill.net = (
            data.get('net_currency', 'PHP'),
            float(data.get('net_amount') or 0))
        payment.bill.qwx_rate = (
            data.get('qwx_rate_base_currency'),
            data.get('qwx_rate_target_currency'),
            float(data.get('qwx_rate_amount')))
        payment.bill.ox_rate = (
            data.get('ox_rate_base_currency'),
            data.get('ox_rate_target_currency'),
            float(data.get('ox_rate_amount')))

        payment.processor_code = data.get('processor_code')
        payment.processor_data = data.get('processor_data')
        payment.invoice_description = data.get('invoice_description')
        payment.invoice_breakdown = data.get('invoice_breakdown')
        payment.retry_attempt_count = data.get('retry_attempt_count')
        payment.is_posted = data.get('is_posted')
        payment.posted_to = data.get('posted_to')

        payment.transaction_expires_at = data.get('transaction_expires_at')
        payment.transaction_created_at = data.get('transaction_created_at')
        payment.transaction_updated_at = data.get('transaction_updated_at')
        payment.invoice_due_at = data.get('invoice_due_at')
        payment.invoice_submitted_at = data.get('invoice_submitted_at')
        payment.invoice_paid_at = data.get('invoice_paid_at')
        payment.invoice_due_at = data.get('invoice_due_at')
        payment.invoice_created_at = data.get('invoice_created_at')
        payment.invoice_updated_at = data.get('invoice_updated_at')

        payment.settlement_id = data.get('settlement_id')
        payment.settlement_reference_id = data.get('settlement_reference_id')
        payment.settled_date = data.get('settled_date')
        return payment


@dataclass
class PaymentLink:
    amount: float = 0
    currency: str = 'PHP'
    payment_type_code: str = None
    project_id: int = 0
    customer_name: str = None
    customer_email: str = None
    mobile_number: str = None
    mobile_number_country_code: str = None
    mobile_number_dial_code: str = None
    expire_time_in_hrs: int = 3
    client_notes: str = None
    external_transaction_id: str = None


def validate_payment_link(data: dict, merchant: Merchant) -> Tuple[ValidationError, PaymentLink]:
    try:
        currency = data.get('currency')
        if not currency:
            raise ValidationError('Currency is missing', 'amount')

        accepted_currency = next((pc for pc in merchant.accepted_currencies if pc.currency == currency), None)
        if not accepted_currency:
            raise ValidationError('Submitted currency is not accepted', 'amount')

        class SubmittedPaymentLinkRequest(BasePaymentLinkRequest):
            amount = fields.Float(required=True,
                validate=validate.Range(min=accepted_currency.min_amount, max=accepted_currency.max_amount))
            currency = fields.Str(required=True)

        valid_data = SubmittedPaymentLinkRequest().load(data)
        payment_link = PaymentLink(**valid_data)
        return None, payment_link
    except ValidationError as validation_error:
        return validation_error, None
