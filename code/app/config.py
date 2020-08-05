from datetime import timedelta
import os

from dotenv import load_dotenv


BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(BASEDIR, "db")
load_dotenv(os.path.join(BASEDIR, ".flaskenv"))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    JWT_EXPIRATION_DELTA = timedelta(days=3)
    JWT_AUTH_USERNAME_KEY = "email"
    JWT_BLACKLIST_ENABLED = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.path.join(
        os.environ.get("SQLALCHEMY_DATABASE_URI"), os.environ.get("DB_DEV2_NAME")
    ) or "sqlite:///" + os.path.join(DB_PATH, "data-dev.sqlite")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.path.join(
        os.environ.get("SQLALCHEMY_DATABASE_URI"), os.environ.get("DB_TEST_NAME")
    ) or "sqlite:///" + os.path.join(DB_PATH, "data-test.sqlite")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(DB_PATH, "data.sqlite")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
