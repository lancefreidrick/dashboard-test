""" transaction_log_model.py """
import re
from datetime import datetime
from marshmallow import Schema, fields, ValidationError


class BasicTransactionLogSchema(Schema):
    logId = fields.Str(attribute='log_id')
    transactionId = fields.Int(attribute='transaction_id')
    invoiceId = fields.Str(attribute='invoice_id')
    status = fields.Str(attribute='action_status')
    content = fields.Function(lambda l: l.normalize_content())
    createdById = fields.Int(attribute='created_by_id')
    createdByName = fields.Str(attribute='created_by_name')
    createdAt = fields.DateTime(attribute='created_at', format='iso')
    updatedById = fields.Int(attribute='updated_by_id')
    updatedByName = fields.Str(attribute='updated_by_name')
    updatedAt = fields.DateTime(attribute='updated_at', format='iso')


class InternalTransactionLogSchema(BasicTransactionLogSchema):
    action = fields.Str(attribute='action_name')
    level = fields.Str(attribute='log_level')
    metadata = fields.Dict(attribute='log_metadata')


class SubmittedTransactionLog(Schema):
    content = fields.Str(required=True)


class TransactionLog():
    def __init__(self):
        self.log_id: int = None
        self.transaction_id: int = None
        self.invoice_id: int = None

        self.action_name: str = None
        self.action_status: str = None
        self.log_level: str = None
        self.log_content: str = None
        self.log_metadata: str = None

        self.created_by_id: int = None
        self.created_by_name: str = None
        self.created_at: datetime = None

        self.updated_by_id: int = None
        self.updated_by_name: str = None
        self.updated_at: datetime = None

    def normalize_content(self):
        content = re.compile('[Mm]aybank').sub('MP', self.log_content)
        content = re.compile('[Bb]raintree|BT').sub('BP', content)
        return content

    def serialize(self, show_metadata=False):
        if show_metadata:
            return InternalTransactionLogSchema().dump(self)

        return BasicTransactionLogSchema().dump(self)

    @staticmethod
    def validate_submitted_log(data: dict):
        try:
            log = SubmittedTransactionLog().load(data)
            return True, log
        except ValidationError as verr:
            return False, verr

    @staticmethod
    def map(data: dict):
        if not data:
            return None

        log = TransactionLog()
        log.log_id = data.get('transaction_invoice_log_id')
        log.transaction_id = data.get('transaction_id')
        log.invoice_id = data.get('invoice_id')

        log.action_name = data.get('action_name')
        log.action_status = data.get('action_status')
        log.log_level = data.get('log_level')
        log.log_content = data.get('log_content')
        log.log_metadata = data.get('log_metadata')

        log.created_by_id = data.get('created_by_id')
        log.created_by_name = data.get('created_by')
        log.created_at = data.get('created_at')

        log.updated_by_id = data.get('updated_by_id')
        log.updated_by_name = data.get('updated_by')
        log.updated_at = data.get('updated_at')
        return log
