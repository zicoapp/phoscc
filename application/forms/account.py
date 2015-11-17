# coding: utf-8
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from leancloud import User, Query, LeanCloudError


class SigninForm(Form):
    """Form for signin"""
    email = StringField('Email',
                        validators=[
                            DataRequired("Email shouldn't be empty."),
                            Email('Email format is not correct.')
                        ])

    password = PasswordField('Password',
                             validators=[DataRequired("Password shouldn't be empty.")])

    def validate_email(self, field):
        user = Query(User).equal_to('email', self.email.data).find()
        if not user:
            raise ValueError("Account doesn't exist.")

    def validate_password(self, field):
        if self.email.data:
            try:
                user = User()
                user.login(self.email.data, self.password.data)
                self.user = user
            except LeanCloudError:
                raise ValueError('Password is not correct.')

class SignupForm(Form):
    """Form for signin"""
    name = StringField('Username',
                       validators=[DataRequired("Username shouldn't be empty.")])

    email = StringField('Email',
                        validators=[
                            DataRequired(message="Email shouldn't be empty."),
                            Email(message='Email format is not correct.')
                        ])

    password = PasswordField('Password',
                             validators=[DataRequired("Password shouldn't be empty.")])

    repassword = PasswordField('Retype password',
                               validators=[
                                   DataRequired("Please retype the password."),
                                   EqualTo('password', message="Passwords must match.")
                               ])

    def validate_name(self, field):
        user = Query(User).equal_to('username', self.name.data).find()
        # user = User.query.filter(User.name == self.name.data).first()
        if user:
            raise ValueError('This username already exists.')

    def validate_email(self, field):
        user = Query(User).equal_to('email', self.email.data).find()
        # user = User.query.filter(User.email == self.email.data).first()
        if user:
            raise ValueError('This email already exists.')
