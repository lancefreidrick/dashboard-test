from attr import dataclass

@dataclass
class TokenStorage:
    jwt_token: str = None
    refresh_token: str = None
    client_id: str = 'test_1csttkfkn6072blo'

    def set_tokens(self, data: dict):
        self.jwt_token = data.get('authenticationToken')
        self.refresh_token = data.get('refresh_token')

    def clear(self):
        self.jwt_token = None
        self.refresh_token = None

    @property
    def bearer_token(self) -> str:
        return f'Bearer {self.jwt_token}'


token_storage = TokenStorage()
