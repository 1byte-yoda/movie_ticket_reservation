from datetime import datetime as dt

from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from werkzeug.security import safe_str_cmp

from .model import ReservationModel
from ...utils import deserialize_datetime


class ReservationResource(Resource):
    """Docstring here."""

    parser = reqparse.RequestParser()
    parser.add_argument(name="id", required=True, type=int,
                        help="id value must be provided.")  
    parser.add_argument(name="head_count", required=True, type=int,
                        help="head_count value must be provided.")

    @jwt_required()
    def get(self, id_):
        """Get a reservation by id."""
        if safe_str_cmp(current_identity.type.value, "admin"):
            temp_reservation = ReservationModel.find_by_id(id_=id_)
            return ((temp_reservation.json(), 200)
                    if temp_reservation
                    else ({"message": "Reservation not found."}, 404))
        return {"message": "Invalid Request."}, 401

    @jwt_required()
    def post(self):
        """Create a reservation."""
        ReservationResource.parser.remove_argument("id")
        request_data = ReservationResource.parser.parse_args()
        current_datetime = deserialize_datetime(dt.now())
        request_data["reserve_datetime"] = current_datetime
        request_data["cancel_datetime"] = None
        request_data["account_id"] = current_identity.id
        temp_reservation = ReservationModel(**request_data)
        temp_reservation.save_to_db()
        return {"message": "Reservation created successfully.",
                "payload": request_data}, 201

    @jwt_required()
    def put(self):
        """Modify a reservation."""
        if request.path == "/reservation/update":
            request_data = ReservationResource.parser.parse_args()
            id_ = request_data.get("id", None)
            current_datetime = dt.now()
            reservation_ = ReservationModel.find_by_id(id_=id_)

            if not reservation_:
                request_data["reserve_datetime"] = deserialize_datetime(current_datetime)
                request_data["cancel_datetime"] = None
                request_data["account_id"] = current_identity.id
                temp_reservation = ReservationModel(**request_data)
                temp_reservation.save_to_db()
                return {"message": "Reservation inserted successfully.",
                        "payload": request_data}, 201
            else:
                if current_identity.id == reservation_.account_id:
                    request_data = ReservationResource.parser.parse_args()
                    request_data["id"] = reservation_.id
                    request_data["reserve_datetime"] = deserialize_datetime(current_datetime)
                    reservation_.update(data=request_data)
                    return {"message": "Reservation updated successfully.",
                            "payload": request_data}, 201
                return {"message": "Invalid Request."}, 401

        elif request.path == "/reservation/cancel":
            ReservationResource.parser.remove_argument("head_count")
            request_data = ReservationResource.parser.parse_args()
            id_ = request_data.get("id", None)
            reservation_ = ReservationModel.find_by_id(id_=id_)

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


class ReservationListResource(Resource):
    """Docstring here."""

    @jwt_required()
    def get(self):
        """Get all of reservations in our system."""
        if safe_str_cmp(current_identity.type.value, "admin"):
            reservations = ReservationModel.query.all()
            reservations = (reservation.json() for reservation in reservations)
            return {"reservations": list(reservations)}, 200
        return {"message": "Invalid Request."}, 401
