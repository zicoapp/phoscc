# coding: utf-8
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from leancloud import User, Query, LeanCloudError


class SigninForm(Form):
    """Form for signin"""
    email = StringField('邮箱',
                        validators=[
                            DataRequired("邮箱不能为空."),
                            Email('邮箱格式不正确.')
                        ])

    password = PasswordField('密码',
                             validators=[DataRequired("密码不能为空.")])

    def validate_email(self, field):
        user = Query(User).equal_to('email', self.email.data).find()
        if not user:
            raise ValueError("账号不存在.")

    def validate_password(self, field):
        if self.email.data:
            try:
                user = User()
                user.login(self.email.data, self.password.data)
                self.user = user
            except LeanCloudError:
                raise ValueError('密码不正确.')

class SignupForm(Form):
    """Form for signin"""
    name = StringField('用户名',
                       validators=[DataRequired("用户名不能为空.")])

    email = StringField('邮箱',
                        validators=[
                            DataRequired(message="邮箱不能为空."),
                            Email(message='邮箱格式不正确.')
                        ])

    password = PasswordField('密码',
                             validators=[DataRequired("密码不能为空.")])

    repassword = PasswordField('密码确认',
                               validators=[
                                   DataRequired("请再次输入密码."),
                                   EqualTo('password', message="密码不匹配.")
                               ])

    def validate_name(self, field):
        user = Query(User).equal_to('username', self.name.data).find()
        # user = User.query.filter(User.name == self.name.data).first()
        if user:
            raise ValueError('该用户名已被注册.')

    def validate_email(self, field):
        user = Query(User).equal_to('email', self.email.data).find()
        # user = User.query.filter(User.email == self.email.data).first()
        if user:
            raise ValueError('该邮箱已被注册.')
