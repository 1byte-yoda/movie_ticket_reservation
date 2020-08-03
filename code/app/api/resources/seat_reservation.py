import simplejson
from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    get_current_user,
)
from werkzeug.security import safe_str_cmp
from marshmallow.exceptions import ValidationError

from ..models.seat_reservation import SeatReservationModel, SeatReservationListModel
from ..models.movie_screen import MovieScreenModel
from ..models.payment import PaymentModel
from ..models.reservation import ReservationModel
from .response_messages import (
    SEAT_RESERVATION_NOT_FOUND_MESSAGE_404,
    INVALID_REQUEST_ADMIN_MESSAGE_401,
    SEATS_OCCUPIED_MESSAGE_401,
    SEATS_NOT_FOUND_MESSAGE_404,
    SEAT_RESERVATION_CREATED_MESSAGE_201,
    MOVIE_SCREEN_NOT_FOUND_MESSAGE_404,
)
from ..schemas.seat_reservation import (
    SeatReservationSchema,
    SeatReservationPostSchema
)


seat_reservation_schema = SeatReservationSchema()
seat_reservation_post_schema = SeatReservationPostSchema()


class SeatReservationResource(Resource):
    """Docstring here."""

    @jwt_required
    def get(self):
        """Get a seat reservation."""
        seat_reservation_data = request.get_json()
        try:
            seat_reservation_data = seat_reservation_schema.load(seat_reservation_data)
        except ValidationError as err:
            return {"message": err.messages}
        claims = get_jwt_claims()
        if safe_str_cmp(claims.get("type"), "admin"):
            seat_reservation = SeatReservationModel.find(data=seat_reservation_data)
            seat_reservation = simplejson.loads(
                seat_reservation_schema.dumps(seat_reservation)
            )
            return (
                {"seat_reservation": seat_reservation}, 200
                if seat_reservation
                else ({"message": SEAT_RESERVATION_NOT_FOUND_MESSAGE_404}, 404)
            )
        return {"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401

    @jwt_required
    def post(self):
        """Create a reservation."""
        seat_reservation_data = request.get_json()
        try:
            seat_reservation_data = (
                seat_reservation_post_schema.load(seat_reservation_data)
            )
        except ValidationError as err:
            return {"message": err.messages}

        # Duplicate Handler will be implemented in frontend as well,
        # eg. show only available seats for a particular screen

        # Account
        account = get_current_user()

        # Movie Screen
        screen_id = seat_reservation_data["screen_id"]
        movie_id = seat_reservation_data["movie_id"]
        schedule_id = seat_reservation_data["schedule_id"]
        movie_screen = MovieScreenModel.find(
            screen_id=screen_id, movie_id=movie_id, schedule_id=schedule_id
        )
        if not movie_screen:
            return (
                {
                    "message": MOVIE_SCREEN_NOT_FOUND_MESSAGE_404,
                    "payload": {
                        "screen_id": screen_id,
                        "movie_id": movie_id,
                        "schedule_id": schedule_id,
                    },
                },
                404,
            )
        max_screen_capacity = movie_screen.screen.capacity

        # Seats
        seat_id_list = seat_reservation_data["seat_id_list"]
        largest_seat_id = max(seat_id_list)
        if largest_seat_id > max_screen_capacity:
            return ({"message": SEATS_NOT_FOUND_MESSAGE_404}, 404)
        occupied_seats = SeatReservationListModel.which_occupied(
            seat_id_list=seat_id_list, movie_screen=movie_screen,
        )
        is_occupied_seats = any(seat_id in occupied_seats for seat_id in seat_id_list)
        if is_occupied_seats:
            return ({"message": SEATS_OCCUPIED_MESSAGE_401}, 400)

        # Payment
        head_count = len(seat_id_list)
        movie_price = movie_screen.movie.price
        total_price = movie_price * head_count
        payment = PaymentModel(
            token_id="some-random-token-that-i-created.",
            total_price=total_price,
            type="paymaya",
        )

        # Reservation
        reservation = ReservationModel(
            head_count=head_count, account=account, payment=payment
        )

        # Seat Reservation
        seat_reservation_list = []
        for seat_id in seat_id_list:
            seat_reservation = SeatReservationModel(
                price=movie_price,
                seat_id=seat_id,
                reservation=reservation,
                movie_screen=movie_screen,
            )
            seat_reservation_list.append(seat_reservation)
        SeatReservationModel.save_all(seat_reservations=seat_reservation_list)
        return (
            {
                "message": SEAT_RESERVATION_CREATED_MESSAGE_201,
                "seat_reservation": reservation.generate_json_ticket(),
            },
            201,
        )

    @jwt_required
    def put(self):
        """Modify a reservation."""
        pass


class SeatReservationListResource(Resource):
    """Docstring here."""

    @jwt_required
    def get(self):
        """Get all of reservations in our system."""
        claims = get_jwt_claims()
        if claims:
            if safe_str_cmp(claims.get("type"), "admin"):
                reservations = SeatReservationListModel.find_all()
                reservations = (
                    simplejson.loads(seat_reservation_schema.dumps(reservation))
                    for reservation in reservations
                )
                return {"seat_reservations": list(reservations)}, 200
        return {"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401
