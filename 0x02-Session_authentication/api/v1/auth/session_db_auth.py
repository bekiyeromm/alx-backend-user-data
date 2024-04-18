#!/usr/bin/env python3
'''
Session Authentication with storage and expiration
'''
from datetime import datetime, timedelta
from flask import request
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    '''
    Class SessionDBAuth with expiration and storage
    - Inherits from SessionAuth
    '''

    def create_session(self, user_id=None) -> str:
        '''
        Creates and stores a Session with unique ID
        '''
        session_id = super().create_session(user_id)
        if type(session_id) == str:
            kwargs = {
                'user_id': user_id,
                'session_id': session_id,
            }
            user_session = UserSession(**kwargs)
            user_session.save()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        '''
        Retrieves User inforation based on Session ID
        '''
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        cur_time = datetime.now()
        time_dur = timedelta(seconds=self.session_duration)
        exp_time = sessions[0].created_at + time_dur
        if exp_time < cur_time:
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None) -> bool:
        '''
        Destroys Authenticated Session
        '''
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        sessions[0].remove()
        return True
