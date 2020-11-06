"""
This is the file which runs server with Python Flask

auth(auth.py): Gives access to auth functions (Register, logout, login)
channel(channel.py): Gives access to channel functinos
channels(channels.py): Gives access to channels functions
message(message.py): Gives access to message functions (send, edit, remove)
pytest(pytest module): Gives access to pytest command
other(other.py): Gives access to other functions (clear)
user(user.py): Gives access to user functions 
error(error.py): Gives access to error classes
"""

from json import dumps
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from error import InputError
import auth
import channel
import channels
import message
import user
import other
import data
import sys


def defaultHandler(err):
    
    response = err.get_response()
    print("response", err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = "application/json"
    return response

APP = Flask(__name__)
CORS(APP)

APP.config["TRAP_HTTP_EXCEPTIONS"] = True
APP.register_error_handler(Exception, defaultHandler)

def convert_to_int(id):
    """
    Http passes everything as strings, so
    If id can be converted to an int, do it,
    else return None
    """
    try:
        return int(id)
    except:
        return None

# Example
@APP.route("/echo", methods=["GET"])
def echo():
    data = request.args.get("data")
    if data == "echo":
        raise InputError(description="Cannot echo 'echo'")
    return dumps({
        "data": data
    })

message.message_send
@APP.route("/auth/register", methods = ["POST"])
def register():
    """
    Registers user using http
    """
    data = request.get_json()
    first = data["name_first"]
    last = data["name_last"]
    email = data["email"]
    password = data["password"]
    return auth.auth_register(email, password, first, last)

@APP.route("/auth/logout", methods = ["POST"])
def logout():
    """
    Logs user out using http
    """
    data = request.get_json()
    token = data["token"]
    return auth.auth_logout(token)

@APP.route("/auth/login", methods = ["POST"])
def login():
    """
    Logs user in using http
    """
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    return auth.auth_login(email, password)

@APP.route("/channel/invite", methods = ["POST"])
def invite():
    """
    Invites a user to join a channel using http
    """
    data = request.get_json()
    token = data["token"]
    channel_id = convert_to_int(data["channel_id"])
    u_id = convert_to_int(data["u_id"])
    return channel.channel_invite(token, channel_id, u_id)

@APP.route("/channel/details", methods = ["GET"])
def details():
    """
    Provides basic details about the channel using http
    """

    token = request.args.get("token")
    channel_id = convert_to_int(request.args.get("channel_id"))
    return channel.channel_details(token, channel_id)
    
    
@APP.route("/channel/messages", methods = ["GET"])    
def messages():
    """
    Returns up to 50 messages between index "start" and "start + 50" (end) using http
    """
    token = request.args.get("token")
    channel_id = convert_to_int(request.args.get("channel_id"))
    start = convert_to_int(request.args.get("start"))
    return dumps(channel.channel_messages(token, channel_id, start))
    
@APP.route("/channel/leave", methods = ["POST"])
def leave():
    """
    Removes user as a member of the channel using http
    """
    data = request.get_json()
    token = data["token"]
    channel_id = convert_to_int(data["channel_id"])
    return channel.channel_leave(token, channel_id)    
    
@APP.route("/channel/join", methods = ["POST"])
def join():
    """
    Adds a user to a public channel using http
    """
    data = request.get_json()
    token = data["token"]
    channel_id = int(data["channel_id"])
    return channel.channel_join(token, channel_id)

@APP.route("/channel/addowner", methods = ["POST"])
def addowner():
    """
    Adds a user to as an owner to a channel using http
    """
    data = request.get_json()
    token = data["token"]
    channel_id = convert_to_int(data["channel_id"])
    u_id = convert_to_int(data["u_id"])
    return channel.channel_addowner(token, channel_id, u_id)

@APP.route("/channel/removeowner", methods = ["POST"])
def removeowner():
    """
    Removes a user to as an owner to a channel using http
    """
    data = request.get_json()
    token = data["token"]
    channel_id = convert_to_int(data["channel_id"])
    u_id = convert_to_int(data["u_id"])
    return channel.channel_removeowner(token, channel_id, u_id)

@APP.route("/channels/list", methods = ["GET"])
def channels_list():
    """
    Returns a list of all channels that the user has joined using http
    """
    token = request.args.get("token")
    return dumps(channels.channels_list(token))

@APP.route("/channels/listall", methods = ["GET"])
def channels_listall():
    """
    Returns a list of all channels in Flockr using http
    """
    token = request.args.get("token")
    return dumps(channels.channels_listall(token))

@APP.route("/channels/create", methods = ["POST"])
def channels_create():
    """
    Creates a new channel that is set as either public or private using http
    """
    data = request.get_json()
    token = data["token"]
    name = data["name"]
    is_public = data["is_public"]
    return channels.channels_create(token, name, is_public)

@APP.route("/message/send", methods = ["POST"])
def send_message():
    """
    Sends a message to a channel using http
    """
    data = request.get_json()
    token = data["token"]
    channel_id = convert_to_int(data["channel_id"])
    message_str = data["message"]
    return message.message_send(token, channel_id, message_str)
@APP.route("/message/remove", methods = ["DELETE"])
def remove_message():
    """
    Remove a message from the channel using http
    """
    data = request.get_json()
    token = data["token"]
    message_id = convert_to_int(data["message_id"])
    return message.message_remove(token, message_id)

@APP.route("/message/edit", methods = ["PUT"])
def edit_message():
    """
    Edit a message from the channel using http
    """
    data = request.get_json()
    token = data["token"]
    message_id = convert_to_int(data["message_id"])
    message_str = data["message"]
    return message.message_edit(token, message_id, message_str)

@APP.route("/users/all", methods = ["GET"])
def users_all():
    """
    Returns a list of all users in Flockr using http
    """
    token = request.args.get("token")
    return other.users_all(token)

@APP.route("/admin/userpermission/change", methods = ["POST"])
def change_permissions():
    """
    Sets a user's permissions according to the permission value using http
    """
    data = request.get_json()
    token = data["token"]
    u_id = convert_to_int(data["u_id"])
    permission_id = convert_to_int(data["permission_id"])
    return other.admin_userpermission_change(token, u_id, permission_id)

@APP.route("/search", methods = ["GET"])
def search_query():
    """
    Returns a list of messages the user has sent matching the search query using http
    """
    token = request.args.get("token")
    query_str = request.args.get("query_str")
    return dumps(other.search(token, query_str))

@APP.route("/user/profile", methods = ["GET"])
def profile():
    """
    Returns information about user user_id, email, first name, last name, and handle using http
    """
    token = request.args.get("token")
    u_id = convert_to_int(request.args.get("u_id"))
    return dumps(user.user_profile(token, u_id))

@APP.route("/user/profile/setname", methods = ["PUT"])
def setname():
    """
    Updates user's first and last name using http
    """
    data = request.get_json()
    token = data["token"]
    name_first = data["name_first"]
    name_last = data["name_last"]
    return user.user_profile_setname(token, name_first, name_last)

@APP.route("/user/profile/setemail", methods = ["PUT"])
def setemail():
    """
    Updates user's email using http
    """
    data = request.get_json()
    token = data["token"]
    email = data["email"]   
    return user.user_profile_setemail(token, email)

@APP.route("/user/profile/sethandle", methods = ["PUT"])
def sethandle():
    """
    Updates user's handle_str using http
    """
    data = request.get_json()
    token = data["token"]
    handle = data["handle_str"]
    return user.user_profile_sethandle(token, handle)
    
@APP.route("/user/profile/uploadphoto", methods = ["POST"])    
def upload_photo():
    """
    Crop image from img_url and saves it.
    """
    data = request.get_json()
    token = data["token"]
    img_url = data["img_url"]
    x_start = data["x_start"]
    x_end = data["x_end"]
    y_start = data["y_start"]
    y_end = data["y_end"]
    user.user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end)

    host_url = request.host_url
    data.update_user_img(host_url, token)

    return {}

@APP.route("/static/<path:path>")
def send_js(path):
    """
    Serves image back to server
    """
    return send_from_directory('/static/', path) 

if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
