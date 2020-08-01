from datetime import datetime
import enum

from db import db


class AccountTypeEnum(enum.Enum):
    """Account type for SQLAlchemy Data Type."""

    user = "regular"
    admin = "admin"


class AccountModel(db.Model):
    """Proxy class to substitute database user table."""

    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    type = db.Column(db.Enum(AccountTypeEnum))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def __init__(self, *, id=None, email="", password="", type=""):
        """Docstring here."""
        self.id = id
        self.email = email
        self.password = password
        self.type = type
        self.created_at = None
        self.updated_at = None

    def json(self) -> dict:
        """JSON representation of the account model."""
        return {"id": self.id, "email": self.email,
                "password": self.password, "type": self.type,
                "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S")}

    @classmethod
    def find_by_email(cls, *, email: str) -> "AccountModel":
        """Docstring here."""
        account = cls.query.filter_by(email=email).first()
        return account

    @classmethod
    def find_by_id(cls, *, _id: int) -> "AccountModel":
        """Docstring here."""
        account = cls.query.filter_by(id=_id).first()
        return account

    def register(self):
        """Docstring here."""
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self):
        """Remove an account from the database."""
        db.session.delete(self)
        db.session.commit()
