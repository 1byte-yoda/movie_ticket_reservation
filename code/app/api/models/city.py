from datetime import datetime

from db import db
from .province import ProvinceModel


class CityModel(db.Model):
    """Docstring here."""

    __tablename__ = "city"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    province_id = db.Column(db.Integer, db.ForeignKey("province.id"), nullable=False)
    province = db.relationship(ProvinceModel, backref="province", lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, name, province_id):
        self.name = name,
        self.province_id = province_id

    def json(self):
        """JSON representation of City."""
        return {
            "name": self.name,
            "province": self.province.json()
        }

    @classmethod
    def find_by_id(cls, id: int):
        return cls.query.filter_by(id=id).first()
