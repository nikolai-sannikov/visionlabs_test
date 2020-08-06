import os
from flask import jsonify
from flask import current_app

class ImageMetadata:
    def __init__(self, filename, dir_path):
        self.filename = filename

        # do not waste processing power on verification of image integrity
        # assume file extension is enough to catch all non-image files     
        self.name, file_extension = os.path.splitext(filename)
        assert file_extension in current_app.config["SUPPORTED_IMAGE_FILE_EXTENSIONS"], file_extension + " extension is not listed as a supported one"
        
        file_path = os.path.join(dir_path,filename)
        self.size = os.path.getsize(file_path)
        # time is provided in a format of a UNIX timestamp
        self.modification_time = os.path.getmtime(file_path)
        
    def to_dict(self):
        return {
            'file_name': self.filename,
            'size': self.size,
            'last_modification_time': self.modification_time
            }