import os
from app.utils.helper import get_env


class Config(object):
    """Base Configuration Class"""
    DEBUG = False
    SECRET = get_env("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = get_env('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class DevConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS= True


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = get_env('DATABASE_TEST_URL')
    DEBUG = True


class StagingConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    DEBUG = False
    TESTING = False

