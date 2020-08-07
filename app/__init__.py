from flask import Flask
from config import config   

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from app.errors import errors
    app.register_blueprint(errors)    

    from app.images import images_api as images_api_blueprint
    app.register_blueprint(images_api_blueprint)

    return app