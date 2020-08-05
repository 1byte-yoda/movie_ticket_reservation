from datetime import datetime

from db import db


class MasterScheduleModel(db.Model):
    """Docstring here."""

    __tablename__ = "master_schedule"

    id = db.Column(db.Integer, primary_key=True)
    launch_datetime = db.Column(db.DateTime, nullable=False)
    phase_out_datetime = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def json(self):
        return {
            "id": self.id,
            "launch_datetime": self.launch_datetime,
            "phase_out_datetime": self.phase_out_datetime
        }

    @classmethod
    def find_by_id(cls, id: int) -> "MasterScheduleModel":
        """Find a master schedule in the database by id."""
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        """Save a new master schedule in the database."""
        db.session.add(self)
        db.session.commit()

    def update(self, update_data: dict):
        """Update a master schedule in the database."""
        (db.session.query(MasterScheduleModel)
                   .filter_by(id=self.id)
                   .update(update_data))
        db.session.commit()

    def remove_from_db(self):
        """Remove a master schedule from the database."""
        db.session.delete(self)
        db.session.commit()
