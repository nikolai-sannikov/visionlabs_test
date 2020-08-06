import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    IMAGES_PATH = './images'

    @staticmethod
    def init_app(app):
        pass

class TestConfig(Config):
    IMAGES_PATH = './test_images'
    CLEAR_IMAGES_AT_END = False

config = {
    'default': Config,
    'testing': TestConfig
}