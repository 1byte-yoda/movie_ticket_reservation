from datetime import datetime

from db import db
from .seat import SeatModel
from .reservation import ReservationModel
from .movie_screen import MovieScreenModel
from .response_messages import UNKNOWN_ERROR_MESSAGE_500


class SeatReservationModel(db.Model):
    """Docstring here."""

    __tablename__ = "seat_reservation"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float(6, 2))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    seat_id = db.Column(db.Integer, db.ForeignKey("seat.id"), nullable=False)
    seats = db.relationship(SeatModel, backref="seats")
    reservation_id = db.Column(
        db.Integer,
        db.ForeignKey("reservation.id"),
        nullable=False
    )
    reservation = db.relationship(ReservationModel, backref="reservation")
    movie_screen_id = db.Column(
        db.Integer,
        db.ForeignKey("movie_screen.id"),
        nullable=False
    )
    movie_screen = db.relationship(MovieScreenModel, backref="movie_screen")
    promo_id = db.Column(db.Integer)

    def __repr__(self) -> str:
        """Str representation of the seat reservation model."""
        return (
            f"<SeatReservationModel seat={self.seat_id},"
            "reservation={self.reservation_id},"
            "movie_screen={self.movie_screen_id}>"
        )

    @classmethod
    def find(cls, *, data: dict) -> "SeatReservationModel":
        """Docstring here."""
        try:
            temp_reservation = cls.query.filter_by(**data).first()
        except:
            return ({"message": UNKNOWN_ERROR_MESSAGE_500}, 500)
        return temp_reservation

    def save_to_db(self):
        """Docstring here."""
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            db.session.flush()
            return ({"message": UNKNOWN_ERROR_MESSAGE_500}, 500)

    @classmethod
    def save_all(cls, *, seat_reservations: list):
        """Docstring here."""
        try:
            db.session.add_all(seat_reservations)
            db.session.commit()
        except:
            db.session.rollback()
            db.session.flush()
            return {"message": UNKNOWN_ERROR_MESSAGE_500}, 500


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
            seats = (
                cls.query.join(MovieScreenModel)
                .filter(movie_screen.id == cls.movie_screen_id)
                .filter(cls.seat_id.in_(seat_id_list))
                .with_entities("seat_reservation.movie_screen_id")
                .all()
            )
        except:
            db.session.rollback()
            db.session.flush()
            return {"message": UNKNOWN_ERROR_MESSAGE_500}, 500
        return list(*zip(*seats))
