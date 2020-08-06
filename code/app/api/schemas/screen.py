from marshmallow import Schema, fields


class ScreenSchema(Schema):
    """Use to represent the ScreenModel as JSON data."""

    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    capacity = fields.Int(required=True)
    cinema_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(format="%Y-%m-%d %H:%M:%S", dump_only=True)
    updated_at = fields.DateTime(format="%Y-%m-%d %H:%M:%S", dump_only=True)
