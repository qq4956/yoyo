import datetime
import jwt
from jwt import exceptions

SALT = "yoyo"
def create_token(nickname, uid):
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    payload = {
        'nickname': nickname,
        'uid': uid,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=9999)
    }
    token = jwt.encode(payload=payload, key=SALT, algorithm="HS256", headers=headers).decode('utf-8')
    return token


def get_payload(token):

    try:
        verified_payload = jwt.decode(token, SALT, True)
        return verified_payload
    except exceptions.ExpiredSignatureError:
        msg = 'token已失效'
    except jwt.DecodeError:
        msg = 'token认证失败'
    except jwt.InvalidTokenError:
        msg = '非法的token'
    return msg