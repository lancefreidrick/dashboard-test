""" server.models.activity_model.py """
from enum import Enum
from datetime import datetime
from marshmallow import Schema, fields
from server.models.person_model import Person
from server.models.merchant_model import Merchant
from server.models.search_option_model import SearchOption

class LogAction(Enum):
    Search = 1
    Export = 2


class ActivitySchema(Schema):
    activityId = fields.Str(attribute='activity_id')
    activityType = fields.Str(attribute='activity_type')
    activityLevel = fields.Str(attribute='activity_level')
    message = fields.Str(attribute='message')
    ipAddress = fields.Str(attribute='ip_address')
    userAgent = fields.Str(attribute='user_agent')
    urlPath = fields.Str(attribute='url_path')
    affectedData = fields.Dict(attribute='affected_data')
    loggedById = fields.Int(attribute='logged_by_id')
    loggedByName = fields.Str(attribute='logged_by_name')
    loggedSource = fields.Str(attribute='logged_source')
    loggedAt = fields.DateTime(attribute='logged_at', format='iso')
    class Meta:
        fields = (
            'activityId', 'activityType', 'activityLevel', 'message',
            'ipAddress', 'userAgent', 'urlPath',
            'affectedData', 'loggedById', 'loggedByName',
            'loggedSource', 'loggedAt'
        )
        ordered = True

class Activity():
    def __init__(self, activity_type: str, message: str, activity_level: str = 'info'):
        self.activity_id = None
        self.activity_type = activity_type
        self.activity_level = activity_level
        self.message = message
        self.ip_address = None
        self.user_agent = None
        self.url_path = None
        self.affected_data = {}
        self.logged_by_id = 0
        self.logged_by_name = 'Aqwire Process'
        self.logged_source = 'ENTD'
        self.logged_at = datetime.now()

    def serialize(self):
        return ActivitySchema().dump(self)

    @staticmethod
    def map(data: dict):
        activity = Activity(
            data.get('activity_type'),
            data.get('activity_message'),
            data.get('activity_level')
        )
        activity.activity_id = data.get('activity_log_id')
        activity.ip_address = data.get('ip_address')
        activity.user_agent = data.get('user_agent')
        activity.url_path = data.get('url_path')
        activity.affected_data = data.get('affected_data')
        activity.logged_by_id = data.get('logged_by_id')
        activity.logged_by_name = data.get('logged_by_name')
        activity.logged_source = data.get('logged_source')
        activity.logged_at = data.get('logged_at')

        return activity


def build_search_activity_log(
        action: LogAction, name: str, current_user: Person, options: dict) -> Activity:
    """
    Creates an instance of an export type of activity log

    Arguments:
        export_type {str} - enrollments, payments, settlement reports
        current_user {Person}
        options {dict} -- Includes request, merchant, total_count and search_option

    Returns:
        Activity
    """
    request = options.get('request')
    merchant = options.get('merchant')
    search_option = options.get('search_option')
    total_count = options.get('total_count') or 0

    if action == LogAction.Search:
        message = f'{current_user.name} has searched {name} for "{search_option.search_term}"'
    elif action == LogAction.Export:
        message = f'''{current_user.name} has exported {name} from {merchant.name if merchant else 'NA'}'''
    else:
        message = f'{current_user.name} has searched something'

    activity_log = Activity('EXPORT', message, 'info')
    activity_log.logged_by_id = current_user.id
    activity_log.logged_by_name = f'{current_user.name} ({current_user.email})'

    activity_log.affected_data['type'] = action.name
    activity_log.affected_data['totalCount'] = total_count

    if request:
        activity_log.ip_address = request.headers.get('HTTP_X_FORWARDED_FOR') or request.remote_addr
        activity_log.user_agent = request.headers.get('User-Agent')
        activity_log.url_path = f'{request.method} {request.path}'

    if merchant and isinstance(search_option, Merchant):
        activity_log.affected_data['merchant'] = merchant.name

    if search_option and isinstance(search_option, SearchOption):
        activity_log.affected_data['searchTerm'] = search_option.search_term
        activity_log.affected_data['page'] = search_option.page
        activity_log.affected_data['size'] = search_option.size
        activity_log.affected_data['settlementStatus'] = search_option.settlement_status
        activity_log.affected_data['showIncomplete'] = search_option.show_incomplete
        activity_log.affected_data['startDate'] = search_option.start_date.isoformat()\
            if search_option.start_date else None
        activity_log.affected_data['endDate'] = search_option.start_date.isoformat()\
            if search_option.start_date else None
        activity_log.affected_data['reportingDate'] = search_option.reporting_date.isoformat()\
            if search_option.reporting_date else None

    return activity_log
