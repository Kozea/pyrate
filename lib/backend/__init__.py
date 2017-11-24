import locale
import logging
import os
import unittest

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

locale.setlocale(locale.LC_ALL, 'fr_FR')

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
appLog = logging.getLogger('pyrate')

# instantiate the app
app = Flask(__name__)

# set config
with app.app_context():
    app.config.from_object('lib.backend.config.DevelopmentConfig')

# set up extensions
db.init_app(app)
bcrypt.init_app(app)
migrate.init_app(app, db)

from .corpus.corpus import corpus_blueprint  # noqa: E402
from .corpus.models import Corpus_category, Corpus_text  #noqa E402
from .users.auth import auth_blueprint  # noqa: E402
from .users.users import users_blueprint  # noqa: E402
from .users.models import User #noqa: E402
from .generator.generator import generator_blueprint  # noqa: E402
from .generator.models import Algorithm  # noqa: E402

app.register_blueprint(users_blueprint, url_prefix='/api')
app.register_blueprint(auth_blueprint, url_prefix='/api')
app.register_blueprint(corpus_blueprint, url_prefix='/api')
app.register_blueprint(generator_blueprint, url_prefix='/api')

if app.debug:
    logging.getLogger('sqlalchemy').setLevel(logging.INFO)
    logging.getLogger('sqlalchemy'
                      ).handlers = logging.getLogger('werkzeug').handlers
    logging.getLogger('sqlalchemy.orm').setLevel(logging.WARNING)
    appLog.setLevel(logging.DEBUG)

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


@app.cli.command()
def recreate_db():
    """Recreates a database."""
    db.drop_all()
    db.create_all()
    db.session.commit()
    print('Database (re)creation done.')


@app.cli.command()
def seed_db():
    """Seeds the database."""
    db.session.add(Algorithm(
        label='markovify'
        ))
    db.session.add(Algorithm(
        label='MarkovChain'
        ))
    db.session.add(User(
        username='admin',
        email='admin@example.com',
        password='admin'
    ))
    db.session.add(Corpus_category(
        label='Romans',
        owner_id=1
    ))
    db.session.add(Corpus_text(
        title="Les Misérables Tome 1",
        filename=os.path.join(
            app.config['UPLOAD_FOLDER'],
            "1/miserables_t1.txt"),
        category_id=1,
        author_id=1
    ))
    db.session.commit()


@app.cli.command()
def test():
    """Runs the tests without code coverage."""
    tests = unittest.TestLoader().discover('lib/backend/tests',
                                           pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1
