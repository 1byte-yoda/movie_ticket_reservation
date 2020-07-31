from datetime import datetime as dt
import simplejson

from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from werkzeug.security import safe_str_cmp

from ..models.seat_reservation import SeatReservationModel
from ..models.parsers import SeatReservationParser
from ..models.movie import MovieModel
from ..models.movie_screen import MovieScreenModel
from ..models.payment import PaymentModel
from ..models.reservation import ReservationModel
from ...utils import deserialize_datetime


class SeatReservationResource(Resource):
    """Docstring here."""

    @jwt_required()
    def get(self):
        """Get a seat reservation by unique_reservation."""
        expected_args = {
            "seat_id": int, "reservation_id": int, "movie_screen_id": int
        }
        data = SeatReservationParser.parse_reservation_input(dict_=expected_args)
        if safe_str_cmp(current_identity.type.value, "admin"):
            seat_reservation = SeatReservationModel.find(unique_reservation=data)
            return ((seat_reservation.json(), 200)
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
        data = SeatReservationParser.parse_reservation_input(dict_=expected_args)
        # Duplicate Handler will be implemented in frontend, eg. showing of available seats for a particular screen
        # Temp duplicate handler

        # Account
        account = current_identity

        # Movie
        unique_movie_screen = {
            "screen_id": data["screen_id"],
            "movie_id": data["movie_id"]
        }
        movie_screen = MovieScreenModel.find(unique_movie_screen=unique_movie_screen)
        movie = MovieModel.find_by_id(id_=data["movie_id"])
        movie_price = movie.price

        # Seats
        seat_id_list = data["seat_id_list"]  # temp_get_from_frontend("seat_id_list")
        head_count = len(seat_id_list)

        # Payment
        total_price = movie_price * head_count
        payment = PaymentModel(token_id="some-random-token-that-i-created.",
                               total_price=total_price, type="paymaya")

        # Reservation
        reservation = ReservationModel(head_count=head_count, account=account,
                                       payment=payment)

        # Seat Reservation
        seat_reservation_list = []
        for seat_id in seat_id_list:
            seat_reservation = SeatReservationModel(price=movie_price, seat_id=seat_id,
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
            parser = reqparse.RequestParser()
            parser.add_argument(name="id", required=True, type=int)
            parser.add_argument(name="head_count", required=True, type=int)
            request_data = parser.parse_args()
            id_ = request_data.get("id", None)
            reservation_ = SeatReservationModel.find_by_id(id_=id_)

            # Insert
            if not reservation_:
                parser.add_argument(name="seat_id", required=True, type=int)
                parser.add_argument(name="ticket_id", required=True, type=int)
                parser.add_argument(name="movie_id", required=True, type=int)
                request_data["account_id"] = current_identity.id
                temp_reservation = SeatReservationModel(**request_data)
                temp_reservation.save_to_db()
                return {"message": "Reservation inserted successfully.",
                        "payload": request_data}, 201

            # Update
            else:
                if current_identity.id == reservation_.account_id:
                    current_datetime = dt.now()
                    request_data = parser.parse_args()
                    request_data["id"] = reservation_.id
                    request_data["reserve_datetime"] = deserialize_datetime(current_datetime)
                    reservation_.update(data=request_data)
                    return {"message": "Reservation updated successfully.",
                            "payload": request_data}, 201
                return {"message": "Invalid Request."}, 401

        # Cancel
        elif request.path == "/reservation/cancel":
            parser = reqparse.RequestParser()
            parser.add_argument(name="id", required=True, type=int)
            parser.add_argument(name="head_count", required=False, type=int)
            request_data = parser.parse_args()
            id_ = request_data.get("id", None)
            reservation_ = SeatReservationModel.find_by_id(id_=id_)

            if reservation_:
                if current_identity.id == reservation_.account_id:
                    if reservation_.cancel_datetime:
                        return {"message": "Reservation cancelled successfully.",
                                "payload": {"reservation_id": reservation_.id}}, 201
                    cancel_datetime = deserialize_datetime(dt.now())
                    reservation_.cancel(updated_cancel_datetime=cancel_datetime)
                    return {"message": "Reservation cancelled successfully.",
                            "payload": {"reservation_id": reservation_.id}}, 201
                else:
                    return {"message": "Invalid Request."}, 401
            else:
                return {"message": "Reservation doesn't exist."}, 400


class SeatReservationListResource(Resource):
    """Docstring here."""

    @jwt_required()
    def get(self):
        """Get all of reservations in our system."""
        if safe_str_cmp(current_identity.type.value, "admin"):
            reservations = SeatReservationModel.query.all()
            reservations = (reservation.json() for reservation in reservations)
            reservations = simplejson.dumps({"reservations": list(reservations)})
            return simplejson.loads(reservations), 200
        return {"message": "Invalid Request."}, 401


def temp_get_from_frontend(item_key: str):
    """Mimic the sample payload data from user journey in frontend."""
    items = {
        "seat_id_list": [1, 2, 3, 4, 5],
        "movie_screen_id": 1
    }
    return items[item_key]
