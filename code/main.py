from marshmallow import ValidationError
from flask import jsonify

from app import create_app


app = create_app()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    """Handle the error made by marshmallow."""
    return jsonify({"message": err.messages})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
