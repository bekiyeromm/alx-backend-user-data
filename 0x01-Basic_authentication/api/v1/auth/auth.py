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
        Class Auth manages API authentication
        """
        if path is None:
            return True
        if not excluded_paths:
            return True
        for excluded_path in excluded_paths:
            if path.startswith(excluded_path.rstrip('/')):
                return False
            if excluded_path.endswith('*'):
                idx_after_last_slash = excluded_path.rfind('/') + 1
                excluded = excluded_path[idx_after_last_slash:-1]

                idx_after_last_slash = path.rfind('/') + 1
                tmp_path = path[idx_after_last_slash:]

                if excluded in tmp_path:
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
