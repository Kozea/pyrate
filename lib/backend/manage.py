from flask_script import Manager
from flask_migrate import MigrateCommand
import unittest

from pyrate_api import create_app, db
from pyrate_api.users.models import User

app = create_app()
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def recreate_db():
    """Recreates a database."""
    db.drop_all()
    db.create_all()
    db.session.commit()
    print('Database (re)creation done.')


@manager.command
def seed_db():
    """Seeds the database."""
    db.session.add(
        User(username='test', email='test@test.com', password='test')
    )
    db.session.add(
        User(username='test2', email='test2@test.com', password='test2')
    )
    db.session.commit()


@manager.command
def test():
    """Runs the tests without code coverage."""
    tests = unittest.TestLoader().discover(
        'pyrate_api/tests', pattern='test*.py'
    )
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
