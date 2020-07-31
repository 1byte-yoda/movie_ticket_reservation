from datetime import datetime

from sqlalchemy.dialects.mysql import TINYINT

from db import db
from .payment import PaymentModel
from .movie import MovieModel


class MovieRatingModel(db.Model):
    """Docstring here."""

    __tablename__ = "movie_rating"

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(TINYINT)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now,
                           onupdate=datetime.now)

    payment_id = db.Column(db.Integer, db.ForeignKey("payment.id"))
    payment = db.relationship(PaymentModel, backref="payment", uselist=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))
    movie = db.relationship(MovieModel, backref="movie")

    def __init__(self):
        pass
