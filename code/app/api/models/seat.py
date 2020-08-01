from datetime import datetime

from db import db
from .screen import ScreenModel


class SeatModel(db.Model):
    """Docstring here."""

    __tablename__ = "seat"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now,
                           onupdate=datetime.now)

    screen_id = db.Column(db.Integer, db.ForeignKey("screen.id"))
    screen = db.relationship(ScreenModel, backref="screen", lazy="select")

    def __init__(self, id=None, screen_id=None):
        self.id = id
        self.screen_id = screen_id

    @classmethod
    def find_by_id(cls, id_: int) -> "SeatModel":
        """Docstring here."""
        return cls.query.filter_by(id=id_).first()


class SeatListModel(SeatModel):
    """Docstring here."""

    @classmethod
    def find_existing(cls, *, screen_id, seat_id_list: list) -> list:
        seat_list = cls.query.with_entities(cls.id)\
                             .filter(SeatModel.screen_id == screen_id)\
                             .filter(SeatModel.id.in_(seat_id_list)).all()
        return list(*zip(*seat_list))
