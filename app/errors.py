from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException
import logging

log = logging.getLogger("ImagesLogger")
errors = Blueprint('errors', __name__)

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

    @property
    def args(self):
        return self.payload

def get_error_summary(error):
    error_summary = {
            'type': error.__class__.__name__,
            'message': getattr(error, 'message', ''),
            'args': [str(x) for x in error.args]
        }
    return error_summary


@errors.app_errorhandler(HTTPException)
def handle_werkzeug_exception(e):    
    # replace the body with JSON
    response = {        
        "type": e.name,
        "message": e.description,        
    }
    return jsonify(response) ,e.code

@errors.app_errorhandler(InvalidUsage)
def handle_expected_error(error):
    log.debug(error)
    status_code = getattr(error, 'status_code', 500)
    response = {
        'success': False,
        'error': get_error_summary(error)
    }
    return jsonify(response), status_code

@errors.app_errorhandler(Exception)
def handle_unexpected_error(error):
    
    log.exception(get_error_summary(error))
    #provide real status_code to the public
    status_code = getattr(error, 'status_code', 500)
    public_response = {
        'success': False,
        'error': {
            'type': "UnknownServerException",
            'message': "Something went wrong"
        }
    }
    return jsonify(public_response), status_code