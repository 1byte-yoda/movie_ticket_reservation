import os
import traceback

from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..utility import image_helper
from ..schemas.image import ImageSchema
from .response_messages import (
    IMAGE_UPLOADED_201,
    IMAGE_ILLEGAL_EXTENSION_400,
    IMAGE_ILLEGAL_FILENAME_400,
    IMAGE_NOT_FOUND_404,
    IMAGE_DELETED_200,
    IMAGE_DELETE_FAILED_500
)


image_schema = ImageSchema()


class ImageUpload(Resource):
    @jwt_required
    def post(self):
        """Use to upload an image file.

        path: /api/image/upload

        It uses JWT retrieve user information then saves the image to the user's folder.
        If there is a filename conflict, it appends a number at the end.
        """
        data = image_schema.load(request.files)  # {"image": FileStorage}
        folder = "__movies__"  # static/images/movies
        try:
            image_path = image_helper.save_image(data["image"], folder=folder)
            basename = image_helper.get_base_name(image_path)
            return ({"message": IMAGE_UPLOADED_201.format(basename)}, 201)
        except UploadNotAllowed:
            extension = image_helper.get_extension(data["image"])
            return ({"message": IMAGE_ILLEGAL_EXTENSION_400.format(extension)}, 400)


class ImageResource(Resource):
    def get(self, filename: str):
        """Return the requested image if it exists.

        path: /api/image/<filename>

        Look up inside the logged in user's folder.
        """
        folder = "__movies__"
        if not image_helper.is_filename_safe(filename):
            return ({"message": IMAGE_ILLEGAL_FILENAME_400.format(filename)}, 400)
        try:
            return send_file(image_helper.get_path(filename=filename, folder=folder))
        except FileNotFoundError:
            return ({"message": IMAGE_NOT_FOUND_404.format(filename)}, 404)

    @jwt_required
    def delete(self, filename: str):
        """Delete the requested image if it exists.

        path: /api/image/<filename>

        Look up inside the logged in user's folder. Then delete the image <filename>
        """
        folder = "__movies__"

        if not image_helper.is_filename_safe(filename):
            return ({"message": IMAGE_ILLEGAL_FILENAME_400.format(filename)}, 400)
        try:
            os.remove(image_helper.get_path(filename=filename, folder=folder))
            return ({"message": IMAGE_DELETED_200.format(filename)}, 200)
        except FileNotFoundError:
            return ({"message": IMAGE_NOT_FOUND_404.format(filename)}, 404)
        except:
            traceback.print_exc()
            return ({"message": IMAGE_DELETE_FAILED_500}, 500)
