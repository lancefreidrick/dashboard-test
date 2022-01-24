from datetime import datetime, timezone
from bson.objectid import ObjectId
from pymongo.errors import PyMongoError
from server.config import database, environment
from server.config.logger import log
from server.models.reset_token_model import ResetToken
from server.models.session_model import Session


config = environment.config


def create_session(data: dict):
    db_params = [
        data['person'].id,
        data['client_id'],
        data['refresh_token'],
        data['ip_address'],
        data['user_agent']
    ]
    success_save = database.func('directory.create_session', db_params)
    if success_save[0]['session_token_id'] == 0:
        return None
    return success_save[0]['session_token_id']


def find_active_session(client_id: str, refresh_token: str = None, person_id: str = None):
    db_params = [client_id, refresh_token, person_id]
    active_session = database.func('directory.find_active_session', db_params)
    if not active_session:
        return None
    return Session.map(active_session[0])


def disable_session(person_id: str, client_id: str):
    db_params = [person_id, client_id]
    success_disable = database.func('directory.disable_session', db_params)
    if not success_disable:
        return None
    return success_disable


def find_reset_token(reset_id: str):
    db_params = [reset_id]
    result = database.func('directory.find_password_reset_request_token', db_params)
    if not result:
        return None
    return ResetToken.map(result[0])


def save_reset_token(reset_id: str, token_hash: str, user_id: str):
    db_params = [
        token_hash,
        reset_id,
        user_id,
        config.reset_token_life
    ]
    result = database.func('directory.save_password_reset_request_token', db_params)
    return (result[0]['status'] == 'success', result[0]['message'])


def mark_reset_token_as_used(reset_token_id: str):
    db_params = [
        reset_token_id
    ]
    result = database.func('directory.mark_password_reset_request_token', db_params)
    return (result[0]['status'] == 'success', result[0]['message'])
