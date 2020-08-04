from werkzeug.security import safe_str_cmp
from flask_restful import Resource
from flask_jwt_extended import get_current_user, get_jwt_claims, jwt_required

from .response_messages import CINEMA_NOT_FOUND_404, INVALID_REQUEST_ADMIN_MESSAGE_401
from ..models.cinema import CinemaModel
from ..schemas.cinema import CinemaSchema


class CinemaResource(Resource):
    """Contains the REST API endpoints for a Cinema."""

    cinema_schema = CinemaSchema()

    @classmethod
    @jwt_required
    def get(cls):
        """GET method that handles the /api/cinema endpoint.

        Description
        -----------
        This will get the cinema info for the current logged in
        user.
        """
        claims = get_jwt_claims()
        if claims:
            if safe_str_cmp(claims.get("type"), "admin"):
                user = get_current_user()
                cinema = CinemaModel.find_by_id(id=user.cinema_id)
                if cinema:
                    return ({"cinema": cls.cinema_schema.dump(cinema.json())}, 200)
                return ({"message": CINEMA_NOT_FOUND_404}, 404)
        return ({"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401)

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass