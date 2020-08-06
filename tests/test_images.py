
import unittest
from flask import current_app
from app import create_app
from app.image_utils import encode_image_base64

from PIL import Image
import requests
import io
import os
import shutil

import base64

class ImageTests(unittest.TestCase):
    IMAGE_URLS=[
        'https://upload.wikimedia.org/wikipedia/en/7/7d/Lenna_%28test_image%29.png',
        'https://vignette.wikia.nocookie.net/mlp/images/4/4b/Rainbow_Dash_Wonderbolt_fantasy_cropped_S1E3.png',
        'https://www.researchgate.net/profile/Seyed_Mohammad_Hossein_Hasheminejad/publication/329563816/figure/fig3/AS:730801767473152@1551248127055/The-cameraman-picture-with-256-256-size_Q640.jpg'
    ]

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)
    
    def tearDown(self):                
        test_images_directory = self.app.config["IMAGES_PATH"]
        
        if os.path.exists(test_images_directory) and self.app.config["CLEAR_IMAGES_AT_END"] == True:
            shutil.rmtree(test_images_directory)        
        self.app_context.pop()

    @staticmethod
    def download_images():
        images = []

        for image_url in ImageTests.IMAGE_URLS:
            response = requests.get(image_url, stream=True)
            response.raw.decode_content = True
            image = Image.open(response.raw)    
            
            images.append(image)
        return images
    

    def test_new_image_add(self):
        images = self.download_images()                
        images_encoded = [encode_image_base64(img) for img in images]     

        for image_encoded in images_encoded[:1]:            
            response = self.client.post("/image", data=image_encoded)
            print(response.data)