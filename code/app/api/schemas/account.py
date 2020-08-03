from ...serializer import ma
from ..models.account import AccountModel


class AccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AccountModel
        load_only = ("password")
