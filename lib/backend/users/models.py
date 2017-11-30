import datetime

import jwt
from flask import current_app

from .. import bcrypt, db


class NoAuthenticationMethod(Exception):
    def __init__(self):
        self.parameter = 'No authentication method (password or github token).'

    def __str__(self):
        return repr(self.parameter)


class NoEmailProvided(Exception):
    def __init__(self):
        self.parameter = 'No email provided.'

    def __str__(self):
        return repr(self.parameter)


class GHUser:
    github_access_token = None

    def __init__(self, github_access_token):
        self.github_access_token = github_access_token


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    github_access_token = db.Column(db.String(200), nullable=True)
    github_id = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def __init__(
            self, username, email=None, password=None,
            created_at=datetime.datetime.utcnow(),
            github_access_token=None, github_id=None
    ):
        if not password and not github_access_token:
            raise NoAuthenticationMethod
        if not email and not github_access_token:
            raise NoEmailProvided
        self.username = username
        if email:
            self.email = email
        if password:
            self.password = bcrypt.generate_password_hash(
                password, current_app.config.get('BCRYPT_LOG_ROUNDS')
            ).decode()
        self.created_at = created_at
        self.github_access_token = github_access_token
        self.github_id = github_id

    def encode_auth_token(self, user_id):
        """Generates the auth token"""
        try:
            payload = {
                'exp':
                    datetime.datetime.utcnow() + datetime.timedelta(
                        days=current_app.config.get('TOKEN_EXPIRATION_DAYS'),
                        seconds=current_app.config.
                        get('TOKEN_EXPIRATION_SECONDS')
                    ),
                'iat':
                    datetime.datetime.utcnow(),
                'sub':
                    user_id
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token - :param auth_token: - :return: integer|string
        """
        try:
            payload = jwt.decode(
                auth_token, current_app.config.get('SECRET_KEY')
            )
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
