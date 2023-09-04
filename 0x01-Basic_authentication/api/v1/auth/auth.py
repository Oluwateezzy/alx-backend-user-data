#!/usr/bin/env python3
""" Auth class
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class """
    
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require auth """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path in excluded_paths:
            return False
        normalize_path = path.rstrip('/')
        normalize_list = [n_list.rstrip('/') for n_list in excluded_paths]
        return normalize_path not in normalize_list

    def authorization_header(self, request=None) -> str:
        """ authorization header """
        if request is None or "Authorization" not in request.headers:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """ current User """
        return None
