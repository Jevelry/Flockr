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
import channel
import channels
import message

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

@APP.route("/channel/join",methods=['POST'])
def join():
    """
    Adds a user to a public channel using http
    """
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    return channel.channel_join(token, channel_id)

@APP.route("/channel/addowner",methods=['POST'])
def addowner():
    """
    Adds a user to as an owner to a channel using http
    """
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    u_id = data['u_id']
    return channel.channel_addowner(token, channel_id, u_id)

@APP.route("/channel/removeowner",methods=['POST'])
def removeowner():
    """
    Removes a user to as an owner to a channel using http
    """
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    u_id = data['u_id']
    return channel.channel_removeowner(token, channel_id, u_id)

@APP.route("/message/send",methods=['POST'])
def send_message():
    """
    Sends a message to a channel using http
    """
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    message = data['message']
    return message.message_send(token, channel_id, message)

@APP.route("/message/remove",methods=['DELETE'])
def remove_message():
    """
    Remove a message from the channel using http
    """
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']
    return message.message_remove(token, message_id)

@APP.route("/message/edit",methods=['PUT'])
def edit_message():
    """
    Edit a message from the channel using http
    """
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']
    message = data['message']
    return message.message_remove(token, message_id, message)

if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
