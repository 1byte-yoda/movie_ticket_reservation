from werkzeug.security import safe_str_cmp
from marshmallow.validate import ValidationError
from flask_restful import Resource, request
from flask_jwt_extended import get_jwt_identity, get_jwt_claims, jwt_required

from db import db
from .response_messages import (
    INVALID_ALREADY_LOGIN_400,
    ACCOUNT_EXISTS_MESSAGE_400,
    ACCOUNT_CREATED_MESSAGE_201,
    ACCOUNT_DELETED_MESSAGE_202,
    ACCOUNT_NOT_FOUND_MESSAGE_404,
    INVALID_REQUEST_ADMIN_MESSAGE_401,
    UNKNOWN_ERROR_MESSAGE_500
)
from ..models.movie_rating import MovieRatingModel
from ..models.account import AccountModel
from ..models.location import LocationModel
from ..models.barangay import BarangayModel
from ..models.user import UserModel
from ..schemas.user import UserSchema
from ..schemas.account import AccountSchema


class UserRegisterResource(Resource):
    """Contains the REST API endpoints for User Registration."""

    user_schema = UserSchema(exclude=["cinema"])

    def post(cls):
        """POST method that handles the /api/user/register endpoint.

        Description
        -----------
        This will create a new entry in the user and account table.
        """
        is_logged_in = get_jwt_identity()
        if is_logged_in:
            return ({"message": INVALID_ALREADY_LOGIN_400}, 400)
        user_data = request.get_json()
        try:
            user_data = cls.user_schema.load(user_data)
        except ValidationError as err:
            return {"message": err.messages}
        if AccountModel.find_by_email(email=user_data["account"]["email"]):
            return {"message": ACCOUNT_EXISTS_MESSAGE_400}, 400
        new_account = AccountModel(**user_data["account"])
        location = LocationModel(
            barangay_id=user_data["location"]["barangay"]["id"],
            latitude=user_data["location"]["latitude"],
            longitude=user_data["location"]["longitude"]
        )
        user = UserModel(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            contact_no=user_data["contact_no"],
            account=new_account,
            location=location
        )
        try:
            user.save_to_db()
        except Exception as e:
            print(e)
            db.session.rollback()
            db.session.flush()
            return ({"message": UNKNOWN_ERROR_MESSAGE_500}, 500)
        return {"message": ACCOUNT_CREATED_MESSAGE_201}, 201


class UserResource(Resource):
    """Contains the REST API endpoints for User in general."""

    account_schema = AccountSchema(only={"email"})

    @classmethod
    @jwt_required
    def delete(cls) -> tuple:
        """POST method that handles the /api/user/delete endpoint.

        Description
        -----------
        This will delete a user entry in the user and account table.
        """
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
                    user = UserModel.find_by_account_id(id=account.id)
                    if user:
                        try:
                            user.remove_from_db()
                        except:
                            db.session.rollback()
                            db.session.flash()
                            return ({"message": UNKNOWN_ERROR_MESSAGE_500}, 500)
                        try:
                            account.remove_from_db()
                        except:
                            db.session.rollback()
                            db.session.flash()
                            return ({"message": UNKNOWN_ERROR_MESSAGE_500}, 500)
                        return {"message": ACCOUNT_DELETED_MESSAGE_202}, 202
                return {"message": ACCOUNT_NOT_FOUND_MESSAGE_404}, 404
        return {"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401
