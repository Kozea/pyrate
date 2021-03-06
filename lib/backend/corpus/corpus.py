import json
import os
import shutil

from flask import Blueprint, jsonify, request
from sqlalchemy import exc
from werkzeug.utils import secure_filename

from .. import app, appLog, db
from ..generator.models import Training
from ..users.models import User
from ..utils import allowed_file, authenticate, is_admin
from .models import Corpus_category, Corpus_text

corpus_blueprint = Blueprint('corpus', __name__)


def update_trainings(category_id):
    # TODO: CHECK SQL ALCHEMY
    """ Empty last training date when the corpus is modified """
    trainings = Training.query.filter_by(category_id=category_id)
    for training in trainings:
        training.last_train_date = None
    # db.session.commit() is the calling function


@corpus_blueprint.route('/categories', methods=['GET'])
def get_corpus_categories():
    """Get all corpus categories"""
    try:
        categories = Corpus_category.query.all()
        categories_list = []
        for category in categories:
            user = User.query.filter_by(id=category.owner_id).first()
            category_object = {
                'id': category.id,
                'label': category.label,
                'is_private': category.private,
                'owner_id': category.owner_id,
                'owner_username': user.username
            }
            categories_list.append(category_object)
        response_object = {
            'status': 'success',
            'data': {
                'categories': categories_list
            }
        }
        return jsonify(response_object), 200
    except exc.OperationalError as e:
        appLog.error(e)
        response_object = {
            'status': 'error',
            'message': 'Internal system error'
        }
        return jsonify(response_object), 500


@corpus_blueprint.route('/categories/<cat_id>', methods=['GET'])
def get_corpus_category(cat_id):
    """Get one corpus category"""
    response_object = {'status': 'fail', 'message': 'Category does not exist'}
    try:
        category = Corpus_category.query.filter_by(id=cat_id).first()
        if not category:
            return jsonify(response_object), 404
        else:
            user = User.query.filter_by(id=category.owner_id).first()
            response_object = {
                'status': 'success',
                'data': {
                    'label': category.label,
                    'is_private': category.private,
                    'owner_id': category.owner_id,
                    'owner_username': user.username
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
            db.session.add(
                Corpus_category(
                    label=label, private=private, owner_id=user_id
                )
            )
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
        return jsonify(response_object), 404

    if not is_admin(user_id) and cat.owner_id != user_id:
        response_object = {
            'status': 'error',
            'message': 'You do not have permission to delete this category.'
        }
        return jsonify(response_object), 401

    try:
        Training.query.filter_by(category_id=cat_id).delete()
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
        return jsonify(response_object), 404

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
        user = User.query.filter_by(id=text.author_id).first()
        text_object = {
            'id': text.id,
            'title': text.title,
            'category_id': text.category_id,
            'creation_date': text.creation_date,
            'owner_id': text.author_id,
            'owner_username': user.username
        }
        corpus_list.append(text_object)
    response_object = {'status': 'success', 'data': {'texts': corpus_list}}
    return jsonify(response_object), 200


@corpus_blueprint.route('/corpus/cat/<cat_id>', methods=['GET'])
def get_cat_corpus(cat_id):
    """Get all texts for a selected category"""
    response_object = {'status': 'fail', 'message': 'Category does not exist.'}
    try:
        category = Corpus_category.query.filter_by(id=cat_id).first()
        if not category:
            return jsonify(response_object), 404
        else:
            corpus = Corpus_text.query.filter_by(category_id=cat_id).all()
            corpus_list = []
            for text in corpus:
                user = User.query.filter_by(id=text.author_id).first()
                text_object = {
                    'id': text.id,
                    'title': text.title,
                    'creation_date': text.creation_date,
                    'owner_id': text.author_id,
                    'owner_username': user.username
                }
                corpus_list.append(text_object)
            response_object = {
                'status': 'success',
                'data': {'texts': corpus_list}
            }
            return jsonify(response_object), 200
    except ValueError as e:
        appLog.error(e)
        return jsonify(response_object), 404


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

    cat = Corpus_category.query.filter_by(id=category_id).first()
    if not is_admin(user_id) and cat.owner_id != user_id:
        response_object = {
            'status': 'error',
            'message': 'You do not have permission to add'
            ' a text in this category.'
        }
        return jsonify(response_object), 401

    if 'file' not in request.files:
        response_object = {'status': 'fail', 'message': 'No file part.'}
        return jsonify(response_object), code
    file = request.files['file']
    if file.filename == '':
        response_object = {'status': 'fail', 'message': 'No selected file.'}
        return jsonify(response_object), code
    if not allowed_file(file.filename):
        response_object = {
            'status': 'fail',
            'message': 'File extension not allowed.'
        }
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
            update_trainings(category_id)
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
        return jsonify(response_object), 404

    cat = Corpus_category.query.filter_by(id=text.category_id).first()
    if not is_admin(user_id) and cat.owner_id != user_id:
        response_object = {
            'status': 'error',
            'message': 'You do not have permission to delete this text.'
        }
        return jsonify(response_object), 401

    filepath = text.filename

    try:
        update_trainings(text.category_id)
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
