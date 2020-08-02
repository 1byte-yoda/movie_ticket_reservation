"""Flask Application Factory."""

from flask import Flask
from flask_restful import Api

from .api.resources.account import AccountRegisterResource, AccountLoginResource
from .api.resources.seat_reservation import (
    SeatReservationResource, SeatReservationListResource
)
from .authenticate import jwt
from .routes import SEAT_RESERVATION_LIST_ROUTES, SEAT_RESERVATION_ROUTES
from db import db
from app.config import config


api = Api()


def create_app(*, config_name="default") -> Flask:
    """Create a Flask application."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    api.add_resource(SeatReservationResource, *SEAT_RESERVATION_ROUTES)
    api.add_resource(SeatReservationListResource, *SEAT_RESERVATION_LIST_ROUTES)
    api.add_resource(AccountRegisterResource, "/register")
    api.add_resource(AccountLoginResource, "/login")

    config[config_name].init_app(app=app)
    api.init_app(app=app)
    jwt.init_app(app=app)
    db.init_app(app=app)
    return app
