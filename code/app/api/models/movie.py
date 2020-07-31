from datetime import datetime

from db import db


class MovieModel(db.Model):
    """Docstring here."""

    __tablename__ = "movie"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    price = db.Column(db.Float(7, 2))
    description = db.Column(db.Text)
    rating = db.Column(db.Float(2, 1))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now,
                           onupdate=datetime.now)

    def __init__(self, id, name, price, description, rating):
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.rating = rating

    @classmethod
    def find_by_id(cls, *, id_: int) -> "MovieModel":
        return cls.query.filter_by(id=id_).first()
