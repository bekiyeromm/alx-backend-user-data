#!/usr/bin/env python3
"""
session auth class
"""
import uuid
from .auth import Auth


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
