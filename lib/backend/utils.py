from functools import wraps

from flask import jsonify, request

from . import app
from .users.models import User


def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response_object = {
            'status': 'error',
            'message': 'Something went wrong. Please contact us.'
        }
        code = 401
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            response_object['message'] = 'Provide a valid auth token.'
            code = 403
            return jsonify(response_object), code
        auth_token = auth_header.split(" ")[1]
        resp = User.decode_auth_token(auth_token)
        if isinstance(resp, str):
            response_object['message'] = resp
            return jsonify(response_object), code
        user = User.query.filter_by(id=resp).first()
        if not user:
            return jsonify(response_object), code
        return f(resp, *args, **kwargs)
    return decorated_function


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in \
           app.config.get('TEXT_ALLOWED_EXTENSIONS')
