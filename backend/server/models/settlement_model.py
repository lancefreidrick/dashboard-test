from datetime import datetime
from typing import Tuple, Optional
from marshmallow import Schema, fields, ValidationError
from server.models.merchant_model import Merchant
from server.models.person_model import Person


class SettlementFileRequestSchema(Schema):
    unique_identifier = fields.Str(data_key='uniqueIdentifier', required=True)
    s3_file_directory = fields.Str(data_key='fileDirectory', required=True)
    s3_file_name = fields.Str(data_key='fileName', required=True)
    s3_file_url = fields.Str(data_key='fileUrl', required=True)
    s3_file_type = fields.Str(data_key='fileType', required=True)
    s3_domain_name = fields.Str(data_key='domainName', required=True)
    s3_bucket_name = fields.Str(data_key='bucketName', required=True)

class SettlementFileResponseSchema(Schema):
    settlementFileId = fields.Int(attribute='settlement_file_id')
    merchantId = fields.Int(attribute='merchant.merchant_id')
    merchantCode = fields.Str(attribute='merchant.merchant_code')
    merchantName = fields.Str(attribute='merchant.name')
    uniqueIdentifier = fields.Str(attribute='unique_identifier')
    fileDirectory = fields.Str(attribute='s3_file_directory')
    fileName = fields.Str(attribute='s3_file_name')
    fileUrl = fields.Str(attribute='s3_file_url')
    fileType = fields.Str(attribute='s3_file_type')
    domainName = fields.Str(attribute='s3_domain_name')
    bucketName = fields.Str(attribute='s3_bucket_name')
    createdAt = fields.DateTime(attribute='created_at')


class SettlementRequestSchema(Schema):
    invoice_ids = fields.List(fields.Int, data_key='invoiceIds', required=True)
    settlement_file_id = fields.Int(data_key='settlementFileId', required=True)
    settled_date = fields.Date(data_key='settledDate', required=True)
    settlement_notes = fields.Str(data_key='settlementNotes', allow_none=True)


class SettlementSchema(Schema):
    """
    Used for return JSON-structured values on the API endpoints
    """
    settlementId = fields.Int(attribute='settlement_id')
    settlementReferenceId = fields.Str(attribute='settlement_reference_id')
    merchantId = fields.Int(attribute='merchant.merchant_id')
    merchantCode = fields.Str(attribute='merchant.merchant_code')
    merchantName = fields.Str(attribute='merchant.name')
    totalSettlementAmount = fields.Function(lambda t: list(t.total_settlement_amount))
    totalBaseAmount = fields.Function(lambda t: list(t.total_base_amount))
    totalWaivedFeeAmount = fields.Function(lambda t: list(t.total_waived_fee_amount))
    totalPaymentCount = fields.Int(attribute='total_payment_count')
    settlementNotes = fields.Str(attribute='settlement_notes')
    settledDate = fields.Date(attribute='settled_date')
    settledById = fields.Int(attribute='settled_by.id')
    settledByEmail = fields.Str(attribute='settled_by.email')
    settledByFirstName = fields.Str(attribute='settled_by.first_name')
    settledByLastName = fields.Str(attribute='settled_by.last_name')
    fileId = fields.Int(attribute='file.settlement_file_id')
    fileDirectory = fields.Str(attribute='file.s3_file_directory')
    fileName = fields.Str(attribute='file.s3_file_name')
    fileUrl = fields.Str(attribute='file.s3_file_url')
    fileType = fields.Str(attribute='file.s3_file_type')
    createdAt = fields.DateTime(attribute='created_at', format='iso')
    updatedAt = fields.DateTime(attribute='updated_at', format='iso')


