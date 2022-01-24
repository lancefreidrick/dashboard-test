""" server.utilities.code_generator.py """
from base64 import b32encode
from os import urandom
from typing import Union

from shortuuid import uuid


def generate_ref_id(transaction_type: str) -> Union[bool, str]:
    if not transaction_type:
        return None

    return 'QW-{}-{}'.format(
        transaction_type.upper()[0],
        b32encode(urandom(5)).decode('utf-8'))


def generate_dispute_ref_id() -> str:
    return f'D-{uuid()[:12]}'
