import simplejson
from marshmallow import Schema, fields

from ...serializer import ma
from ..models.seat_reservation import SeatReservationModel


class SeatReservationPostSchema(Schema):
    """Use only for post requests or insertion of a seat reservation in the DB."""

    seat_id_list = fields.List(fields.Int(), required=True)
    movie_id = fields.Int(required=True)
    screen_id = fields.Int(required=True)
    schedule_id = fields.Int(required=True)


class SeatReservationSchema(ma.SQLAlchemyAutoSchema):
    """Use to represent the SeatReservationModel as JSON data."""

    class Meta:
        model = SeatReservationModel
        json_module = simplejson
        load_only = ("id", )
        dump_only = ("movie_screen_id", "reservation_id", "seat_id")
        include_fk = True
