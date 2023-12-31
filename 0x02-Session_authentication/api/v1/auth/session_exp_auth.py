#!/usr/bin/env python3
""" Basic Auth class
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ session expiration """
    def __init__(self) -> None:
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ create session """
        id = super().create_session(user_id)
        if not id:
            return None
        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[id] = session_dictionary
        return id

    def user_id_for_session_id(self, session_id=None):
        """ user id for session """
        try:
            if session_id is None:
                return None
            if session_id not in self.user_id_by_session_id:
                return None
            print(session_id)
            session_dict = self.user_id_by_session_id[session_id]
            if session_dict["created_at"] is None:
                return None
            if self.session_duration <= 0:
                return session_dict["user_id"]
            created_at = session_dict["created_at"]
            exp = timedelta(seconds=self.session_duration) + created_at
            print(exp, created_at)
            if exp < datetime.now():
                return None
            else:
                return session_dict["user_id"]
        except Exception:
            return None
