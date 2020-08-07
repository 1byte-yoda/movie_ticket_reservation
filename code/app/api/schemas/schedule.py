from datetime import datetime

from marshmallow import (
    Schema,
    fields,
    validates_schema,
    ValidationError,
    post_load,
    pre_dump
)

from .master_schedule import MasterScheduleSchema


class ScheduleSchema(Schema):

    id = fields.Int()
    play_time = fields.Time(required=True, format="%H:%M:%S")
    end_time = fields.Time(required=True, format="%H:%M:%S")
    master_schedule = fields.Nested(MasterScheduleSchema, required=True, dump_only=True)

    @post_load
    def load_serialize_time(self, in_data, **kwargs):
        in_data["play_time"] = in_data["play_time"].strftime("%H:%M:%S")
        in_data["end_time"] = in_data["end_time"].strftime("%H:%M:%S")
        return in_data

    @pre_dump
    def dump_serialize_time(self, in_data, **kwargs):
        in_data["play_time"] = (datetime.min + in_data["play_time"]).time()
        in_data["end_time"] = (datetime.min + in_data["end_time"]).time()
        return in_data

    @validates_schema
    def validate_time(self, in_data, **kwargs):
        errors = {}
        if in_data["play_time"] >= in_data["end_time"]:
            errors["end_time"] = "end_time must be later than play_time."
        if errors:
            raise ValidationError(errors)
