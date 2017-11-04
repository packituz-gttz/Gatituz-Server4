from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "secret_pass"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:secret@localhost/db_gatituz4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.index'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from my_app.auth.views import auth
app.register_blueprint(auth)

from my_app.settings.views import settings
app.register_blueprint(settings)

from my_app.sections.views import sections
app.register_blueprint(sections)

db.create_all()