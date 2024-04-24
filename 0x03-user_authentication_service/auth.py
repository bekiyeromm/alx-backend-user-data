#!/usr/bin/env python3
"""
module to hash and return hashed password using bcrypt
"""
from db import DB
import bcrypt
from user import User
from sqlalchemy.orm.exc import NoResultFound


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


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with the provided email and password

        Args:
            email: The email of the user
            password: The password of the user

        Returns:
            User: The registered User object

        Raises:
            ValueError: If a user already exists with the given email
        """
        """Check if user with email already exists"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))
