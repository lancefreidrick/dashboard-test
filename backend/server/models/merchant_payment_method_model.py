""" merchant_payment_method_model.py """
from typing import List
from datetime import datetime
from marshmallow import Schema, fields as _fields


class MerchantPaymentMethodSchema(Schema):
    mpmId = _fields.Int(attribute='merchant_payment_method_id')
    code = _fields.Str(attribute='method_code')
    mode = _fields.Str(attribute='method_mode')
    currency = _fields.Str()
    paymentProcessor = _fields.Str(attribute='payment_processor')
    isAutoDebitEnabled = _fields.Bool(attribute='is_auto_debit_enabled')
    channels = _fields.List(_fields.Dict())
    isEnabled = _fields.Bool(attribute='is_enabled')
    updatedAt = _fields.DateTime(attribute='updated_at')


class MerchantPaymentMethod:
    def __init__(self):
        self.merchant_payment_method_id: int = 0
        self.method_code: str = 'none'
        self.method_mode: str = 'tiered'
        self.currency: str = 'USD'
        self.payment_processor: str = None
        self.rate_markup: float = 1
        self.rate_fixed_amount: float = 0
        self.conversion_markup: float = 1
        self.conversion_fixed_amount: float = 0
        self.is_auto_debit_enabled: bool = False
        self.metadata: dict = {}
        self.is_enabled: bool = False
        self.created_at: datetime = None
        self.updated_at: datetime = None

    def __str__(self) -> str:
        return '#{0}: {1} {2} ({3})'.format(
            self.merchant_payment_method_id,
            self.method_code,
            self.currency,
            self.payment_processor)

    def __repr__(self) -> str:
        return 'MerchantPaymentMethod({0}, {1}, {2}, {3})'.format(
            self.merchant_payment_method_id,
            self.method_code,
            self.currency,
            self.payment_processor)

    def __eq__(self, other):
        if not isinstance(other, MerchantPaymentMethod):
            return False
        return self.merchant_payment_method_id == other.merchant_payment_method_id

    def __lt__(self, other):
        if not isinstance(other, MerchantPaymentMethod):
            return False
        return self.merchant_payment_method_id < other.merchant_payment_method_id

    def  __hash__(self):
        return hash(self.merchant_payment_method_id)

    def is_match(self, mpm_id: int) -> bool:
        return self.merchant_payment_method_id == mpm_id

    @property
    def channels(self) -> List[dict]:
        if 'channels' not in self.metadata:
            return []

        return self.metadata['channels']

    def serialize(self):
        return MerchantPaymentMethodSchema().dump(self)

    @staticmethod
    def map_from_row(data: dict):
        if not data:
            return None

        payment_method = MerchantPaymentMethod()
        payment_method.merchant_payment_method_id = data.get('merchant_payment_method_id')
        payment_method.method_code = data.get('method_code')
        payment_method.method_mode = data.get('method_mode')
        payment_method.currency = data.get('currency')
        payment_method.payment_processor = data.get('payment_processor')
        payment_method.rate_markup = data.get('rate_markup')
        payment_method.rate_fixed_amount = data.get('rate_fixed_amount')
        payment_method.conversion_markup = data.get('conversion_markup')
        payment_method.conversion_fixed_amount = data.get('conversion_fixed_amount')
        payment_method.is_auto_debit_enabled = data.get('is_auto_debit_enabled')
        payment_method.metadata = data.get('metadata')
        payment_method.is_enabled = data.get('is_enabled')
        payment_method.created_at = data.get('created_at')
        payment_method.updated_at = data.get('updated_at')
        return payment_method
