from datetime import datetime

from db import db
from .account import AccountModel
from .cinema import CinemaModel


class UserModel(db.Model):
    """Docstring here."""

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    contact_no = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now,
                           onupdate=datetime.now)

    account_id = db.Column(db.Integer, db.ForeignKey("account.id"))
    account = db.relationship(AccountModel, backref="account", lazy="dynamic",
                              uselist=False)
    cinema_id = db.Column(db.Integer, db.ForeignKey("cinema.id"))
    cinema = db.relationship(CinemaModel, backref="cinema", lazy="dynamic",
                             uselist=False)

    def __init__(self):
        pass
