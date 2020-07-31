from datetime import datetime

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

    def __init__(self, id=None, price=None, seat_id=None, reservation=None,
                 movie_screen=None, promo=None):
        """Docstring here."""
        self.id = id
        self.price = price
        self.created_at = None
        self.updated_at = None
        self.seat_id = seat_id
        self.reservation = reservation
        self.movie_screen = movie_screen
        self.promo_id = promo

    def __repr__(self) -> str:
        """Str representation of the seat reservation model."""
        return ("<SeatReservationModel {}, {}, {}>".format(self.seat_id,
                self.reservation, self.movie_screen))

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
        temp_reservation = cls.query.filter_by(**data).first()
        return temp_reservation

    def save_to_db(self):
        """Docstring here."""
        db.session.add(self)
        db.session.commit()

    @classmethod
    def save_all(cls, *, seat_reservations: list):
        """Docstring here."""
        db.session.add_all(seat_reservations)
        db.session.commit()


class SeatReservationListModel(SeatReservationModel):
    """Docstring here."""

    @classmethod
    def find_taken_seats(cls, *, movie_screen_id: int, seat_id_list: list) -> list:
        # https://docs.sqlalchemy.org/en/13/orm/tutorial.html#querying
        return cls.query.filter_by(movie_screen_id=movie_screen_id)\
                        .filter(cls.seat_id.in_(seat_id_list)).all()

    @classmethod
    def find_all(cls) -> list:
        return cls.query.all()
