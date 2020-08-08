from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt_claims, get_current_user
from werkzeug.security import safe_str_cmp

from .response_messages import (
    INVALID_REQUEST_ADMIN_MESSAGE_401,
    UNKNOWN_ERROR_MESSAGE_500,
    SCREEN_ADDED_201,
    SCREEN_EXISTS_400,
    SCREEN_NOT_FOUND_404,
    SCREEN_DELETED_201,
    SCREEN_UPDATED_201
)
from ..models.seat import SeatModel, SeatListModel
from ..models.screen import ScreenListModel, ScreenModel
from ..schemas.screen import ScreenSchema
from db import db


SCREEN_COLUMN_SEAT_SIZE = 20
LAST_SEAT_LETTER = "J"


class ScreenResource(Resource):

    screen_schema = ScreenSchema()

    @jwt_required
    def get(cls, cinema_id: int, screen_id: int):
        """GET method that pulls a particular screen.

        path: /api/cinema/<int:cinema_id>/screen/<int:screen_id>

        Description:
        -----------
        This will parse a screen object in the database, given
        the current cinema_id and the screen_id.
        """
        claims = get_jwt_claims()
        if claims:
            if safe_str_cmp(claims.get("type"), "admin"):
                user = get_current_user()
                if user.cinema_id != cinema_id:
                    return ({"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401)
                screen = ScreenModel.find_by_id_cinema(cinema_id=cinema_id, id=screen_id)
                if screen:
                    return ({"payload": cls.screen_schema.dump(screen)}, 200)
                return ({"message": SCREEN_NOT_FOUND_404}, 404)
        return ({"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401)

    @jwt_required
    def post(cls, cinema_id: int):
        """POST method that handles the creation of a screen.

        path : /api/cinema/<int:cinema_id>/screen/add

        Description
        -----------
        This will add a screen and its corresponding seats for the current logged in
        user.
        """
        claims = get_jwt_claims()
        if claims:
            if safe_str_cmp(claims.get("type"), "admin"):
                user = get_current_user()
                if not user.cinema_id == cinema_id:
                    return ({"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401)
                screen_data = request.get_json()
                screen_data = cls.screen_schema.load(screen_data)
                if ScreenModel.find_by_name(name=screen_data["name"]):
                    return ({"message": SCREEN_EXISTS_400}, 400)
                screen_data["cinema"] = user.cinema
                screen = ScreenModel(**screen_data)
                seats = SeatListModel.populate_screen_seat(screen)
                try:
                    screen.save_to_db(seats=seats)
                except:
                    db.session.rollback()
                    db.session.flush()
                    return ({"message": UNKNOWN_ERROR_MESSAGE_500}, 500)
                return ({
                    "message": SCREEN_ADDED_201,
                    "screen": cls.screen_schema.dump(screen.json())
                }, 201)
        return ({"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401)

    @jwt_required
    def put(cls, cinema_id: int, screen_id: int):
        """PUT method that handles the attribute updates for a screen.

        path : /api/cinema/<int:cinema_id>/screen/<int:screen_id>/edit

        Description
        -----------
        This will modify a screen and its corresponding seats for the current logged in
        user.
        """
        claims = get_jwt_claims()
        if claims:
            if safe_str_cmp(claims.get("type"), "admin"):
                user = get_current_user()
                if not user.cinema_id == cinema_id:
                    return ({"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401)
                screen = ScreenModel.find_by_id(id=screen_id)
                if not screen:
                    return ({"message": SCREEN_NOT_FOUND_404}, 404)
                screen_data = request.get_json()
                screen_data = cls.screen_schema.load(screen_data)
                new_screen = ScreenModel.find_by_name(name=screen_data["name"])
                if new_screen:
                    if screen != new_screen:
                        return ({"message": SCREEN_EXISTS_400}, 400)
                capacity = screen.capacity
                if capacity > screen_data["capacity"]:
                    total_deletes = capacity - screen_data["capacity"]
                    for seat in screen.seat[-total_deletes:]:
                        db.session.delete(seat)
                elif capacity < screen_data["capacity"]:
                    total_adds = screen_data["capacity"] - capacity
                    last_row = SeatModel.last_row(screen.id)
                    last_row_id = last_row.row_id + 1
                    last_row_letter = last_row.row_letter
                    last_row_letter_id = last_row.row_letter_id
                    row_letter = last_row_letter
                    if last_row_letter_id == 20:
                        counter = 0
                        if row_letter == LAST_SEAT_LETTER:
                            row_letter = "@"
                        row_letter = chr(ord(row_letter) + 1)
                    else:
                        counter = last_row_letter_id
                    for row_id in range(last_row_id, last_row_id + total_adds):
                        counter += 1
                        new_screen = SeatModel(
                            row_id=row_id,
                            screen=screen,
                            row_letter=row_letter,
                            row_letter_id=counter
                        )
                        screen.seat.append(new_screen)
                        if counter >= SCREEN_COLUMN_SEAT_SIZE:
                            counter = 0
                            if row_letter == LAST_SEAT_LETTER:
                                row_letter = "@"
                            row_letter = chr(ord(row_letter) + 1)
                screen.capacity = screen_data["capacity"]
                screen.name = screen_data["name"]
                try:
                    db.session.commit()
                except Exception as e:
                    print(e)
                    db.session.rollback()
                    db.session.flush()
                    return ({"message": UNKNOWN_ERROR_MESSAGE_500}, 500)
                return ({"message": SCREEN_UPDATED_201}, 201)
        return ({"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401)

    @jwt_required
    def delete(self, cinema_id: int, screen_id: int):
        """DELETE method that handles the deletion of a screen.

        path : /api/cinema/<int:cinema_id>/screen/<int:screen_id>/delete.

        Description
        -----------
        This will add a screen and its corresponding seats for the current logged in
        user.
        """
        claims = get_jwt_claims()
        if claims:
            if safe_str_cmp(claims.get("type"), "admin"):
                user = get_current_user()
                if not user.cinema_id == cinema_id:
                    return ({"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401)
                screen = ScreenModel.find_by_id(id=screen_id)
                if not screen:
                    return ({"message": SCREEN_NOT_FOUND_404}, 404)
                try:
                    db.session.query(SeatModel).filter_by(screen_id=screen_id).delete()
                    db.session.delete(screen)
                    db.session.commit()
                except:
                    db.session.rollback()
                    db.session.flush()
                    return ({"message": UNKNOWN_ERROR_MESSAGE_500}, 500)
                return ({"message": SCREEN_DELETED_201}, 201)
        return ({"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401)


class ScreenListResource(Resource):

    screen_schema = ScreenSchema()

    @classmethod
    @jwt_required
    def get(cls, cinema_id: int):
        """GET method that handles the pulling of all screens for a particular cinema.

        path : /api/cinema/<int:cinema_id>/screens

        Description
        -----------
        This will get all the screens for the current logged in
        user.
        """
        claims = get_jwt_claims()
        if claims:
            if safe_str_cmp(claims.get("type"), "admin"):
                user = get_current_user()
                if not user.cinema_id == cinema_id:
                    return ({"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401)
                screens = ScreenListModel.find_screens_by_cinema(cinema_id=cinema_id)
                return {"screens": cls.screen_schema.dump(screens, many=True)}
        return ({"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401)
