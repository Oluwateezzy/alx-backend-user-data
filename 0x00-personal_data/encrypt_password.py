#!/usr/bin/env python3
"""
Main file
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ password hashing """
    bytye = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytye, salt)
