# coding: utf-8
from flask import session
from leancloud import User

def signin_user(uname, passwd, permenent=True):
    """Sign in user."""
    user = User().login(uname, passwd)
    session.permanent = True
    session['user_id'] = user.get_session_token()

def signout_user():
    """Sign out user."""
    session.pop('user_id', None)


def get_current_user():
    """Get current user."""
    if not 'user_id' in session:
        return None
    # # user = session
    # user = User.get_current()
    # user = User.query.filter(User.id == session['user_id']).first()
    user = User.become(session['user_id'])
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