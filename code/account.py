import pymysql
from flask_restful import Resource, reqparse


class Account:
    """Proxy class to substitute database user table."""

    TABLE_NAME = "account"

    def __init__(self, *, id, email, password):
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


class AccountRegister(Resource):
    """Docstring Here."""

    TABLE_NAME = "account"

    parser = reqparse.RequestParser()
    parser.add_argument(name="email", type=str, required=True,
                        help="This field cannot be left blank!")
    parser.add_argument(name="password", type=str, required=True,
                        help="This field cannot be left blank!")

    def post(self):
        """Docstring Here."""
        data = AccountRegister.parser.parse_args()

        if Account.find_by_email(email=data["email"]):
            return {"message": "Account with that email already exists."}, 400

        connection = pymysql.connect(host="localhost", user="root", password="123456",
                                     db="anonymouse", charset="utf8mb4",
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = f"INSERT INTO {self.TABLE_NAME} (`email`, `password`) VALUES (%s, %s);"
                cursor.execute(sql, (data["email"], data["password"]))
                connection.commit()
        finally:
            connection.close()
        return {"message": "Account created successfully."}, 201
