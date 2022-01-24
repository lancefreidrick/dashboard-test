""" server.controllers.activity_controller.py """
# pylint: disable=unused-argument
from datetime import datetime, timedelta
from flask import request, jsonify, Blueprint, g
import pytz
from server.config.authentication import authentication
from server.repositories import activity_repository
from server.models.search_option_model import SearchOption
from server.models.person_model import Roles, MerchantRoles

tzone = 'Asia/Manila'
activity_blueprint = Blueprint('activity', __name__)

@activity_blueprint.route('/activities', methods=['GET'])
@authentication.jwt_required
@authentication.min_system_access_role(Roles.CUSTOMERSUPPORT)
def search_activities():
    current_user = g.user
    search_option = SearchOption.map_from_query(request.args)
    activities, total_count = activity_repository.get_activities(search_option, current_user)

    serialized_activities = [a.serialize() for a in activities]

    return jsonify({
        'activities': serialized_activities,
        'totalCount': total_count
    }), 200


@activity_blueprint.route('/merchants/<int:merchant_id>/activities', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_ADMIN)
def search_merchant_activities(merchant_id: int):
    current_user = g.user
    search_option = SearchOption.map_from_query(request.args)

    end_date = localize_date(datetime.now(), tzone)
    start_date = datetime.now() - timedelta(days=30)
    start_date = localize_date(start_date.replace(hour=0, minute=0, second=0, microsecond=0), tzone)
    search_option.end_date = end_date
    search_option.start_date = start_date

    activities, total_count = activity_repository.get_activities(search_option, current_user)

    serialized_activities = [a.serialize() for a in activities]

    return jsonify({
        'activities': serialized_activities,
        'totalCount': total_count
    }), 200


def localize_date(dt: datetime, t_zone='Asia/Manila'):
    return pytz.timezone(t_zone).localize(dt, is_dst=None)
