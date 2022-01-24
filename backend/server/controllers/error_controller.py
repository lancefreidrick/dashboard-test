""" server.route.error_route """

import traceback
from flask import Blueprint, jsonify, make_response
from server.config.logger import log

error_blueprint = Blueprint('error', __name__)


@error_blueprint.app_errorhandler(400)
def bad_request_error(error):
    payload = error.description

    if not isinstance(payload, dict):
        return make_response(jsonify({'message': 'Bad request'}), 400)

    log.warning(f'HTTP 400: {error.description}')
    return make_response(jsonify(payload), 400)


@error_blueprint.app_errorhandler(401)
def unauthorized_error(error):
    payload = error.description
    message = 'Unauthorized access'
    if isinstance(payload, dict):
        if 'message' in payload:
            message = payload.get('message')
    log.warning(f'HTTP 401: {message}')
    return make_response(jsonify({'message': message}), 401)

@error_blueprint.app_errorhandler(405)
def method_not_allowed(error):
    message = 'Method Not Allowed'
    log.warning(f'HTTP 405: {message}\nActual error: {error}')
    return make_response(jsonify({'message': message}), 405)

@error_blueprint.app_errorhandler(403)
def forbidden_error(error):
    payload = error.description
    message = 'Unauthorized access'
    if isinstance(payload, dict):
        if 'message' in payload:
            message = payload.get('message')
    log.warning(f'HTTP 403: {message}')
    return make_response(jsonify({'message': message}), 403)


@error_blueprint.app_errorhandler(404)
def page_not_found_error(error):
    payload = error.description
    message = 'Not found'
    if isinstance(payload, dict):
        message = payload['message']
    log.warning(f'HTTP 404: {message}')
    return make_response(jsonify({'message': message}), 404)


@error_blueprint.app_errorhandler(500)
def internal_server_error(error):
    log.error(traceback.format_exc())
    log.error(f'HTTP 500 {error}')
    return make_response(jsonify({'message': 'Internal server error'}), 500)


@error_blueprint.app_errorhandler(Exception)
def unhandled_exception_error(error):
    log.critical(traceback.format_exc())
    log.critical(f'Unhandled exception error {error}')
    msgs = {
        308: 'Permanent redirect'
    }
    if error and hasattr(error, 'code') and error.code >= 200 and error.code < 600:
        msg = msgs[error.code] if error.code in msgs else 'Nothing to do here'
        return make_response(jsonify({'message': msg}), error.code)
    return make_response(jsonify({'message': 'Internal server error'}), 500)
