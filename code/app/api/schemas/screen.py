from marshmallow import Schema, fields


class ScreenSchema(Schema):
    """Use to represent the ReservationModel as JSON data."""

    id = fields.Int()
