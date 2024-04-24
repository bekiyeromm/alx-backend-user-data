#!/usr/bin/env python3
"""
module to hash and return hashed password using bcrypt
"""
from db import DB
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt

    Args:
        password: The password to hash

    Returns:
        bytes: The salted hash of the password
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
