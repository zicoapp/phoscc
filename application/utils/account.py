# coding: utf-8
from flask import session
from leancloud import User


def signin_user(uname, passwd):
    """Sign in user."""
    User().login(uname, passwd)
    # session.permanent = permenent
    # session['user_id'] = user.id


def signout_user():
    """Sign out user."""
    session.pop('user_id', None)


def get_current_user():
    """Get current user."""
    if not 'user_id' in session:
        return None
    user = User.query.filter(User.id == session['user_id']).first()
    if not user:
        signout_user()
        return None
    return user