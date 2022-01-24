import secrets

import bcrypt

from server.config import environment
from server.repositories import auth_repository


UNAMBIGUOUS_CHARS = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'

config = environment.config


def check_password(password, encoded_pw) -> bool:
    if not (password and encoded_pw):
        return False
    return bcrypt.checkpw(password.encode('utf8'), encoded_pw.encode('utf8'))


def hash_password(password) -> str:
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()).decode()


def get_random_str(length: int) -> str:
    char_list = list(UNAMBIGUOUS_CHARS)
    secrets.SystemRandom().shuffle(char_list)
    return ''.join(char_list[:length])


def generate_password_reset_tokens() -> (str, str):
    reset_id = get_random_str(config.reset_id_length)
    if auth_repository.find_reset_token(reset_id):
        return generate_password_reset_tokens()

    token = get_random_str(config.reset_token_length)
    token_hash = hash_password(token)
    return (reset_id, token, token_hash)
