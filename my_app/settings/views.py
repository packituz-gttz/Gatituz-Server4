from flask import render_template, request, redirect, url_for, Blueprint, g, session, make_response, \
    flash
from flask_login import current_user, login_user, login_required
from my_app.auth.models import Users
from my_app import login_manager
from my_app import auth
from my_app.settings.models import NewUserForm, UpdateProfile
import os

settings = Blueprint('settings', __name__)

@auth.before_request
def get_current_user():
    g.user = current_user

@settings.route('/main_panel')
@login_required
def main_panel():
    if 'usr_type' in session:
        if session['usr_type'] == 'Admin':
            return redirect(url_for('settings.admin_panel'))

@settings.route('/admin_panel')
@settings.route('/admin_panel/admin_tab')
@login_required
def admin_panel(admin_tab='users'):
    if session['usr_type'] == 'Admin':
        users = Users.query.all()
        form = NewUserForm()
        resp = make_response(render_template('admin_settings.html',
                                             titles=['Name', 'Type', 'Disk Quota(GB)', 'Delete', 'Password'],
                                             rows=users, new=form))
        resp.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
        return resp
    else:
        return redirect('settings.main_panel')

# TODO add user to db
@settings.route('/new_user', methods=['GET', 'POST'])
@login_required
def new_user():
    if session['usr_type'] == 'Admin':
        form = NewUserForm(request.form)
        flash('Successfully added', 'success')
        return redirect(url_for('settings.admin_panel'))
    return redirect('settings.main_panel')

@settings.route('/change_profile')
@login_required
def change_profile():
    form = UpdateProfile()
    try:
        print (current_user.get_id())
        user = Users.query.filter_by(usr_name=current_user.get_id()).first()
        print (user.usr_name)
    except TimeoutError:
        pass
    return render_template('user_profile.html', new=form)