from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, PasswordField, SubmitField, FileField, SelectMultipleField, widgets, Form, SelectField
from wtforms import TextAreaField
from wtforms.validators import InputRequired, Length, EqualTo, Optional
from my_app import db
from my_app import bcrypt
import datetime
from sqlalchemy import Sequence


class Users(db.Model):
    usr_name = db.Column(db.String(50), primary_key=True)
    passwd = db.Column(db.TEXT)
    email = db.Column(db.String(70))
    usr_type = db.Column(db.String(10))
    storage_size = db.Column(db.BigInteger)
    used_storage_size = db.Column(db.BigInteger)
    bio = db.Column(db.TEXT)
    profile_pic = db.Column(db.String(100))
    profession = db.Column(db.String(50))


    def __init__(self, usr_name, passwd, email, usr_type, storage_size, used_storage_size, bio, profile_pic, profession):
        self.usr_name = usr_name
        self.email = email
        self.passwd = bcrypt.generate_password_hash(passwd)
        self.usr_type = usr_type
        self.storage_size = storage_size
        self.used_storage_size = used_storage_size
        self.bio = bio
        self.profile_pic = profile_pic
        self.profession = profession

    def check_password(self, password):
        return bcrypt.check_password_hash(self.passwd, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return (self.usr_name)


class MainLoginForm(FlaskForm):
    usr_name = StringField('User', validators=[InputRequired()])
    passwd = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')