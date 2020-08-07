from marshmallow import Schema, fields, validates_schema, ValidationError

from .movie import MovieSchema
from .screen import ScreenSchema
from .schedule import ScheduleSchema
from .master_schedule import MasterScheduleSchema


class MovieScreenSchema(Schema):

    id = fields.Int()
    price = fields.Int(required=True)
    movie = fields.Nested(MovieSchema, required=True)
    screen = fields.Nested(ScreenSchema)
    schedules = fields.List(
        fields.Nested(ScheduleSchema, required=True), required=True
    )
    master_schedule = fields.Nested(MasterScheduleSchema, required=True)

    @staticmethod
    def sched_a_larger_than_b(sched_a, sched_b):
        return (sched_a["play_time"] >= sched_b["play_time"] and
                sched_a["play_time"] >= sched_b["end_time"])

    @staticmethod
    def sched_a_smaller_than_b(sched_a, sched_b):
        return (sched_a["play_time"] <= sched_b["play_time"] and
                sched_a["play_time"] <= sched_b["end_time"])

    @validates_schema
    def validate_schedules(self, in_data, **kwargs):
        errors = {}
        errors["conflicting_schedules"] = list()
        _schedules = in_data["schedules"]
        for i, sched_a in enumerate(_schedules):
            for j, sched_b in enumerate(_schedules):
                if (i != j) and not (
                    self.sched_a_larger_than_b(sched_a, sched_b) or
                    self.sched_a_smaller_than_b(sched_a, sched_b)
                ):
                    errors["conflicting_schedules"].append({
                        f"schedule_{i}": sched_a,
                        f"schedule_{j}": sched_b
                    })
        if errors["conflicting_schedules"]:
            raise ValidationError(errors)
