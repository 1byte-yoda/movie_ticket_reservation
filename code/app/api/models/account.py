from datetime import datetime
import enum

from db import db


class AccountTypeEnum(enum.Enum):
    """Account type for SQLAlchemy Data Type."""

    regular = "regular"
    admin = "admin"

    def __str__(self):
        return self.value


class AccountModel(db.Model):
    """Proxy class to substitute database user table."""

    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.now
    )

    def json(self):
        """JSON representation of AccountModel."""
        return {"id": self.id, "email": self.email, "type": self.type}

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

    def update(self, update_data: dict):
        """Update an account in the database."""
        (db.session.query(AccountModel)
                   .filter_by(id=self.id)
                   .update(update_data))
        db.session.commit()
