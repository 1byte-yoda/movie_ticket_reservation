import pymysql


class ReservationModel:
    """Docstring here."""

    def __init__(self, id=None, account_id=None, movie_screen_id=None, head_count=None,
                 reserve_datetime="", cancel_datetime=""):
        """Docstring here."""
        self.id = id
        self.account_id = account_id
        self.movie_screen_id = movie_screen_id
        self.head_count = head_count
        self.reserve_datetime = reserve_datetime
        self.cancel_datetime = cancel_datetime

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
                temp_reservation = cursor.fetchone()
        except:
            return {"message": "An error occured."}, 500
        finally:
            connection.close()

        if temp_reservation["reserve_datetime"]:
            temp_reservation["reserve_datetime"] = temp_reservation["reserve_datetime"].strftime("%Y-%m-%d %H:%M:%S")
        if temp_reservation["cancel_datetime"]:
            temp_reservation["cancel_datetime"] = temp_reservation["cancel_datetime"].strftime("%Y-%m-%d %H:%M:%S")
        return temp_reservation

    @classmethod
    def find_id_by_account_movie_screen(cls, *, account_id, movie_screen_id):  # Move this on its own class
        """Docstring here."""
        connection = pymysql.connect(host="localhost", user="root", password="123456",
                                     db="anonymouse", charset="utf8mb4",
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM reservation WHERE account_id=%s AND movie_screen_id=%s"
                cursor.execute(sql, (account_id, movie_screen_id))
                temp_reservation = cursor.fetchone()
        except:
            return {"message": "An error occured."}, 500
        finally:
            connection.close()

        if temp_reservation["reserve_datetime"]:
            temp_reservation["reserve_datetime"] = temp_reservation["reserve_datetime"].strftime("%Y-%m-%d %H:%M:%S")
        if temp_reservation["cancel_datetime"]:
            temp_reservation["cancel_datetime"] = temp_reservation["cancel_datetime"].strftime("%Y-%m-%d %H:%M:%S")
        return temp_reservation

    def insert(self):
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
                new_reservation = (self.account_id,
                                   self.movie_screen_id,
                                   self.head_count,
                                   self.reserve_datetime,
                                   self.cancel_datetime)
                cursor.execute(sql, new_reservation)
            connection.commit()
        except:
            return {"message": "An error occured."}, 500
        finally:
            connection.close()

    def update(self):
        """Docstring here."""
        connection = pymysql.connect(host="localhost", user="root", password="123456",
                                     db="anonymouse", charset="utf8mb4",
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = """UPDATE reservation SET `head_count`=%s,
                         `movie_screen_id`=%s WHERE id=%s;"""
                updated_reservation = (self.head_count,
                                       self.movie_screen_id,
                                       self.id)
                cursor.execute(sql, updated_reservation)
            connection.commit()
        except:
            return {"message": "An error occured."}, 500
        finally:
            connection.close()

    def cancel(self):
        """Docstring here."""
        connection = pymysql.connect(host="localhost", user="root", password="123456",
                                     db="anonymouse", charset="utf8mb4",
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = """UPDATE reservation SET `cancel_datetime`=%s WHERE id=%s"""
                updated_reservation = (self.cancel_datetime, self.id)
                cursor.execute(sql, updated_reservation)
            connection.commit()
        except:
            return {"message": "An error occured."}, 500
        finally:
            connection.close()


class ReservationListModel:
    """Docstring here."""

    @staticmethod
    def find_all_reservation():
        """Docstring here."""
        connection = pymysql.connect(host="localhost", user="root", password="123456",
                                     db="anonymouse", charset="utf8mb4",
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM reservation;"
                cursor.execute(sql)
                temp_reservations = cursor.fetchall()
        except:
            return {"message": "An error occured."}, 500
        finally:
            connection.close()

        for reservation in temp_reservations:
            if reservation["reserve_datetime"]:
                reservation["reserve_datetime"] = reservation["reserve_datetime"].strftime("%Y-%m-%d %H:%M:%S")
            if reservation["cancel_datetime"]:
                reservation["cancel_datetime"] = reservation["cancel_datetime"].strftime("%Y-%m-%d %H:%M:%S")
        return temp_reservations
