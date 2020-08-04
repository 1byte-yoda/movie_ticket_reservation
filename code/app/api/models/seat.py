from datetime import datetime
from typing import List

from db import db
from .screen import ScreenModel


class SeatModel(db.Model):
    """A model that will interact with the seat table SQL queries.

    Contains multiple functions that can perform the basic CRUD operation
    for 1 row/entry in the seat table.
    """

    __tablename__ = "seat"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    screen_id = db.Column(db.Integer, db.ForeignKey("screen.id"), nullable=False)
    screen = db.relationship(ScreenModel, backref="screen", lazy="select")

    @classmethod
    def find_by_id(cls, id: int) -> "SeatModel":
        """Find a seat in the database by id."""
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        """Save a new seat in the database."""
        db.session.add(self)
        db.session.commit()

    def update(self, update_data: dict):
        """Update a seat in the database."""
        (db.session.query(SeatModel)
                   .filter_by(id=self.id)
                   .update(update_data))
        db.session.commit()

    def remove_from_db(self):
        """Remove a seat from the database."""
        db.session.delete(self)
        db.session.commit()


class SeatListModel(SeatModel):
    """An extension of SeatModel.

    All SQL queries that works with an array of
    SeatModel is implemented here.
    """

    @classmethod
    def find_existing_seats(cls, *, screen_id, seat_id_list: list) -> List[SeatModel]:
        """Find all of existing seats w.r.t screen and array of seat.

        Find all seats within a specified screen and also
        within a specified array of seat.
        """
        seat_list = (
            cls.query.with_entities(cls.id)
            .filter(SeatModel.screen_id == screen_id)
            .filter(SeatModel.id.in_(seat_id_list))
            .all()
        )
        return list(*zip(*seat_list))

    @classmethod
    def find_seats_by_screen(cls, screen_id: int) -> List[SeatModel]:
        """Find a list of seats that is within a specified screen."""
        return cls.query.filter_by(screen_id=screen_id).all()
