from flask import Blueprint, jsonify
from .models import Corpus_text, Corpus_category


corpus_blueprint = Blueprint('corpus', __name__)


@corpus_blueprint.route('/corpus/', methods=['GET'])
def get_corpus():
    """Get all texts"""
    corpus = Corpus_text.query.all()
    corpus_list = []
    for text in corpus:
        text_object = {
            'id': text.id,
            'title': text.title,
            'filename': text.filename,
            'category_id': text.category_id,
            'creation_date': text.creation_date,
            'author': text.author_id
        }
        corpus_list.append(text_object)
    response_object = {
        'status': 'success',
        'data': {
            'text': corpus_list
        }
    }
    return jsonify(response_object), 200


@corpus_blueprint.route('/categories/', methods=['GET'])
def get_corpus_categories():
    """Get all corpus categories"""
    categories = Corpus_category.query.all()
    categories_list = []
    for category in categories:
        category_object = {
            'id': category.id,
            'label': category.label
        }
        categories_list.append(category_object)
    response_object = {
        'status': 'success',
        'data': {
            'text': categories_list
        }
    }
    return jsonify(response_object), 200
