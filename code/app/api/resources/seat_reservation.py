# from datetime import datetime as dt

import simplejson
from flask import request
from flask_restful import Resource
from flask_jwt import jwt_required, current_identity
from werkzeug.security import safe_str_cmp

from ..models.seat_reservation import (
    SeatReservationModel, SeatReservationListModel
)
from ..models.seat import SeatListModel
from ..models.parsers import SeatReservationParser
from ..models.movie import MovieModel
from ..models.movie_screen import MovieScreenModel
from ..models.payment import PaymentModel
from ..models.reservation import ReservationModel
# from ...utils import deserialize_datetime


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
            "screen_id": int, "movie_id": int, "seat_id_list": list
        }
        data = SeatReservationParser.parse_expected_input(dict_=expected_args)
        # Duplicate Handler will be implemented in frontend as well,
        # eg. showing only available seats for a particular screen

        # Account
        account = current_identity

        # Movie
        movie_screen_query = {
            "screen_id": data["screen_id"],
            "movie_id": data["movie_id"]
        }
        movie_screen = MovieScreenModel.find(data=movie_screen_query)
        if not movie_screen:
            return ({
                "message": "Movie-Screen combination not found.",
                "payload": movie_screen_query
            }, 404)
        movie = MovieModel.find_by_id(id_=data["movie_id"])
        movie_price = movie.price

        # Seats
        seat_id_list = data["seat_id_list"]
        existing_seats = SeatListModel.find_existing(seat_id_list=seat_id_list)
        invalid_seats = [seat for seat in seat_id_list if seat not in existing_seats]

        if invalid_seats:
            return ({
                "message": f"Seat IDs: {invalid_seats} does not exists."
            }, 404)
        seat_reservation_query = {"movie_screen_id": movie_screen.id,
                                  "seat_id_list": seat_id_list}
        taken_seats = SeatReservationListModel.find_taken_seats(**seat_reservation_query)
        taken_seats = [seat_reservation.seat_id for seat_reservation in taken_seats]

        if taken_seats:
            return ({
                "message": f"Invalid request. Seat IDs: {taken_seats} already reserved."
            }, 400)

        # Payment
        head_count = len(seat_id_list)
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
        return {"message": "Reservation created successfully.",
                "payload": data}, 201

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
