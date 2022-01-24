import hmac
import hashlib
import base64
from urllib import parse

def digest(msg: str, key: str):
    b_key = bytes(key, 'utf-8')
    b_message = bytes(msg, 'utf-8')
    signature = hmac.new(b_key, b_message, hashlib.sha256).digest()

    encoded_token = base64.urlsafe_b64encode(signature)
    urlsafe_token = parse.quote(encoded_token)
    return urlsafe_token