from marshmallow import Schema, fields

from .city import CitySchema


class BarangaySchema(Schema):
    """Use to represent the BarangayModel as JSON data."""

    class Meta:
        dump_only = ("name",)

    id = fields.Int(required=True)
    name = fields.Str()
    city = fields.Nested(CitySchema)
