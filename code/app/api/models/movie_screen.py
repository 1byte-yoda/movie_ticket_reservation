from datetime import datetime

from db import db
from .screen import ScreenModel
from .movie import MovieModel
from .schedule import ScheduleModel


class MovieScreenModel(db.Model):
    """Docstring here."""

    __tablename__ = "movie_screen"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now,
                           onupdate=datetime.now)

    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))
    movie = db.relationship(MovieModel, backref="movie", lazy=True)
    screen_id = db.Column(db.Integer, db.ForeignKey("screen.id"))
    screen = db.relationship(ScreenModel, backref="screen_movie_screen_model", lazy=True)
    schedule_id = db.Column(db.Integer, db.ForeignKey("schedule.id"))
    schedule = db.relationship(ScheduleModel, backref="schedule", lazy=True)

    def __init__(self, id, movie, screen, schedule):
        self.id = id
        self.movie = movie
        self.screen = screen
        self.schedule = schedule

    def __repr__(self) -> str:
        """Str representation of the seat reservation model."""
        return ("<SeatReservationModel {}, {}>".format(self.movie,
                self.screen))

    @classmethod
    def _is_valid_representation(cls, *, data: dict) -> bool:
        """Check validity of dictionary keys as representation of this model."""
        base = {"screen_id", "movie_id"}
        return True if set(base) == set(data) else False

    @classmethod
    def find(cls, *, data: dict) -> "MovieScreenModel":
        """Docstring here."""
        if not cls._is_valid_representation(data=data):
            return {"message": "Invalid request."}, 400
        movie_screen = cls.query.filter_by(**data).first()
        return movie_screen
