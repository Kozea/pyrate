from flask_testing import TestCase

from lib.backend import app, db
from lib.backend.generator.models import Algorithm

class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('lib.backend.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.add(Algorithm(
            label='markovify',
            default_param='phrases',
            default_param_value=5
        ))
        db.session.add(Algorithm(
            label='MarkovChain',
            default_param='mots',
            default_param_value=50
        ))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
