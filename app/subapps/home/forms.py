from flask_wtf import Form
from wtforms import BooleanField,PasswordField,StringField,IntegerField
from wtforms.validators import DataRequired, EqualTo,ValidationError

class LoginForm(Form):
    email = StringField('Email', validators = [DataRequired()])
    password = PasswordField('password', validators = [DataRequired()])
    # remember_me = BooleanField('remember_me', default = False)


class RegisterForm(Form):

    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm', validators=[DataRequired()])

    city = StringField('City', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    post_code = IntegerField("Post Code",validators=[DataRequired()])
