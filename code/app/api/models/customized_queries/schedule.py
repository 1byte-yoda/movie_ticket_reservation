SELECT_CONFLICT_SCHEDULE_QUERY = (
    "SELECT schedule.id, schedule.screen_id, schedule.play_datetime, schedule.end_datetime "
    "FROM schedule "
    "WHERE (('{play_datetime}' BETWEEN play_datetime AND end_datetime) "
    "OR ('{end_datetime}' BETWEEN play_datetime AND end_datetime)) "
    "AND schedule.screen_id={screen_id}"
)
