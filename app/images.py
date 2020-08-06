import os
from io import BytesIO
import base64
import string

from flask import Blueprint, request, jsonify, current_app
from PIL import Image

import random

from app.image_utils import decode_image_base64

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
    