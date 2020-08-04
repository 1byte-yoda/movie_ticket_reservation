from marshmallow import Schema, fields


class CinemaSchema(Schema):
    """Use to represent the CinemaModel as JSON data."""

    id = fields.Int()
    name = fields.Str()
