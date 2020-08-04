from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_optional,
    get_raw_jwt,
    get_jwt_claims,
    get_jwt_identity,
    get_current_user,
)
from flask_restful import Resource
from flask import request
from werkzeug.security import safe_str_cmp
from marshmallow.exceptions import ValidationError

from ...authenticate.blacklist import BLACK_LIST
from ..models.account import AccountModel
from ..models.user import UserModel
from .response_messages import (
    ACCOUNT_NOT_FOUND_MESSAGE_404,
    INVALID_ACCOUNT_MESSAGE_401,
    ACCOUNT_LOGGED_OUT_MESSAGE_201,
    INVALID_REQUEST_ADMIN_MESSAGE_401,
    INVALID_ALREADY_LOGIN_400,
    ACCOUNT_DELETED_MESSAGE_202,
    ACCOUNT_UPDATED_MESSAGE_202,
)
from ..schemas.account import AccountSchema


class AccountRegisterResource(Resource):
    """Docstring Here."""

    @classmethod
    def post(cls):
        """Docstring Here."""
        pass


class AccountLoginResource(Resource):
    """Docstring here."""

    account_schema = AccountSchema()

    @classmethod
    @jwt_optional
    def post(cls):
        is_logged_in = get_jwt_identity()
        print(get_jwt_identity())
        if is_logged_in:
            return ({"message": INVALID_ALREADY_LOGIN_400}, 400)
        account_data = request.get_json()
        try:
            account_data = cls.account_schema.load(account_data)
        except ValidationError as err:
            return {"message": err.messages}
        account = AccountModel.find_by_email(email=account_data["email"])
        if account and safe_str_cmp(account.password, account_data["password"]):
            user = UserModel.find_by_account_id(id=account.id)
            access_token = create_access_token(identity=user, fresh=True)
            refresh_token = create_refresh_token(identity=user)
            return (
                {"access_token": access_token, "refresh_token": refresh_token},
                201,
            )
        return {"message": INVALID_ACCOUNT_MESSAGE_401}, 401

    @classmethod
    @jwt_required
    def put(cls) -> tuple:
        current_user = get_current_user().account
        if current_user:
            try:
                update_data = request.get_json()
                update_data = cls.account_schema.load(update_data)
            except ValidationError as err:
                return {"message": err.messages}
            current_user.update(update_data=update_data)
            return {"message": ACCOUNT_UPDATED_MESSAGE_202}, 202
        return {"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401


class AccountLogoutResource(Resource):
    """Docstring here."""

    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]
        BLACK_LIST.add(jti)
        return {"message": ACCOUNT_LOGGED_OUT_MESSAGE_201}, 201


class AccountResource(Resource):
    """Docstring here."""

    account_schema = AccountSchema()

    @classmethod
    @jwt_required
    def get(cls) -> tuple:
        claims = get_jwt_claims()
        if claims:
            if safe_str_cmp(claims.get("type"), "admin"):
                try:
                    account_data = request.get_json()
                    account_data = cls.account_schema.load(account_data)
                except ValidationError as err:
                    return {"message": err.messages}
                account = AccountModel.find_by_email(email=account_data["email"])
                if account:
                    return {"account": cls.account_schema.dump(account)}, 200
                return {"message": ACCOUNT_NOT_FOUND_MESSAGE_404}, 404
        return {"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401
