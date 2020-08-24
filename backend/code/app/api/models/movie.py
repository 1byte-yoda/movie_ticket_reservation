from datetime import datetime
from typing import List
import math
import json
import ast

from sqlalchemy import desc, asc

from db import db


PAGINATION_SIZE = 20


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
    youtube = db.Column(db.Text)
    price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    db.UniqueConstraint(name, cinema_id)

    def __init__(
        self,name, cinema_id, description, duration, release_date, price, company=None,
        genre=None, casts=None, youtube=None, rating=None
    ):
        self.name = name
        self.cinema_id = cinema_id
        self.description = description
        self.duration = duration
        self.release_date = release_date
        self.rating = rating
        self.price = price
        self.company = company
        self.genre = genre
        self.casts = casts
        self.youtube = youtube

    def json(self):
        """JSON representation of the MovieModel."""
        return {
            "id": self.id,
            "name": self.name,
            "cinema": self.cinema.json(),
            "description": self.description,
            "duration": self.duration,
            "release_date": self.release_date,
            "rating": self.rating,
            "price": self.price,
            "company": self.company,
            "genre": self.genre,
            "casts": ast.literal_eval(
                json.loads(self.casts if self.casts else '{"casts": "[]"}')["casts"]
            ),
            "youtube": json.dumps(json.loads(self.youtube if self.youtube else '{"results": "none"}').get("results"))
            
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

    @classmethod
    def calculate_page_size(cls):
        """Calculate the page size of the movie page."""
        return math.ceil(db.session.query(cls.id).count() / PAGINATION_SIZE)


class MovieListModel(MovieModel):
    """An extension of MovieModel.

    All SQL queries that works with an array of
    MovieModel is implemented here.
    """

    @classmethod
    def find_recommended_movies(cls, movie_id_list: list) -> List[MovieModel]:
        """Find all of recommended movies for a user."""
        return cls.query.filter(MovieModel.id.in_(movie_id_list))

    @classmethod
    def find_all_movies(cls) -> List[MovieModel]:
        """Find all of movies registered in the system."""
        # end_item = page * PAGINATION_SIZE
        # start_item = end_item - PAGINATION_SIZE
        # return cls.query.order_by(desc("rating"), desc("release_date")).offset(start_item).limit(end_item).all()
        return cls.query.order_by(desc("rating"), asc("release_date")).all()
