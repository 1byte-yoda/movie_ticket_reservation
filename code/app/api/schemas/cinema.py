from marshmallow import Schema, fields

from .location import LocationSchema


class CinemaSchema(Schema):
    """Use to represent the CinemaModel as JSON data."""

    id = fields.Int()
    name = fields.Str()
    open_time = fields.Time()
    close_time = fields.Time()
    location = fields.Nested(LocationSchema)