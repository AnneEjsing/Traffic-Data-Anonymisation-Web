import base64
import requests
import json
import hashlib
import hmac
from enum import IntEnum
from datetime import datetime, timedelta


secretKey = json.load(open("config.secrets.json"))['JWT']['SECRET_KEY']

def verify_credentials(email, pwd):
    data = {"email": email, "password": pwd}
    resp = requests.request(method='get', url='http://profileservice:1338/login', headers={'content-type': 'text/json'}, json=data)

    if (resp.status_code == 200):
        json_data = resp.json()
        return (True, json_data['id'], json_data['rights'])
    else:
        return (False, "", "")


def is_not_expiered(token):
    if ((not '.' in token) or len(token.split('.')) < 3):
        return False
    header, payload, signature = token.split('.')
    id, subject, role, expiration = get_payload_info(payload)
    isValid = verify_date(expiration)
    if not isValid:
        return False
    else:
        return True


def authenticate(token):
    header, payload, signature = token.split('.')
    new_signature = encode(create_signature(header, payload))

    if (new_signature == signature):
        return is_not_expiered(token)
    else:
        return False


def verify_token(token, desired_role):
    isSuccess = authenticate(token)
    if (isSuccess):
        isAuth = is_authorized(token, desired_role)
        if (isAuth):
            return True, 200
        else:
            return False, 403
    else:
        return False, 401


def is_authorized(token, desiredRole):
    header, payload, signature = token.split('.')
    id, subject, role, expiration = get_payload_info(payload)
    return role == desiredRole


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
    jsonObj = json.loads(text)
    return jsonObj['jid'], jsonObj['sub'], jsonObj['rights'], jsonObj['exp']


def create_token(userId, rights):
    header = encode(create_header())
    payload = encode(create_payload(userId, rights))
    signature = encode(create_signature(header, payload))
    return '.'.join([header, payload, signature])


def encode(encodingInput):
    """This function converts a string to base64, and removes trailing ="""
    if (isinstance(encodingInput, str)):
        byte = str.encode(encodingInput)
    else:
        byte = encodingInput

    b64 = base64.urlsafe_b64encode(byte)
    res = b64.decode('utf-8')
    return res.replace('=', '')


def create_header():
    return json.dumps({"alg": "HS512", "type": "JWT"})


def create_payload(userId, rights):
    return json.dumps({'jid': '1', 'sub': userId, 'rights': rights, 'exp': generate_token_exp_time()})


def create_signature(header, payload):
    return hmac.new(str.encode(secretKey), str.encode(header + '.' + payload), hashlib.sha512).digest()


def generate_token_exp_time():
    return (datetime.utcnow() + timedelta(hours=3)).isoformat()
