# coding: utf-8
from flask import render_template, Blueprint, redirect, request, url_for
from ..forms import SigninForm, SignupForm
from ..utils.account import signin_user, signout_user
from ..utils.permissions import VisitorPermission, UserPermission
from leancloud import User, LeanCloudError

bp = Blueprint('account', __name__)


@bp.route('/signin', methods=['GET', 'POST'])
@VisitorPermission()
def signin():
    """Signin"""
    form = SigninForm()
    if form.validate_on_submit():
        signin_user(email=form.data['email'], password=form.data['password'])
        return redirect(request.args.get('next') or url_for('site.index'))
    return render_template('account/signin/signin.html', form=form)


@bp.route('/signup', methods=['GET', 'POST'])
@VisitorPermission()
def signup():
    """Signup"""
    print request.args.get('next')
    form = SignupForm()
    if form.validate_on_submit():
        params = form.data.copy()
        params.pop('repassword')
        user = User()
        user.set("username", params['name'])
        user.set("password", params['password'])
        user.set("email", params['email'])
        user.sign_up()
        signin_user(email=params['email'], password=params['password'])
        return redirect(request.args.get('next') or url_for('site.index'))
    return render_template('account/signup/signup.html', form=form)


@bp.route('/signout')
def signout():
    """Signout"""
    signout_user()
    return redirect(request.referrer or url_for('site.index'))
