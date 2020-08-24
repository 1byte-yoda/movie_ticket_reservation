import json
import ast

from marshmallow import Schema, fields, post_load, pre_dump, post_dump

from .cinema import CinemaSchema


class MovieSchema(Schema):
    """Use to represent the MovieModel as JSON data."""

    id = fields.Int()
    name = fields.Str(required=True)
    cinema = fields.Nested(CinemaSchema, dump_only=True)
    description = fields.Str(required=True)
    duration = fields.Integer(required=True)
    rating = fields.Float(allow_none=True)
    release_date = fields.Date(required=True, format="%Y-%m-%d")
    price = fields.Float()
    company = fields.Str()
    genre = fields.Str()
    casts = fields.List(fields.Str())
    youtube = fields.Str()

    @post_load
    def serialize_datetime(self, in_data, **kwargs):
        in_data["release_date"] = in_data["release_date"].strftime("%Y-%m-%d")
        in_data["duration"] = in_data["duration"].strftime("%H:%M:%S")
        return in_data

    # @pre_dump
    # def deserialize_json(self, in_data, **kwargs):
    #     pass
    #     # if in_data["casts"]:
    #     #     in_data["casts"] = json.loads(in_data["casts"])["casts"]