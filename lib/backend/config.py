import os

from flask import current_app


class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 13
    TOKEN_EXPIRATION_DAYS = 30
    TOKEN_EXPIRATION_SECONDS = 0
    TRAINING_FOLDER = os.path.join(
        current_app.root_path, 'trainings'
    )
    UPLOAD_FOLDER = os.path.join(
        current_app.root_path, 'uploads'
    )
    TEXT_ALLOWED_EXTENSIONS = set(['txt', 'pdf'])


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(
        current_app.root_path, 'database/pyrate.db'
    )
    SECRET_KEY = 'development key'
    USERNAME = 'admin'
    PASSWORD = 'default'
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(
        current_app.root_path, 'database/pyrate_test.db'
    )
    SECRET_KEY = 'test key'
    USERNAME = 'admin'
    PASSWORD = 'default'
    BCRYPT_LOG_ROUNDS = 4
    TOKEN_EXPIRATION_DAYS = 0
    TOKEN_EXPIRATION_SECONDS = 3
    TRAINING_FOLDER = os.path.join(
        current_app.root_path, 'tests/trainings'
    )
    UPLOAD_FOLDER = os.path.join(
        current_app.root_path, 'tests/uploads'
    )
