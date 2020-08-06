from io import BytesIO
from PIL import Image
import base64

def encode_image_base64(pillow_image):        
    byteIOBuffer = BytesIO()
    pillow_image.save(byteIOBuffer, format='JPEG')
    byte_array = byteIOBuffer.getvalue()

    base64_encoded = base64.b64encode(byte_array)
    return str(base64_encoded.decode("utf-8"))

def decode_image_base64(base64_string):  
    base64_decoded = base64.b64decode(base64_string)

    decoded_image = Image.open(BytesIO(base64_decoded))
    return decoded_image