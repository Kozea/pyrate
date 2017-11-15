from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# instantiate the db
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()


def create_app():

    # instantiate the app
    app = Flask(__name__)

    # set config
    with app.app_context():
        app.config.from_object('pyrate_api.config.DevelopmentConfig')

    # set up extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from pyrate_api.users.users import users_blueprint
    app.register_blueprint(users_blueprint)
    from pyrate_api.users.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)
    from pyrate_api.corpus.views import corpus_blueprint
    app.register_blueprint(corpus_blueprint)

    return app
