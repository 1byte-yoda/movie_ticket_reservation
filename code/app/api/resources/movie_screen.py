from flask_restful import Resource, request
from flask_jwt_extended import get_current_user, get_jwt_claims, jwt_required
from werkzeug.security import safe_str_cmp

from db import db
from .response_messages import (
    INVALID_REQUEST_ADMIN_MESSAGE_401,
    SCREEN_NOT_FOUND_404,
    SCHEDULE_CONFLICT_400,
    MOVIE_SCREENS_ADDED_201,
    MOVIE_SCREEN_NOT_FOUND_MESSAGE_404,
    MOVIE_SCREEN_DELETED_201,
    MOVIE_NAME_EXISTS_400,
    UNKNOWN_ERROR_MESSAGE_500
)
from ..models.screen import ScreenModel
from ..models.movie_screen import MovieScreenModel, MovieScreenListModel
from ..models.movie import MovieModel
from ..models.master_schedule import MasterScheduleModel
from ..models.schedule import ScheduleModel
from ..schemas.movie_screen import MovieScreenSchema


class MovieScreenResource(Resource):
    """Contains the REST API methods for Movie-Screen transactions.

    Description
    -----------
    Movie-Screen interacts with the movie_screen table which contains
    all the product posts of a Cinema Manager.
    """

    ms_schema = MovieScreenSchema()

    @classmethod
    @jwt_required
    def get(cls, cinema_id: int, screen_id: int, movie_screen_id: int):
        """GET method that pulls a particular movie product.

        path : /api/cinema/<int:cinema_id>/screen/<int:screen_id>/movie-screen/<int:movie_screen_id>

        Description
        -----------
        This will parse a movie-screen for a given screen
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
                movie_screen = MovieScreenModel.find_movie_screen(
                    id=movie_screen_id, screen_id=screen_id
                )
                if not movie_screen:
                    return ({"message": MOVIE_SCREEN_NOT_FOUND_MESSAGE_404}, 404)
                return ({"payload": cls.ms_schema.dump(movie_screen.json())}, 200)
        return ({"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401)

    @jwt_required
    def post(cls, cinema_id: int, screen_id: int):
        """POST method that handles the creation of a movie product.

        path : /api/cinema/<int:cinema_id>/screen/<int:screen_id>/movie-screen/add

        Description
        -----------
        This will create a new entry in the ff. tables: movie_screen, movie,
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
                price = movie_screen_data["price"]
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
                        MovieScreenModel(
                            movie=movie, screen=screen, schedule=schedule, price=price)
                    )
                try:
                    MovieScreenListModel.save_all(movie_screens)
                except:
                    db.session.rollback()
                    db.session.flush()
                    return ({"message": UNKNOWN_ERROR_MESSAGE_500}, 500)
                return ({"message": MOVIE_SCREENS_ADDED_201}, 201)
        return ({"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401)

    @classmethod
    @jwt_required
    def put(cls, cinema_id: int, screen_id: int, movie_screen_id: int):
        """PUT method that modifies a particular movie-screen.

        path : /api/cinema/<int:cinema_id>/screen/<int:screen_id>/movie-screen/<int:movie_screen_id>/edit

        Description
        -----------
        This will update a movie-screen product in the database.
        """
        claims = get_jwt_claims()
        if claims:
            if not safe_str_cmp(claims.get("type"), "admin"):
                return ({"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401)
            user = get_current_user()
            if user.cinema_id != cinema_id:
                return ({"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401)
            screen = ScreenModel.find_by_id_cinema(
                id=screen_id, cinema_id=cinema_id
            )
            if not screen:
                return ({"message": SCREEN_NOT_FOUND_404}, 404)
            movie_screen = MovieScreenModel.find_movie_screen(
                id=movie_screen_id, screen_id=screen_id
            )
            if not movie_screen:
                return ({"message": MOVIE_SCREEN_NOT_FOUND_MESSAGE_404}, 404)
            movie_screen_data = cls.ms_schema.load(request.get_json())
            movie_data = movie_screen_data["movie"]
            schedules_data = movie_screen_data["schedules"]
            master_schedule_data = movie_screen_data["master_schedule"]
            price_data = schedules = movie_screen_data["price"]
            movie = MovieModel.find_by_name(name=movie_data["name"])

    @classmethod
    @jwt_required
    def delete(cls, cinema_id: int, screen_id: int):
        """DELETE method that deletes a deployed movie-screen.

        path : /api/cinema/<int:cinema_id>/screen/<int:screen_id>/movie-screen/delete

        Description
        -----------
        This will delete a movie for a give screen.
        """
        claims = get_jwt_claims()
        if claims:
            if safe_str_cmp(claims.get("type"), "admin"):
                user = get_current_user()
                if user.cinema_id != cinema_id:
                    return ({"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401)
                _ms_schema = MovieScreenSchema(only=["id"])
                screen = ScreenModel.find_by_id_cinema(
                    id=screen_id, cinema_id=cinema_id
                )
                if not screen:
                    return ({"message": SCREEN_NOT_FOUND_404}, 404)
                movie_screen_id = _ms_schema.load(request.get_json())["id"]
                movie_screen = MovieScreenModel.find_movie_screen(
                    id=movie_screen_id, screen_id=screen_id
                )
                if not movie_screen:
                    return ({"message": MOVIE_SCREEN_NOT_FOUND_MESSAGE_404}, 404)
                schedule = movie_screen.schedule
                master_schedule_id = schedule.master_schedule_id
                master_schedule_dependents = ScheduleModel.count_instances(
                    master_schedule_id=master_schedule_id
                )
                db.session.delete(movie_screen)
                db.session.delete(schedule)
                if master_schedule_dependents == 1:
                    db.session.delete(schedule.master_schedule)
                try:
                    db.session.commit()
                except Exception as e:
                    print(e)
                    db.session.rollback()
                    db.session.flush()
                    return ({"message": UNKNOWN_ERROR_MESSAGE_500}, 500)
                return ({"message": MOVIE_SCREEN_DELETED_201}, 201)
        return ({"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401)


class MovieScreenListResource(MovieScreenResource):
    """Contains the REST API methods for Movie-Screen-List transactions.

    Description
    -----------
    Inherits MovieScreenReource to work with list of MovieScreens.
    """

    ms_schema = MovieScreenSchema()

    @classmethod
    @jwt_required
    def get(cls, cinema_id: int, screen_id: int):
        """GET method that pulls all of the movie products.

        path : /api/cinema/<int:cinema_id>/screen/<int:screen_id>/movie-screens

        Description
        -----------
        This will parse all of the deployed movies for the given screen.
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
                movie_screens = MovieScreenListModel.find_all_owned(screen_id=screen_id)
                movie_screens = list(map(lambda ms: ms.json(), movie_screens))
                return ({"payload": cls.ms_schema.dump(movie_screens, many=True)}, 200)
        return ({"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401)
