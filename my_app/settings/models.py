from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, PasswordField, SubmitField, FileField, SelectMultipleField, widgets, Form, \
    SelectField, DecimalField
from wtforms import TextAreaField
from wtforms.validators import InputRequired, Length, EqualTo, Optional, Email
from my_app import db
from my_app import bcrypt
import datetime
from sqlalchemy import Sequence
import os

class NewUserForm(FlaskForm):
    usr_name = StringField('', validators=[InputRequired()])
    usr_type = SelectField('', choices=[('Admin', 'Admin'), ('Premium', 'Premium'), ('Standard', 'Standard'),
                                        ('Free', 'Free')])
    disk_quota = DecimalField('', validators=[InputRequired()])
    password = PasswordField('', validators=[InputRequired()])
    submit = SubmitField('Add')

class UpdateProfile(FlaskForm):
    picture = FileField("Profile Picture", validators=[Optional(), FileRequired()])
    description = TextAreaField("Your Biography", validators=[Optional(), Length(max=500)])
    profession = StringField("Your Profession", validators=[Optional(), Length(max=50)])
    email = StringField("Email", validators=[Optional(), Email()])
    submit = SubmitField("OK")


class CoursesEdit(FlaskForm):
    picture = FileField("Course Cover:", validators=[FileRequired()])
    name = StringField("Course Name:", validators=[InputRequired(), Length(max=100)])
    submit = SubmitField("Add")


class NewSeries(FlaskForm):
    title = StringField("Serie Title:", validators=[InputRequired(), Length(max=200)])
    description = TextAreaField("Description", validators=[InputRequired(), Length(max=100)])
    submit = SubmitField("Add")


class SeriesBooks(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200))
    description = db.Column(db.TEXT)
    dir_path = db.Column(db.String(500), unique=True)

    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.dir_path = os.path.join('my_app', 'static', 'sections', 'Books', title )

class SeriesMedia(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(500))
    description = db.Column(db.TEXT)
    dir_path = db.Column(db.String(150), unique=True)

    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.dir_path = os.path.join('my_app', 'static', 'sections', 'Media', title )