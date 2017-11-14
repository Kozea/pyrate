from flask_script import Manager
from pyrate_api import create_app, db
from pyrate_api.users.models import User


app = create_app()
manager = Manager(app)


@manager.command
def recreate_db():
    """Recreates a database."""
    db.drop_all()
    db.create_all()
    db.session.commit()
    print('Database (re)creation done.')


if __name__ == '__main__':
    manager.run()
