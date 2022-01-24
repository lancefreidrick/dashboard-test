from datetime import timedelta
from marshmallow import Schema, fields


def format_timedelta(td):
    if td.days < 0:
        return f'UTC-{timedelta() - td}'[:-3]
    return f'UTC+{td}'[:-3]

class TimezoneSchema(Schema):
    name = fields.Str()
    abbreviation = fields.Str()
    utcOffset = fields.Str(attribute='utc_offset')
    isDst = fields.Bool(attribute='is_dst')

    class Meta:
        fields = (
            'name',
            'abbreviation',
            'utcOffset',
            'isDst'
            )
        ordered = True

class Timezone():
    def __init__(self):
        self.name = None
        self.abbreviation = None
        self.utc_offset = None
        self.is_dst = None

    def serialize(self):
        return TimezoneSchema().dump(self)

    @staticmethod
    def map(data: dict):
        """
        @returns Timezone
        """
        timezone = Timezone()
        timezone.name = data.get('name')
        timezone.abbreviation = data.get('abbreviation')
        timezone.utc_offset = format_timedelta(data.get('utc_offset'))
        timezone.is_dst = data.get('is_dst')

        return timezone
