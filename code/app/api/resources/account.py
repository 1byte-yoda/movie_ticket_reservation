from flask_jwt_extended import create_access_token, create_refresh_token, get_raw_jwt
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from werkzeug.security import safe_str_cmp

from ...authenticate.blacklist import BLACK_LIST
from ..models.account import AccountModel
from ..models.parsers import BaseParser
from .response_messages import (
    ACCOUNT_EXISTS_MESSAGE_400,
    INVALID_ACCOUNT_MESSAGE_401,
    ACCOUNT_CREATED_MESSAGE_201,
    ACCOUNT_LOGGED_OUT_MESSAGE_201,
)


REGISTER_EXPECTED_INPUT = {"email": str, "password": str, "type": str}
LOGIN_EXPECTED_INPUT = {"email": str, "password": str}


class AccountRegisterResource(Resource):
    """Docstring Here."""

    def post(self):
        """Docstring Here."""
        data = BaseParser.parse_expected_input(dict_=REGISTER_EXPECTED_INPUT)
        if AccountModel.find_by_email(email=data["email"]):
            return {"message": ACCOUNT_EXISTS_MESSAGE_400}, 400

        new_account = AccountModel(**data)
        new_account.register()
        return {"message": ACCOUNT_CREATED_MESSAGE_201}, 201


class AccountLoginResource(Resource):
    """Docstring here."""

    @classmethod
    def post(cls):
        data = BaseParser.parse_expected_input(dict_=LOGIN_EXPECTED_INPUT)
        email = AccountModel.find_by_email(email=data["email"])
        if email and safe_str_cmp(email.password, data["password"]):
            access_token = create_access_token(identity=email, fresh=True)
            refresh_token = create_refresh_token(identity=email)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        return {"message": INVALID_ACCOUNT_MESSAGE_401}, 401


class AccountLogoutResource(Resource):
    """Docstring here."""

    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]
        BLACK_LIST.add(jti)
        return {"message": ACCOUNT_LOGGED_OUT_MESSAGE_201}, 201
