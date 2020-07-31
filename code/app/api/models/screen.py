from datetime import datetime

from db import db
from .cinema import CinemaModel


class ScreenModel(db.Model):
    """Docstring here."""

    __tablename__ = "screen"

    id = db.Column(db.Integer, primary_key=True)
    capacity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now,
                           onupdate=datetime.now)

    cinema_id = db.Column(db.Integer, db.ForeignKey("cinema.id"))
    cinema = db.relationship(CinemaModel, backref="cinema", lazy=True)

    def __init__(self):
        pass
