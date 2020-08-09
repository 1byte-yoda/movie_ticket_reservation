"""Flask Application Factory."""

from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate

from .api.resources.seat_reservation import (
    SeatReservationResource,
    SeatReservationListResource,
)
from .api.resources.account import (
    AccountResource,
    AccountLoginResource,
    AccountLogoutResource,
    TokenRefresh
)
from .api.resources.user import UserRegisterResource, UserResource
from .api.resources.cinema import CinemaResource, CinemaUserResourse
from .api.resources.screen import ScreenListResource, ScreenResource
from .api.resources.movie_screen import MovieScreenResource, MovieScreenListResource
from .api.resources.movie import MovieResource
from .authenticate import jwt
from .routes import (
    SEAT_RESERVATION_LIST_ROUTES,
    SEAT_RESERVATION_ROUTES,
    USER_REGISTER_ROUTES,
    USER_ROUTES,
    ACCOUNT_ROUTES,
    ACCOUNT_LOGIN_ROUTES,
    ACCOUNT_LOGOUT_ROUTES,
    ACCOUNT_FRESH_TOKEN_ROUTES,
    CINEMA_ROUTES,
    CINEMA_USER_ROUTES,
    SCREEN_LIST_ROUTES,
    SCREEN_ROUTES,
    MOVIE_SCREEN_ROUTES,
    MOVIE_SCREEN_LIST_ROUTES,
    MOVIE_ROUTES
)
from db import db
from app.config import config


api = Api()
migrate = Migrate()


def create_app(*, config_name="default") -> Flask:
    """Create a Flask application."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    api.add_resource(SeatReservationResource, *SEAT_RESERVATION_ROUTES)
    api.add_resource(SeatReservationListResource, *SEAT_RESERVATION_LIST_ROUTES)
    api.add_resource(UserRegisterResource, *USER_REGISTER_ROUTES)
    api.add_resource(UserResource, *USER_ROUTES)
    api.add_resource(AccountLoginResource, *ACCOUNT_LOGIN_ROUTES)
    api.add_resource(AccountLogoutResource, *ACCOUNT_LOGOUT_ROUTES)
    api.add_resource(AccountResource, *ACCOUNT_ROUTES)
    api.add_resource(TokenRefresh, *ACCOUNT_FRESH_TOKEN_ROUTES)
    api.add_resource(CinemaResource, *CINEMA_ROUTES)
    api.add_resource(CinemaUserResourse, *CINEMA_USER_ROUTES)
    api.add_resource(ScreenListResource, *SCREEN_LIST_ROUTES)
    api.add_resource(ScreenResource, *SCREEN_ROUTES)
    api.add_resource(MovieScreenResource, *MOVIE_SCREEN_ROUTES)
    api.add_resource(MovieScreenListResource, *MOVIE_SCREEN_LIST_ROUTES)
    api.add_resource(MovieResource, *MOVIE_ROUTES)

    config[config_name].init_app(app=app)
    api.init_app(app=app)
    jwt.init_app(app=app)
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    return app
