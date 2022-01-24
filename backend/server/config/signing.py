# pylint: disable=global-statement
from itsdangerous import BadData, SignatureExpired, URLSafeTimedSerializer

__key = None
__max_age = None


BAD_DATA = 'BAD_DATA'
SIGNATURE_EXPIRED = 'SIGNATURE_EXPIRED'

def setup(key: str, max_age: int):
    global __key, __max_age
    __key = key
    __max_age = max_age


def sign(data, namespace):
    global __key
    s = URLSafeTimedSerializer(__key, salt=namespace)

    return s.dumps(data)


def unsign(data, namespace):
    global __key, __max_age
    s = URLSafeTimedSerializer(__key, salt=namespace)

    error = None
    decoded_payload = None

    try:
        decoded_payload = s.loads(data, max_age=__max_age)
    except SignatureExpired:
        error = SIGNATURE_EXPIRED
    except BadData:
        error = BAD_DATA

    return (decoded_payload, error)


def sign_invite(data):
    return sign(data, 'send-invite')


def unsign_invite(data):
    return unsign(data, 'send-invite')
