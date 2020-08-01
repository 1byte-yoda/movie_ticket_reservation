from datetime import timedelta
import os


BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config:
    SECRET_KEY = "change_this_later_bro"
    JWT_EXPIRATION_DELTA = timedelta(seconds=3600)
    JWT_AUTH_USERNAME_KEY = "email"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@localhost/anonymouse"
    # or "sqlite:///" + os.path.join(BASEDIR, "db/data-dev.sqlite")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@localhost/testing"
    # or "sqlite:///" + os.path.join(BASEDIR, "db/data-test.sqlite")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join('data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
