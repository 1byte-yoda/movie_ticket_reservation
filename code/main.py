from marshmallow import ValidationError
from flask import jsonify

from app import create_app, db
from app.api.models.user import UserModel
from app.api.models.account import AccountModel
from app.api.models.location import LocationModel
from app.api.models.barangay import BarangayModel
from app.api.models.city import CityModel
from app.api.models.province import ProvinceModel


app = create_app()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    """Handle the error made by marshmallow."""
    return jsonify({"message": err.messages})


@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        UserModel=UserModel,
        AccountModel=AccountModel,
        LocationModel=LocationModel,
        BarangayModel=BarangayModel,
        CityModel=CityModel,
        ProvinceModel=ProvinceModel
    )
