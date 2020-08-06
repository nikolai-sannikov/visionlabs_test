from io import BytesIO
from PIL import Image

def encode_image_base64(pillow_image):        
    byteIOBuffer = BytesIO()
    pillow_image.save(byteIOBuffer, format='JPEG')
    byte_array = byteIOBuffer.getvalue()
    return byte_array

def decode_image_base64(base64_string):        
    decoded_image = Image.open(BytesIO(base64_string))
    return decoded_image