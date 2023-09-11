#!/usr/bin/env python3
""" Basic Auth class
"""
from flask import request
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """ Basic Auth """

    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """ extract base64 header """
        if authorization_header is None or\
            type(authorization_header) != str or\
                not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """ decode base64 """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None
        try:
            decoded_byte = base64.b64decode(base64_authorization_header)
            decoded_str = decoded_byte.decode('utf-8')
            return decoded_str
        except Exception:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """ extract user credentials """
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) != str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        lis = decoded_base64_authorization_header.split(':')
        return lis[0], ":".join(lis[1:])

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar('User'):
        """ user Object """
        if user_email is None or type(user_email) != str:
            return None
        if user_pwd is None or type(user_pwd) != str:
            return None
        try:
            user_instance = User()
            users = user_instance.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ current user """
        auth_header = self.authorization_header(request)
        extract_header = self.extract_base64_authorization_header(auth_header)
        decode_header = self.decode_base64_authorization_header(extract_header)
        user_email, user_pwd = self.extract_user_credentials(decode_header)
        return self.user_object_from_credentials(user_email, user_pwd)
