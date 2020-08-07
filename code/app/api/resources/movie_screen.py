from flask_restful import Resource, request
from flask_jwt_extended import get_current_user, get_jwt_claims, jwt_required
from werkzeug.security import safe_str_cmp

from db import db
from .response_messages import (
    INVALID_REQUEST_ADMIN_MESSAGE_401,
    SCREEN_NOT_FOUND_404,
    SCHEDULE_CONFLICT_400,
    MOVIE_SCREEN_ADDED_201,
    UNKNOWN_ERROR_MESSAGE_500
)
from ..models.screen import ScreenModel
from ..models.movie_screen import MovieScreenModel
from ..models.movie import MovieModel
from ..models.master_schedule import MasterScheduleModel
from ..models.schedule import ScheduleModel
from ..schemas.movie_screen import MovieScreenSchema


class MovieScreenResource(Resource):
    """Contains the REST API paths for Movie-Screen transactions.

    Description
    -----------
    Movie-Screen interacts with the movie_screen table which contains
    all the product posts of a Cinema Manager.
    """

    ms_schema = MovieScreenSchema()

    @jwt_required
    def post(cls, cinema_id: int, screen_id: int):
        """POST method that handles the creation of a movie product.

        path : /api/cinema/<int:cinema_id>/screen/<int:screen_id>/movie/add

        Description
        -----------
        This will create a new entry in the movie_screen, movie,
        schedule, and master_schedule table.
        """
        claims = get_jwt_claims()
        if claims:
            if safe_str_cmp(claims.get("type"), "admin"):
                user = get_current_user()
                if user.cinema_id != cinema_id:
                    return ({"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401)

                screen = ScreenModel.find_by_id_cinema(
                    id=screen_id, cinema_id=cinema_id
                )
                if not screen:
                    return ({"message": SCREEN_NOT_FOUND_404}, 404)
                movie_screen_data = cls.ms_schema.load(request.get_json())
                movie_data = movie_screen_data["movie"]
                schedules_data = movie_screen_data["schedules"]
                master_schedule_data = movie_screen_data["master_schedule"]

                movie = MovieModel.find_by_name(name=movie_data["name"])
                if not movie:
                    movie = MovieModel(**movie_data)

                master_schedule = MasterScheduleModel.find_by_dates(
                    dates=master_schedule_data
                )
                if not master_schedule:
                    master_schedule = MasterScheduleModel(**master_schedule_data)

                schedules = ScheduleModel.find_conflicts(
                    **master_schedule_data, scheds=schedules_data, screen_id=screen_id
                )
                schedules = list(sched for sched in schedules)
                scheds_zip = zip(schedules, schedules_data)
                conflicts = [inp_sch for db_sch, inp_sch in scheds_zip if db_sch is not None]
                if conflicts:
                    return (
                        {
                            "message": SCHEDULE_CONFLICT_400,
                            "payload": conflicts
                        }, 400
                    )
                movie_screens = []
                for sched in schedules_data:
                    schedule = (
                        ScheduleModel(
                            screen=screen, master_schedule=master_schedule, **sched
                        )
                    )
                    movie_screens.append(
                        MovieScreenModel(movie=movie, screen=screen, schedule=schedule)
                    )
                try:
                    MovieScreenModel.save_all(movie_screens)
                except Exception as err:
                    print(err)
                    db.session.rollback()
                    db.session.flush()
                    return ({"message": UNKNOWN_ERROR_MESSAGE_500}, 500)
                return ({"message": MOVIE_SCREEN_ADDED_201}, 201)
        return ({"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401)
