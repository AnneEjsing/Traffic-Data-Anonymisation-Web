import base64
import requests
import json
import hashlib
import hmac
from enum import IntEnum
from datetime import datetime, timedelta
import os


secretKey = os.getenv("SECRET_KEY")

def verify_credentials(email, pwd):
    data = {"email": email, "password": pwd}
    resp = requests.request(method='get', url='http://profileservice:1338/login', headers={'content-type': 'text/json'}, json=data)

    if (resp.status_code == 200):
        json_data = resp.json()
        return (True, json_data['user_id'], json_data['role'])
    else:
        return (False, "", "")


def is_not_expired(token):
    if ((not '.' in token) or len(token.split('.')) < 3):
        return False
    header, payload, signature = token.split('.')
    id, subject, role, expiration = get_payload_info(payload)
    is_valid = verify_date(expiration)
    if not is_valid:
        return False
    else:
        return True


def authenticate(token):
    header, payload, signature = token.split('.')
    new_signature = encode(create_signature(header, payload))

    if (new_signature == signature):
        return is_not_expired(token)
    else:
        return False


def verify_token(token, desired_rights):
    is_success = authenticate(token)
    if (is_success):
        is_auth = is_authorized(token, desired_rights)
        if (is_auth):
            return True, 200
        else:
            return False, 403
    else:
        return False, 401


def is_authorized(token, desired_rights):
    header, payload, signature = token.split('.')
    id, subject, role, expiration = get_payload_info(payload)
    return role == desired_rights


def get_user_id(token):
    header, payload, signature = token.split('.')
    id, subject, role, expiration = get_payload_info(payload)
    return subject

def get_rights(token):
    header, payload, signature = token.split('.')
    id, subject, role, expiration = get_payload_info(payload)
    return role

def verify_date(date):
    return (datetime.utcnow() < datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f'))


def get_payload_info(payload):
    text = base64.urlsafe_b64decode(payload + '=' * (4 - len(payload) % 4))
    json_obj = json.loads(text)
    return json_obj['jid'], json_obj['sub'], json_obj['rights'], json_obj['exp']


def create_token(user_id, rights):
    header = encode(json.dumps({"alg": "HS512", "type": "JWT"}))
    payload = encode(create_payload(user_id, rights))
    signature = encode(create_signature(header, payload))
    return '.'.join([header, payload, signature])


def encode(encoding_input):
    """This function converts a string to base64, and removes trailing ="""
    if (isinstance(encoding_input, str)):
        byte = str.encode(encoding_input)
    else:
        byte = encoding_input

    b64 = base64.urlsafe_b64encode(byte)
    res = b64.decode('utf-8')
    return res.replace('=', '')


def create_payload(user_id, rights):
    return json.dumps({'jid': '1', 'sub': user_id, 'rights': rights, 'exp': generate_token_exp_time()})


def create_signature(header, payload):
    return hmac.new(str.encode(secretKey), str.encode(header + '.' + payload), hashlib.sha512).digest()


def generate_token_exp_time():
    return (datetime.utcnow() + timedelta(hours=3)).isoformat()
