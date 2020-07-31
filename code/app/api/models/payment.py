from datetime import datetime
import enum

from db import db


class PaymentTypeEnum(enum.Enum):
    """Docstring here."""

    paymaya = "paymaya"


class PaymentModel(db.Model):
    """Docstring Here."""

    __tablename__ = "payment"

    id = db.Column(db.Integer, primary_key=True)
    token_id = db.Column(db.Text)
    total_price = db.Column(db.Float(8, 2))
    type = db.Column(db.Enum(PaymentTypeEnum))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now,
                           onupdate=datetime.now)

    def __init__(self, token_id, total_price, type, id=None):
        self.id = id
        self.token_id = token_id
        self.total_price = total_price,
        self.type = type

    def save_to_db(self):
        """Docstring here."""
        db.session.add(self)
        db.session.commit()
