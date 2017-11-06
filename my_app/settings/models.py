from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, PasswordField, SubmitField, FileField, SelectMultipleField, widgets, Form, \
    SelectField, DecimalField
from wtforms import TextAreaField
from wtforms.validators import InputRequired, Length, EqualTo, Optional
from my_app import db
from my_app import bcrypt
import datetime
from sqlalchemy import Sequence

class NewUserForm(FlaskForm):
    usr_name = StringField('', validators=[InputRequired()])
    usr_type = SelectField('', choices=[('Admin', 'Admin'), ('Premium', 'Premium'), ('Standard', 'Standard'),
                                        ('Free', 'Free')])
    disk_quota = DecimalField('', validators=[InputRequired()])
    password = PasswordField('', validators=[InputRequired()])
    submit = SubmitField('Add')