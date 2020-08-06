from flask import Blueprint, jsonify
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
        return (self.message, self.payload)

def get_error_summary(error):
    message = [str(x) for x in error.args]
    error_summary = {
            'type': error.__class__.__name__,
            'message': message
        }
    return error_summary

def log_error(error):
    log_entry = {        
        'error': get_error_summary(error)
    }
    log.exception(log_entry)

@errors.app_errorhandler(InvalidUsage)
def handle_error(error):
    status_code = getattr(error, 'status_code', 500)
    response = {
        'success': False,
        'error': get_error_summary(error)
    }
    return jsonify(response), status_code

@errors.app_errorhandler(Exception)
def handle_error(error):
    
    log_error(error)

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