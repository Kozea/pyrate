import json
import os
import shutil

from flask import Blueprint, jsonify, request
from sqlalchemy import exc
from werkzeug.utils import secure_filename

from .. import app, appLog, db
from ..utils import allowed_file, authenticate, is_admin
from .models import Corpus_category, Corpus_text

corpus_blueprint = Blueprint('corpus', __name__)


@corpus_blueprint.route('/categories', methods=['GET'])
def get_corpus_categories():
    """Get all corpus categories"""
    categories = Corpus_category.query.all()
    categories_list = []
    for category in categories:
        category_object = {'id': category.id, 'label': category.label}
        categories_list.append(category_object)
    response_object = {'status': 'success',
                       'data': {'categories': categories_list}}
    return jsonify(response_object), 200


@corpus_blueprint.route('/categories/<cat_id>', methods=['GET'])
def get_corpus_category(cat_id):
    """Get one corpus category"""
    response_object = {'status': 'fail', 'message': 'Category does not exist'}
    try:
        category = Corpus_category.query.filter_by(id=cat_id).first()
        if not category:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'label': category.label
                }
            }
            return jsonify(response_object), 200
    except ValueError as e:
        appLog.error(e)
        return jsonify(response_object), 404


@corpus_blueprint.route('/categories', methods=['POST'])
@authenticate
def add_corpus_category(user_id):
    """Add a new corpus category"""
    post_data = request.get_json()
    if not post_data:
        response_object = {'status': 'fail', 'message': 'Invalid payload.'}
        return jsonify(response_object), 400
    label = post_data.get('label')
    private = post_data.get('private')
    try:
        category = Corpus_category.query.filter_by(label=label).first()
        if not category:
            db.session.add(Corpus_category(label=label,
                                           private=private,
                                           owner_id=user_id))
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': f'"{label}" was added!'
            }
            return jsonify(response_object), 201
        else:
            response_object = {
                'status': 'fail',
                'message': f'Sorry. The category "{label}" already exists.'
            }
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        appLog.error(e)
        response_object = {'status': 'fail', 'message': 'Invalid payload.'}
        return jsonify(response_object), 400


@corpus_blueprint.route('/categories/<cat_id>', methods=['DELETE'])
@authenticate
def delete_corpus_category(user_id, cat_id):
    """Delete one corpus category"""
    cat = Corpus_category.query.filter_by(id=cat_id).first()
    if not cat:
        response_object = {
            'status': 'error',
            'message': f'Category {cat_id} does not exist.'
        }
        return jsonify(response_object), 400

    if not is_admin(user_id) and cat.owner_id != user_id:
        response_object = {
            'status': 'error',
            'message': 'You do not have permission to delete this category.'
        }
        return jsonify(response_object), 401

    try:
        Corpus_text.query.filter_by(category_id=cat_id).delete()
        Corpus_category.query.filter_by(id=cat_id).delete()
        db.session.commit()

        dirpath = os.path.join(app.config['UPLOAD_FOLDER'], str(cat_id))
        shutil.rmtree(dirpath, ignore_errors=True)

        response_object = {
            'status': 'success',
            'message': f'Category {cat_id} deleted.'
        }
        return jsonify(response_object), 200
    except (exc.IntegrityError, ValueError, TypeError, OSError) as e:
        db.session.rollback()
        appLog.error(e)
        response_object = {'status': 'fail', 'message': 'Invalid payload.'}
        return jsonify(response_object), 400


@corpus_blueprint.route('/categories/<cat_id>', methods=['PUT'])
@authenticate
def update_corpus_category(user_id, cat_id):
    """Update a corpus category"""
    post_data = request.get_json()
    if not post_data:
        response_object = {'status': 'fail', 'message': 'Invalid payload.'}
        return jsonify(response_object), 400
    label = post_data.get('label')

    cat = Corpus_category.query.filter_by(id=cat_id).first()
    if not cat:
        response_object = {
            'status': 'error',
            'message': f'Category {cat_id} does not exist.'
        }
        return jsonify(response_object), 400

    if not is_admin(user_id) and cat.owner_id != user_id:
        response_object = {
            'status': 'error',
            'message': 'You do not have permission to update this category.'
        }
        return jsonify(response_object), 401

    try:
        cat.label = label
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Category was updated!'
        }
        return jsonify(response_object), 200
    except (exc.IntegrityError, ValueError, TypeError) as e:
        db.session().rollback()
        appLog.error(e)
        response_object = {'status': 'fail', 'message': 'Invalid payload.'}
        return jsonify(response_object), 400


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
    response_object = {'status': 'success', 'data': {'text': corpus_list}}
    return jsonify(response_object), 200


@corpus_blueprint.route('/corpus', methods=['POST'])
@authenticate
def add_corpus_text(user_id):
    """Add a text in corpus"""

    code = 400
    if not request.form:
        response_object = {'status': 'fail', 'message': 'Invalid payload.'}
        return jsonify(response_object), code

    post_data = json.loads(request.form["data"])
    if not post_data or 'title' not in post_data \
            or 'category_id' not in post_data:
        response_object = {'status': 'fail', 'message': 'Invalid payload.'}
        return jsonify(response_object), code

    title = post_data['title']
    category_id = post_data['category_id']

    if 'file' not in request.files:
        response_object = {'status': 'fail', 'message': 'No file part.'}
        return jsonify(response_object), code
    file = request.files['file']
    if file.filename == '':
        response_object = {'status': 'fail', 'message': 'No selected file.'}
        return jsonify(response_object), code
    if not allowed_file(file.filename):
        response_object = {'status': 'fail',
                           'message': 'File extension not allowed.'}
        return jsonify(response_object), code

    filename = secure_filename(file.filename)
    dirpath = os.path.join(app.config['UPLOAD_FOLDER'], str(category_id))
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    filepath = os.path.join(dirpath, filename)

    try:
        file.save(filepath)
        text = Corpus_text.query.filter_by(title=title).first()
        if not text:
            db.session.add(
                Corpus_text(
                    title=title,
                    filename=filepath,
                    category_id=category_id,
                    author_id=user_id
                )
            )
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': f'Text "{title}" was added!'
            }
            return jsonify(response_object), 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry. A text with the same title already exists.'
            }
            return jsonify(response_object), code
    except exc.IntegrityError as e:
        db.session.rollback()
        appLog.error(e)
        response_object = {'status': 'fail', 'message': 'Invalid payload.'}
        return jsonify(response_object), code


@corpus_blueprint.route('/corpus/<text_id>', methods=['DELETE'])
@authenticate
def delete_corpus_text(user_id, text_id):
    """Delete a text from a corpus"""
    text = Corpus_text.query.filter_by(id=text_id).first()

    if not text:
        response_object = {
            'status': 'error',
            'message': f'Text {text_id} does not exist.'
        }
        return jsonify(response_object), 400

    cat = Corpus_category.query.filter_by(id=text.category_id).first()
    if not is_admin(user_id) and cat.owner_id != user_id:
        response_object = {
            'status': 'error',
            'message': 'You do not have permission to delete this text.'
        }
        return jsonify(response_object), 401

    filepath = text.filename

    try:
        Corpus_text.query.filter_by(id=text_id).delete()
        db.session.commit()

        os.remove(filepath)

        response_object = {
            'status': 'success',
            'message': f'Corpus text {text_id} deleted.'
        }
        return jsonify(response_object), 200
    except (exc.IntegrityError, ValueError, TypeError, OSError) as e:
        db.session().rollback()
        appLog.error(e)
        response_object = {'status': 'fail', 'message': 'Invalid payload.'}
        return jsonify(response_object), 400
