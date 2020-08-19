from marshmallow import Schema, fields, validates_schema, ValidationError, post_load

from .response_messages import PHASE_OUT_GT_LAUNCH_DATE


class MasterScheduleSchema(Schema):
    id = fields.Int()
    launch_date = fields.Date(required=True, format="%Y-%m-%d")
    phase_out_date = fields.Date(required=True, format="%Y-%m-%d")

    @validates_schema
    def validate_schedule_date(self, in_data, **kwargs):
        errors = {}
        if in_data["launch_date"] > in_data["phase_out_date"]:
            errors["phase_out_date"] = PHASE_OUT_GT_LAUNCH_DATE
        if errors:
            raise ValidationError(errors)

    @post_load
    def serialize_datetime(self, in_data, **kwargs):
        in_data["launch_date"] = in_data["launch_date"].strftime("%Y-%m-%d")
        in_data["phase_out_date"] = in_data["phase_out_date"].strftime("%Y-%m-%d")
        return in_data
