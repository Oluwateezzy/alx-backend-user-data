#!/usr/bin/env python3
""" Basic Auth class
"""
from flask import request
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.models.user import User


class SessionAuth(Auth):
    """ Session Authentication """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ create session """
        if user_id is None:
            return None
        if type(user_id) != str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(
        self, session_id: str = None
    ) -> str:
        """ user_id for session_id """
        if session_id is None:
            return None
        if type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ return the user id base on the cookies """
        sessionCookie = self.session_cookie(request)
        sessionId = self.user_id_for_session_id(sessionCookie)
        return User.get(sessionId)

    def destroy_session(self, request=None):
        """ destroy session """
        if request is None:
            return False
        if not request.headers.get("Cookie"):
            return False
        session = request.headers.get("Cookie").split("=")
        print(session[1])
        if session[1] not in self.user_id_by_session_id:
            return False
        del self.user_id_by_session_id[session[1]]
        return True
