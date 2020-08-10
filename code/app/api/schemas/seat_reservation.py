from marshmallow import Schema, fields

from .reservation import ReservationSchema
from .cinema import CinemaSchema
from .movie_screen import MovieScreenSchema
from .seat import SeatSchema


class SeatReservationPostSchema(Schema):
    """Use only for post requests or insertion of a seat reservation in the DB."""

    seat_id_list = fields.List(fields.Int(), required=True)
    movie_id = fields.Int(required=True)
    screen_id = fields.Int(required=True)
    schedule_id = fields.Int(required=True)


class SeatReservationSchema(Schema):
    """Use to represent the SeatReservationModel as JSON data."""

    id = fields.Int(required=True)
    price = fields.Float()
    reservation = fields.Nested(ReservationSchema)
    cinema = fields.Nested(CinemaSchema)
    movie_screen = fields.Nested(MovieScreenSchema)
    seats = fields.Nested(SeatSchema)
