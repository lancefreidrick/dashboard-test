""" exchange_rate_repository.py """
from pymongo import DESCENDING
from server.models.exchange_rate_model import ExchangeRate
from server.config import mongodb

def get_latest_exchange_rate() -> ExchangeRate:
    db = mongodb.get('directory')
    exchange_rates_collection = db.get_collection('exchangerates')
    sort = [('_id', DESCENDING)]
    queried_exchange_rate = exchange_rates_collection.find().limit(1).sort(sort)

    rates = [ExchangeRate.map(xrate) for xrate in queried_exchange_rate]

    if not rates:
        return None
    return rates[0]
