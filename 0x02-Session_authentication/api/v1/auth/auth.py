#!/usr/bin/env python3

"""
authorization file for basic authentication
"""
from flask import request, Flask
from typing import List, TypeVar
import os


class Auth:
    """
    class which manages API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Class Auth manages API authentication
        """
        if path is None:
            return True
        if not excluded_paths or excluded_paths is None:
            return True

        if path[-1] == '/':
            path = path[:-1]

        contains_slash = False
        for excluded_path in excluded_paths:
            if excluded_path[-1] == '/':
                excluded_path = excluded_path[:-1]
                contains_slash = True

            if excluded_path.endswith('*'):
                idx_after_last_slash = excluded_path.rfind('/') + 1
                excluded = excluded_path[idx_after_last_slash:-1]

                idx_after_last_slash = path.rfind('/') + 1
                tmp_path = path[idx_after_last_slash:]

                if excluded in tmp_path:
                    return False

            if contains_slash:
                contains_slash = False

        path += '/'

        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        function authorization header
        """
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """
        function current user
        """
        request = Flask(__name__)
        return None

    def session_cookie(self, request=None):
        """
        a function returns a cookie value from a request:
        Return:
            None if request is None
            value of the cookie named _my_session_id from request
        """
        if request is None:
            return None
        session_name = os.getenv("SESSION_NAME", "_my_session_id")
        return request.cookies.get(session_name)
