from datetime import datetime

from sqlalchemy.dialects.mysql import TINYINT

from db import db
from .user import UserModel
from .reservation import ReservationModel
from .movie import MovieModel


class MovieRatingModel(db.Model):
    """Docstring here."""

    __tablename__ = "movie_rating"

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(TINYINT)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship(UserModel, backref="user.id")
    reservation_id = db.Column(
        db.Integer, db.ForeignKey("reservation.id"), unique=True, nullable=False
    )
    reservation = db.relationship(ReservationModel, backref="movie_rating_reservation", uselist=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"), nullable=False)
    movie = db.relationship(MovieModel, backref="movie_rating_movie")

    def __init__(self):
        pass
