from .. import db
from ..corpus.models import Corpus_category, Corpus_text
from ..users.models import User


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


def add_corpus_text(title, filename, category_id, author_id):
    text = Corpus_text(title=title,
                       filename=filename,
                       category_id=category_id,
                       author_id=author_id)
    db.session.add(text)
    db.session.commit()
    return text
