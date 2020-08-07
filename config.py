import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    IMAGES_PATH = os.environ.get('IMAGES_PATH') or '/var/www/visionlabs_test/images'
    SUPPORTED_IMAGE_FILE_EXTENSIONS = {'.jpg'}

    @staticmethod
    def init_app(app):
        pass

class TestConfig(Config):
    IMAGES_PATH = os.environ.get('IMAGES_PATH') or '/var/www/visionlabs_test/images'
    CLEAR_IMAGES_AT_END = False

config = {
    'default': Config,
    'testing': TestConfig
}