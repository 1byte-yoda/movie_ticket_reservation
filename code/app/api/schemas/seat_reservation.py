import simplejson
from marshmallow import Schema, fields

from .reservation import ReservationSchema
from .cinema import CinemaSchema
from .screen import ScreenSchema
from .seat import SeatSchema
from .movie import MovieSchema
from .schedule import ScheduleSchema


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
    screen = fields.Nested(ScreenSchema)
    seat = fields.Nested(SeatSchema)
    movie = fields.Nested(MovieSchema)
    schedule = fields.Nested(ScheduleSchema)
