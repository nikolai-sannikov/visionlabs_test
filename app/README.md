##### Intentional file fuctionality
```errors.py``` - provides handlers for:
* expected api usage errors - return serialized custom ```InvalidUsage``` exception
* unexpected exceptions - return non-informative server error, log real exception

```image_utils.py``` - provides functions for base64 image encoding and decoding.

```images.py``` - handles outing and API methods for the outlined functionality

```models.py``` - created classes to constuct image file metadata for image listing

```__init__.py``` - provides runnable app and handles ```$flask test``` cli command
