from flask import Blueprint, g, jsonify, request
from sqlalchemy import exc, or_

from .. import app, bcrypt, db, github
from ..utils import authenticate
from .models import GHUser, NoAuthenticationMethod, NoEmailProvided, User

auth_blueprint = Blueprint('auth', __name__)


@github.access_token_getter
def token_getter():
    user = g.user
    if user is not None:
        return user.github_access_token


@auth_blueprint.route('/auth/register', methods=['POST'])
def register_user():
    # get post data
    post_data = request.get_json()
    if not post_data:
        response_object = {'status': 'error', 'message': 'Invalid payload.'}
        return jsonify(response_object), 400
    username = post_data.get('username')
    email = post_data.get('email')
    password = post_data.get('password')
    try:
        # check for existing user
        user = User.query.filter(
            or_(User.username == username, User.email == email)
        ).first()
        if not user:
            # add new user to db
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            # generate auth token
            auth_token = new_user.encode_auth_token(new_user.id)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.',
                'auth_token': auth_token.decode()
            }
            return jsonify(response_object), 201
        else:
            response_object = {
                'status': 'error',
                'message': 'Sorry. That user already exists.'
            }
            return jsonify(response_object), 400
    # handler errors
    except (exc.IntegrityError, NoAuthenticationMethod, ValueError,
            NoEmailProvided) as e:
        db.session.rollback()
        response_object = {'status': 'error', 'message': 'Invalid payload.'}
        return jsonify(response_object), 400


@auth_blueprint.route('/auth/login', methods=['POST'])
def login_user():
    # get post data
    post_data = request.get_json()
    if not post_data:
        response_object = {'status': 'error', 'message': 'Invalid payload.'}
        return jsonify(response_object), 400
    email = post_data.get('email')
    password = post_data.get('password')
    try:
        # check for existing user
        user = User.query.filter(User.email == email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            # generate auth token
            auth_token = user.encode_auth_token(user.id)
            response_object = {
                'status': 'success',
                'message': 'Successfully logged in.',
                'auth_token': auth_token.decode()
            }
            return jsonify(response_object), 200
        else:
            response_object = {
                'status': 'error',
                'message': 'Invalid credentials.'
            }
            return jsonify(response_object), 404
    # handler errors
    except (exc.IntegrityError, ValueError) as e:
        db.session.rollback()
        response_object = {'status': 'error', 'message': 'Try again'}
        return jsonify(response_object), 500


@auth_blueprint.route('/auth/gh-login', methods=('GET', 'POST'))
def login_github_user():

    if (app.config['GITHUB_CLIENT_ID'] == '' or
       app.config['GITHUB_CLIENT_ID'] == None or
       app.config['GITHUB_CLIENT_SECRET'] == '' or
       app.config['GITHUB_CLIENT_SECRET'] == None):
        response_object = {
            'status': 'error',
            'message': 'Github configuration missing'
        }
        return jsonify(response_object), 500

    response = github.authorize(scope="user")
    if response.status_code == 302:
        response_object = {
            'status': 'success',
            'message': 'redirection to github',
            'url': response.headers.get('location')
        }
        return jsonify(response_object), 200
    else:
        response_object = {'status': 'error', 'message': 'Try again'}
        return jsonify(response_object), 500


@auth_blueprint.route('/auth/callback')
@github.authorized_handler
def authorized(oauth_token):
    if oauth_token is None:
        response_object = {
            'status': 'fail',
            'message': 'Authorization failed.'
        }
        return jsonify(response_object), 400

    user = User.query.filter_by(github_access_token=oauth_token).first()
    if user is None:
        ghuser = GHUser(oauth_token)
        g.user = ghuser
        user_profile = github.get('user')

        user = User.query.filter_by(github_id=user_profile['id']).first()
        if user is None:
            user = User(
                username=user_profile['login'],
                email=None,
                password=None,
                github_access_token=oauth_token,
                github_id=user_profile['id'])
            db.session.add(user)
            db.session.commit()

    # generate pyrate auth token
    auth_token = user.encode_auth_token(user.id)
    response_object = {
        'status': 'success',
        'message': 'Successfully logged in.',
        'auth_token': auth_token.decode()
    }
    return jsonify(response_object), 200


@auth_blueprint.route('/auth/logout', methods=['GET'])
@authenticate
def logout_user(resp):
    # get auth token
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            response_object = {
                'status': 'success',
                'message': 'Successfully logged out.'
            }
            return jsonify(response_object), 200
        else:
            response_object = {'status': 'error', 'message': resp}
            return jsonify(response_object), 401
    else:
        response_object = {
            'status': 'error',
            'message': 'Provide a valid auth token.'
        }
        return jsonify(response_object), 403
