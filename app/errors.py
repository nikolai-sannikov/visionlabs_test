import logging

from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException, InternalServerError


log = logging.getLogger("ImagesLogger")
errors = Blueprint('errors', __name__)


class InvalidUsage(Exception):
    def __init__(self, description, status_code=400, payload=[]):
        Exception.__init__(self)
        self.description = description
        self.status_code = status_code or 400
        self.payload = payload

    def to_dict(self):
        result = {'args': self.payload}
        result['message'] = self.description
        return result

    @property
    def args(self):
        return self.payload


def get_error_summary(error):
    error_summary = {
            'type': error.__class__.__name__,
            'message': getattr(error, 'description', ''),
            'args': [str(x) for x in error.args]
        }
    return error_summary


@errors.app_errorhandler(HTTPException)
def handle_werkzeug_exception(e):
    # replace the body with JSON
    response = {
        "success": False,
        "error": {
            "type": e.name,
            "message": e.description
        }
    }
    return jsonify(response), e.code


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
def handle_unexpected_exception(exception):
    # write a real exception to logs
    log.exception(get_error_summary(exception))
    # give a non-informative error to the public
    raise InternalServerError("Something went wrong")
