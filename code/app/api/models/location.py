from datetime import datetime

from sqlalchemy.types import CHAR

from db import db
from .barangay import BarangayModel


class LocationModel(db.Model):
    """Docstring here."""

    __tablename__ = "location"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    barangay_id = db.Column(db.Integer, db.ForeignKey("barangay.id"), nullable=False)
    barangay = db.relationship(BarangayModel, backref="barangay", lazy=True)
    longitude = db.Column(CHAR(16), nullable=False)
    latitude = db.Column(CHAR(16), nullable=False)

    def __init__(self, barangay_id):
        self.barangay_id = barangay_id

    def json(self) -> dict:
        """JSON representation of the LocationModel."""
        return {
            "id": self.id,
            "barangay": self.barangay.json()
        }

    @classmethod
    def find_by_id(cls, id: int) -> "LocationModel":
        return cls.query.filter_by(id=id).first()

    def remove_from_db(self):
        db.session.delete(self)
        db.session.comit()
