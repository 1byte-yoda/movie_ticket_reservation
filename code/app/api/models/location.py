from datetime import datetime

from sqlalchemy.dialects.mysql import CHAR

from db import db


class LocationModel(db.Model):
    """Docstring here."""

    __tablename__ = "location"

    id = db.Column(db.Integer, primary_key=True)
    province = db.Column(db.String(120))
    city = db.Column(db.String(120))
    barangay = db.Column(db.String(120))
    longitude = db.Column(CHAR(30))
    latitude = db.Column(CHAR(30))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def json(self) -> dict:
        """JSON representation of the LocationModel."""
        return {
            "id": self.id,
            "province": self.province,
            "city": self.city,
            "barangay": self.barangay,
            "longitude": self.longitude,
            "latitude": self.latitude
        }
