from flask_restful import Resource, request
from flask_jwt_extended import (
    get_current_user,
    get_jwt_claims,
    jwt_required,
    fresh_jwt_required
)
from werkzeug.security import safe_str_cmp

from db import db
from ..models.movie import MovieModel
from ..schemas.movie import MovieSchema
from .response_messages import (
    INVALID_REQUEST_ADMIN_MESSAGE_401,
    UNKNOWN_ERROR_MESSAGE_500,
    MOVIE_NOT_FOUND_404,
    MOVIE_NAME_EXISTS_400,
    MOVIE_ADDED_201,
    MOVIE_UPDATED_201,
    MOVIE_DELETED_201
)


class MovieResource(Resource):
    """Contains the REST API methods for Movie transactions.

    Description
    -----------
    Movie interacts with the movie table which contains
    all of the movies owned by a Cinema Manager.
    """

    movie_schema = MovieSchema()

    @classmethod
    @jwt_required
    def get(cls, cinema_id: int, movie_id: int):
        """GET method that pulls all of the movie owned by a cinema manager.

        path : /api/cinema/<int:cinema_id>/movie/<int:movie_id>

        Description
        -----------
        This will parse a particular movie based on its id.
        """
        claims = get_jwt_claims()
        if claims:
            if safe_str_cmp(claims.get("type"), "admin"):
                user = get_current_user()
                if user.cinema_id != cinema_id:
                    return ({"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401)
                movie = MovieModel.find_by_id(id=movie_id, cinema_id=cinema_id)
                if not movie:
                    return ({"message": MOVIE_NOT_FOUND_404}, 404)
                return cls.movie_schema.dump(movie.json())
        return ({"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401)

    @classmethod
    @jwt_required
    def post(cls, cinema_id: int):
        """POST method that will add a movie for a particular cinema manager.

        path : /api/cinema/<int:cinema_id>/movie/add

        Description
        -----------
        This will add a movie for a particular manager.
        """
        claims = get_jwt_claims()
        if claims:
            if safe_str_cmp(claims.get("type"), "admin"):
                user = get_current_user()
                if user.cinema_id != cinema_id:
                    return ({"message": INVALID_REQUEST_ADMIN_MESSAGE_401})
                movie_data = cls.movie_schema.load(request.get_json())
                movie_data["cinema_id"] = cinema_id
                movie = MovieModel.find_by_name(
                    name=movie_data["name"], cinema_id=cinema_id
                )
                if movie:
                    return ({"message": MOVIE_NAME_EXISTS_400}, 400)
                movie = MovieModel(**movie_data)
                try:
                    movie.save_to_db()
                except:
                    db.session.rollback()
                    db.session.flush()
                    return ({"message": UNKNOWN_ERROR_MESSAGE_500}, 500)
                return (
                    {
                        "message": MOVIE_ADDED_201,
                        "payload": cls.movie_schema.dump(movie.json())
                    }, 201
                )
        return ({"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401)

    @classmethod
    @fresh_jwt_required
    def put(cls, cinema_id: int, movie_id: int):
        """PUT method that will update a movie for a particular cinema manager.

        path : /api/cinema/<int:cinema_id>/movie/<int:movie_id>/edit

        Description
        -----------
        This will update a movie for a particular manager.
        """
        claims = get_jwt_claims()
        if claims:
            if safe_str_cmp(claims.get("type"), "admin"):
                user = get_current_user()
                if user.cinema_id != cinema_id:
                    return ({"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401)
                movie = MovieModel.find_by_id(id=movie_id, cinema_id=cinema_id)
                if not movie:
                    return ({"message": MOVIE_NOT_FOUND_404}, 404)
                movie_data = cls.movie_schema.load(request.get_json())
                if MovieModel.find_by_name(
                    name=movie_data["name"], cinema_id=cinema_id
                ):
                    if movie.name != movie_data["name"]:
                        return ({"message": MOVIE_NAME_EXISTS_400}, 400)
                additional_msg = None
                if str(movie.duration) != movie_data["duration"]:
                    additional_msg = ("Some deployed movies' with the name: "
                                      f"{movie.name} were affected. "
                                      "Please update those accordingly.")
                try:
                    movie.update(update_data=movie_data)
                except Exception as e:
                    print(e)
                    db.session.rollback()
                    db.session.flush()
                    return ({"message": UNKNOWN_ERROR_MESSAGE_500}, 500)
                return (
                    {
                        "message": MOVIE_UPDATED_201,
                        "additional msg": additional_msg
                    }, 201
                )
        return ({"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401)
    
    @classmethod
    @fresh_jwt_required
    def delete(cls, cinema_id: int, movie_id: int):
        """DELETE method that will delete a movie for a particular cinema manager.

        path : /api/cinema/<int:cinema_id>/movie/<int:movie_id>delete

        Description
        -----------
        This will delete a movie for a particular manager.
        """
        claims = get_jwt_claims()
        if claims:
            if safe_str_cmp(claims.get("type"), "admin"):
                user = get_current_user()
                if user.cinema_id != cinema_id:
                    return ({"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401)
                movie = MovieModel.find_by_id(id=movie_id, cinema_id=cinema_id)
                if not movie:
                    return ({"message": MOVIE_NOT_FOUND_404}, 404)
                try:
                    movie.remove_from_db()
                except:
                    db.session.rollback()
                    db.session.flush()
                    return ({"message": UNKNOWN_ERROR_MESSAGE_500}, 500)
                return ({"message": MOVIE_DELETED_201}, 201)
        return ({"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401)
