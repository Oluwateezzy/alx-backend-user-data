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

def is_valid(hashed_password: bytes, password: str) -> bool:
    """ check validity """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
