
import unittest
from flask import current_app
from app import create_app
from app.image_utils import encode_image_base64

from PIL import Image
import requests
import io
import os
import logging
import shutil

import base64

# test cases rely on their order as listed in this file
unittest.TestLoader.sortTestMethodsUsing = None

log = logging.getLogger("TestLog")

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
    def delete_and_verify_deletion(filename_to_delete, client):
        log.info("Deleting file %s",filename_to_delete)
        client.delete("/image", data=filename_to_delete)                
        
        response = client.get("/image")                
        listed_files = [image_metadata['file_name'] for image_metadata in response.get_json()]

        if not filename_to_delete.endswith('.jpg'):
            filename_to_delete+='.jpg'
        assert filename_to_delete not in listed_files, "File with this name still exists in the list"

    @staticmethod
    def download_images():
        images = []

        for image_url in ImageTests.IMAGE_URLS:
            response = requests.get(image_url, stream=True)
            response.raw.decode_content = True
            image = Image.open(response.raw)    
            
            images.append(image)
        log.info("Retrieved %d images for future test out of %d", len(images), len(ImageTests.IMAGE_URLS))      
        return images

    def test_images_full_scenario(self):
        #download preset images to be used in testing from the web
        images = self.download_images()                 
        #encode images in base64  
        images_encoded = [encode_image_base64(img) for img in images]     

        self.image_filenames = []
        for image_encoded in images_encoded:            
            # send encoded images to the server
            response = self.client.post("/image", data=image_encoded)
            # success code 200 is expected in this case
            self.assertEqual(response.status_code, 200)
            # response should contain filename assigned to this image, store these filenames to verify their existense later
            self.assertTrue('new_image_filename' in response.get_json())
            self.image_filenames.append(response.get_json()['new_image_filename'])
        log.info("Created files: %s", str(self.image_filenames))
                
        #all the newly added files should be now listed
        response = self.client.get("/image")        
        log.debug(response.get_json())
        listed_files = [image_metadata['file_name'] for image_metadata in response.get_json()]
        for image_filename in self.image_filenames:
            self.assertTrue(image_filename in listed_files)

        # remove one new image from list with extension 
        filename_to_delete = self.image_filenames[-1]
        self.image_filenames = self.image_filenames[:-1]
        ImageTests.delete_and_verify_deletion(filename_to_delete, self.client)
        # and anouther one without
        filename_to_delete = self.image_filenames[-1]
        self.image_filenames = self.image_filenames[:-1]
        filename_to_delete = os.path.splitext(filename_to_delete)[0]
        ImageTests.delete_and_verify_deletion(filename_to_delete, self.client)

    def test_delete_non_existing_image(self):
        response = self.client.delete("/image", data="definitely_non_existent_image")
        log.debug(response.get_json())
        self.assertEqual(response.status_code, 400)
    
        