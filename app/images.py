import os
from io import BytesIO
import base64
import string
import logging
from app.errors import InvalidUsage, log_error

from flask import Blueprint, request, jsonify, current_app
from PIL import Image

import random

from app.image_utils import decode_image_base64
from app.models import *

images_api = Blueprint('images_api', __name__)
log = logging.getLogger("ImagesLogger")

def setup_images_directory():
    # check if directory to store images exists
    images_directory = current_app.config["IMAGES_PATH"]
    if not os.path.exists(images_directory):
        os.makedirs(images_directory)
    return images_directory

def get_random_string(length=10):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
    
@images_api.route('/image', methods=['POST'])
def add_image():
    #assume request data field contains base64-encoded image
    base64_encoded_image = request.data
    
    try:
        decoded_image = decode_image_base64(base64_encoded_image)
    except Exception as e:
        log_error(e)
        raise InvalidUsage("Could not decode image from the provided data", 400)

    # filename is not provided in encoded image
    images_directory = setup_images_directory()
    random_filename = get_random_string()+'.jpg'
    image_path = os.path.join(images_directory, random_filename)

    decoded_image.save(image_path)

    response = {'success':True, 'new_image_filename': random_filename}
    return jsonify(response), 200

def list_images_dir_contents():
    try:
        images_dir_contents= os.listdir(current_app.config["IMAGES_PATH"])
        return images_dir_contents
    except FileNotFoundError:
        log.debug("Requested list of images, but images directory %s was not found", current_app.config["IMAGES_PATH"])
        # if images directory was not found, assume it is not yet created
        # no action needed, it is created automatically on first image upload
        return []

@images_api.route('/image', methods=['GET'])
def list_images():
    images_dir_contents = list_images_dir_contents()
    found_images = []
    for filename in images_dir_contents:                        
        try:
            image = ImageMetadata(filename, current_app.config["IMAGES_PATH"])
            found_images.append(image)
        except AssertionError:            
            log.warning("Images folder contains non-supported file: %s",filename)
            # simply ignore all non-image or non-supported files
            pass        
        
    response = [image.to_dict() for image in found_images]   
    return jsonify(response),200
    
@images_api.route('/image', methods=['DELETE'])
def delete_image():
    to_delete = request.data.decode('utf-8')
    
    # if filename to delete given without extension, all options with supported extensions will be removed   
    filenames_to_delete = []
    if os.path.splitext(to_delete)[1] == "":        
        filenames_to_delete = [to_delete+extension for extension in current_app.config["SUPPORTED_IMAGE_FILE_EXTENSIONS"]]
    else:
        filenames_to_delete = [to_delete]

    something_was_deleted = False
    for filename_to_delete in filenames_to_delete:
        try:
            os.remove(os.path.join(current_app.config["IMAGES_PATH"],filename_to_delete))
            something_was_deleted = True            
        except FileNotFoundError:
            pass        
    
    if something_was_deleted:
        response ={'success':True, 'deleted_filename': filename_to_delete}
        return response, 200
    else:
        raise InvalidUsage("File does not exist", 400, filename_to_delete)
        
