""" data_repository.py """
from server.config import database
from server.models.timezone_model import Timezone


def get_timezones():
    queried_timezones = database.func('directory.get_all_timezones')
    if not queried_timezones:
        return []
    timezones = [Timezone.map(tz) for tz in queried_timezones]
    return timezones
