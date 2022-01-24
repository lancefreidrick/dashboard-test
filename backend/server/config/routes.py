"""
routes.py
"""
from server.config.logger import log
from server.controllers.index_controller import index_blueprint
from server.controllers.auth_controller import auth_blueprint
from server.controllers.user_controller import user_blueprint
from server.controllers.image_controller import image_blueprint
from server.controllers.merchant_controller import merchant_blueprint
from server.controllers.merchant_member_controller import merchant_member_blueprint
from server.controllers.project_controller import project_blueprint
from server.controllers.transaction_controller import transaction_blueprint
from server.controllers.payment_controller import payment_blueprint
from server.controllers.payment_link_controller import payment_link_blueprint
from server.controllers.enrollment_controller import enrollment_blueprint
from server.controllers.error_controller import error_blueprint
from server.controllers.upload_controller import upload_blueprint
from server.controllers.settlement_controller import settlement_blueprint
from server.controllers.reports_controller import reports_blueprint
from server.controllers.account_controller import account_blueprint
from server.controllers.activity_controller import activity_blueprint
from server.controllers.exchange_rate_controller import exchange_rate_blueprint
from server.controllers.lookup_controller import lookup_blueprint
from server.controllers.log_controller import log_blueprint
from server.controllers.dispute_controller import dispute_blueprint
from server.controllers.merchant_payment_method_controller import merchant_payment_method_blueprint

qw_url_prefix = '/xqwapi'


def setup(app):
    log.info('routes:  Setting up all the routes...')
    app.register_blueprint(error_blueprint)
    app.register_blueprint(index_blueprint, url_prefix=qw_url_prefix)
    app.register_blueprint(auth_blueprint, url_prefix=qw_url_prefix)
    app.register_blueprint(user_blueprint, url_prefix=qw_url_prefix)
    app.register_blueprint(image_blueprint, url_prefix=qw_url_prefix)
    app.register_blueprint(merchant_blueprint, url_prefix=qw_url_prefix)
    app.register_blueprint(merchant_member_blueprint, url_prefix=qw_url_prefix)
    app.register_blueprint(project_blueprint, url_prefix=qw_url_prefix)
    app.register_blueprint(transaction_blueprint, url_prefix=qw_url_prefix)
    app.register_blueprint(payment_blueprint, url_prefix=qw_url_prefix)
    app.register_blueprint(payment_link_blueprint, url_prefix=qw_url_prefix)
    app.register_blueprint(enrollment_blueprint, url_prefix=qw_url_prefix)
    app.register_blueprint(upload_blueprint, url_prefix=qw_url_prefix)
    app.register_blueprint(settlement_blueprint, url_prefix=qw_url_prefix)
    app.register_blueprint(reports_blueprint, url_prefix=qw_url_prefix)
    app.register_blueprint(account_blueprint, url_prefix=qw_url_prefix)
    app.register_blueprint(activity_blueprint, url_prefix=qw_url_prefix)
    app.register_blueprint(exchange_rate_blueprint, url_prefix=qw_url_prefix)
    app.register_blueprint(lookup_blueprint, url_prefix=qw_url_prefix)
    app.register_blueprint(log_blueprint, url_prefix=qw_url_prefix)
    app.register_blueprint(dispute_blueprint, url_prefix=qw_url_prefix)
    app.register_blueprint(merchant_payment_method_blueprint, url_prefix=qw_url_prefix)
