""" app """
from flask import Flask
from server.config import (
    routes, mongodb, jsonwebtoken, environment,
    signing, mailer, tenjin_templater, s3, logger, authentication,
    database
)

app = Flask(__name__)
config = environment.config

logger.setup(app, config.flask_env, __name__ != '__main__')
log = logger.log

mongodb.start(config.mongodb_host, config.mongodb_port)
database.start(config.pg_connection_string)
jsonwebtoken.setup(config.jwt_secret, config.jwt_token_life)
authentication.authentication.setup(config.zxcvbn_min_score)
signing.setup(config.app_secret_key, config.signup_link_max_age)
mailer.setup()
tenjin_templater.setup()
s3.setup(config.aws_s3_access_key_id, config.aws_s3_secret_key, config.aws_s3_bucket_name, config.aws_s3_region)
routes.setup(app)

if __name__ == '__main__':
    log.info(f'app:     Running on {config.app_host}:{config.app_port}')
    app.run(host=config.app_host, port=config.app_port, debug=config.flask_env != 'production')
