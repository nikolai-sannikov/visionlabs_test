import logging
import sys

from flask import Flask
from config import config

app = Flask(__name__)


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    stdout_handler = logging.StreamHandler(sys.stdout)    
    logger = logging.getLogger("ImagesLogger")
    logger.setLevel(logging.INFO)
    logger.addHandler(stdout_handler)

    with app.app_context():
        from app.errors import errors
        app.register_blueprint(errors)

        from app.images import images_api as images_api_blueprint
        app.register_blueprint(images_api_blueprint)

    return app


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest        
    
    stdout_handler = logging.StreamHandler(sys.stdout)    
    logger = logging.getLogger("TestLog")
    logger.setLevel(logging.INFO)
    logger.addHandler(stdout_handler)

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
