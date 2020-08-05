from marshmallow import Schema, fields


class AccountSchema(Schema):
    class Meta:
        load_only = ("password",)

    id = fields.Int()
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    type = fields.Str(required=True)
