""" logger.py """
import sys
import logging
from flask import Flask


log = logging.getLogger('werkzeug')

class DebugLogFilter(logging.Filter):
    def filter(self, record):
        return record.levelno >= logging.NOTSET


class ProductionLogFilter(logging.Filter):
    def filter(self, record):
        return record.levelno >= logging.INFO

def setup(app: Flask, flask_env: str, runs_on_gunicorn=False):
    """
    Sets the messages lower than logging.WARNING to stdout
        and the messages logging.WARNING and above to stderr

    Sets the logging level for werkzeug based on `flask_env` variable.

    Arguments:
        flask_env {str}
    """
    log_filter = ProductionLogFilter() if flask_env == 'production' else DebugLogFilter()

    out_handler = logging.StreamHandler(sys.stdout)
    error_handler = logging.StreamHandler(sys.stderr)

    out_handler.addFilter(log_filter)
    out_handler.setLevel(logging.DEBUG)
    error_handler.setLevel(logging.WARNING)
    rootLogger = logging.getLogger()
    rootLogger.addHandler(out_handler)
    rootLogger.addHandler(error_handler)

    logger = logging.getLogger('werkzeug')
    logger.setLevel(logging.INFO if flask_env == 'production' else logging.DEBUG)

    if runs_on_gunicorn:
        gunicorn_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers.extend(gunicorn_logger.handlers)
        app.logger.setLevel(gunicorn_logger.level)
