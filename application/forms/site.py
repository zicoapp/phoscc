# coding: utf-8
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from leancloud import User, Query, LeanCloudError

class MultiTagForm(Form):
    """Form for tags"""
    photoid = StringField('ID')
    tags = StringField('标签',
                        validators=[
                            DataRequired("可不可以帮打几个标签撒^_^~")
                        ])

    # def validate_tags(self, field):
    #     user = Query(User).equal_to('email', self.email.data).find()
    #     if not user:
    #         raise ValueError("账号不存在.")