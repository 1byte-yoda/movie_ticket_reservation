from marshmallow import Schema, fields

from .account import AccountSchema
from .cinema import CinemaSchema
from .location import LocationSchema


class UserSchema(Schema):

    id = fields.Int()
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    contact_no = fields.Str(required=True)
    location = fields.Nested(LocationSchema, required=True)
    account = fields.Nested(AccountSchema, required=True)
    cinema = fields.Nested(CinemaSchema, required=True)
