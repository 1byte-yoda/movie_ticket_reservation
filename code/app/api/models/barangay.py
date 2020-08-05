from datetime import datetime

from db import db
from .city import CityModel


class BarangayModel(db.Model):
    """Docstring here."""

    __tablename__ = "barangay"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey("city.id"), nullable=False)
    city = db.relationship(CityModel, backref="city", lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, name, city_id):
        self.name = name
        self.city_id = city_id

    def json(self):
        """JSON representation of Barangay."""
        return {
            "name": self.name,
            "city": self.city.json()
        }

    @classmethod
    def find_by_id(cls, id: int):
        return cls.query.filter_by(id=id).first()
