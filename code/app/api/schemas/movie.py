from marshmallow import Schema, fields


class MovieSchema(Schema):
    """Use to represent the MovieModel as JSON data."""

    id = fields.Int()
    name = fields.Str()
    play_datetime = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    end_datetime = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
