from marshmallow import Schema, fields


class ScheduleSchema(Schema):
    id = fields.Int()
    play_datetime = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    end_datetime = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
