# coding: utf-8
from flask import session, abort, flash, redirect, url_for, g, request
from permission import Rule
from leancloud import User


class VisitorRule(Rule):
    def check(self):
        return 'session_token' not in session

    def deny(self):
        return redirect(url_for('site.index'))


class UserRule(Rule):
    def check(self):
        return g.user

    def deny(self):
        flash('Sign in first.')
        return redirect(url_for('account.signin', next=request.url))
        
class AdminRule(Rule):
    def base(self):
        return UserRule()

    def check(self):
        user = User.become(session['session_token'])
        return user and user.get('isAdmin')

    def deny(self):
        abort(403)
