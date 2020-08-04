from marshmallow import Schema, fields


class PaymentSchema(Schema):
    """Use to represent the PaymentModel as JSON data."""

    id = fields.Int()
    type = fields.Str()
