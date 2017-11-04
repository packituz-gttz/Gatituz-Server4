from flask import render_template, request, redirect, url_for, Blueprint, g, session, make_response
from flask_login import current_user, login_user, login_required
from my_app.auth.models import Users, MainLoginForm
from my_app import login_manager
from my_app import auth
import os

sections = Blueprint('sections', __name__)


@auth.before_request
def get_current_user():
    g.user = current_user


@sections.route('/show_categories')
@login_required
def show_categories():
    if 'usr_type' in session:
        if session['usr_type'] == 'Guest':
            sections_options = {
                'Games': 'Download lots of Wii games to an usb and enjoy!!!'
            }
        elif session['usr_type'] == 'Standard':
            sections_options = {
                'Courses': 'Learn about a variety of computer related topics',
                'Games': 'Download lots of Wii games to an usb and enjoy!!!',
                'Library': 'Read our collection of books'
            }
        else:
            sections_options = {
                'Cloud': 'Upload your files, up to 30Mb. You have 5GB free',
                'Courses': 'Learn about a variety of computer related topics',
                'Games': 'Download lots of Wii games to an usb and enjoy!!!',
                'Library': 'Read our collection of books, comics, mangas and novels'
            }
        print (sorted(sections_options.items()))
        resp = make_response(render_template('sections.html', sections=sorted(sections_options.items())))
        resp.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
        return resp
    return redirect(url_for('auth.dashboard'))

@sections.route('/show_Cloud')
@login_required
def show_Cloud():
    return 'cloud'

@sections.route('/show_Games')
@login_required
def show_Games():
    resp = make_response(render_template('games.html', section_image=os.path.join('sections', 'Games-Wii.jpg')))
    resp.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return resp

@sections.route('/show_Courses')
@login_required
def show_Courses():
    resp = make_response(render_template('courses.html', section_image=os.path.join('sections', 'Courses-Cover.jpg')))
    resp.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return resp

@sections.route('/show_Library')
@login_required
def show_Library():
    resp = make_response(render_template('library.html'))
    resp.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return resp