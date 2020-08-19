from datetime import datetime, time

from marshmallow import (
    Schema,
    fields,
    validates_schema,
    ValidationError,
    post_load,
    pre_dump
)

from .response_messages import END_TIME_GT_PLAY_TIME


class ScheduleSchema(Schema):

    id = fields.Int()
    play_datetime = fields.DateTime(required=True, format="%Y-%m-%d %H:%M:%S")
    end_datetime = fields.DateTime(required=True, format="%Y-%m-%d %H:%M:%S")

    @post_load
    def load_serialize_time(self, in_data, **kwargs):
        in_data["play_datetime"] = in_data["play_datetime"].strftime("%Y-%m-%d %H:%M:%S")
        in_data["end_datetime"] = in_data["end_datetime"].strftime("%Y-%m-%d %H:%M:%S")
        return in_data

    # @pre_dump
    # def dump_serialize_time(self, in_data, **kwargs):
    #     if isinstance(in_data["play_datetime"], str):
    #         in_data["play_datetime"] = datetime.strptime(in_data["play_datetime"]).time()
    #     if isinstance(in_data["end_datetime"], str):
    #         in_data["end_datetime"] = (datetime.min + in_data["end_datetime"]).time()
    #     return in_data

    @validates_schema
    def validate_time(self, in_data, **kwargs):
        errors = {}
        if in_data["play_datetime"] >= in_data["end_datetime"]:
            errors["end_datetime"] = END_TIME_GT_PLAY_TIME
        if errors:
            raise ValidationError(errors)
