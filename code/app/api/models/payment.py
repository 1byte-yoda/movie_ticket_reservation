from datetime import datetime

from db import db


class PaymentModel(db.Model):
    """Docstring Here."""

    __tablename__ = "payment"

    id = db.Column(db.Integer, primary_key=True)
    token_id = db.Column(db.Text, nullable=False)
    total_price = db.Column(db.Float(8, 2), nullable=False)
    type = db.Column(db.String(50), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, token_id, total_price, type, id=None):
        self.id = id
        self.token_id = token_id
        self.total_price = (total_price,)
        self.type = type

    def json(self):
        """JSON representation of PaymentModel."""
        return {"id": self.id, "type": self.type, "total_price": self.total_price}

    def save_to_db(self):
        """Docstring here."""
        db.session.add(self)
        db.session.commit()
