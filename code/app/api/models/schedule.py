from datetime import datetime

from db import db
from .master_schedule import MasterScheduleModel
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
    play_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    screen_id = db.Column(
        db.Integer, db.ForeignKey("screen.id"), nullable=False
    )
    screen = db.relationship(
        ScreenModel, backref="schedule_screen", lazy=True
    )
    master_schedule_id = db.Column(
        db.Integer, db.ForeignKey("master_schedule.id"), nullable=False
    )
    master_schedule = db.relationship(
        MasterScheduleModel, backref="master_schedule", lazy=True
    )
    db.UniqueConstraint(screen_id, master_schedule_id, play_time, end_time,)

    def __init__(self, play_time, end_time, screen, master_schedule):
        self.play_time = play_time
        self.end_time = end_time
        self.screen = screen
        self.master_schedule = master_schedule

    def json(self):
        """JSON representation of the ScheduleModel."""
        return {
            "id": self.id,
            "play_time": self.play_time,
            "end_time": self.end_time,
            "screen": self.screen.json(),
            "master_schedule": self.master_schedule.json()
        }

    @classmethod
    def find_by_id(cls, id: int) -> "ScheduleModel":
        """Find a schedule in the database by id."""
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_conflicts(cls, screen_id, launch_date, phase_out_date, scheds):
        """Find a schedule in the database by screen_id its schedule."""

        # schedule = cls.query.from_statement(db.text(SELECT_CONFLICT_SCHEDULE_QUERY)).all()
        for sched in scheds:
            yield (cls.query.from_statement(db.text(
                SELECT_CONFLICT_SCHEDULE_QUERY.format(
                    screen_id=screen_id,
                    launch_date=launch_date,
                    phase_out_date=phase_out_date,
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
        db.session.commit()

    def remove_from_db(self):
        """Remove a schedule from the database."""
        db.session.delete(self)
        db.session.commit()
