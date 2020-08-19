from datetime import datetime, date

from marshmallow import Schema, fields, validates_schema, ValidationError

from .movie import MovieSchema
from .screen import ScreenSchema
from .schedule import ScheduleSchema
from .response_messages import (
    SCHEDULE_GT_RELEASE_DATE,
    WRONG_TIME_DURATIONS,
    OVERLAP_SCHEDULES
)


class MovieScreenSchema(Schema):
    id = fields.Int()
    price = fields.Float(required=True)
    movie = fields.Nested(MovieSchema, required=True)
    screen = fields.Nested(ScreenSchema)
    schedule = fields.Nested(ScheduleSchema, dump_only=True)
    schedules = fields.List(
        fields.Nested(ScheduleSchema, required=True), required=True
    )

    @staticmethod
    def sched_a_larger_than_b(sched_a: dict, sched_b: dict) -> bool:
        return (sched_a["play_datetime"] > sched_b["play_datetime"] and
                sched_a["play_datetime"] > sched_b["end_datetime"])

    @staticmethod
    def sched_a_smaller_than_b(sched_a: dict, sched_b: dict) -> bool:
        return (sched_a["play_datetime"] < sched_b["play_datetime"] and
                sched_a["play_datetime"] < sched_b["end_datetime"])

    @classmethod
    def check_conflict_schedules(cls, _schedules: list) -> list:
        _conflicting_schedules = list()
        for i, sched_a in enumerate(_schedules):
            for j, sched_b in enumerate(_schedules):
                if (i != j) and not (
                    cls.sched_a_larger_than_b(sched_a, sched_b) or
                    cls.sched_a_smaller_than_b(sched_a, sched_b)
                ):
                    _new_conflict = {
                        f"schedule_{i}": sched_a,
                        f"schedule_{j}": sched_b
                    }
                    if _new_conflict not in _conflicting_schedules:
                        _conflicting_schedules.append(_new_conflict)
        return _conflicting_schedules

    @classmethod
    def check_schedule_durations(cls, base_time: str, _schedules: list) -> list:
        _wrong_durations = list()
        date_time_format = "%Y-%m-%d %H:%M:%S"
        _time_format = "%H:%M:%S"
        base_time = datetime.strptime(base_time, _time_format).time()
        for sched in _schedules:
            _play_datetime = datetime.strptime(
                sched["play_datetime"], date_time_format
            ).time()
            _end_datetime = datetime.strptime(
                sched["end_datetime"], date_time_format
            ).time()
            _duration = (
                datetime.combine(date.min, _end_datetime) -
                datetime.combine(date.min, _play_datetime)
            )
            _duration = (datetime.min + _duration).time()
            if _duration < base_time:
                _wrong_durations.append(sched)
        return _wrong_durations

    @classmethod
    def check_schedule_within_release_date(cls, release_date: datetime, schedules: list):
        date_time_format = "%Y-%m-%d %H:%M:%S"
        date_format = "%Y-%m-%d"
        release_date = datetime.strptime(release_date, date_format).date()
        invalid_schedules = []
        for schedule in schedules:
            play_datetime = datetime.strptime(
                schedule.get("play_datetime"), date_time_format
            ).date()
            end_datetime = datetime.strptime(
                schedule.get("end_datetime"), date_time_format
            ).date()
            if play_datetime < release_date or end_datetime < release_date:
                invalid_schedules.append(schedule)
        return invalid_schedules

    @validates_schema
    def validate_schedules(self, in_data, **kwargs):
        errors = {}
        _schedules = in_data.get("schedules", None)
        _movie = in_data.get("movie", None)

        if _schedules:
            conflicting_schedules = self.check_conflict_schedules(
                _schedules=_schedules
            )
            if conflicting_schedules:
                if not errors.get("schedules"):
                    errors["schedules"] = []
                errors["schedules"].append({
                    "error": OVERLAP_SCHEDULES,
                    "payload": conflicting_schedules
                })
            if _movie:
                _base_time = _movie["duration"]
                wrong_schedules = self.check_schedule_durations(
                    base_time=_base_time, _schedules=_schedules
                )
                if wrong_schedules:
                    if not errors.get("schedules"):
                        errors["schedules"] = []
                    errors["schedules"].append({
                        "error": WRONG_TIME_DURATIONS.format(_base_time),
                        "payload": wrong_schedules
                    })
                outof_release_list = self.check_schedule_within_release_date(
                    release_date=_movie["release_date"], schedules=_schedules
                )
                if outof_release_list:
                    if not errors.get("schedules"):
                        errors["schedules"] = []
                    errors["schedules"].append({
                        "error": SCHEDULE_GT_RELEASE_DATE,
                        "payload": outof_release_list
                    })
        if errors:
            raise ValidationError(errors)
