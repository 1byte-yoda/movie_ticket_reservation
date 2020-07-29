from datetime import datetime as dt

from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from .model import ReservationModel, ReservationListModel


class ReservationResource(Resource):
    """Docstring here."""

    parser = reqparse.RequestParser()
    parser.add_argument(name="account_id", required=True, type=int,
                        help="account_id value must be provided.")
    parser.add_argument(name="head_count", required=True, type=int,
                        help="head_count value must be provided.")
    parser.add_argument(name="movie_screen_id", required=True, type=int,
                        help="movie_screen_id value must be provided.")

    @jwt_required()
    def get(self, id_):
        """Get a reservation by account_id."""
        temp_reservation = ReservationModel.find_by_id(id_=id_)
        return ((temp_reservation, 200)
                if temp_reservation
                else ({"message": "Reservation not found."}, 404))

    @jwt_required()
    def post(self):
        """Create a reservation."""
        request_data = ReservationResource.parser.parse_args()
        current_datetime = dt.now().strftime("%Y-%m-%d %H:%M:%S")
        request_data["reserve_datetime"] = current_datetime
        request_data["cancel_datetime"] = None
        temp_reservation = ReservationModel(**request_data)
        temp_reservation.insert()
        return {"message": "Reservation created successfully.",
                "payload": request_data}, 201

    @jwt_required()
    def put(self):
        """Modify a reservation."""
        if request.path == "/reservation/update":
            request_data = ReservationResource.parser.parse_args()
            account_id = request_data.get("account_id", None)
            movie_screen_id = request_data.get("movie_screen_id", None)
            reservation_ = ReservationModel.find_id_by_account_movie_screen(account_id=account_id,
                                                                            movie_screen_id=movie_screen_id)

            if not reservation_:
                current_datetime = dt.now().strftime("%Y-%m-%d %H:%M:%S")
                request_data["reserve_datetime"] = current_datetime
                request_data["cancel_datetime"] = None
                temp_reservation = ReservationModel(**request_data)
                temp_reservation.insert()
                return {"message": "Reservation inserted successfully.",
                        "payload": request_data}, 201
            else:
                request_data["id"] = reservation_.get("id", None)
                reservation = ReservationModel(**request_data)
                reservation.update()
                return {"message": "Reservation updated successfully.",
                        "payload": request_data}, 201

        elif request.path == "/reservation/cancel":
            ReservationResource.parser.remove_argument("head_count")
            request_data = ReservationResource.parser.parse_args()
            account_id = request_data.get("account_id", None)
            movie_screen_id = request_data.get("movie_screen_id", None)
            reservation_ = ReservationModel.find_id_by_account_movie_screen(account_id=account_id,
                                                                            movie_screen_id=movie_screen_id)

            if reservation_:
                reservation_id = reservation_.get("id")
                if reservation_.get("cancel_datetime", None):
                    return {"message": "Reservation cancelled successfully.",
                            "payload": {"reservation_id": reservation_id}}, 201
                cancel_datetime = dt.now().strftime("%Y-%m-%d %H:%M:%S")
                temp_reservation = ReservationModel(id=reservation_id,
                                                    cancel_datetime=cancel_datetime)
                temp_reservation.cancel()
                return {"message": "Reservation cancelled successfully.",
                        "payload": {"reservation_id": reservation_id}}, 201
            else:
                return {"message": "Reservation doesn't exist."}, 400


class ReservationListResource(Resource):
    """Docstring here."""

    def get(self):
        """Get all of reservations in our system."""
        temp_reservations = ReservationListModel.find_all_reservation()
        return {"reservations": temp_reservations}, 200
