from datetime import datetime

from db import db
from .screen import ScreenModel
from .movie import MovieModel
from .schedule import ScheduleModel
from .customized_queries.movie_screen import SELECT_NOW_SHOWING_QUERY


class MovieScreenModel(db.Model):
    """A model that will interact with the movie_screen table SQL queries.

    Contains multiple functions that can perform the basic CRUD operation
    for 1 row/entry in the movie_screen table.
    """

    __tablename__ = "movie_screen"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"), nullable=False)
    movie = db.relationship(MovieModel, backref="movie", lazy="joined", join_depth=1)
    screen_id = db.Column(db.Integer, db.ForeignKey("screen.id"), nullable=False)
    screen = db.relationship(
        ScreenModel, backref="screen_movie_screen_model", lazy="joined", join_depth=1
    )
    schedule_id = db.Column(db.Integer, db.ForeignKey("schedule.id"), nullable=False)
    schedule = db.relationship(ScheduleModel, backref="schedule", lazy=True)
    db.UniqueConstraint(movie_id, screen_id, schedule_id,)

    def json(self):
        """JSON representation of the MovieModel."""
        return {
            "id": self.id,
            "movie": self.movie.json(),
            "screen": self.screen.json(),
            "schedule": self.schedule.json()
        }

    @classmethod
    def find(
        cls, *, screen_id: int, movie_id: int, schedule_id: int
    ) -> "MovieScreenModel":
        """Find a unique row in the movie_screen table."""
        movie_screen = cls.query.filter_by(
            schedule_id=schedule_id, screen_id=screen_id, movie_id=movie_id
        )
        return movie_screen.first()

    @classmethod
    def find_by_id(cls, *, id: int) -> "MovieScreenModel":
        """Find a movie-screen by id."""
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        """Save a new movie-screen in the database."""
        db.session.add(self)
        db.session.commit()

    def update(self, update_data: dict):
        """Update a movie-screen in the database."""
        (db.session.query(MovieScreenModel)
                   .filter_by(id=self.id)
                   .update(update_data))
        db.session.commit()

    def remove_from_db(self):
        """Remove a movie-screen from the database."""
        db.session.delete(self)
        db.session.commit()


class MovieScreenListModel(MovieScreenModel):
    """An extension of MovieScreenModel.

    All SQL queries that works with an array of
    MovieScreenModel is implemented here.
    """

    @classmethod
    def find_showing(cls):
        """Find all movie_screen_id of showing movies.

        Use to get the movies to show for every user.
        """
        movie_screen = cls.query.from_statement(db.text(SELECT_NOW_SHOWING_QUERY)).all()
        now_showing = map(lambda ms: (
            ms.screen.cinema.name,
            ms.screen_id,
            ms.movie.name,
            ms.schedule.play_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            ms.schedule.end_datetime.strftime("%Y-%m-%d %H:%M:%S")
        ), movie_screen)
        return list(now_showing)
