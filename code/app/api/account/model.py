import pymysql


class AccountModel:
    """Proxy class to substitute database user table."""

    TABLE_NAME = "account"

    def __init__(self, *, id=None, email="", password=""):
        """Docstring here."""
        self.id = id
        self.email = email
        self.password = password

    @classmethod
    def find_by_email(cls, *, email):
        """Docstring here."""
        connection = pymysql.connect(host="localhost", user="root", password="123456",
                                     db="anonymouse", charset="utf8mb4",
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                query = f"SELECT * FROM {cls.TABLE_NAME} WHERE email=%s"
                cursor.execute(query, (email,))
                row = cursor.fetchone()
                if row:
                    account = cls(**row)
                else:
                    account = None
        finally:
            connection.close()
        return account

    @classmethod
    def find_by_id(cls, *, _id):
        """Docstring here."""
        connection = pymysql.connect(host="localhost", user="root", password="123456",
                                     db="anonymouse", charset="utf8mb4",
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                query = f"SELECT * FROM {cls.TABLE_NAME} WHERE id=%s"
                cursor.execute(query, (_id,))
                row = cursor.fetchone()
                if row:
                    account = cls(**row)
                else:
                    account = None
        finally:
            connection.close()
        return account

    def register(self):
        """Docstring here."""
        connection = pymysql.connect(host="localhost", user="root", password="123456",
                                     db="anonymouse", charset="utf8mb4",
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = f"INSERT INTO {self.TABLE_NAME} (`email`, `password`) VALUES (%s, %s);"
                cursor.execute(sql, (self.email, self.password))
                connection.commit()
        except:
            return {"message": "An error occured."}, 500
        finally:
            connection.close()
