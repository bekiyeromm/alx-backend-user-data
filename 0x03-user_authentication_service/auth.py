#!/usr/bin/env python3
"""
module to hash and return hashed password using bcrypt
"""
from db import DB
import bcrypt
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


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

    def valid_login(self, email: str, password: str) -> bool:
        """Check if the provided email and password are valid for login

        Args:
            email: The email of the user
            password: The password of the user

        Returns:
            bool: True if the login is valid, False otherwise
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                """Check if the provided password matches the hashed
                password in the database"""
                return bcrypt.checkpw(
                    password.encode('utf-8'), user.hashed_password)
            else:
                return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Create a session for the user with the provided email

        Args:
            email: The email of the user

        Returns:
            str: The session ID
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if user is None:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str):
        """Get the user corresponding to the provided session ID

        Args:
            session_id (str): The session ID

        Returns:
            User or None: The corresponding user if found, None otherwise
        """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """Destroy the session for the user with the provided user ID
        Args:
            user_id (int): The ID of the user
        Returns:
            None
        """
        if not user_id:
            return None
        self._db.update_user(user_id=user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        Find the user corresponding to the email. If the user does not exist,
        raise a ValueError exception. If it exists, generate a UUID and
        update the user’s reset_token database field. Return the token
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError()
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update the password of the user corresponding to the reset token.

        Args:
            reset_token (str): The reset token
            password (str): The new password

        Returns:
            None
        """
        user = self._db.find_user_by(reset_token=reset_token)
        if not user:
            raise ValueError()
        hashed_password = self._hash_password(password)
        self._db.update_user(
            user.id, hashed_password=hashed_password, reset_token=None)


def _generate_uuid() -> str:
    """
    generates a new UUID
    Return:string representation of a new UUID
    """
    return str(uuid.uuid4())
