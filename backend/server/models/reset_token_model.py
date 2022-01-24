from datetime import datetime, timezone
from marshmallow import Schema, fields
from server.config import environment
from server.utilities import passwords


SECONDS_IN_AN_HOUR = 3600
config = environment.config


class ResetTokenSchema(Schema):
    """
    Used for returning JSON-structured values on the API endpoints
    """
    id = fields.Str()
    resetId = fields.Str(attribute='reset_id')
    tokenHash = fields.Str(attribute='token_hash')
    userId = fields.Str(attribute='user_id')
    isUsed = fields.Bool(attribute='is_used')
    isExpired = fields.Bool(attribute='is_expired')
    expiredAt = fields.DateTime(attribute='expired_at', format='iso')
    createdAt = fields.DateTime(attribute='created_at', format='iso')
    class Meta:
        fields = ('id', 'resetId', 'tokenHash', 'userId', 'isUsed', 'isExpired', 'expiredAt', 'createdAt')
        ordered = True


class ResetToken():
    def __init__(self):
        self.id = None
        self.reset_id = None
        self.token_hash = None
        self.user_id = None
        self.is_used = False
        self.is_expired = False
        self.expired_at = None
        self.created_at = None

    def serialize(self):
        return ResetTokenSchema().dump(self)

    @staticmethod
    def map(data: dict):
        """
        @returns ResetToken
        """
        resettoken = ResetToken()
        resettoken.id = data.get('password_reset_request_id')
        resettoken.reset_id = data.get('reset_id')
        resettoken.token_hash = data.get('token_hash')
        resettoken.user_id = data.get('person_id')
        resettoken.is_used = data.get('is_used')
        resettoken.is_expired = data.get('is_expired')
        resettoken.expired_at = data.get('expired_at')
        resettoken.created_at = data.get('created_at')
        return resettoken

    def check_token(self, token: str) -> bool:
        return passwords.check_password(token, self.token_hash)
