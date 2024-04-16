#!/usr/bin/env python3

"""
authorization file for basic authentication
"""
from flask import request, Flask
from typing import List, TypeVar


class Auth:
    """
    class which manages API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        function authorization header
        """
        if request is None:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        function current user
        """
        request = Flask(__name__)
        return None
