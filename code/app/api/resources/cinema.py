from werkzeug.security import safe_str_cmp
from flask_restful import Resource, request
from flask_jwt_extended import (
    get_current_user,
    get_jwt_claims,
    get_jwt_identity,
    jwt_required,
    jwt_optional
)
from marshmallow.validate import ValidationError

from db import db
from .response_messages import (
    CINEMA_NOT_FOUND_404,
    INVALID_REQUEST_ADMIN_MESSAGE_401,
    INVALID_ALREADY_LOGIN_400,
    ACCOUNT_EXISTS_MESSAGE_400,
    ACCOUNT_CREATED_MESSAGE_201,
    UNKNOWN_ERROR_MESSAGE_500,
    ACCOUNT_NOT_FOUND_MESSAGE_404,
    ACCOUNT_DELETED_MESSAGE_202
)
from ..models.cinema import CinemaModel
from ..models.location import LocationModel
from ..models.account import AccountModel
from ..models.user import UserModel
from ..schemas.cinema import CinemaSchema
from ..schemas.user import UserSchema
from ..schemas.account import AccountSchema


class CinemaResource(Resource):
    """Contains the REST API endpoints for a Cinema."""

    cinema_schema = CinemaSchema()

    @classmethod
    @jwt_required
    def get(cls, cinema_id: int):
        """GET method that handles the /api/cinema/<int:cinema_id> endpoint.

        Description
        -----------
        This will get the cinema info for the current logged in
        user.
        """
        claims = get_jwt_claims()
        if claims:
            if safe_str_cmp(claims.get("type"), "admin"):
                user = get_current_user()
                if not user.cinema_id == cinema_id:
                    return ({"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401)
                cinema = CinemaModel.find_by_id(id=user.cinema_id)
                if cinema:
                    return ({"cinema": cls.cinema_schema.dump(cinema.json())}, 200)
                return ({"message": CINEMA_NOT_FOUND_404}, 404)
        return ({"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401)


class CinemaUserResourse(Resource):
    """Contains the REST API endpoint for Cinema-User transactions."""

    user_schema = UserSchema()

    @classmethod
    @jwt_optional
    def post(cls):
        """POST method that handles the /api/cinema/register endpoint.

        Description
        -----------
        This will create a new entry in the cinema, location, user and account table.
        """
        is_logged_in = get_jwt_identity()
        if is_logged_in:
            return {"message": INVALID_ALREADY_LOGIN_400}, 400
        user_data = request.get_json()
        try:
            user_data = cls.user_schema.load(user_data)
        except ValidationError as err:
            return {"message": err.messages}
        if AccountModel.find_by_email(email=user_data["account"]["email"]):
            return {"message": ACCOUNT_EXISTS_MESSAGE_400}, 400
        new_account = AccountModel(**user_data["account"])
        new_location = LocationModel(
            barangay_id=user_data["location"]["barangay"]["id"],
            longitude=user_data["location"]["longitude"],
            latitude=user_data["location"]["latitude"]
        )
        new_cinema = CinemaModel(**user_data["cinema"])
        new_cinema_user = UserModel(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            contact_no=user_data["contact_no"],
            location=new_location,
            account=new_account,
            cinema=new_cinema
        )
        try:
            new_cinema_user.save_to_db()
        except Exception as e:
            print(e)
            db.session.rollback()
            db.session.flush()
            return ({"message": UNKNOWN_ERROR_MESSAGE_500}, 500)
        return ({"message": ACCOUNT_CREATED_MESSAGE_201}, 201)

    def put(self):
        pass

    @classmethod
    @jwt_required
    def delete(self):
        """DELETE method that handles the /api/cinema/delete endpoint.

        Description
        -----------
        FOR TESTING ONLY
        This will delete a row in the related tables: cinema, location, user, account
        """
        claims = get_jwt_claims()
        if claims:
            if safe_str_cmp(claims.get("type"), "super_admin"):
                user_schema = AccountSchema(only={"email"})
                try:
                    user_data = user_schema.load(request.get_json())
                except ValidationError as err:
                    return {"message": err.messages}

                account = AccountModel.find_by_email(email=user_data["email"])
                if not account:
                    return ({"message": ACCOUNT_NOT_FOUND_MESSAGE_404}, 404)
                if not safe_str_cmp(account.type, "admin"):
                    return ({"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401)

                user = UserModel.find_by_account_id(id=account.id)
                cinema = CinemaModel.find_by_id(id=user.cinema_id)
                location = LocationModel.find_by_id(id=user.location_id)
                try:
                    db.session.delete(user)
                    db.session.delete(account)
                    db.session.delete(cinema)
                    db.session.delete(location)
                    db.session.commit()
                except:
                    db.session.rollback()
                    db.session.flush()
                    return ({"message": UNKNOWN_ERROR_MESSAGE_500}, 500)
                return ({"message": ACCOUNT_DELETED_MESSAGE_202}, 202)
        return ({"message": INVALID_REQUEST_ADMIN_MESSAGE_401}, 401)
