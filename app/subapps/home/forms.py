from flask_wtf import FlaskForm as Form
from wtforms import PasswordField,StringField,IntegerField,DateField,SelectField,SelectMultipleField
from wtforms.validators import DataRequired, EqualTo,Email,ValidationError
from app.db_info import Session
from app.models import User,Service,ApptTimeSlot
from flask_login import current_user

class LoginForm(Form):
    email = StringField('Email', validators = [DataRequired()])
    password = PasswordField('password', validators = [DataRequired()])
    # remember_me = BooleanField('remember_me', default = False)


def unique_email(form, field):
    session = Session()
    email = session.query(User).filter(User.email == field.data).first()
    session.close()
    if email:
        raise ValidationError('%s[%s] is already registered' % (field.name,field.data))


class RegisterForm(Form):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    dob = DateField('Date Of Birth', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email(),unique_email])
    phone = StringField('Mobile Phone')
    home_number = StringField('Home Phone')
    work_number = StringField('Work Phone')
    gender = SelectField('Gender', validators=[DataRequired()], choices=[('M', 'Male'), ('F', 'Female')])
    password = PasswordField('Password', validators=[DataRequired(),EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm', validators=[DataRequired()])

    city = StringField('City', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    post_code = IntegerField("Post Code",validators=[DataRequired()])


class UserProfileForm(Form):
    # user_id = IntegerField("User ID",validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    phone = StringField('Mobile Phone')
    home_number = StringField('Home Phone')
    work_number = StringField('Work Phone')
    dob = DateField('Date Of Birth', validators=[DataRequired()])
    gender = SelectField('Gender', validators=[DataRequired()],choices=[('M', 'Male'), ('F', 'Female')])
    # address related
    # address_id = IntegerField("Address ID",validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    post_code = IntegerField("Post Code",validators=[DataRequired()])


class PetForm(Form):
    id = IntegerField("Pet ID")
    name = StringField('Name', validators = [DataRequired()])
    breed = StringField('Breed', validators = [DataRequired()])
    gender = SelectField('Gender', validators=[DataRequired()], choices=[('M', 'Male'), ('F', 'Female')])
    dob = DateField('Date Of Birth', validators=[DataRequired()])
    # remember_me = BooleanField('remember_me', default = False)

class CardForm(Form):
    id = IntegerField("Card ID")
    card_num = StringField('Card No.', validators = [DataRequired()])
    bank = StringField('Bank', validators = [DataRequired()])

class NoValidationSelectField(SelectField):
    def pre_validate(self, form):
        """per_validation is disabled"""


class ApptForm(Form):
    id = IntegerField("Appointment ID")
    appt_date = DateField("Appointment Date")
    appt_timeslot = NoValidationSelectField("Time Slot",coerce=int,choices=[(1,"Select date first")])
    appt_service = SelectMultipleField("Services",coerce=int,choices=Session().query(Service.id,Service.type,Service.desc).all())

    def pre_validate(self, form):
        pass
