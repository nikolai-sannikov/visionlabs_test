from io import BytesIO
from PIL import Image
from base64 import b64encode, b64decode


def encode_image_base64(pillow_image):
    """Encodes image in a base64 string with UTF-8 representation
    Uses Pillow built-in function to convert image to a JPEG byte array.
    """
    byteIOBuffer = BytesIO()
    # write image in JPEG format to a byte buffer
    pillow_image.save(byteIOBuffer, format='JPEG')
    # flush IO buffer to an array
    byte_array = byteIOBuffer.getvalue()

    base64_encoded = b64encode(byte_array)
    # use string utf-8 representation for usage convenience
    return str(base64_encoded.decode("utf-8"))


def decode_image_base64(base64_string):
    """Decodes image from a base64 encoded string.
    Uses built-in Pillow function to get an image from decoded bytes.
    If the data is corrupted (or not an image), Pillow will fail to do that.
    """
    bytes_decoded = b64decode(base64_string)
    # load image from IO buffer filled from base64 decoding
    decoded_image = Image.open(BytesIO(bytes_decoded))
    return decoded_image
