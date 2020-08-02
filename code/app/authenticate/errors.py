from flask import jsonify


# @jwt._set_error_handler_callbacks
def customized_jwt_error_handler(error):
    """Error handler when a JWT error occured."""
    return jsonify({
        "message": error.description,
        "code": error.status_code
    }), error.status_code
