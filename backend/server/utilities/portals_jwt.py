from calendar import timegm
from datetime import datetime, timedelta
import jwt
from server.config.environment import config as env
from server.config.logger import log

def jwt_encode() -> str:
    prefix = 'jwt_encode'

    try:
        with open(env.portals_jwt_private_key, 'r') as key_file:
            token = key_file.read()
    except Exception as e: # pylint: disable=broad-except
        log.error(f'{prefix}: Error encountered trying to read, {env.portals_jwt_private_key} > {str(e)}')
        return ''

    portals_jwt = jwt.encode({
            'merchantCode': env.portals_jwt_merchant_code,
            'timestamp': timegm(datetime.utcnow().utctimetuple()),
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=env.portals_jwt_expiry),
            'iss': env.portals_jwt_issuer,
            'sub': env.portals_jwt_subject
        },
        token,
        algorithm='RS256',
        headers={'kid': env.portals_jwt_key_id}
    )
    return portals_jwt.decode("utf-8")
