import os
from logging.config import dictConfig


class Config:
    # folder to store images
    IMAGES_PATH = os.environ.get('IMAGES_PATH') or '/tmp/visionlabs_test/images'

    # non-supported file extensions will not be available to users
    SUPPORTED_IMAGE_FILE_EXTENSIONS = {'.jpg'}

    @staticmethod
    def init_app(app):
        pass


class TestConfig(Config):
    IMAGES_PATH = os.environ.get('IMAGES_PATH') or '/tmp/visionlabs_test/test_ images'    
    # delete directory containing images obtained during automated testing
    CLEAR_IMAGES_AT_END = True


config = {
    'default': Config,
    'testing': TestConfig
}

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {
        'wsgi': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'},
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})