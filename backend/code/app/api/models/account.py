from datetime import datetime
import enum

from werkzeug.security import generate_password_hash, check_password_hash

from db import db


class AccountTypeEnum(enum.Enum):
    """Account type for SQLAlchemy Data Type."""

    regular = "regular"
    admin = "admin"
    super_admin = "super_admin"

    def __str__(self):
        return self.value


class AccountModel(db.Model):
    """Proxy class to substitute database user table."""

    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    type = db.Column(db.Enum("regular", "admin", "super_admin"), default="regular")
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.now)
    

    def __init__(self, email, password, type):
        self.email = email
        self.password = password
        self.type = type

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def json(self):
        """JSON representation of AccountModel."""
        return {"id": self.id, "email": self.email, "type": self.type}

    @classmethod
    def find_by_email(cls, *, email: str) -> "AccountModel":
        """Docstring here."""
        account = cls.query.filter_by(email=email).first()
        return account

    @classmethod
    def find_by_id(cls, *, id: int) -> "AccountModel":
        """Docstring here."""
        account = cls.query.filter_by(id=id).first()
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
        (db.session.query(AccountModel).filter_by(id=self.id).update(update_data))
        db.session.commit()

    def change_password(self, password: str):
        self.password = password
        db.session.commit()
