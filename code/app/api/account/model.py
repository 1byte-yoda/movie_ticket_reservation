from datetime import datetime
import enum

from db import db


class AccountTypeEnum(enum.Enum):
    """Account type for SQLAlchemy Data Type."""

    user = "user"
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

    def __init__(self, *, id=None, email="", password=""):
        """Docstring here."""
        self.id = id
        self.email = email
        self.password = password
        self.created_at = None
        self.updated_at = None

    def json(self):
        """JSON representation of this object."""
        return {"id": self.id, "email": self.email, "password": self.password,
                "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S")}

    @classmethod
    def find_by_email(cls, *, email):
        """Docstring here."""
        account = cls.query.filter_by(email=email).first()
        return account

    @classmethod
    def find_by_id(cls, *, _id):
        """Docstring here."""
        account = cls.query.filter_by(id=_id).first()
        return account

    def register(self):
        """Docstring here."""
        db.session.add(self)
        db.session.commit()
