import string
from datetime import datetime
from typing import List

from sqlalchemy.dialects import mysql 
from sqlalchemy import func

from db import db
from .screen import ScreenModel


class SeatModel(db.Model):
    """A model that will interact with the seat table SQL queries.

    Contains multiple functions that can perform the basic CRUD operation
    for 1 row/entry in the seat table.
    """

    __tablename__ = "seat"

    id = db.Column(db.Integer, primary_key=True)
    row_id = db.Column(db.Integer, nullable=False)
    row_letter = db.Column(
        db.Enum('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'), nullable=False
    )
    row_letter_id = db.Column(mysql.INTEGER(2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    screen_id = db.Column(db.Integer, db.ForeignKey("screen.id"), nullable=False)
    screen = db.relationship(ScreenModel, backref="screen", lazy="select")
    db.UniqueConstraint(screen_id, row_id, row_letter,)

    def __init__(self, row_id, screen, row_letter, row_letter_id):
        self.row_id = row_id
        self.screen = screen
        self.row_letter = row_letter
        self.row_letter_id = row_letter_id

    def json(self):
        return {
            "id": self.id,
            "row_id": self.row_id,
            "col_letter": self.row_letter,
            "col_id": self.row_letter_id
        }

    @classmethod
    def find_by_id(cls, id: int) -> "SeatModel":
        """Find a seat in the database by id."""
        return cls.query.filter_by(id=id).first()

    @classmethod
    def last_row(cls, screen_id: int):
        return cls.query.filter_by(screen_id=screen_id).all()[-1]

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

    @classmethod
    def last_letter_count(cls, screen_id: int, row_letter: str) -> "SeatModel":
        return (cls.query.with_entities(
            cls.row_letter, func.count(cls.row_id)
        ).group_by(cls.row_letter)
         .filter_by(row_letter=row_letter, screen_id=screen_id).first())[-1]


class SeatListModel(SeatModel):
    """An extension of SeatModel.

    All SQL queries that works with an array of
    SeatModel is implemented here.
    """

    @classmethod
    def find_all_seats(cls, *, screen_id) -> List[SeatModel]:
        """Find all of existing seats w.r.t screen

        Find all seats within a specified screen.
        """
        seat_list = (
            cls.query.with_entities(cls.id)
            .filter(SeatModel.screen_id == screen_id)
            .all()
        )
        return list(*zip(*seat_list))

    @classmethod
    def find_seats_by_screen(cls, screen_id: int) -> List[SeatModel]:
        """Find a list of seats that is within a specified screen."""
        return list(map(lambda x: x.id, cls.query.filter_by(screen_id=screen_id).all()))

    @classmethod
    def save_all(cls, *, seats: list):
        """Docstring here."""
        db.session.add_all(seats)
        db.session.commit()

    @staticmethod
    def seat_letters() -> list:
        return [_ for _ in string.ascii_uppercase[:10]]

    @classmethod
    def populate_screen_seat(cls, screen: object, last_row_id: int = 1) -> list:
        seats = []
        letters = cls.seat_letters()
        seats_per_row = screen.capacity // len(letters)
        for letter in letters:
            for i in range(1, 1 + seats_per_row):
                seats.append(
                    SeatModel(row_id=last_row_id, screen=screen, row_letter=letter, row_letter_id=i)
                )
                last_row_id += 1
        return seats

    @classmethod
    def delete_by_screen_id(cls, screen_id: int):
        db.session.query(SeatModel).filter_by(screen_id=screen_id).delete()
        db.session.commit()
