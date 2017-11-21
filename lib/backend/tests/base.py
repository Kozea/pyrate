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
            label='markovify'
        ))
        db.session.add(Algorithm(
            label='MarkovChain'
        ))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
