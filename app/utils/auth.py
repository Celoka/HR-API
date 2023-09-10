import jwt
from flask import request, jsonify, make_response
from config import get_env
from datetime import datetime, timedelta


class Auth:

    authentication_header_ignore = [
        '/api/v1/user', '/api/v1/user/login','/api/v1/']

    @staticmethod
    def create_token(user_object):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.now() + timedelta(days=1, seconds=120),
                'iat': datetime.now(),
                'sub': user_object
            }
            return jwt.encode(
                payload,
                get_env('SECRET_KEY'),
                algorithm='HS256'
            )

        except Exception as e:
            return e

    @staticmethod
    def check_token():
        if request.method != 'OPTIONS':
            for endpoint in Auth.authentication_header_ignore:
                if request.path.startswith(endpoint):
                    try:
                        token = Auth.get_token()
                        return Auth.decode_token(token)
                    except Exception as e:
                        return make_response(jsonify({'msg': str(e)}), 400)
            return None
    
    @staticmethod
    def get_token(request_obj=None):
        if request_obj:
            header = request_obj.headers.get('Authorization', None)
        else:
            header = request.headers.get('Authorization', None)
        if not header:
            raise Exception('Authorization Header is Expected')
        header_parts = header.split()
        if header_parts[0].lower() != 'bearer':
            raise Exception('Authorization header must start with bearer')
        elif len(header_parts) > 1:
            return header_parts[1]

        raise Exception('Internal application error')

    @staticmethod
    def decode_token(token):
        try:
            decoded = jwt.decode(
                token, 
                get_env('SECRET_KEY'),
                algorithms=['HS256'])
            return decoded
        except jwt.ExpiredSignatureError:
            return make_response(jsonify({'msg': 'Token is expired'})), 400
        except jwt.DecodeError as e:
            raise Exception(f'Error decoding {e}')
