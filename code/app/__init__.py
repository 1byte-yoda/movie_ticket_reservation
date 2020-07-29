"""Flask Application Factory."""

from datetime import timedelta
from flask import Flask
from flask_restful import Api

from .api.account.resource import AccountRegisterResource
from .api.reservation.resource import ReservationResource, ReservationListResource
from .authenticate import jwt
from .routes import RESERVATION_LIST_ROUTES, RESERVATION_ROUTES
from db import db

api = Api()


def create_app(*, config_name=""):
    """Create a Flask application."""
    app = Flask(__name__)
    app.secret_key = "change_this_later_bro"

    app.config["JWT_EXPIRATION_DELTA"] = timedelta(seconds=3600)
    app.config["JWT_AUTH_USERNAME_KEY"] = "email"
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:123456@localhost/anonymouse"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    api.add_resource(ReservationResource, *RESERVATION_ROUTES)
    api.add_resource(ReservationListResource, *RESERVATION_LIST_ROUTES)
    api.add_resource(AccountRegisterResource, "/register")

    api.init_app(app=app)
    jwt.init_app(app=app)
    db.init_app(app=app)
    return app
