""" server.controllers.lookup_controller.py """
# pylint: disable=global-statement

from flask import jsonify, Blueprint
from server.repositories import data_repository

lookup_blueprint = Blueprint('lookup', __name__)

__timezones = []

@lookup_blueprint.route('/lookup/timezones', methods=['GET'])
def get_timezones():
    global __timezones
    if not __timezones:
        timezones = data_repository.get_timezones()
        __timezones = [tz.serialize() for tz in timezones]

    return jsonify(__timezones), 200
