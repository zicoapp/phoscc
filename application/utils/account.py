# coding: utf-8
from flask import session
from leancloud import User

def signin_user(email, password, permenent=True):
    """Sign in user."""
    session.permanent = True

    leanuser = User()
    leanuser.login(email, password)
    token = leanuser.get_session_token()
    session['session_token'] = token


def signout_user():
    """Sign out user."""
    session.pop('session_token', None)


def get_current_user():
    """Get current user."""
    if not 'session_token' in session:
        return None
    user = User.become(session['session_token'])
    if not user:
        signout_user()
        return None
    return user

    # user = User.get_current()
    # return user

    # if 'session_token' in session:
        # user = User.become(session['session_token'])
    # if not 'token' in session:
    #     return None
    # token = session['token']
    # user = User.become(token)
    # if not user:
    #     signout_user()
    #     return None
    # return user
    # if not user:
    #     # signout_user()
    #     return None
    # return user