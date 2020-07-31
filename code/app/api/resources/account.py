from flask_restful import Resource, reqparse

from ..models.account import AccountModel


class AccountRegisterResource(Resource):
    """Docstring Here."""

    TABLE_NAME = "account"

    parser = reqparse.RequestParser()
    parser.add_argument(name="email", type=str, required=True,
                        help="This field cannot be left blank!")
    parser.add_argument(name="password", type=str, required=True,
                        help="This field cannot be left blank!")
    parser.add_argument(name="type", type=str, required=True,
                        help="This field cannot be left blank!")

    def post(self):
        """Docstring Here."""
        data = AccountRegisterResource.parser.parse_args()

        if AccountModel.find_by_email(email=data["email"]):
            return {"message": "Account with that email already exists."}, 400

        new_account = AccountModel(**data)
        new_account.register()
        return {"message": "Account created successfully."}, 201
