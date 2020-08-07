SELECT_CONFLICT_SCHEDULE_QUERY = (
    "SELECT schedule.id, schedule.screen_id, schedule.play_time, schedule.end_time "
    "FROM schedule "
    "JOIN master_schedule AS ms ON ms.id = schedule.master_schedule_id "
    "WHERE ((('{launch_date}' BETWEEN launch_date AND phase_out_date) "
    "OR ('{phase_out_date}' BETWEEN launch_date AND phase_out_date)) "
    "AND (('{play_time}' BETWEEN play_time AND end_time) "
    "OR ('{end_time}' BETWEEN play_time AND end_time))) "
    "AND schedule.screen_id={screen_id}"
)
