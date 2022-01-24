""" exchange_rate_model.py """
from collections import OrderedDict
from datetime import datetime
from marshmallow import Schema, fields


class ExchangeRateResponseSchema(Schema):
    baseCurrency = fields.Str(attribute='base_currency')
    rates = fields.Function(lambda r: r.supported_rates)
    timestamp = fields.DateTime(attribute='timestamp')


class ExchangeRate:
    def __init__(self):
        self.rates = dict()
        self.base_currency = 'USD'
        self.timestamp = datetime.utcnow()
        self.license = None
        self.disclaimer = None

    @property
    def supported_rates(self):
        """
        The current supported currency for total amount are PHP and USD
        with the default base is USD. Later on, this model will change to account for it.
        """
        return {
            'PHP': self.rates.get('PHP') or 0
        }

    def serialize(self) -> OrderedDict:
        return ExchangeRateResponseSchema().dump(self)

    @staticmethod
    def map(data):
        if not data:
            return None

        if 'error' in data:
            return None

        exchange_rate = ExchangeRate()
        exchange_rate.base_currency = data.get('base')
        exchange_rate.license = data.get('license')
        exchange_rate.disclaimer = data.get('disclaimer')
        exchange_rate.timestamp = datetime.fromtimestamp(data.get('timestamp'))
        exchange_rate.rates = data.get('rates')
        return exchange_rate
