import locale
import logging

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

locale.setlocale(locale.LC_ALL, 'fr_FR')

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()

# instantiate the app
app = Flask(__name__)

# set config
with app.app_context():
    app.config.from_object('lib.backend.config.DevelopmentConfig')

# set up extensions
db.init_app(app)
bcrypt.init_app(app)
migrate.init_app(app, db)

from .corpus.corpus import corpus_blueprint
from .users.auth import auth_blueprint
from .users.users import users_blueprint

app.register_blueprint(users_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(corpus_blueprint)

if app.debug:
    logging.getLogger('sqlalchemy').setLevel(logging.INFO)
    logging.getLogger('sqlalchemy'
                      ).handlers = logging.getLogger('werkzeug').handlers
    logging.getLogger('sqlalchemy.orm').setLevel(logging.WARNING)

if app.debug or app.config.get('STAGING'):
    # Enable CORS
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add(
            'Access-Control-Allow-Headers', 'Content-Type,Authorization'
        )
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH,OPTIONS'
        )
        return response
