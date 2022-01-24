from json import dumps
from datetime import datetime
from contextlib import suppress
from typing import List, Optional

from marshmallow import Schema, fields, ValidationError


class EmailTaskSchema(Schema):
    recipients = fields.List(fields.Str, required=True)
    cc = fields.List(fields.Str)
    bcc = fields.List(fields.Str)
    retries = fields.Int()
    retryTimestamp = fields.DateTime(attribute='retry_timestamp')
    taskId = fields.Str(attribute='task_id', required=True)
    source = fields.Str(required=True)
    args = fields.Dict(required=True)


class EmailTask:
    def __init__(self, **kwargs):
        self.recipients: List[str] = kwargs.get('recipients', [])
        self.cc: Optional[List[str]] = kwargs.get('cc')
        self.bcc: Optional[List[str]] = kwargs.get('bcc')
        self.retries: Optional[int] = kwargs.get('retries', 0)
        self.retry_timestamp: Optional[datetime] = None
        self.task_id: str = kwargs.get('taskId', '')
        self.source: str = kwargs.get('source', '')
        self.args: dict = kwargs.get('args', {})

        with suppress(ValueError, TypeError):
            self.retry_timestamp = datetime.fromisoformat(kwargs.get('retryTimestamp'))

    @property
    def must_execute(self) -> bool:
        return self.retry_timestamp is None or \
               (self.retry_timestamp is not None and self.retry_timestamp < datetime.now())

    def __str__(self) -> str:
        return f'{self.task_id}/{self.recipients}'

    def __repr__(self) -> str:
        return f'EmailTask({self.task_id}, {self.recipients})'

    def json(self) -> str:
        return dumps({
            k: v
            for k, v in EmailTaskSchema().dump(self).items()
            if v is not None
        })

    def validate(self) -> Optional[ValidationError]:
        try:
            EmailTaskSchema().load(self.__dict__)
            return None
        except ValidationError as verr:
            return verr
