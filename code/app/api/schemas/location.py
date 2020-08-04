from marshmallow import Schema, fields


class LocationSchema(Schema):
    """Use to represent the LocationModel as JSON data."""

    id = fields.Int(),
    province = fields.Str()
    city = fields.Str()
    barangay = fields.Str()
    longitude = fields.Str()
    latitude = fields.Str()
