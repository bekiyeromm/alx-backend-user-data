#!/usr/bin/env python3
"""
session auth class
"""
import uuid
from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        a function creates a Session ID for a user_id:
        Return
            None if user_id is None or if user_id is not a string
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        returns a User ID based on a Session ID:
            Return None if session_id is None or session id is
            not string
            Return the value (the User ID) for the key
            session_id in the dictionary user_id_by_session_id
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        returns a User instance based on a cookie value:
        """
        if request is None:
            return None
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None
        return User.get(user_id)
