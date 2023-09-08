#!/usr/bin/env python3
""" Auth class
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """ Auth class """
    
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require auth """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        for pattern in excluded_paths:
            if pattern.endswith('/'):
                pattern = pattern[:-1]
                if path.startswith(pattern):
                    return False
            elif path == pattern:
                return False
        return True
        

    def authorization_header(self, request=None) -> str:
        """ authorization header """
        if request is None or "Authorization" not in request.headers:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """ current User """
        return None
    
    def session_cookie(self, request=None):
        """ session cookies """
        if request is None:
            return None
        return request.cookies.get(getenv('SESSION_NAME'))
