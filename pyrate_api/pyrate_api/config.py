import os
from flask import current_app


class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 13


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(current_app.root_path, 'db/pyrate.db')
    SECRET_KEY = 'development key'
    USERNAME = 'admin'
    PASSWORD = 'default'
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(current_app.root_path, 'db/pyrate_test.db')
    SECRET_KEY = 'test key'
    USERNAME = 'admin'
    PASSWORD = 'default'
    BCRYPT_LOG_ROUNDS = 4
