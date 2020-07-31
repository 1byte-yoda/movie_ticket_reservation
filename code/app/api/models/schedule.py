from datetime import datetime

from db import db


class ScheduleModel(db.Model):
    """Docstring here."""

    __tablename__ = "schedule"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now,
                           onupdate=datetime.now)
    play_datetime = db.Column(db.DateTime)
    end_datetime = db.Column(db.DateTime)
