import os
from io import BytesIO
import string
import random
import logging

from flask import Blueprint, request, jsonify, current_app, send_from_directory
from werkzeug.exceptions import NotFound
from PIL import Image

from app.image_utils import decode_image_base64
from app.models import *
from app.errors import InvalidUsage

images_api = Blueprint('images_api', __name__)
log = logging.getLogger("ImagesLogger")


def _setup_image_directory():
    # check if directory to store images exists
    images_directory = current_app.config["IMAGES_PATH"]
    if not os.path.exists(images_directory):
        os.makedirs(images_directory)
    return images_directory


def _get_random_string(length=10):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


@images_api.route('/image', methods=['POST'])
def add_image():
    """Recieve a string data representing base64 encoded image. Decode and save it.
    Input integrity is protected by attempting to open the decoded image with Pillow library.
    If the image is good, pillow can be used to save it to the designated folder.
    Image name is not provided on input and is generated automatically.
    """

    base64_encoded_image = request.data
    try:
        decoded_image = decode_image_base64(base64_encoded_image)
    except Exception as e:
        log.info(e)
        raise InvalidUsage("Could not decode image from the provided data", 400)

    # filename is not provided for an encoded image: generate it randomly
    images_directory = _setup_image_directory()
    random_filename = _get_random_string() + '.jpg'
    image_path = os.path.join(images_directory, random_filename)

    decoded_image.save(image_path, "JPEG")

    # reply with success code and the name of a newly added image
    response = {'success': True, 'new_image_filename': random_filename}
    return jsonify(response), 200


def _list_parent_dir_contents():
    try:
        images_dir_contents = os.listdir(current_app.config["IMAGES_PATH"])
        return images_dir_contents
    except FileNotFoundError:
        # if images directory was not found, assume it is not yet created
        # no action needed, it is created automatically on first image upload
        log.debug("Requested list of images, but images directory %s was not found", current_app.config["IMAGES_PATH"])
        return []


@images_api.route('/image', methods=['GET'])
def list_images():
    """Return image file metadata: file names, modification time, size.
    Modification time returned as UNIX timestamp, size in bytes.
    Non-supported file extensions are filtered out.
    """
    images_dir_contents = _list_parent_dir_contents()
    found_images = []
    for filename in images_dir_contents:
        try:
            # constructor returns assertion error if the provided file extension if not supported
            image = ImageMetadata(filename, current_app.config["IMAGES_PATH"])
            found_images.append(image)
        except AssertionError:
            log.warning("Images folder contains non-supported file: %s", filename)
            # simply ignore all files with a non-supported extension
            pass

    response = [image.to_dict() for image in found_images]
    return jsonify(response), 200


@images_api.route('/image', methods=['DELETE'])
def delete_image():
    """Deletes file from the storage directory by a specified username.
    If no extension provided, all supported files with same name will be deleted.
    Returns success if at least 1 file was deleted, failure if no matching files were found.
    """
    to_delete = request.data.decode('utf-8')

    # if filename to delete given without extension, all options of supported extensions will be removed
    filenames_to_delete = []
    if os.path.splitext(to_delete)[1] == "":
        filenames_to_delete = [to_delete + extension for extension in current_app.config["SUPPORTED_IMAGE_FILE_EXTENSIONS"]]
    else:
        filenames_to_delete = [to_delete]

    # in case extension is not provided and we are deleting every file with same name,
    # report successful delete if at least 1 file was deleted; otherwise, report failure
    something_was_deleted = False
    for filename_to_delete in filenames_to_delete:
        try:
            os.remove(os.path.join(current_app.config["IMAGES_PATH"], filename_to_delete))
            something_was_deleted = True
        except FileNotFoundError:
            # if no such file was found, ignore it; highly likely, it was just a bad extension guess
            pass

    if something_was_deleted:
        response = {'success': True, 'deleted_filename': filename_to_delete}
        return response, 200
    else:
        raise InvalidUsage("File does not exist", 400, payload=[filename_to_delete])


@images_api.route("/images/<string:filename>", methods=['GET'])
def get_file(filename):
    """Retrieve file from the storage directory by a specified name.
    Checks if the file extension is supported before sending the file.
    """
    file_extension = os.path.splitext(filename)[1]
    if file_extension not in current_app.config["SUPPORTED_IMAGE_FILE_EXTENSIONS"]:
        raise InvalidUsage("Extension is not supported", 400, [file_extension])
    # extension is supported, cas safely send the file
    try:
        return send_from_directory(current_app.config['IMAGES_PATH'], filename, as_attachment=False)
    except NotFound:
        raise InvalidUsage("Image with this name has not been found", 404, [current_app.config['IMAGES_PATH'], filename + file_extension])
