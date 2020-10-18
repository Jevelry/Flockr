"""
Replace this with your own docstring
I just want to pass pipeline
Also uncomment out "import sys"!!!!!!!!!!!!!!
"""
#import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import auth

def defaultHandler(err):
    """
    Replace this with your own docstring.
    I just want to pass pylint
    """
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    """
    Replace this with your own docstring.
    I just want to pass pylint
    """
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })


@APP.route("/auth/register", methods=["POST"])
def register():
    """
    Registers user using http
    """
    data = request.get_json()
    first = data['name_first']
    last = data['name_last']
    email = data['email']
    password = data['password']
    return auth.auth_register(email, password, first, last)

if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
