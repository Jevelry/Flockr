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
import user
import other

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
    return dumps(auth.auth_register(email, password, first, last))

@APP.route("/channel/join", methods=['POST'])
def join():
    """
    Adds a user to a public channel using http
    """
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    return dumps(channel.channel_join(token, channel_id))

@APP.route("/channel/addowner",methods=['POST'])
def addowner():
    """
    Adds a user to as an owner to a channel using http
    """
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    u_id = data['u_id']
    return dumps(channel.channel_addowner(token, channel_id, u_id))

@APP.route("/channel/removeowner", methods=['POST'])
def removeowner():
    """
    Removes a user to as an owner to a channel using http
    """
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    u_id = data['u_id']
    return dumps(channel.channel_removeowner(token, channel_id, u_id))

@APP.route("/channels/list", methods=['GET'])
def channels_list():
    """
    Returns a list of all channels that the user has joined using http
    """
    request.args.get('token')
    return dumps(channels.channels_list(token))

@APP.route("/channels/listall", methods=['GET'])
def channels_listall():
    """
    Returns a list of all channels in Flockr using http
    """
    token = request.args.get('token')
    return dumps(channels.channels_listall(token))

@APP.route("/channels/create", methods=['POST'])
def channels_create():
    """
    Creates a new channel that is set as either public or private using http
    """
    data = request.get_json()
    token = data['token']
    name = data['name']
    is_public = data['is_public']
    return dumps(channels.channels_create(token, name, is_public))

@APP.route("/message/send", methods=['POST'])
def send_message():
    """
    Sends a message to a channel using http
    """
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    message = data['message']
    return dumps(message.message_send(token, channel_id, message))

@APP.route("/message/remove", methods=['DELETE'])
def remove_message():
    """
    Remove a message from the channel using http
    """
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']
    return dumps(message.message_remove(token, message_id))

@APP.route("/message/edit", methods=['PUT'])
def edit_message():
    """
    Edit a message from the channel using http
    """
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']
    message = data['message']
    return dumps(message.message_remove(token, message_id, message))

@APP.route("/users/all", methods=['GET'])
def users_all():
    """
    Returns a list of all users in Flockr using http
    """
    token = request.args.get('token')
    return dumps(other.users_all(token))

@APP.route("/admin/userpermission/change", methods=['POST'])
def change_permissions():
    """
    Sets a user's permissions according to the permission value using http
    """
    data = request.get_json()
    token = data['token']
    u_id = data['u_id']
    permission_id = data['permission_id']
    return dumps(other.users_all(token, u_id, permission_id))

@APP.route("/search", methods=['GET'])
def search_query():
    """
    Returns a list of messages the user has sent matching the search query using http
    """
    token = request.args.get('token')
    query_str = request.args.get('query_str')
    return dumps(other.search(token, query_str))

@APP.route("user/profile", methods=['GET'])
def profile():
    """
    Returns information about user user_id, email, first name, last name, and handle
    """
    return dumps(user.user_profile(request.args.get('token'), request.args.get('u_id')))

@APP.route("user/profile/setname", methods=['PUT'])
    """
    updates users first and last name
    """
    data = request.get_json()
    token = data['token']
    name_first = data["name_first"]
    name_last = data['name_last']
    return dumps(user.user_profile_setname(token, name_first, name_last))

@APP.route("user/profile/setemail", methods=['PUT'])
    data = request.get_json()
    token = data['token']
    email = data["email"]   
    return dumps(user.user_profile_setemail(token, email))

@APP.route("user/profile/sethandle", methods=['PUT'])
    data = request.get_json()
    token = data['token']
    handle = data['handle_str']
    return dumps(user.user_profile_sethandle(token, handle))
if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
