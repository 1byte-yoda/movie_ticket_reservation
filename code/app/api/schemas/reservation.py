from marshmallow import Schema, fields

from .account import AccountSchema
from .payment import PaymentSchema


class ReservationSchema(Schema):
    """Use to represent the ReservationModel as JSON data."""

    id = fields.Int()
    head_count = fields.Int()
    reserve_datetime = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    account = fields.Nested(AccountSchema)
    payment = fields.Nested(PaymentSchema)
