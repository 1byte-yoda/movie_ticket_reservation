from datetime import datetime
from typing import List

from db import db


class MovieModel(db.Model):
    """A model that will interact with the movie table SQL queries.

    Contains multiple functions that can perform the basic CRUD operation
    for 1 row/entry in the movie table.
    """

    __tablename__ = "movie"

    id = db.Column(db.Integer, primary_key=True)
    cinema_id = db.Column(db.Integer, db.ForeignKey("cinema.id"), nullable=False)
    cinema = db.relationship("CinemaModel", backref="movie_cinema", lazy=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    company = db.Column(db.String(120))
    genre = db.Column(db.String(64))
    casts = db.Column(db.Text)
    rating = db.Column(db.Float(2, 1))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    db.UniqueConstraint(name, cinema_id)

    def __init__(self, name, cinema_id, description, duration, release_date, rating=None):
        self.name = name
        self.cinema_id = cinema_id
        self.description = description
        self.duration = duration
        self.release_date = release_date
        self.rating = rating

    def json(self):
        """JSON representation of the MovieModel."""
        return {
            "id": self.id,
            "name": self.name,
            "cinema": self.cinema.json(),
            "description": self.description,
            "duration": self.duration,
            "release_date": self.release_date,
            "rating": self.rating
        }

    @classmethod
    def find_by_id(cls, *, id: int, cinema_id: int) -> "MovieModel":
        """Find a movie by id."""
        return cls.query.filter_by(id=id, cinema_id=cinema_id).first()
    
    @classmethod
    def find_by_name(cls, *, name: str, cinema_id: int) -> "MovieModel":
        """Find a movie by name."""
        return cls.query.filter_by(name=name, cinema_id=cinema_id).first()

    def save_to_db(self):
        """Save a new movie in the database."""
        db.session.add(self)
        db.session.commit()

    def update(self, update_data: dict):
        """Update a movie in the database."""
        (db.session.query(MovieModel)
                   .filter_by(id=self.id)
                   .update(update_data))
        db.session.commit()

    def remove_from_db(self):
        """Remove a movie from the database."""
        db.session.delete(self)
        db.session.commit()


class MovieListModel(MovieModel):
    """An extension of MovieModel.

    All SQL queries that works with an array of
    MovieModel is implemented here.
    """

    @classmethod
    def find_recommended_movies(cls, movie_id_list: list) -> List[MovieModel]:
        """Find all of recommended movies for a user."""
        return cls.query.filter(MovieModel.id.in_(movie_id_list))
