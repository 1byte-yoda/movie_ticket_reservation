from marshmallow import Schema, fields

from ..models.account import AccountModel


class AccountSchema(Schema):
    class Meta:
        load_only = ("password",)

    id = fields.Int()
    email = fields.Email()
    password = fields.Str()
    type = fields.Str()
