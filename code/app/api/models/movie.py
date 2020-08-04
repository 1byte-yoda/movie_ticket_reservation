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
    name = db.Column(db.String(120))
    price = db.Column(db.Float(7, 2))
    description = db.Column(db.Text)
    rating = db.Column(db.Float(2, 1))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def json(self):
        """JSON representation of the MovieModel."""
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "rating": self.rating
        }

    @classmethod
    def find_by_id(cls, *, id: int) -> "MovieModel":
        """Find a movie by id."""
        return cls.query.filter_by(id=id).first()

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
