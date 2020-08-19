from marshmallow import Schema, fields


class CinemaSchema(Schema):
    """Use to represent the CinemaModel as JSON data."""

    id = fields.Int()
    name = fields.Str(required=True)
    open_time = fields.Time(required=True)
    close_time = fields.Time(required=True)
