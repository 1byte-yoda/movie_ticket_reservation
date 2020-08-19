from datetime import datetime

from db import db
from .account import AccountModel
from .cinema import CinemaModel
from .location import LocationModel


class UserModel(db.Model):
    """Docstring here."""

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    contact_no = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    account_id = db.Column(db.Integer, db.ForeignKey("account.id", ondelete="CASCADE"))
    account = db.relationship(
        AccountModel, backref="user_account", lazy=True, uselist=False
    )
    cinema_id = db.Column(db.Integer, db.ForeignKey("cinema.id", ondelete="CASCADE"))
    cinema = db.relationship(
        CinemaModel, backref="user_cinema", lazy=True
    )
    location_id = db.Column(db.Integer, db.ForeignKey("location.id", ondelete="CASCADE"))
    location = db.relationship(
        LocationModel, backref="location", lazy=True
    )

    def __init__(
        self, first_name, last_name, contact_no, account, location, cinema=None
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.contact_no = contact_no
        self.location = location
        self.account = account
        self.cinema = cinema

    def json(self):
        """JSON representation of the UserModel."""
        return {
            "id": self.id,
            "account": self.account.json(),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "contact_no": self.contact_no,
            "location": self.location.json()
        }

    @classmethod
    def find_by_id(cls, id: int) -> "UserModel":
        """Find a user in the database by id."""
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_account_id(cls, id: int) -> "UserModel":
        """Find a user in the database by account_id."""
        return cls.query.filter_by(account_id=id).first()

    def save_to_db(self):
        """Save a new user in the database."""
        db.session.add(self)
        db.session.commit()

    def update(self, update_data: dict):
        """Update a user in the database."""
        (db.session.query(UserModel)
                   .filter_by(id=self.id)
                   .update(update_data))
        db.session.commit()

    def remove_from_db(self):
        """Remove a user from the database."""
        db.session.delete(self)
        db.session.commit()
