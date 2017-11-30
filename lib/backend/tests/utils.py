import os

from lib.backend import app, db
from lib.backend.corpus.models import Corpus_category, Corpus_text
from lib.backend.users.models import User


def add_user(username, email, password):
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user


def add_category(label, owner_id, private=False):
    cat = Corpus_category(label=label, owner_id=owner_id, private=private)
    db.session.add(cat)
    db.session.commit()
    return cat


def add_corpus_text(title, filename, category_id, author_id):
    text = Corpus_text(
        title=title,
        filename=filename,
        category_id=category_id,
        author_id=author_id
    )
    db.session.add(text)
    db.session.commit()
    return text


def add_all():
    user = add_user('test', 'test@test.com', 'test')
    cat = add_category('romans', user.id)
    filename = 'les_miserables_markov.txt'
    dirpath = os.path.join(app.root_path, 'tests/files')
    filepath = os.path.join(dirpath, filename)
    add_corpus_text('les_miserables_markov',
                    filepath,
                    cat.id,
                    user.id)
