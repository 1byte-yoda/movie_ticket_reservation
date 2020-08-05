from datetime import datetime

from db import db
from .master_schedule import MasterScheduleModel


class ScheduleModel(db.Model):
    """A model that will interact with the schedule table SQL queries.

    Contains multiple functions that can perform the basic CRUD operation
    for 1 row/entry in the schedule table.
    """

    __tablename__ = "schedule"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    play_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    master_schedule_id = db.Column(
        db.Integer, db.ForeignKey("master_schedule.id"), nullable=False
    )
    master_schedule = db.relationship(
        MasterScheduleModel, backref="master_schedule", lazy=True
    )
    db.UniqueConstraint(master_schedule_id, play_datetime, end_datetime,)

    def json(self):
        """JSON representation of the ScheduleModel."""
        return {
            "id": self.id,
            "play_datetime": self.play_datetime,
            "end_datetime": self.end_datetime,
            "master_schedule": self.master_schedule.json()
        }

    @classmethod
    def find_by_id(cls, id: int) -> "ScheduleModel":
        """Find a schedule in the database by id."""
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        """Save a new schedule in the database."""
        db.session.add(self)
        db.session.commit()

    def update(self, update_data: dict):
        """Update a schedule in the database."""
        (db.session.query(ScheduleModel)
                   .filter_by(id=self.id)
                   .update(update_data))
        db.session.commit()

    def remove_from_db(self):
        """Remove a schedule from the database."""
        db.session.delete(self)
        db.session.commit()
