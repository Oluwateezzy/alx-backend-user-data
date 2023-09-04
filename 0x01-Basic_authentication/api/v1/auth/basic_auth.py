#!/usr/bin/env python3
""" Basic Auth class
"""
from flask import request
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """ Basic Auth """
    
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """ extract base64 header """
        if authorization_header is None or type(authorization_header) != str or not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(' ')[1]
    
    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """ decode base64 """
        if base64_authorization_header is None or type(base64_authorization_header) != str:
            return None
        try:
            decoded_byte = base64.b64decode(base64_authorization_header)
            decoded_str  = decoded_byte.decode('utf-8')
            return decoded_str
        except:
            return None
    
    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """ extract user credentials """
        
