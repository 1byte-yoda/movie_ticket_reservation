from marshmallow import Schema, fields, validates_schema, ValidationError, post_load


class MasterScheduleSchema(Schema):
    id = fields.Int()
    launch_date = fields.Date(required=True, format="%Y-%m-%d")
    phase_out_date = fields.Date(required=True, format="%Y-%m-%d")

    @validates_schema
    def validate_schedule_date(self, in_data, **kwargs):
        errors = {}
        if in_data["launch_date"] > in_data["phase_out_date"]:
            errors["phase_out_date"] = "phase_out_date must be later than launch_date."
        if errors:
            raise ValidationError(errors)

    @post_load
    def serialize_datetime(self, in_data, **kwargs):
        in_data["launch_date"] = in_data["launch_date"].strftime("%Y-%m-%d")
        in_data["phase_out_date"] = in_data["phase_out_date"].strftime("%Y-%m-%d")
        return in_data
