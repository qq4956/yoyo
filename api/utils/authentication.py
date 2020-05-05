from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from api.utils.jwt import get_payload


class AthenticateToken(BaseAuthentication):
    def authenticate(self, request):
        token = request.query_params.get('token')
        if not token:
            token = request.data.get('token')
        payload = get_payload(token)
        if payload == 'token已失效':
            raise exceptions.AuthenticationFailed(  {"code":"1005","msg":'token已失效'})
        elif payload == 'token认证失败':
            raise exceptions.AuthenticationFailed({"code":"1005","msg":'token认证失败'})
        elif payload == '非法的token':
            raise exceptions.AuthenticationFailed({"code":"1005","msg":'非法的token'})
        return (payload, token)


