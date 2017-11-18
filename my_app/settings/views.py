from flask import render_template, request, redirect, url_for, Blueprint, g, session, make_response, \
    flash
from flask_login import current_user, login_user, login_required
from my_app.auth.models import Users
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError
from my_app import login_manager
from my_app import auth, db
from my_app.settings.models import NewUserForm, UpdateProfile, CoursesEdit, NewSeries, SeriesBooks, SeriesMedia
import os

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

settings = Blueprint('settings', __name__)

# TODO limit upload size
# TODO add option for deleting users and modifying them
# TODO implement Courses settings

@auth.before_request
def get_current_user():
    g.user = current_user

@settings.route('/main_panel')
@login_required
def main_panel():
    if session['usr_type'] == 'Admin':
        return redirect(url_for('settings.admin_panel'))
    else:
        return redirect(url_for('settings.change_profile'))


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

@settings.route('/new_user', methods=['GET', 'POST'])
@login_required
def new_user():
    if session['usr_type'] == 'Admin':
        form = NewUserForm(request.form)
        if form.validate_on_submit():
            try:
                new_user = Users(usr_name=form.usr_name.data, passwd=form.password.data, email='myemail@example.com',
                                 usr_type=form.usr_type.data, storage_size=form.disk_quota.data*1024*1024*1024, used_storage_size='0',
                                 bio='My bio', profile_pic='static/sections/user_icon.jpg', profession='My profession')
                db.session.add(new_user)
                db.session.commit()
                print (os.getcwd())
                os.mkdir(os.path.join('my_app','static', 'Users', form.usr_name.data))
                flash('Successfully added', 'success')
                return redirect(url_for('settings.admin_panel'))
            except TimeoutError:
                flash('Error please try later', 'error')
            except IntegrityError:
                flash('User already exists', 'error')
            except (IOError, OSError):
                db.session.delete(new_user)
                db.session.commit()
                flash('Error please try later', 'error')

    return redirect(url_for('settings.main_panel'))

@settings.route('/change_profile')
@login_required
def change_profile():
    form = UpdateProfile()
    try:
        print (current_user.get_id())
        user = Users.query.filter_by(usr_name=current_user.get_id()).first()
        print (user.usr_name)
        form.description.data = user.bio
        form.profession.data = user.profession
        form.email.data = user.email
    except TimeoutError:
        flash('Error couldn\'t load data')
    if session['usr_type'] == 'Admin':
        print ("admin")
        return render_template('user_profile.html', new=form, admin=True)
    else:
        print ("noadmin")
        return render_template('user_profile.html', new=form, admin=False)

@settings.route('/validate_change_profile', methods=['GET', 'POST'])
@login_required
def validate_change_profile():
    band = False
    form = UpdateProfile(request.form)
    if form.validate_on_submit():
        pic_file = request.files['picture']
        try:
            user = Users.query.filter_by(usr_name=current_user.get_id()).first()
            if pic_file.filename:
                pic_filename = secure_filename(pic_file.filename)
                if pic_filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS:
                    pic_file.save(os.path.join('my_app', 'static', 'Users_Pics',
                                               current_user.get_id() + "." + pic_filename.rsplit(".", 1)[1]))
                    user.profile_pic = os.path.join('static', 'Users_Pics',
                                                    current_user.get_id() + "." + pic_filename.rsplit(".", 1)[1])
                    band = True
            if form.profession.data:
                band = True
                user.profession = form.profession.data
            if form.description.data:
                band = True
                user.bio = form.description.data
            if form.email.data:
                band = True
                user.email = form.email.data
            if band:
                db.session.commit()
                flash('Succesfully Changed', 'success')
            print (form.profession.data)
            print (form.description.data)
        except (TimeoutError) as err:
            flash('Error, please try later', 'error')
    return redirect(url_for('settings.change_profile'))

@settings.route('/courses')
@login_required
def courses():
    if session['usr_type'] == 'Admin':
        form = CoursesEdit()
        return render_template('admin_courses.html', new=form)
    else:
        return redirect(url_for('settings.main_panel'))

@settings.route('/books')
@login_required
def books():
    if session['usr_type'] == 'Admin':
        form = NewSeries()
        return render_template('admin_books.html', new=form)
    return redirect(url_for('auth.index'))

@settings.route('/media')
@login_required
def media():
    if session['usr_type'] == 'Admin':
        form = NewSeries()
        return render_template('admin_media.html', new=form)
    return redirect(url_for('auth.index'))

@settings.route('/validate_new_series/<series_type>', methods=['GET', 'POST'])
@login_required
def validate_new_series(series_type):
    if session['usr_type'] == 'Admin':
        form = NewSeries(request.form)
        try:
            if series_type == 'Books':
                new_series = SeriesBooks(form.title.data, form.description.data)
                db.session.add(new_series)
                db.session.commit()
                print (new_series.dir_path)
                os.mkdir(new_series.dir_path)
            elif series_type == 'Media':
                new_series = SeriesMedia(form.title.data, form.description.data)
                db.session.add(new_series)
                db.session.commit()
                print(new_series.dir_path)
                os.mkdir(new_series.dir_path)
            else:
                return url_for('settings.books')
            flash('Successfully added', 'success')
        except IntegrityError:
            flash('Series already exists', 'error')
        except TimeoutError:
            flash('Error please try later', 'success')
        except (IOError, OSError):
            db.session.delete(new_series)
            db.session.commit()
            flash('Error, couldn\'t add series', 'error')
        return redirect(url_for('settings.' + series_type.lower()))