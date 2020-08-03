from datetime import datetime

from db import db
from .location import LocationModel


class CinemaModel(db.Model):
    """Docstring here."""

    __tablename__ = "cinema"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    open_time = db.Column(db.Time)
    close_time = db.Column(db.Time)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    location_id = db.Column(db.Integer, db.ForeignKey("location.id"))
    location = db.relationship(
        LocationModel, backref="location", lazy=True, uselist=False
    )

    def __init__(self):
        pass
