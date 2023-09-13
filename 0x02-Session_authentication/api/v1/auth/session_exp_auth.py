#!/usr/bin/env python3
""" Basic Auth class
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime


class SessionExpAuth(SessionAuth):
    """ session expiration """
    def __init__(self) -> None:
        env = getenv("SESSION_DURATION")
        self.session_duration = int(env) if env else 0

    def create_session(self, user_id=None):
        """ create session """
        id = super().create_session(user_id)
        if not id:
            return None
        self.user_id_by_session_id[id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return id

    def user_id_for_session_id(self, session_id=None):
        """ user id for session """
        try:
            if session_id is None:
                return None
            if session_id not in self.user_id_by_session_id:
                return None
            session_dict = self.user_id_by_session_id[session_id]
            if session_dict["created_at"] is None:
                return None
            if self.session_duration <= 0:
                return session_dict["user_id"]
            created_at = session_dict["created_at"].timestamp()
            if created_at + self.session_duration < datetime.now().timestamp():
                del session_dict[session_id]
                return None
            return session_dict["user_id"]
        except Exception:
            return None
