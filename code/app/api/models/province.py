from datetime import datetime

from db import db


class ProvinceModel(db.Model):
    """Docstring here."""

    __tablename__ = "province"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def json(self):
        """JSON representation of Province."""
        return {
            "name": self.name
        }

    @classmethod
    def find_by_id(cls, id: int):
        return cls.query.filter_by(id=id).first()
