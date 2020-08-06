import os
from io import BytesIO
import base64
import string

from flask import Blueprint, request, jsonify, current_app
from PIL import Image

import random

from app.image_utils import decode_image_base64
from app.models import *

images_api = Blueprint('images_api', __name__)

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
        
    decoded_image = decode_image_base64(base64_encoded_image)

    # filename is not provided in encoded image
    images_directory = setup_images_directory()
    random_filename = get_random_string()+'.jpg'
    image_path = os.path.join(images_directory, random_filename)

    decoded_image.save(image_path)

    response = {'success':True, 'new_image_filename': random_filename}
    return jsonify(response), 200

@images_api.route('/image', methods=['GET'])
def list_images():

    images_dir_contents = []
    try:
        images_dir_contents= os.listdir(current_app.config["IMAGES_PATH"])    
    except FileNotFoundError:
        # if images directory was not found, assume it is not yet created
        # no action needed, it is created automatically on first image upload
        pass
    
    found_images = []
    for filename in images_dir_contents:                        
        try:
            image = ImageMetadata(filename, current_app.config["IMAGES_PATH"])
            found_images.append(image)
        except AssertionError as error:            
            # simply ignore all non-image or non-supported files
            pass        
        
    response = [image.to_dict() for image in found_images]   
    return jsonify(response),200
    

        