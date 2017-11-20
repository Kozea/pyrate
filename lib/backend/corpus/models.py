import datetime

from .. import db


class Corpus_category(db.Model):
    __tablename__ = "corpus_categories"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(80), unique=True, nullable=False)
    private = db.Column(db.Boolean, default=False, nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship(
        'User', backref=db.backref('corpus_categories', lazy=True)
    )

    def __repr__(self):
        return '<Corpus_category %r>' % self.label

    def __init__(self, label, owner_id, private=False):
        self.label = label
        self.owner_id = owner_id
        self.private = private


class Corpus_text(db.Model):
    __tablename__ = "corpus_texts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    filename = db.Column(db.String(80), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)

    category_id = db.Column(
        db.Integer, db.ForeignKey('corpus_categories.id'), nullable=False
    )
    corpus_category = db.relationship(
        'Corpus_category', backref=db.backref('corpus_texts', lazy=True)
    )

    author_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False
    )
    user = db.relationship(
        'User', backref=db.backref('corpus_texts', lazy=True)
    )

    def __repr__(self):
        return '<Corpus_text %r>' % self.title

    def __init__(
            self,
            title,
            filename,
            category_id,
            author_id,
            creation_date=datetime.datetime.utcnow()
    ):
        self.title = title
        self.filename = filename
        self.category_id = category_id
        self.author_id = author_id
        self.creation_date = creation_date
