from flask import Blueprint, jsonify, request

from .models import Corpus_text, Corpus_category
from pyrate_api import db

corpus_blueprint = Blueprint('corpus', __name__)


@corpus_blueprint.route('/categories', methods=['GET'])
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


@corpus_blueprint.route('/categories', methods=['POST'])
def add_category():
    """Add a new corpus category"""
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    label = post_data.get('label')
    try:
        category = Corpus_category.query.filter_by(label=label).first()
        if not category:
            db.session.add(Corpus_category(label=label))
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': f'"{label}" was added!'
            }
            return jsonify(response_object), 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry. That category already exists.'
            }
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400


@corpus_blueprint.route('/categories/<cat_id>', methods=['GET'])
def get_corpus_category(cat_id):
    """Get one corpus categories"""
    category = Corpus_category.query.filter_by(id=cat_id).first()
    response_object = {
        'status': 'success',
        'data': {
            'label': category.label
        }
    }
    return jsonify(response_object), 200


@corpus_blueprint.route('/categories/<cat_id>', methods=['DELETE'])
def delete_corpus_category(cat_id):
    """Delete one corpus category"""
    cat = Corpus_category.query.filter_by(id=cat_id).first()
    if not cat:
        response_object = {
            'status': 'error',
            'message': f'Category {cat_id} does not exist.'
        }
        return jsonify(response_object), 400

    Corpus_category.query.filter_by(id=cat_id).delete()
    response_object = {
        'status': 'success',
        'message': f'Category {cat_id} deleted.'
    }
    return jsonify(response_object), 200



@corpus_blueprint.route('/corpus', methods=['GET'])
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


@corpus_blueprint.route('/corpus', methods=['POST'])
def add_corpus():
    """Add a text in corpus"""
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    code = 401
    auth_header = request.headers.get('Authorization')
    if not auth_header:
            response_object['message'] = 'Provide a valid auth token.'
            code = 403
            return jsonify(response_object), code
    auth_token = auth_header.split(" ")[1]
    user_id = User.decode_auth_token(auth_token)
    if isinstance(user_id, str):
        response_object['message'] = user_id
        return jsonify(response_object), code

    title = post_data.get('title')
    filename = post_data.get('filename')
    category_id = post_data.get('category_id')

    try:
        text = Corpus_text.query.filter_by(title=title).first()
        if not text:
            db.session.add(Corpus_category(title=title,
                                           filename=filename,
                                           category_id=category_id))
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': f'"{label}" was added!'
            }
            return jsonify(response_object), 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry. That category already exists.'
            }
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
