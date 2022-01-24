from typing import Tuple, Union
from datetime import datetime

from marshmallow import fields, Schema, ValidationError

from .payment_model import Payment, PaymentSchema


class DisputeSchema(Schema):
    id = fields.Int(attribute='id')
    referenceId = fields.Str(attribute='reference_id')
    invoiceId = fields.Int(attribute='invoice_id')
    reason = fields.Str(attribute='reason')
    status = fields.Str(attribute='status')
    createdAt = fields.DateTime(attribute='created_at')
    updatedAt = fields.DateTime(attribute='updated_at')

    disputedPayment = fields.Function(lambda p: PaymentSchema().dump(p.payment))

class DisputeDetailsSchema(Schema):
    id = fields.Int(attribute='id')
    referenceId = fields.Str(attribute='reference_id')
    reason = fields.Str(attribute='reason')
    status = fields.Str(attribute='status')
    createdAt = fields.DateTime(attribute='created_at')
    updatedAt = fields.DateTime(attribute='updated_at')


class SubmittedDispute(Schema):
    notes = fields.Str(data_key='disputeNotes', required=False)
    status = fields.Str(data_key='disputeStatus', required=True)


class Dispute:
    def __init__(self):
        self.id = None
        self.reference_id = None
        self.invoice_id = None

        self.reason: str = None
        self.status: str = None
        self.created_at: datetime = None
        self.updated_at: datetime = None

        self.payment: Payment = None

    def serialize(self):
        if self.payment:
            return DisputeSchema().dump(self)
        return DisputeDetailsSchema().dump(self)

    def __str__(self) -> str:
        return f'{self.reference_id}/{self.invoice_id} {self.status} ({self.reason})'

    @staticmethod
    def validate_submitted_dispute_update(data: dict) -> Tuple[bool, Union[dict, ValidationError]]:
        try:
            dispute_update = SubmittedDispute().load(data)
            return True, dispute_update
        except ValidationError as verr:
            return False, verr

    @staticmethod
    def map(data: dict) -> any:
        if not data:
            return None

        dispute = Dispute()
        dispute.id = data.get('dispute_id')
        dispute.reference_id = data.get('dispute_reference_id')
        dispute.reason = data.get('dispute_reason')
        dispute.status = data.get('dispute_status')
        dispute.created_at = data.get('created_at')
        dispute.updated_at = data.get('updated_at')

        if data.get('transaction_id'):
            dispute.invoice_id = data.get('invoice_id')
            dispute.payment = Payment.map(data)

        return dispute
