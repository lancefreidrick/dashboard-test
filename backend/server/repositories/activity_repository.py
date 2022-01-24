""" activity_repository.py """
from typing import Tuple
from psycopg2.extras import Json
from server.config import database
from server.models.search_option_model import SearchOption
from server.models.person_model import Person
from server.models.activity_model import Activity


def get_activities(search_option: SearchOption, requested_by: Person) -> Tuple[list, int]:
    db_params = [
        requested_by.id,
        search_option.start_date,
        search_option.end_date,
        search_option.size,
        search_option.skip()
    ]
    queried_activities = database.func('auditing.get_activity_logs', db_params)
    if not queried_activities:
        return ([], 0)
    activities = [Activity.map(a) for a in queried_activities]
    total_count = queried_activities[0]['full_count']
    return activities, total_count


def add_activity_log(activity_log: Activity) -> Tuple[bool, str]:
    db_params = [
        activity_log.activity_type,
        activity_log.message,
        activity_log.activity_level,
        activity_log.ip_address,
        activity_log.user_agent,
        activity_log.url_path,
        Json(activity_log.affected_data),
        activity_log.logged_by_id,
        activity_log.logged_by_name,
        activity_log.logged_source
    ]
    db_result = database.func('auditing.add_activity_log', db_params)
    if not db_result:
        return (False, 'Activity log has not been added')
    return db_result[0]['status'] == 'success', db_result[0]['message']
