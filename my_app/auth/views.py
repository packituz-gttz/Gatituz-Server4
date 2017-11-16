from flask import render_template, request, redirect, url_for, Blueprint, g, session, make_response,\
    flash
from flask_login import current_user, login_user, logout_user, login_required
from my_app.auth.models import Users, MainLoginForm
from my_app import login_manager

auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(username):
    return Users.query.get(username)

@auth.before_request
def get_current_user():
    g.user = current_user

@auth.route('/')
def index():
    if g.user is not None and current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    resp = make_response(render_template('index.html', form=MainLoginForm(request.form)))
    resp.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return resp

@auth.route('/check_login', methods=['GET', 'POST'])
def check_login():
    if g.user is not None and current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    form = MainLoginForm(request.form)
    if form.validate_on_submit():
        user = Users.query.filter_by(usr_name=form.usr_name.data).first()
        if user and user.check_password(form.passwd.data):
            login_user(user)
            session['usr_type'] = user.usr_type
            return redirect(url_for('auth.dashboard'))
    return redirect(url_for('auth.index'))


@auth.route('/dashboard')
@login_required
def dashboard():
    try:
        user = Users.query.filter_by(usr_name=current_user.get_id()).first()
    except (TimeoutError) as err:
        resp = make_response(render_template('logged_main.html'))
    else:
        resp = make_response(render_template('logged_main.html', picture=user.profile_pic,
                                             bio=user.bio, profession=user.profession, username=current_user.get_id()))
    resp.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return resp

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index'))
