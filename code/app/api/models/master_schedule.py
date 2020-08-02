from datetime import datetime

from db import db


class MasterScheduleModel(db.Model):
    """Docstring here."""

    __tablename__ = "master_schedule"

    id = db.Column(db.Integer, primary_key=True)
    launch_datetime = db.Column(db.DateTime)
    phase_out_datetime = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now,
                           onupdate=datetime.now)
