# pylint: disable=global-statement
import json
from datetime import datetime, timedelta
import jwt
from server.config.logger import log

__key = None
__token_life = None

def setup(key: str, token_life: int):
    global __key, __token_life
    __key = key
    __token_life = token_life
    log.info('jwt:     Setting up the JWT key with %sm life', __token_life)


def encode(payload, token_life_mins=0):
    global __key, __token_life
    payload = json.loads(json.JSONEncoder().encode(payload))
    minutes = token_life_mins if token_life_mins > 0 else __token_life
    payload['exp'] = datetime.utcnow() + timedelta(minutes=minutes)
    encoded = jwt.encode(payload, __key, algorithm='HS256')
    return encoded.decode('utf-8')


def decode(token) -> (bool, dict):
    global __key, __token_life
    try:
        decoded_value = jwt.decode(token, __key, algorithms=['HS256'])
        return (True, decoded_value)
    except jwt.DecodeError as e:
        return (False, str(e))
