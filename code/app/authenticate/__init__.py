"""JWT Authentication."""
from flask_jwt_extended import JWTManager

from ..api.models.user import UserModel
from .blacklist import BLACK_LIST


jwt = JWTManager()


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    """Add claims that we can use when we log in."""
    return {"type": user.account.type}


@jwt.user_identity_loader
def user_identity_lookup(user):
    """Add identity for creating jwt access token."""
    return user.id


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    """Add the current UserModel Object to the current session."""
    return UserModel.find_by_id(id=identity)


@jwt.token_in_blacklist_loader
def check_blacklist_token(decrypted_token):
    """Check for blacklisted tokens. Will be used to implement logout endpoint."""
    return decrypted_token["jti"] in BLACK_LIST
