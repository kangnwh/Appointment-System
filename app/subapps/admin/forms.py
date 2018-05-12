from flask_wtf import FlaskForm as Form
from wtforms import PasswordField,StringField,IntegerField,DateField,SelectField,SelectMultipleField,FloatField
from wtforms.validators import DataRequired, EqualTo,Email,ValidationError
from app.db_info import Session
from app.models import User,Service,ApptTimeSlot
from flask_login import current_user


class ServiceForm(Form):
    id = IntegerField("Service ID")
    type = StringField("Service Type")
    desc = StringField("Description")
    fee = FloatField("Cost of this service")
