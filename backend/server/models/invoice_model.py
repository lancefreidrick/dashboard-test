from datetime import datetime
from marshmallow import Schema, fields


class InvoiceSchema(Schema):
    invoiceId = fields.Int(attribute='invoice_id')
    invoiceReferenceId = fields.Str(attribute='invoice_reference_id')
    paymentReferenceId = fields.Str(attribute='payment_reference_id')
    status = fields.Str(attribute='status.code')
    billConverted = fields.Function(lambda t: list(t.bill.converted))
    billBase = fields.Function(lambda t: list(t.bill.base))
    billFee = fields.Function(lambda t: list(t.bill.fee))
    billTotal = fields.Function(lambda t: list(t.bill.total))
    invoiceDescription = fields.Str(attribute='invoice_description')
    retryAttemptCount = fields.Int(attribute='retry_attempt_count')
    dueAt = fields.DateTime(attribute='due_at', format='iso')
    submittedAt = fields.DateTime(attribute='submitted_at', format='iso')
    paidAt = fields.DateTime(attribute='paid_at', format='iso')
    createdAt = fields.DateTime(attribute='created_at', format='iso')
    updatedAt = fields.DateTime(attribute='updated_at', format='iso')


class Invoice:
    class LookupItem:
        def __init__(self, lookup_id: int, code: str, name: str):
            self.id: int = lookup_id
            self.code: str = code
            self.name: str = name

        def __str__(self):
            return f'Invoice.LookupItem({self.id},{self.code},{self.name})'

        def __repr__(self):
            return f'Invoice.LookupItem({self.id},{self.code},{self.name})'

    class Bill:
        def __init__(self):
            self.total = ('PHP', 0)
            self.base = ('PHP', 0)
            self.fee = ('PHP', 0)
            self.converted = ('PHP', 0)
            # base, target, amount
            self.qwx_rate = ('USD', 'PHP', 0)
            self.ox_rate = ('USD', 'PHP', 0)

    def __init__(self):
        self.invoice_id: int = None
        self.invoice_reference_id: str = None
        self.payment_reference_id: str = None
        self.status: Invoice.LookupItem = None
        self.bill: Invoice.Bill = None
        self.processor_code: str = None
        self.processor_data: dict = {}
        self.invoice_description: str = None
        self.invoice_breakdown: dict = {}
        self.retry_attempt_count: int = 0
        self.is_posted: bool = False
        self.posted_to: str = None
        self.due_at: datetime = None
        self.submitted_at: datetime = None
        self.paid_at: datetime = None
        self.updated_at: datetime = None
        self.created_at: datetime = None

    def serialize(self):
        return InvoiceSchema().dump(self)

    @staticmethod
    def map(data: dict):
        if not data:
            return None

        invoice = Invoice()
        invoice.invoice_id = data.get('invoice_id')
        invoice.invoice_reference_id = data.get('invoice_reference_id')
        invoice.payment_reference_id = data.get('payment_reference_id')
        invoice.status = Invoice.LookupItem(
            lookup_id=data.get('invoice_status_id'),
            code=data.get('invoice_status_code'),
            name=data.get('invoice_status_name'))

        invoice.bill = Invoice.Bill()
        invoice.bill.base = (data.get('bill_base_currency'), float(data.get('bill_base_amount')))
        invoice.bill.converted = (data.get('bill_converted_currency'), float(data.get('bill_converted_amount')))
        invoice.bill.fee = (data.get('bill_fee_currency'), float(data.get('bill_fee_amount')))
        invoice.bill.total = (data.get('bill_total_currency'), float(data.get('bill_total_amount')))
        invoice.bill.qwx_rate = (
            data.get('qwx_rate_base_currency'),
            data.get('qwx_rate_target_currency'),
            float(data.get('qwx_rate_amount')))
        invoice.bill.ox_rate = (
            data.get('ox_rate_base_currency'),
            data.get('ox_rate_target_currency'),
            float(data.get('ox_rate_amount')))

        invoice.processor_code = data.get('processor_code')
        invoice.processor_data = data.get('processor_data')
        invoice.invoice_description = data.get('invoice_description')
        invoice.invoice_breakdown = data.get('invoice_breakdown')
        invoice.retry_attempt_count = data.get('retry_attempt_count')
        invoice.is_posted = data.get('is_posted')
        invoice.posted_to = data.get('posted_to')

        invoice.due_at = data.get('due_at')
        invoice.submitted_at = data.get('submitted_at')
        invoice.paid_at = data.get('paid_at')
        invoice.created_at = data.get('created_at')
        invoice.updated_at = data.get('updated_at')

        return invoice
