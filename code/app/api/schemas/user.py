from marshmallow import Schema, fields

from .account import AccountSchema


class UserSchema(Schema):

    id = fields.Int()
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    contact_no = fields.Str(required=True)
    account = fields.Nested(AccountSchema, required=True)
    cinema_id = fields.Int()
