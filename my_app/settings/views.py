from flask import render_template, request, redirect, url_for, Blueprint, g
from flask_login import current_user, login_user, login_required
from my_app.auth.models import Users, MainLoginForm
from my_app import login_manager
from my_app import auth

settings = Blueprint('settings', __name__)

@auth.before_request
def get_current_user():
    g.user = current_user

@settings.route
@login_required
def main_panel():
    pass