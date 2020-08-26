from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    get_current_user,
)
from werkzeug.security import safe_str_cmp
from marshmallow.exceptions import ValidationError

from db import db
from ..models.seat_reservation import SeatReservationModel, SeatReservationListModel
from ..models.movie_screen import MovieScreenModel
from ..models.reservation import ReservationModel
from ..models.seat import SeatListModel
from .response_messages import (
    SEAT_RESERVATION_NOT_FOUND_MESSAGE_404,
    INVALID_REQUEST_ADMIN_MESSAGE_401,
    SEATS_OCCUPIED_MESSAGE_401,
    SEATS_NOT_FOUND_MESSAGE_404,
    SEAT_RESERVATION_CREATED_MESSAGE_201,
    MOVIE_SCREEN_NOT_FOUND_MESSAGE_404,
    UNKNOWN_ERROR_MESSAGE_500,
    RESERVATION_NOT_FOUND_MESSAGE_404,
)
from ..schemas.seat_reservation import SeatReservationSchema, SeatReservationPostSchema


seat_reservation_post_schema = SeatReservationPostSchema()


class SeatReservationResource(Resource):
    """Docstring here."""

    schema = SeatReservationSchema()

    @classmethod
    @jwt_required
    def get(cls):
        """Get a seat reservation."""
        seat_reservation_data = request.get_json()
        try:
            seat_reservation_data = cls.schema.load(seat_reservation_data)
        except ValidationError as err:
            return {"message": err.messages}

        claims = get_jwt_claims()
        if safe_str_cmp(claims.get("type"), "admin"):
            try:
                seat_reservation = SeatReservationModel.find(data=seat_reservation_data)
            except:
                return {"message": UNKNOWN_ERROR_MESSAGE_500}, 500
            if seat_reservation:
                try:
                    seat_reservation = cls.schema.dump(seat_reservation[0].json())
                except ValidationError as err:
                    return {"message": err.messages}, 400
                return {"seat_reservation": seat_reservation}, 200

            return {"message": SEAT_RESERVATION_NOT_FOUND_MESSAGE_404}, 404
        return {"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401

    @classmethod
    @jwt_required
    def post(cls):
        """Create a reservation."""
        seat_reservation_data = request.get_json()
        try:
            seat_reservation_data = seat_reservation_post_schema.load(
                seat_reservation_data
            )
        except ValidationError as err:
            return {"message": err.messages}, 400

        # Duplicate Handler will be implemented in frontend as well,
        # eg. show only available seats for a particular screen

        # Account
        account = get_current_user().account

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
        largest_seat_id = len(seat_id_list)
        if largest_seat_id > max_screen_capacity:
            return ({"message": SEATS_NOT_FOUND_MESSAGE_404}, 404)
        valid_seats = SeatListModel.find_all_seats(screen_id=screen_id)
        all_seats_valid = all([x in valid_seats for x in seat_id_list])
        if not all_seats_valid:
            return ({"message": SEATS_NOT_FOUND_MESSAGE_404}, 404)
        try:
            occupied_seats = SeatReservationListModel.which_occupied(
                seat_id_list=seat_id_list, movie_screen=movie_screen,
            )
            is_occupied_seats = any(
                seat_id in occupied_seats for seat_id in seat_id_list
            )
            if is_occupied_seats:
                return ({"message": SEATS_OCCUPIED_MESSAGE_401}, 400)
        except:
            db.session.rollback()
            db.session.flush()
            return {"message": UNKNOWN_ERROR_MESSAGE_500}, 500

        # Reservation
        head_count = len(seat_id_list)
        movie_price = movie_screen.price
        total_price = movie_price * head_count
        token = seat_reservation_data.get("token") or ""
        reservation = ReservationModel(
            head_count=head_count, account=account, total_price=total_price, token=token
        )
        # reservation.save_to_db()

        reservation.set_status("failed")
        # item_details = {
        #     "amount": total_price,
        #     "description": f"[{movie_price} x {head_count}] - {movie_screen.movie.name}"
        #                    f"_{movie_screen.movie.cinema_id}"
        # }
        # reservation.charge_with_stripe(item_details=item_details, token=token)
        reservation.set_status("success")

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
        try:
            SeatReservationModel.save_all(seat_reservations=seat_reservation_list)
        except Exception as e:
            print(e)
            db.session.rollback()
            db.session.flush()
            return {"message": UNKNOWN_ERROR_MESSAGE_500}, 500

        try:
            tickets = []
            tickets = cls.schema.dump(seat_reservation_list, many=True)
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            return {"message": UNKNOWN_ERROR_MESSAGE_500}, 500

        return (
            {
                "message": SEAT_RESERVATION_CREATED_MESSAGE_201,
                "tickets": tickets,
            },
            201,
        )

    @jwt_required
    def put(self):
        """Modify a reservation."""
        pass


class SeatReservationListResource(Resource):
    """Docstring here."""

    schema = SeatReservationSchema(load_only=["reservation"], dump_only=["id"])

    @classmethod
    @jwt_required
    def get(cls):
        """Get a list of reservations in our system."""
        claims = get_jwt_claims()
        if claims:
            if safe_str_cmp(claims.get("type"), "admin"):
                try:
                    data = {
                        "reservation_id": cls.schema.load(request.get_json())[
                            "reservation"
                        ]["id"]
                    }
                except ValidationError as err:
                    return {"message": err.messages}, 400

                try:
                    reservations = SeatReservationModel.find(data=data)
                except:
                    return {"message": UNKNOWN_ERROR_MESSAGE_500}, 500

                if reservations:
                    try:
                        reservations = (
                            cls.schema.dump(reservation.json())
                            for reservation in reservations
                        )
                    except ValidationError as err:
                        return {"message": err.messages}, 400
                    return {"seat_reservations": list(reservations)}, 200

                return {"message": RESERVATION_NOT_FOUND_MESSAGE_404}
        return {"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401
