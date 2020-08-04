from marshmallow import Schema, fields


class SeatSchema(Schema):
    """Use to represent the SeatModel as JSON data."""

    id = fields.Int()
