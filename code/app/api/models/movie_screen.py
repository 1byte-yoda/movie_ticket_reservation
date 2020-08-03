from datetime import datetime

from db import db
from .screen import ScreenModel
from .movie import MovieModel
from .schedule import ScheduleModel
from .response_messages import UNKNOWN_ERROR_MESSAGE_500


class MovieScreenModel(db.Model):
    """Docstring here."""

    __tablename__ = "movie_screen"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))
    movie = db.relationship(MovieModel, backref="movie", lazy="joined", join_depth=1)
    screen_id = db.Column(db.Integer, db.ForeignKey("screen.id"))
    screen = db.relationship(
        ScreenModel, backref="screen_movie_screen_model", lazy="joined", join_depth=1
    )
    schedule_id = db.Column(db.Integer, db.ForeignKey("schedule.id"))
    schedule = db.relationship(ScheduleModel, backref="schedule", lazy=True)

    def __init__(self, id, movie, screen, schedule):
        self.id = id
        self.movie = movie
        self.screen = screen
        self.schedule = schedule

    def __repr__(self) -> str:
        """Printable representation of the seat reservation model."""
        return "<MovieScreenModel {}, {}>".format(self.movie, self.screen)

    @classmethod
    def find(
        cls, *, screen_id: int, movie_id: int, schedule_id: int
    ) -> "MovieScreenModel":
        """Docstring here."""
        try:
            movie_screen = cls.query.filter_by(
                schedule_id=schedule_id, screen_id=screen_id, movie_id=movie_id
            )
        except Exception as e:
            return {"message": UNKNOWN_ERROR_MESSAGE_500}, 500
        return movie_screen.first()
