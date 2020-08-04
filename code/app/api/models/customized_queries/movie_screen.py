SELECT_NOW_SHOWING_QUERY = (
    "SELECT ms.id "
    "FROM movie_screen ms "
    "JOIN schedule sch ON sch.id = ms.schedule_id "
    "AND sch.play_datetime >= DATE(NOW()) "
    "JOIN movie AS m ON m.id = ms.movie_id "
    "JOIN screen AS s ON s.id = ms.screen_id "
    "JOIN cinema c ON c.id = s.cinema_id "
)