from datetime import datetime
from typing import List

from db import db
from .location import LocationModel


class CinemaModel(db.Model):
    """A model that will interact with the cinema table SQL queries.

    Contains multiple functions that can perform the basic CRUD operation
    for 1 row/entry in the cinema table.
    """

    __tablename__ = "cinema"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    open_time = db.Column(db.Time)
    close_time = db.Column(db.Time)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    location_id = db.Column(db.Integer, db.ForeignKey("location.id"), nullable=False)
    location = db.relationship(
        LocationModel, backref="location", lazy=True
    )

    def json(self) -> dict:
        """JSON representation of the CinemaModel."""
        return {
            "id": self.id,
            "name": self.name,
            "open_time": self.open_time,
            "close_time": self.close_time,
            "location": self.location.json()
        }

    @classmethod
    def find_by_id(cls, id: int) -> "CinemaModel":
        """Find a cinema in the database by id."""
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        """Save a new cinema in the database."""
        db.session.add(self)
        db.session.commit()

    def update(self, update_data: dict):
        """Update a cinema in the database."""
        (db.session.query(CinemaModel)
                   .filter_by(id=self.id)
                   .update(update_data))
        db.session.commit()

    def remove_from_db(self):
        """Remove a cinema from the database."""
        db.session.delete(self)
        db.session.commit()


class CinemaListModel(CinemaModel):
    """An extension of CinemaModel.

    All SQL queries that works with an array of
    CinemaModel is implemented here.
    """

    @classmethod
    def find_cinemas_by_location(cls, location_id: int) -> List[CinemaModel]:
        """Find a list of cinema that is within a specified location."""
        return cls.query.filter_by(location_id=location_id).all()
