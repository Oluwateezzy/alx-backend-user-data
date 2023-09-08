#!/usr/bin/env python3
""" Basic Auth class
"""
from flask import request
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """ Session Authentication """
    