from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_raw_jwt
)
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from werkzeug.security import safe_str_cmp

from ...authenticate.blacklist import BLACK_LIST
from ..models.account import AccountModel
from ..models.parsers import BaseParser


class AccountRegisterResource(Resource):
    """Docstring Here."""

    def post(self):
        """Docstring Here."""
        expected_input = {"email": str, "password": str, "type": str}
        data = BaseParser.parse_expected_input(dict_=expected_input)

        if AccountModel.find_by_email(email=data["email"]):
            return {"message": "Account with that email already exists."}, 400

        new_account = AccountModel(**data)
        new_account.register()
        return {"message": "Account created successfully."}, 201


class AccountLoginResource(Resource):
    """Docstring here."""

    @classmethod
    def post(cls):
        expected_input = {"email": str, "password": str}
        data = BaseParser.parse_expected_input(dict_=expected_input)
        email = AccountModel.find_by_email(email=data["email"])

        if email and safe_str_cmp(email.password, data["password"]):
            access_token = create_access_token(identity=email, fresh=True)
            refresh_token = create_refresh_token(identity=email)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200
        return {"message": "Invalid Credentials"}, 401


class AccountLogoutResource(Resource):
    """Docstring here."""

    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]
        BLACK_LIST.add(jti)
        return {"message": "Logged out successfully."}, 201
