from datetime import datetime

from db import db
from ..account.model import AccountModel
from ...utils import deserialize_datetime


class ReservationModel(db.Model):
    """Docstring here."""

    __tablename__ = "reservation"

    id = db.Column(db.Integer, primary_key=True)

    head_count = db.Column(db.Integer)
    reserve_datetime = db.Column(db.DateTime, default=datetime.now)
    cancel_datetime = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now,
                           onupdate=datetime.now)

    account_id = db.Column(db.Integer, db.ForeignKey("account.id"))
    account = db.relationship(AccountModel, backref="account")

    def __init__(self, id=None, account_id=None, head_count=None,
                 reserve_datetime=None, cancel_datetime=None):
        """Docstring here."""
        self.id = id
        self.account_id = account_id
        self.head_count = head_count
        self.reserve_datetime = reserve_datetime
        self.cancel_datetime = cancel_datetime
        self.created_at = None
        self.updated_at = None

    def json(self):
        """JSON representation of the reservation model."""
        return {
            "id": self.id, "account_id": self.account_id,
            "head_count": self.head_count,
            "reserve_datetime": deserialize_datetime(self.reserve_datetime),
            "cancel_datetime": deserialize_datetime(self.cancel_datetime),
            "created_at": deserialize_datetime(self.created_at),
            "updated_at": deserialize_datetime(self.updated_at)
        }

    @classmethod
    def find_by_id(cls, *, id_):
        """Docstring here."""
        temp_reservation = cls.query.filter_by(id=id_).first()
        return temp_reservation

    @classmethod
    def find_by_account_movie_screen(cls, *, account_id, movie_screen_id):  # Move this on its own class
        """Docstring here."""
        temp_reservation = cls.query.filter_by(account_id=account_id,
                                               movie_screen_id=movie_screen_id).first()
        return temp_reservation

    def save_to_db(self):
        """Docstring here."""
        db.session.add(self)
        db.session.commit()

    def update(self, *, data):
        """Docstring here."""
        self.head_count = data["head_count"]
        self.reserve_datetime = data["reserve_datetime"]
        db.session.commit()

    def cancel(self, *, updated_cancel_datetime):
        """Docstring here."""
        self.cancel_datetime = updated_cancel_datetime
        db.session.commit()
