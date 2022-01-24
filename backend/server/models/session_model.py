class Session():
    def __init__(self):
        self.id = None
        self.person_id = None
        self.client_id = None
        self.refresh_token = None
        self.ip_address = None
        self.user_agent = None
        self.is_session_enabled = None

    @staticmethod
    def map(data: dict):
        """
        @returns Session
        """
        session = Session()
        session.id = data.get('session_token_id')
        session.person_id = data.get('person_id')
        session.client_id = data.get('client_id')
        session.refresh_token = data.get('refresh_token')
        session.ip_address = data.get('ip_address')
        session.user_agent = data.get('user_agent')
        session.is_session_enabled = data.get('is_session_enabled')
        return session
