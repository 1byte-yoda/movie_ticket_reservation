from datetime import datetime as dt

import pymysql
from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Reservation(Resource):
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
        row = self.find_by_id(id_=id_)
        return (row, 200) if row else ({"message": "Reservation not found."}, 404)

    @classmethod
    def find_by_id(cls, *, id_):
        """Docstring here."""
        connection = pymysql.connect(host="localhost", user="root", password="123456",
                                     db="anonymouse", charset="utf8mb4",
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM reservation WHERE id=%s"
                cursor.execute(sql, (id_,))
                row = cursor.fetchone()
        except:
            return {"message": "An error occured."}, 500
        finally:
            connection.close()

        if row["reserve_datetime"]:
            row["reserve_datetime"] = row["reserve_datetime"].strftime("%Y-%m-%d %H:%M:%S")
        if row["cancel_datetime"]:
            row["cancel_datetime"] = row["cancel_datetime"].strftime("%Y-%m-%d %H:%M:%S")
        return row

    @classmethod
    def find_id_by_account_movie_screen(cls, *, account_id, movie_screen_id):
        """Docstring here."""
        connection = pymysql.connect(host="localhost", user="root", password="123456",
                                     db="anonymouse", charset="utf8mb4",
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM reservation WHERE account_id=%s AND movie_screen_id=%s"
                cursor.execute(sql, (account_id, movie_screen_id))
                row = cursor.fetchone()
        except:
            return {"message": "An error occured."}, 500
        finally:
            connection.close()

        if row["reserve_datetime"]:
            row["reserve_datetime"] = row["reserve_datetime"].strftime("%Y-%m-%d %H:%M:%S")
        if row["cancel_datetime"]:
            row["cancel_datetime"] = row["cancel_datetime"].strftime("%Y-%m-%d %H:%M:%S")
        return row

    @jwt_required()
    def post(self):
        """Create a reservation."""
        request_data = Reservation.parser.parse_args()
        current_datetime = dt.now().strftime("%Y-%m-%d %H:%M:%S")
        request_data["reserve_datetime"] = current_datetime
        request_data["cancel_datetime"] = None
        self.insert(request_data=request_data)
        return {"message": "Reservation created successfully.",
                "payload": request_data}

    @classmethod
    def insert(cls, *, request_data):
        """Docstring here."""
        connection = pymysql.connect(host="localhost", user="root", password="123456",
                                     db="anonymouse", charset="utf8mb4",
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = """INSERT INTO reservation
                (`account_id`, `movie_screen_id`, `head_count`,
                 `reserve_datetime`, `cancel_datetime`)
                 VALUES (%s, %s, %s, %s, %s)"""
                new_reservation = (request_data.get("account_id"),
                                   request_data.get("movie_screen_id"),
                                   request_data.get("head_count"),
                                   request_data["reserve_datetime"],
                                   request_data["cancel_datetime"])
                cursor.execute(sql, new_reservation)
            connection.commit()
        except:
            return {"message": "An error occured."}, 500
        finally:
            connection.close()

    @jwt_required()
    def put(self):
        """Modify a reservation."""
        if request.path == "/reservation/update":
            request_data = Reservation.parser.parse_args()
            account_id = request_data.get("account_id", None)
            movie_screen_id = request_data.get("movie_screen_id", None)
            reservation_ = self.find_id_by_account_movie_screen(account_id=account_id,
                                                                movie_screen_id=movie_screen_id)

            if not reservation_:
                current_datetime = dt.now().strftime("%Y-%m-%d %H:%M:%S")
                request_data["reserve_datetime"] = current_datetime
                request_data["cancel_datetime"] = None
                self.insert(request_data=request_data)
                return {"message": "Reservation inserted successfully.",
                        "payload": request_data}, 201
            else:
                request_data["id"] = reservation_.get("id", None)
                self.update(request_data=request_data)
                return {"message": "Reservation updated successfully.",
                        "payload": request_data}, 201

        elif request.path == "/reservation/cancel":
            Reservation.parser.remove_argument("head_count")
            request_data = Reservation.parser.parse_args()
            account_id = request_data.get("account_id", None)
            movie_screen_id = request_data.get("movie_screen_id", None)
            reservation_ = self.find_id_by_account_movie_screen(account_id=account_id,
                                                                movie_screen_id=movie_screen_id)

            if reservation_:
                if reservation_.get("cancel_datetime", None):
                    return {"message": "Reservation cancelled successfully.",
                            "payload": {"reservation_id": reservation_["id"]}}, 201
                reservation_id = reservation_.get("id")
                cancel_datetime = dt.now().strftime("%Y-%m-%d %H:%M:%S")
                self.cancel(id_=reservation_id,
                            cancel_datetime=cancel_datetime)
                return {"message": "Reservation cancelled successfully.",
                        "payload": {"reservation_id": reservation_["id"]}}, 201
            else:
                return {"message": "Reservation doesn't exist."}, 400

    @classmethod
    def update(cls, *, request_data):
        """Docstring here."""
        connection = pymysql.connect(host="localhost", user="root", password="123456",
                                     db="anonymouse", charset="utf8mb4",
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = """UPDATE reservation SET `head_count`=%s,
                         `movie_screen_id`=%s WHERE id=%s;"""
                updated_reservation = (request_data.get("head_count"),
                                       request_data.get("movie_screen_id"),
                                       request_data.get("id"))
                cursor.execute(sql, updated_reservation)
            connection.commit()
        except:
            return {"message": "An error occured."}, 500
        finally:
            connection.close()

    @classmethod
    def cancel(cls, *, id_, cancel_datetime):
        """Docstring here."""
        connection = pymysql.connect(host="localhost", user="root", password="123456",
                                     db="anonymouse", charset="utf8mb4",
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = """UPDATE reservation SET `cancel_datetime`=%s WHERE id=%s"""
                updated_reservation = (cancel_datetime, id_)
                cursor.execute(sql, updated_reservation)
            connection.commit()
        except:
            return {"message": "An error occured."}, 500
        finally:
            connection.close()


class ReservationList(Resource):
    """Docstring here."""

    def get(self):
        """Get all of reservations in our system."""
        connection = pymysql.connect(host="localhost", user="root", password="123456",
                                     db="anonymouse", charset="utf8mb4",
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM reservation;"
                cursor.execute(sql)
                rows = cursor.fetchall()
        except:
            return {"message": "An error occured."}, 500
        finally:
            connection.close()

        for row in rows:
            if row["reserve_datetime"]:
                row["reserve_datetime"] = row["reserve_datetime"].strftime("%Y-%m-%d %H:%M:%S")
            if row["cancel_datetime"]:
                row["cancel_datetime"] = row["cancel_datetime"].strftime("%Y-%m-%d %H:%M:%S")
        return {"reservations": rows}, 200
