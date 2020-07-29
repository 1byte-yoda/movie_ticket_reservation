from flask import jsonify
from . import jwt


@jwt.jwt_error_handler
def customized_jwt_error_handler(error):
    """Error handler when a JWT error occured."""
    return jsonify({
        "message": error.description,
        "code": error.status_code
    }), error.status_code
