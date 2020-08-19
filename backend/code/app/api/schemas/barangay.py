from marshmallow import Schema, fields

from .city import CitySchema


class BarangaySchema(Schema):
    """Use to represent the BarangayModel as JSON data."""

    id = fields.Int()
    name = fields.Str(required=True)
    city = fields.Nested(CitySchema)
