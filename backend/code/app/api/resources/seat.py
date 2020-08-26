from flask_restful import Resource, request
from flask_jwt_extended import (
    get_current_user, get_jwt_claims, jwt_required
)

from ..models.seat import SeatListModel
from ..models.seat_reservation import SeatReservationListModel
from ..models.movie_screen import MovieScreenModel
from ..models.screen import ScreenModel
from .response_messages import (
    SCREEN_NOT_FOUND_404,
    MOVIE_SCREEN_NOT_FOUND_MESSAGE_404,
)


class ReservedSeatResource(Resource):
    """Contains the REST API methods for ReservedSeatResource transactions.

    Description
    -----------
    ReservedSeatResource interacts with the seat table which represents a seat in a cinema.
    """

    @classmethod
    def get(cls):
        """GET method that pulls all of the Reserved Seats in the system.

        path : /api/seat/reserved-seats

        Description
        -----------
        This will parseall of the Reserved Seats of a particular movie-screen.
        """
        data = request.get_json()
        screen_id = data.get("screen_id")
        schedule_id = data.get("schedule_id")
        movie_id = data.get("movie_id")
        movie_screen = MovieScreenModel.find(
            schedule_id=schedule_id, screen_id=screen_id, movie_id=movie_id
        )
        if not movie_screen:
            return ({"message": MOVIE_SCREEN_NOT_FOUND_MESSAGE_404}, 404)
        seat_id_list = SeatListModel.find_seats_by_screen(screen_id=screen_id)
        occupied_seats = SeatReservationListModel.which_occupied(
            seat_id_list=seat_id_list, movie_screen=movie_screen
        )
        return ({
            "payload": {
                "occupied": occupied_seats,
                "all": seat_id_list
            }
        }, 200)
