import simplejson
from flask import request
from flask_restful import Resource
from flask_jwt import jwt_required, current_identity
from werkzeug.security import safe_str_cmp

from ..models.seat_reservation import (
    SeatReservationModel, SeatReservationListModel
)
from ..models.parsers import SeatReservationParser
from ..models.movie_screen import MovieScreenModel
from ..models.payment import PaymentModel
from ..models.reservation import ReservationModel


class SeatReservationResource(Resource):
    """Docstring here."""

    @jwt_required()
    def get(self):
        """Get a seat reservation by unique_reservation."""
        expected_args = {
            "seat_id": int, "movie_screen_id": int
        }
        data = SeatReservationParser.parse_expected_input(dict_=expected_args)
        if safe_str_cmp(current_identity.type.value, "admin"):
            seat_reservation = SeatReservationModel.find(data=data).json()
            seat_reservation = simplejson.dumps(seat_reservation)
            seat_reservation = simplejson.loads(seat_reservation)
            return ((seat_reservation, 200)
                    if seat_reservation
                    else ({"message": "Reservation not found."}, 404))
        return {"message": "Invalid Request."}, 401

    @jwt_required()
    def post(self):
        """Create a reservation."""
        expected_args = {
            # Get these from frontend
            "screen_id": int, "movie_id": int,
            "seat_id_list": list, "schedule_id": int
        }
        data = SeatReservationParser.parse_expected_input(dict_=expected_args)
        # Duplicate Handler will be implemented in frontend as well,
        # eg. show only available seats for a particular screen

        # Account
        account = current_identity

        # Movie Screen
        screen_id = data["screen_id"]
        movie_id = data["movie_id"]
        schedule_id = data["schedule_id"]
        movie_screen = MovieScreenModel.find(screen_id=screen_id, movie_id=movie_id,
                                             schedule_id=schedule_id)
        if not movie_screen:
            return ({
                "message": "movie-screen-schedule combination not found.",
                "payload": {"screen_id": screen_id, "movie_id": movie_id,
                            "schedule_id": schedule_id}
            }, 404)
        max_screen_capacity = movie_screen.screen.capacity

        # Seats
        seat_id_list = data["seat_id_list"]
        largest_seat_id = max(seat_id_list)
        if largest_seat_id > max_screen_capacity:
            return ({"message": "Seat(s) not found."}, 404)
        occupied_seats = SeatReservationListModel.which_occupied(
            seat_id_list=seat_id_list,
            movie_screen=movie_screen,
        )
        is_occupied_seats = any(seat_id in occupied_seats for seat_id in seat_id_list)
        if is_occupied_seats:
            return ({"message": "Seat(s) Occupied"}, 400)

        # Payment
        head_count = len(seat_id_list)
        movie_price = movie_screen.movie.price
        total_price = movie_price * head_count
        payment = PaymentModel(token_id="some-random-token-that-i-created.",
                               total_price=total_price, type="paymaya")

        # Reservation
        reservation = ReservationModel(head_count=head_count, account=account,
                                       payment=payment)

        # Seat Reservation
        seat_reservation_list = []
        for seat_id in seat_id_list:
            seat_reservation = SeatReservationModel(price=movie_price,
                                                    seat_id=seat_id,
                                                    reservation=reservation,
                                                    movie_screen=movie_screen)
            seat_reservation_list.append(seat_reservation)
        SeatReservationModel.save_all(seat_reservations=seat_reservation_list)
        payload = {
            "reservation_id": reservation.id,
            "cinema_name": movie_screen.screen.cinema.name,
            "screen_id": screen_id,
            "movie_name": movie_screen.movie.name,
            "seat_id_list": seat_id_list,
            "price_breakdown": f"{float(movie_price)} x {head_count}",
            "total_price": float(total_price)
        }
        return {"message": "Reservation created successfully.",
                "payload": payload}, 201

    @jwt_required()
    def put(self):
        """Modify a reservation."""
        # Upsert
        if request.path == "/reservation/update":
            pass

        # Cancel
        elif request.path == "/reservation/cancel":
            pass


class SeatReservationListResource(Resource):
    """Docstring here."""

    @jwt_required()
    def get(self):
        """Get all of reservations in our system."""
        if safe_str_cmp(current_identity.type.value, "admin"):
            reservations = SeatReservationListModel.find_all()
            reservations = (reservation.json() for reservation in reservations)
            reservations = simplejson.dumps({"reservations": list(reservations)})
            return simplejson.loads(reservations), 200
        return {"message": "Invalid Request."}, 401
