from marshmallow import Schema, fields

from .province import ProvinceSchema


class CitySchema(Schema):
    """Use to represent the CityModel as JSON data."""

    id = fields.Int()
    name = fields.Str()
    province = fields.Nested(ProvinceSchema)
    longitude = fields.Str()
    latitude = fields.Str()
