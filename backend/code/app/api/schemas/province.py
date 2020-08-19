from marshmallow import Schema, fields


class ProvinceSchema(Schema):
    """Use to represent the ProvinceModel as JSON data."""

    id = fields.Int(),
    name = fields.Str()
