from marshmallow import Schema, fields

from .barangay import BarangaySchema


class LocationSchema(Schema):
    """Use to represent the LocationModel as JSON data."""

    id = fields.Int()
    barangay = fields.Nested(BarangaySchema, required=True)
    longitude = fields.String(required=False)
    latitude = fields.String(required=False)
