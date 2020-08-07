import os

from flask import jsonify, current_app


_SUPPORTED_EXTENSIONS = current_app.config["SUPPORTED_IMAGE_FILE_EXTENSIONS"]


class ImageMetadata:
    """Retrieves metadata for files, checks for a supported extension.
    Inputs: filename and directory path
    Uses os functions to retrieve file size and last modification time.
    Is serializeable to dictionary.
    """

    def __init__(self, filename, dir_path):
        self.filename = filename

        # does not verify image integrity (doesn't actually try to open it)
        # assume file extension is enough to catch all non-image files
        self.name, file_extension = os.path.splitext(filename)
        assert file_extension in _SUPPORTED_EXTENSIONS, \
            file_extension + " extension is not listed as a supported one"

        file_path = os.path.join(dir_path, filename)
        self.size = os.path.getsize(file_path)
        # time is provided in a format of a UNIX timestamp
        self.modification_time = os.path.getmtime(file_path)

    def to_dict(self):
        return {
            'file_name': self.filename,
            'size': self.size,
            'last_modification_time': self.modification_time
            }