class SettlementFile:
    def __init__(self):
        self.settlement_file_id: int = 0
        self.merchant: Merchant = None
        self.unique_identifier: str = None
        self.s3_file_directory: str = None
        self.s3_file_name: str = None
        self.s3_bucket_name: str = None
        self.s3_domain_name: str = None
        self.s3_file_url: str = None
        self.s3_file_type: str = None
        self.created_at: datetime = None
        self.deleted_at: datetime = None

    def __repr__(self):
        sf_id = self.settlement_file_id
        mc_code = self.merchant.merchant_code
        return f'SettlementFile({sf_id}, {self.unique_identifier}, {mc_code})'

    def __str__(self):
        sf_id = self.settlement_file_id
        mc_code = self.merchant.merchant_code
        return f'SettlementFile: {mc_code}, {sf_id}, {self.unique_identifier}, {self.s3_file_url}'

    def serialize(self, presigned_url: str) -> dict:
        payload = SettlementFileResponseSchema().dump(self)
        payload['presignedUrl'] = presigned_url
        return payload

    @staticmethod
    def validate(merchant: Merchant, request_body: dict) -> Tuple[Optional[ValidationError], any]:
        try:
            data = SettlementFileRequestSchema().load(request_body)
            settlement_file = SettlementFile()
            settlement_file.merchant = merchant
            settlement_file.unique_identifier = data['unique_identifier']
            settlement_file.s3_file_directory = data['s3_file_directory']
            settlement_file.s3_file_name = data['s3_file_name']
            settlement_file.s3_file_type = data['s3_file_type']
            settlement_file.s3_file_url = data['s3_file_url']
            settlement_file.s3_domain_name = data['s3_domain_name']
            settlement_file.s3_bucket_name = data['s3_bucket_name']
            return None, settlement_file
        except ValidationError as verr:
            return verr, None

    @staticmethod
    def map(data: dict) -> any:
        if not data:
            return None

        settlement_file = SettlementFile()
        settlement_file.settlement_file_id = data.get('settlement_file_id')

        settlement_file.merchant = Merchant()
        settlement_file.merchant.merchant_id = data.get('merchant_id')
        settlement_file.merchant.merchant_code = data.get('merchant_code')
        settlement_file.merchant.name = data.get('merchant_name')

        settlement_file.unique_identifier = data.get('unique_identifier')
        settlement_file.s3_domain_name = data.get('s3_domain_name')
        settlement_file.s3_bucket_name = data.get('s3_bucket_name')
        settlement_file.s3_file_name = data.get('s3_file_name')
        settlement_file.s3_file_url = data.get('s3_file_url')
        settlement_file.s3_file_type = data.get('s3_file_type')
        settlement_file.s3_file_directory = data.get('s3_file_directory')

        settlement_file.created_at = data.get('created_at')
        settlement_file.deleted_at = data.get('deleted_at')

        return settlement_file


class Settlement:
    class RequestData:
        def __init__(self, data: dict):
            self.settled_date = data.get('settled_date')
            self.settlement_notes = data.get('settlement_notes')
            self.settlement_file_id = data.get('settlement_file_id')
            self.invoice_ids = data.get('invoice_ids')

        def are_invoices_unique(self):
            return len(self.invoice_ids) != len(set(self.invoice_ids))

    def __init__(self):
        self.settlement_id: int = None
        self.settlement_reference_id: str = None
        self.merchant: Merchant = None
        self.payments: list = []
        self.settlement_notes: str = None
        self.settled_date: datetime = None
        self.settled_by: Person = None
        self.file: SettlementFile = SettlementFile()
        self.total_settlement_amount: Tuple[str, float] = None
        self.total_base_amount: Tuple[str, float] = None
        self.total_waived_fee_amount: Tuple[str, float] = None
        self.total_payment_count: int = None
        self.created_at: datetime = None
        self.updated_at: datetime = None

    def serialize(self):
        return SettlementSchema().dump(self)

    def __str__(self):
        return f'Settlement {self.merchant.merchant_code}/{self.settlement_id}'

    @staticmethod
    def validate(request_body: dict) -> Tuple[Optional[ValidationError], any]:
        try:
            data = SettlementRequestSchema().load(request_body)
            return None, Settlement.RequestData(data)
        except ValidationError as verr:
            return verr, None

    @staticmethod
    def map(data: dict) -> any:
        if not data:
            return None

        settlement = Settlement()
        settlement.settlement_id = data.get('settlement_id')
        settlement.settlement_reference_id = data.get('settlement_reference_id')

        settlement.merchant = Merchant()
        settlement.merchant.merchant_id = data.get('merchant_id')
        settlement.merchant.merchant_code = data.get('merchant_code')
        settlement.merchant.name = data.get('merchant_name')

        settlement.settled_by = Person()
        settlement.settled_by.id = data.get('settled_by_id')
        settlement.settled_by.email = data.get('settled_by_email')
        settlement.settled_by.first_name = data.get('settled_by_first_name')
        settlement.settled_by.last_name = data.get('settled_by_last_name')

        settlement.file = SettlementFile.map(data)
        settlement.settlement_notes = data.get('settlement_notes')
        settlement.settled_date = data.get('settled_date')

        settlement.total_base_amount = (
            data.get('settlement_currency'),
            float(data.get('settlement_base_amount') or 0)
        )

        settlement.total_settlement_amount = (
            data.get('settlement_currency'),
            float(data.get('settlement_net_amount') or 0)
        )

        settlement.total_waived_fee_amount = (
            data.get('settlement_currency'),
            float(data.get('waived_fee_base_amount') or 0)
        )

        settlement.total_payment_count = data.get('settlement_payment_count')

        settlement.created_at = data.get('created_at')
        settlement.updated_at = data.get('updated_at')

        return settlement
