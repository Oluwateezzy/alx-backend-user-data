#!/usr/bin/env python3
""" Authentication
"""

from bcrypt import hashpw, gensalt, checkpw
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from db import DB
from user import User


def _hash_password(password: str) -> str:
    """ hash password """
    return hashpw(password.encode('utf-8'), gensalt())


def _generate_uuid() -> str:
    """ generate uuid """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ initialize """
        self._db = DB()
    
    def register_user(self, email: str, password: str) -> User:
        """ Register User """
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists")
        except NoResultFound:
            hash = _hash_password(password)
            user = self._db.add_user(email, hash)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """ Validate login """
        try:
            user = self._db.find_user_by(email=email)
            return checkpw(
                password.encode('utf-8'), user.hashed_password
            )
        except NoResultFound:
            return False
    
    def create_session(self, email: str) -> str:
        """create session """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        id = _generate_uuid()
        self._db.update_user(user.id, session_id=id)
        return id
    
    def 
