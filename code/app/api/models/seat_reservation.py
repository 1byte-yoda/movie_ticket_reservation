from datetime import datetime

import simplejson

from db import db
from .seat import SeatModel
from .reservation import ReservationModel
from .movie_screen import MovieScreenModel
from ...utils import deserialize_datetime


class SeatReservationModel(db.Model):
    """Docstring here."""

    __tablename__ = "seat_reservation"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float(6, 2))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now,
                           onupdate=datetime.now)

    seat_id = db.Column(db.Integer, db.ForeignKey("seat.id"))
    seats = db.relationship(SeatModel, backref="seats")
    reservation_id = db.Column(db.Integer, db.ForeignKey("reservation.id"))
    reservation = db.relationship(ReservationModel, backref="reservation")
    movie_screen_id = db.Column(db.Integer, db.ForeignKey("movie_screen.id"))
    movie_screen = db.relationship(MovieScreenModel, backref="movie_screen")
    promo_id = db.Column(db.Integer)

    def __init__(self, price, seat_id, reservation,
                 movie_screen, promo_id=None, id=None):
        """Docstring here."""
        self.id = id
        self.price = price
        self.created_at = None
        self.updated_at = None
        self.seat_id = seat_id
        self.reservation = reservation
        self.movie_screen = movie_screen
        self.promo_id = promo_id

    def __repr__(self) -> str:
        """Str representation of the seat reservation model."""
        return (f"<SeatReservationModel seat={self.seat_id},"
                "reservation={self.reservation_id},"
                "movie_screen={self.movie_screen_id}>")

    def json(self) -> dict:
        """JSON representation of the seat reservation model."""
        return {
            "id": self.id, "price": self.price,
            "created_at": deserialize_datetime(self.created_at),
            "updated_at": deserialize_datetime(self.updated_at),
            "seat_id": self.seat_id, "reservation_id": self.reservation_id,
            "movie_screen_id": self.movie_screen_id
        }

    @classmethod
    def _is_valid_representation(cls, *, data: dict) -> bool:
        """Check validity of dictionary keys as representation of this model."""
        base = {"seat_id", "movie_screen_id"}
        return True if set(base) == set(data) else False

    @classmethod
    def find(cls, *, data: dict) -> "SeatReservationModel":
        """Docstring here."""
        if not cls._is_valid_representation(data=data):
            return {"message": "Invalid request."}, 400
        try:
            temp_reservation = cls.query.filter_by(**data).first()
        except Exception as e:
            return {"message": "An unknown error occured"}, 500
        if temp_reservation:
            temp_reservation = simplejson.dumps(temp_reservation.json())
            temp_reservation = simplejson.loads(temp_reservation.json())
        return temp_reservation

    def save_to_db(self):
        """Docstring here."""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            return {"message": "An unknown error occured"}, 500

    @classmethod
    def save_all(cls, *, seat_reservations: list):
        """Docstring here."""
        try:
            db.session.add_all(seat_reservations)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            return {"message": "An unknown error occured"}, 500


class SeatReservationListModel(SeatReservationModel):
    """Docstring here."""

    @classmethod
    def find_all(cls) -> list:
        """Query all of the seat_reservation table rows."""
        return cls.query.all()

    @classmethod
    def which_occupied(cls, *, seat_id_list: list, movie_screen: object) -> list:
        """Query the database for occupied seats in a given movie_screen."""
        try:
            seats = (cls.query.join(MovieScreenModel)
                        .filter(movie_screen.id == cls.movie_screen_id)
                        .filter(cls.seat_id.in_(seat_id_list))
                        .with_entities("seat_reservation.movie_screen_id")
                        .all())
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            return {"message": "An unknown error occured"}, 500
        return list(*zip(*seats))
