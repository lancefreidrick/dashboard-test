"""
context_manager.py
"""
from enum import Enum
from contextlib import contextmanager
from server.config.logger import log
from server.models.person_model import Person
from server.models.activity_model import Activity
from server.repositories.activity_repository import add_activity_log


class ContextStatus(Enum):
    ERROR = 'ERROR'
    SUCCESS = 'SUCCESS'
    NONE = 'NONE'


class LogContext:
    def __init__(self):
        self.status = ContextStatus.NONE
        self.action: str = None
        self.description: str = None
        self.metadata: dict = {}

    def propset(self,
                status: ContextStatus = None,
                action: str = None,
                description: str = None,
                metadata: dict = None):
        self.status = status or self.status
        self.action = action or self.action
        self.description = description or self.description
        self.metadata = metadata or self.metadata

    def set_exc(self, exception_text: str):
        self.status = ContextStatus.ERROR
        self.description = exception_text

    def __repr__(self):
        return f'LogContext({self.status}, {self.action}, {self.metadata})'

    def __str__(self):
        return f'LogContext: {self.status} {self.action} {self.metadata}'


@contextmanager
def open_transaction_context(user: Person, source: str):
    context = LogContext()
    try:
        yield context
    finally:
        if context.status == ContextStatus.ERROR:
            log.error(f'{context.action}: {context.description}')

        activity_log = Activity(
            activity_type=context.action,
            message=context.description or 'No indicated action on the context',
            activity_level=context.status.value)
        activity_log.affected_data = context.metadata
        activity_log.logged_by_id = user.id
        activity_log.logged_by_name = user.name
        activity_log.logged_source = source

        is_logged, msg = add_activity_log(activity_log)
        log.debug(f'Activity log: {context} => {is_logged}: {msg}')
