from pyrate_api.users.models import User
from pyrate_api.corpus.models import Corpus_category
from pyrate_api import db


def add_user(username, email, password):
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user

def add_category(label):
    cat = Corpus_category(label=label)
    db.session.add(cat)
    db.session.commit()
    return cat
