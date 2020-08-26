from datetime import datetime

from db import db
from .seat import SeatModel
from .reservation import ReservationModel
from .movie_screen import MovieScreenModel


class SeatReservationModel(db.Model):
    """Docstring here."""

    __tablename__ = "seat_reservation"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float(6, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    seat_id = db.Column(db.Integer, db.ForeignKey("seat.id"), nullable=False)
    seats = db.relationship(SeatModel, backref="seats", lazy=True)
    reservation_id = db.Column(
        db.Integer, db.ForeignKey("reservation.id"), nullable=False
    )
    reservation = db.relationship(ReservationModel, backref="reservation", lazy=True)
    movie_screen_id = db.Column(
        db.Integer, db.ForeignKey("movie_screen.id"), nullable=False
    )
    movie_screen = db.relationship(MovieScreenModel, backref="movie_screen", lazy=True)
    promo_id = db.Column(db.Integer)
    db.UniqueConstraint(seat_id, reservation_id, movie_screen_id,)

    def json(self):
        """JSON represation of SeatReservationModel."""
        return {
            "id": self.id,
            "reservation": self.reservation.json(),
            "cinema": self.movie_screen.screen.cinema.json(),
            "screen": self.movie_screen.json(),
            "seat": self.seats.json()
        }

    @classmethod
    def find(cls, *, data: dict) -> "SeatReservationModel":
        """Docstring here."""
        temp_reservation = cls.query.filter_by(**data).all()
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
    def find_all(cls) -> list:
        """Query all of the seat_reservation table rows."""
        return cls.query.all()

    @classmethod
    def which_occupied(cls, *, seat_id_list: list, movie_screen: object) -> list:
        """Query the database for occupied seats in a given movie_screen."""
        seats = (
            cls.query.join(MovieScreenModel)
            .filter(movie_screen.id == cls.movie_screen_id)
            .filter(cls.seat_id.in_(seat_id_list))
            .with_entities("seat_reservation.seat_id")
            .all()
        )
        return list(*zip(*seats))
