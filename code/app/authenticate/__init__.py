"""JWT Authentication."""

from flask_jwt import JWT

from .security import authenticate, identity

jwt = JWT(authentication_handler=authenticate,
          identity_handler=identity)

from . import errors
