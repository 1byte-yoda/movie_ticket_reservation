from datetime import datetime, date

from marshmallow import Schema, fields, validates_schema, ValidationError

from .movie import MovieSchema
from .screen import ScreenSchema
from .schedule import ScheduleSchema
from .master_schedule import MasterScheduleSchema
from .response_messages import LAUNCH_DATE_GT_RELEASE_DATE, WRONG_TIME_DURATIONS


class MovieScreenSchema(Schema):
    id = fields.Int()
    price = fields.Float(required=True)
    movie = fields.Nested(MovieSchema, required=True)
    screen = fields.Nested(ScreenSchema)
    schedule = fields.Nested(ScheduleSchema, dump_only=True)
    schedules = fields.List(
        fields.Nested(ScheduleSchema, required=True), required=True
    )
    master_schedule = fields.Nested(MasterScheduleSchema, required=True)

    @staticmethod
    def sched_a_larger_than_b(sched_a: dict, sched_b: dict) -> bool:
        return (sched_a["play_time"] >= sched_b["play_time"] and
                sched_a["play_time"] >= sched_b["end_time"])

    @staticmethod
    def sched_a_smaller_than_b(sched_a: dict, sched_b: dict) -> bool:
        return (sched_a["play_time"] <= sched_b["play_time"] and
                sched_a["play_time"] <= sched_b["end_time"])

    @classmethod
    def check_conflict_schedules(cls, _schedules: list) -> list:
        _conflicting_schedules = list()
        for i, sched_a in enumerate(_schedules):
            for j, sched_b in enumerate(_schedules):
                if (i != j) and not (
                    cls.sched_a_larger_than_b(sched_a, sched_b) or
                    cls.sched_a_smaller_than_b(sched_a, sched_b)
                ):
                    _conflicting_schedules.append({
                        f"schedule_{i}": sched_a,
                        f"schedule_{j}": sched_b
                    })
        return _conflicting_schedules

    @classmethod
    def check_schedule_durations(cls, base_time: str, _schedules: list) -> list:
        _wrong_durations = list()
        _time_format = "%H:%M:%S"
        base_time = datetime.strptime(base_time, _time_format).time()
        for sched in _schedules:
            _play_time = datetime.strptime(sched["play_time"], _time_format).time()
            _end_time = datetime.strptime(sched["end_time"], _time_format).time()
            _duration = (
                datetime.combine(date.min, _end_time) - 
                datetime.combine(date.min, _play_time)
            )
            _duration = (datetime.min + _duration).time()
            if _duration < base_time:
                _wrong_durations.append(sched)
        return _wrong_durations

    @validates_schema
    def validate_schedules(self, in_data, **kwargs):
        errors = {}
        _schedules = in_data.get("schedules", None)
        _movie = in_data.get("movie", None)
        _master_schedule = in_data.get("master_schedule", None)

        if _schedules:
            conflicting_schedules = self.check_conflict_schedules(
                _schedules=_schedules
            )
            if conflicting_schedules:
                errors["conflicting_schedules"] = conflicting_schedules

        if _master_schedule and _movie:
            if _master_schedule["launch_date"] < _movie["release_date"]:
                errors["launch_date"] = LAUNCH_DATE_GT_RELEASE_DATE

        if _schedules and _movie:
            _base_time = _movie["duration"]
            wrong_schedules = self.check_schedule_durations(
                base_time=_base_time, _schedules=_schedules
            )
            if wrong_schedules:
                errors["schedules"] = {
                    "error": WRONG_TIME_DURATIONS.format(_base_time),
                    "payload": wrong_schedules
                }
        if errors:
            raise ValidationError(errors)
