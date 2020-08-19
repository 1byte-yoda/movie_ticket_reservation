from datetime import datetime

from db import db
from .screen import ScreenModel
from .customized_queries.schedule import SELECT_CONFLICT_SCHEDULE_QUERY


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
    screen_id = db.Column(
        db.Integer, db.ForeignKey("screen.id"), nullable=False
    )
    screen = db.relationship(
        ScreenModel, backref="schedule_screen", lazy=True
    )
    db.UniqueConstraint(screen_id, play_datetime, end_datetime,)

    def __init__(self, play_datetime, end_datetime, screen):
        self.play_datetime = play_datetime
        self.end_datetime = end_datetime
        self.screen = screen

    def json(self):
        """JSON representation of the ScheduleModel."""
        return {
            "id": self.id,
            "play_datetime": self.play_datetime,
            "end_datetime": self.end_datetime,
            "screen": self.screen.json()
        }

    @classmethod
    def find_by_id(cls, id: int) -> "ScheduleModel":
        """Find a schedule in the database by id."""
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_conflicts(cls, screen_id, scheds):
        """Find a schedule in the database by screen_id its schedule."""
        for sched in scheds:
            yield (cls.query.from_statement(db.text(
                SELECT_CONFLICT_SCHEDULE_QUERY.format(
                    screen_id=screen_id,
                    **sched
                )
            )).first())

    def save_to_db(self):
        """Save a new schedule in the database."""
        db.session.add(self)
        db.session.commit()

    def update(self, update_data: dict):
        """Update a schedule in the database."""
        (db.session.query(ScheduleModel)
                   .filter_by(id=self.id)
                   .update(update_data))

    def remove_from_db(self):
        """Remove a schedule from the database."""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def count_instances(cls, master_schedule_id: int) -> list:
        """Count instances of a master_schedule_id."""
        return cls.query.filter_by(master_schedule_id=master_schedule_id).count()
