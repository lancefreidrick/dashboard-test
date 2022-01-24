""" environment.py """
import os
from dotenv import load_dotenv


class Environment:
    def __init__(self):
        load_dotenv()
        self.app_host = os.environ.get('APP_HOST', '0.0.0.0')
        self.app_port = int(os.environ.get('APP_PORT', 8021))
        self.client_url = os.environ.get('APP_CLIENT_URL', 'http://localhost:3000')

        self.flask_env = os.environ.get('FLASK_ENV', 'development')
        self.flask_app = os.environ.get('FLASK_APP')

        self.mongodb_host = os.environ.get('MONGODB_HOST')
        self.mongodb_port = int(os.environ.get('MONGODB_PORT', 27017))

        self.pg_connection_string = os.environ.get('PG_CONNECTION_STRING')

        self.jwt_secret = os.environ.get('JWT_SECRET')
        self.jwt_token_life = int(os.environ.get('JWT_TOKEN_LIFE', 1440))

        self.sendgrid_secret_key = os.environ.get('SENDGRID_SECRET_KEY')
        self.sendgrid_mode = os.environ.get('SENDGRID_MODE', 'development')
        self.sendgrid_sender = os.environ.get('SENDGRID_SENDER')

        self.app_secret_key = os.environ.get('APP_SIGNING_SECRET_KEY', 'SUP3R_S3CR3T_K3Y')
        self.signup_link_max_age = int(os.environ.get('APP_SIGNING_LINK_MAX_AGE', 604800))

        self.root_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))

        self.reset_id_length = int(os.environ.get('RESET_ID_LENGTH', 24))
        self.reset_token_length = int(os.environ.get('RESET_TOKEN_LENGTH', 12))
        self.reset_token_life = int(os.environ.get('RESET_TOKEN_LIFE', 2))  # hours

        self.aws_s3_access_key_id = os.environ.get('AWS_S3_ACCESS_KEY')
        self.aws_s3_secret_key = os.environ.get('AWS_S3_SECRET_KEY')
        self.aws_s3_bucket_name = os.environ.get('AWS_S3_BUCKET_NAME')
        self.aws_s3_region = os.environ.get('AWS_S3_REGION')

        self.zxcvbn_min_score = int(os.environ.get('ZXCVBN_MIN_SCORE', 3))

        self.apocalypse_url = os.environ.get('APOCALYPSE_URL', 'http://localhost:8040')
        self.portals_url = os.environ.get('PORTALS_URL', 'http://localhost:4200')

        self.portals_jwt_enabled = os.getenv('PORTALS_JWT_ENABLED')
        self.portals_jwt_expiry = int(os.getenv('PORTALS_JWT_EXPIRY', '24'))
        self.portals_jwt_issuer = os.getenv('PORTALS_JWT_ISSUER', 'qwikwire')
        self.portals_jwt_key_id = os.getenv('PORTALS_JWT_KEY_ID')
        self.portals_jwt_merchant_code = os.getenv(
            'PORTALS_JWT_MERCHANT_CODE', 'dashboards-api'
        )
        self.portals_jwt_subject = os.getenv(
            'PORTALS_JWT_SUBJECT', 'developers@aqwire.io'
        )
        self.portals_jwt_private_key = os.getenv(
            'PORTALS_JWT_PRIVATE_KEY', 'portals_key'
        )

config = Environment()
