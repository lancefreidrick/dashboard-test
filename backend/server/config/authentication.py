from typing import Tuple
from uuid import uuid4
from functools import partial, wraps
import datetime
import secrets

from flask import request, g, abort, make_response
from jwt.exceptions import ExpiredSignatureError
from werkzeug.datastructures import Authorization
from zxcvbn import zxcvbn

from server.config import jsonwebtoken
from server.config.logger import log
from server.models.person_model import MerchantRoles, Person, Roles
from server.repositories import auth_repository, person_repository, merchant_repository


SysRole = Tuple[int, str, str, str]
MerchantRole = Tuple[int, str, str, str]

class JWTAuthentication:
    def __init__(self):
        self.scheme = 'Bearer'
        self.realm = 'Authentication Required'
        self.expiry = 31536000000
        self.zxcvbn_min_score = None

    def setup(self, zxcvbn_min_score: int):
        self.zxcvbn_min_score = zxcvbn_min_score

    def verify_token_callback(self, token):
        """ Decodes the token and sets the user to g.user """
        g.user = None
        g.token = token
        try:
            is_decoded, decoded_value = jsonwebtoken.decode(token)
        except ExpiredSignatureError:
            return False

        if not is_decoded:
            return False

        if 'user_email' in decoded_value:
            user_id = int(decoded_value.get('id'))
            queried_user = person_repository.find_person_by_id(user_id)

            if queried_user:
                g.user = queried_user
                return True

        log.warning('Unable to verify the API token')

        return False

    def validate_export_token(self, token: str) -> Tuple[bool, Person]:
        """
        This is only used to validate the export token which contains user and sessionkey
        Arguments:
            token {str} -- JWT token
        Returns:
            (bool, Person)
        """
        try:
            is_decoded, decoded_value = jsonwebtoken.decode(token)
            if not is_decoded or 'user' not in decoded_value:
                return (False, None)

            person_id = int(decoded_value.get('user').get('id'))
            person = person_repository.find_person_by_id(person_id)

            if not person:
                return False, None

            return True, person
        except ValueError:
            return False, None
        except ExpiredSignatureError:
            return False, None

    def auth_error_callback(self):
        res = make_response()
        if res.status_code == 200:
            # if user didn't set status code, use 401
            res.status_code = 401
        if 'WWW-Authenticate' not in res.headers.keys():
            res.headers['WWW-Authenticate'] = self.authenticate_header()
        abort(401)

    def authenticate_header(self):
        return '{0} realm="{1}"'.format(self.scheme, self.realm)

    def parse_auth(self, auth):
        if auth is None and 'Authorization' in request.headers:
            try:
                auth_type, token = request.headers['Authorization'].split(None, 1)
                auth = Authorization(auth_type, {'token': token})
            except ValueError:
                # The Authorization header is either empty or has no token
                pass

        if auth is not None and auth.type.lower() != self.scheme.lower():
            auth = None

        return auth

    def authenticate(self, auth):
        if auth:
            token = auth['token']
        else:
            token = ''

        return self.verify_token_callback(token)

    def jwt_required(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            new_token = False
            auth = self.parse_auth(request.authorization)

            if request.method != 'OPTIONS':
                if not self.authenticate(auth):
                    new_token = self.verify_refresh_token(request.headers)
                    if not new_token:

                        # Clear TCP receive buffer of any pending data
                        request.data = None
                        return self.auth_error_callback()

            res = make_response(f(*args, **kwargs))
            if new_token:
                res.headers['x-access-token'] = new_token
            return res
        return decorated

    def jwt_optional(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            new_token = False
            auth = self.parse_auth(request.authorization)

            if request.method != 'OPTIONS':
                if not self.authenticate(auth):
                    new_token = self.verify_refresh_token(request.headers)
                    if not new_token:
                        # Create anonymous user
                        g.user = Person.create_anonymous_user()

            res = make_response(f(*args, **kwargs))
            if new_token:
                res.headers['x-access-token'] = new_token
            return res
        return decorated

    def admin_required(self, f=None, *, message=None):
        """Restricts a route for admin users only

        Keyword arguments:
            message {str} -- The error message the API returns (default "You shouldn't be here.")
        """
        if f is None:
            return partial(self.admin_required, message=message)

        message = message if message else "You shouldn't be here."

        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                if not g.user.is_admin:
                    abort(403, {'message': message})
            except AttributeError:
                abort(403, {'message': message})
            return f(*args, **kwargs)
        return decorated

    def min_system_access_role(self, role: tuple):
        """
        Checks for the minimum system role level of the user to access the API

        Arguments:
            role {tuple} -- Minimum access role level
        """
        def decorator(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                try:
                    if g.user and g.user.system_role[0] > role[0]:
                        abort(403, {'message': 'You are not allowed here'})
                except AttributeError:
                    abort(403, {'message': 'You are not allowed here'})
                return f(*args, **kwargs)
            return decorated
        return decorator

    def min_access_role(self, sys_role: SysRole, m_role: MerchantRole = MerchantRoles.NO_ACCESS):
        """
        Checks for the minimum merchant role level of the user to access the API
        """
        fn = 'min_access_role'
        def decorator(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                try:
                    if not g.user:
                        log.error(f'{fn}: Unauthorized access. Request user is empty.')
                        abort(401, {'message': 'Unauthorized'})

                    if g.user.system_role[0] > sys_role[0]:
                        log.error(f'{fn}: Forbidden on system role {g.user.system_role} > {sys_role}')
                        abort(403, {'message': 'You are not allowed here'})

                    if g.user.system_role[0] == Roles.USER[0] and m_role and g.user.merchant_role[0] > m_role[0]:
                        log.error(f'{fn}: Forbidden on merchant role {m_role} > {sys_role}')
                        abort(403, {'message': 'You are not allowed here'})

                    return f(*args, **kwargs)
                except AttributeError as ae:
                    log.error(f'{fn}: Exception on attribute error {ae}')
                    abort(403, {'message': 'You are not allowed here'})
            return decorated
        return decorator

    def min_access_merchant_role(self, sys_role: SysRole, m_role: MerchantRole = MerchantRoles.NO_ACCESS):
        """
        Checks for the minimum merchant role level of the user to access the API
        """
        fn = 'min_access_merchant_role'
        def decorator(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                try:
                    if not g.user:
                        log.error(f'{fn}: Unauthorized access. Request user is empty.')
                        abort(401, {'message': 'Unauthorized'})

                    merchant_id = request.view_args.get('merchant_id')
                    merchant = merchant_repository.find_merchant_by_id(merchant_id)
                    if not merchant:
                        log.error(f'{fn}: Merchant does not exist.')
                        abort(404, {'message': 'Merchant does not exist'})

                    if not merchant.is_enabled:
                        log.error(f'{fn}: Merchant is closed.')
                        abort(404, {'message': 'Merchant account is closed.'})

                    g.merchant = merchant

                    if g.user.system_role[0] < sys_role[0]:
                        return f(*args, **kwargs)

                    if merchant.merchant_code not in g.user.scopes:
                        log.error(f'{fn}: Forbidden for user, merchant not in scope')
                        abort(403, {'message': 'You are not allowed here'})

                    user = person_repository.find_merchant_member_by_id(merchant, g.user.id)
                    if not user:
                        log.error(f'{fn}: User not found')
                        abort(400, {'message': 'User not found'})

                    if user.system_role[0] == Roles.USER[0] and m_role and user.merchant_role[0] > m_role[0]:
                        log.error(f'{fn}: Forbidden on merchant role {m_role} > {sys_role}')
                        abort(403, {'message': 'You are not allowed here'})

                    g.merchant = merchant

                    return f(*args, **kwargs)
                except AttributeError as ae:
                    log.error(f'{fn}: Exception on attribute error {ae}')
                    abort(403, {'message': 'You are not allowed here'})
            return decorated
        return decorator

    def validate_password_strength(self, query_param: str):
        """
        Checks if the specified password is strong enough

        Arguments:
            query_param: str
        """
        def decorator(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                body = request.get_json()
                password = body.get(query_param) or ''
                results = zxcvbn(password)
                if results['score'] < self.zxcvbn_min_score:
                    messages = []
                    if results['feedback']['warning']:
                        messages.append('WARNING: ' + results['feedback']['warning'])
                    messages.append('You need a stronger password.')
                    messages.extend(results['feedback']['suggestions'])
                    abort(401, {'message': '\n'.join(messages)})
                return f(*args, **kwargs)
            return decorated
        return decorator

    def generate_export_token(self, person: Person) -> str:
        """Generates the JWT with encoded user session

        Arguments:
            person {Person} -- Authenticated User

        Returns:
            token -- JWT authentication token
        """
        max_token_life_mins = 3
        payload = {
            'user': person.get_jwt_serialized_person(),
            'sessionkey': str(uuid4())
        }
        log.info(f'auth: Generating export token for {person.email}', )
        return jsonwebtoken.encode(payload, token_life_mins=max_token_life_mins)

    def get_refresh_token(self) -> str:
        """Gets the associated refresh token for the client

        Arguments:
            person {Person} -- Authenticated User
            client_id {str} -- 40 character long text string in hexadecimal

        Returns:
            refresh_token -- Refresh token
        """
        # refresh_token = secrets.token_hex(40)
        return secrets.token_hex(40)

    def verify_refresh_token(self, headers):
        """Returns a new JWT authentication token if refresh token is valid"""
        client_id = headers.get('X-Client-Id')
        refresh_token = headers.get('X-Refresh-Token')
        queried_user = None

        if not client_id or not refresh_token:
            log.debug('auth: X-Client-Id or X-Refresh-Token is missing')
            return False

        active_session = auth_repository.find_active_session(client_id, refresh_token)

        if not active_session:
            log.debug('No existing session from db')
            return False

        queried_user = person_repository.find_person_by_id(active_session.person_id)
        if not queried_user:
            log.debug('auth: queried user is missing from db')
            return False

        token = jsonwebtoken.encode({'user_email': queried_user.email, 'id': queried_user.id})
        g.user = queried_user
        g.token = token

        log.info(f'auth: JWT refreshed for {queried_user.email} at {datetime.datetime.now()}')

        return token

    def login(self, data: dict) -> str:
        """
        - Generates JWT and refresh token
        - Saves session to directory.session

        Argument: {
            'person':
            'client_id':
            'ip_address'
            'user_agent'
        }

        Returns:
            jwt_token,
            refresh_token
        """

        data['refresh_token'] = self.get_refresh_token()
        jwt_token = jsonwebtoken.encode({'user_email': data['person'].email, 'id': data['person'].id})
        session_id = auth_repository.create_session(data)
        log.info(f'Saved new session with id: {session_id}')
        return jwt_token, data['refresh_token']

    def logout(self, person, client_id):
        if not auth_repository.disable_session(person.id, client_id):
            return False
        return True

authentication = JWTAuthentication()
