"""
Contains all functions to do with the global variables and dictionaries.
Only file that interacts with the data state.
Note: Many functions in this file assume that everything is valid.
eg message_remove assumes that the message is already in the channel.
The validation checks are generally done before these functions are called.
"""
from error import AccessError, InputError
"""
Global variables containing the state of flockr
"""

# Users is a dictionary that contains information of every user
# and uses u_id as the key.
users = {
     # u_id = {
        #     "channel_list"  = set()
        #     "name_first" : "",
        #     "name_last" : "",
        #     "email": "",
        #     "u_id" : "",
        #     "password" : ""
        #     "handle" : ""
        #     "permission_id" : ""
        #     "num_logged_in : ""
        # }
}

# Logged_in is a set of all logged in users by u_id.
logged_in = set() 

# Channels is a dictionary that contains information of every channel
# and uses channel_id as the key.
channels = {
        # channel_id = {
        #     "name" : "",
        #     "is_public" : "", # public or private (True or False)
        #     "channel_id" : ""
        #     "owners" = set(),
        #     "members" : set(),
         #    "messages" = {
        #         message_id = {
            #         {
            #             "message" : "",
            #             "message_id" : "",
            #             "u_id" : "",
            #             "date" : ""
            #         }
            #    }
            #}
            # "hangman" : {
            #     is_active : False,
            #     u_id : '',
            #     word : None,
            #     guesses : set(),
            #     failures : 0,
            #     status_message : ''
            # }
        #      
    #}
}

# Message_num is the total number of messages that have been sent.
# This number does not decrease when a message is removed.
message_num = 0

# jwt_secret is the secret string used in jwt encoding.
# It never changes.
jwt_secret = "Mango2Team"


# Clears the data variable.
# Removes all users, channels, etc.
def clear_data():
    """
    Restarts the global variable to it"s default state (empty)
    """
    global users, channels, logged_in, message_num
    users = {}
    channels = {

    }
    logged_in = set()
    message_num = 0
    

def get_user_with(attributes):  
    """
    Given an attribute(dict), finds user(dict) with matching attribute and returns it
    """
    for user in users:
        if attributes.items() <= users[user].items():
            return users[user]
    return None
     

def get_user_info(u_id):
    """
    Returns user dictionary from u_id
    """
    try:
        return users[u_id]
    except:
        return None

def get_user_secret(u_id):
    """
    Returns the user's secret session code
    to validate tokens
    """
    user = get_user_info(u_id)
    return user["session_secret"]

def update_user(user,attributes):
    """
    Given a user(dict) and attribute(dict), updates that user with given new attributes
    """
    for item in attributes:
        user[item] = attributes[item]    

def update_user_channel_list(user,channel_id):
    """
    Given a user(dict) and channel_id(int), adds the channel id to the users channel list
    """
    user["channel_list"].add(channel_id)  
          
def register_user(user):
    """
    Given a user(dict), adds it to list of existing users
    """
    users[user["u_id"]] = user

def login_user(u_id):
    """
    Given a u_id(int), adds u_id to list of logged in users
    """
    logged_in.add(u_id) 

def check_logged_in(u_id):
    """
    Given a u_id(int) checks and returns true if user is logged in
    """
    return u_id in logged_in 

def logout_user(u_id):
    """
    Given a u_id(int), removes u_id from logged in list
    """
    logged_in.remove(u_id)

def get_channel_info(channel_id):
    """
    Given a channel_id(int), returns infomation on channel(dict)
    """
    try:
        return channels[channel_id]
    except:
        return None
    
def get_hangman_info(channel_id):
    """
    Given a channel_id(int), returns infomation on channel's hangman session(dict).
    Assumes channel_id exists.
    """
    channel = get_channel_info(channel_id)
    return channel['hangman']

def get_hangman_status_message(channel_id):
    message_id = list(channels)[-1]
    return get_message(channel_id, message_id)

def channel_add_member(channel_id, u_id):
    """
    Given a channel_id(int) and u_id(int), add the u_id to channel
    """
    channel = channels[channel_id]   
    if u_id == 1:
        channel["owners"].add(u_id)
    channel["members"].add(u_id)
    user = get_user_info(u_id)
    user["channel_list"].add(channel_id)

def check_user_in_channel(channel_id, u_id):
    """
    Given a channel_id(int) and u_id(int), returns true if user is a member of channel
    """
    channel = get_channel_info(channel_id)
    return u_id in channel["members"]

def check_channel_owner(channel_id, u_id):
    """
    Given a channel_id(int) and u_id(int), returns true if user is an owner of channel
    """
    channel_info = get_channel_info(channel_id)
    return u_id in channel_info["owners"]

def channel_add_owner(channel_id, u_id):
    """
    Given a channel_id(int) and u_id(int), adds user to list of owners of channel
    """
    channel = channels[channel_id]   
    channel["owners"].add(u_id)

def channel_remove_member(channel_id, u_id):
    """
    Given a channel_id(int) and u_id(int), removes that member from the channel
    """
    channel = channels[channel_id]
    if u_id in channel["owners"]:
        channel["owners"].remove(u_id)
    channel["members"].remove(u_id)

def channel_remove_owner(channel_id,u_id):
    """
    Given a channel_id(int) and u_id(int), removes that member as an owner of the channel
    """
    channel = channels[channel_id]   
    channel["owners"].remove(u_id)

def get_message_num():
    """
    Return the value of message_num (the total number of messages).
    This function is used to generate a message_id, so it also includes
    all deleted messages as part of the count.
    """
    return message_num

def get_num_users():
    """
    Returns the number of total users
    """
    return len(users)

def get_jwt_secret():
    """
    Returns the jwt_secret
    """
    return jwt_secret
    
def make_message_id():
    """
    Creates a unique message_id for a new message
    """
    global message_num
    message_num += 1

    return message_num

def channels_list_user(u_id):
    """
    Given a u_id(int), generates a list of all channels user is a part of and returns it
    """
    user = get_user_info(u_id)
    channels_info = []
    for channel in user["channel_list"]:
        chan_info = get_channel_info(channel)
        channel_copy = {
            "channel_id" : chan_info["channel_id"],
            "name" : chan_info["name"]
        }
        channels_info.append(channel_copy)
    return {"channels" : channels_info}    

def channels_list_all():
    """
    Generates a list of all existing channels and returns it
    """
    channels_info = []
    for channel in channels:
        channel_copy = {
            "channel_id" : channel,
            "name" : channels[channel]["name"]
        }
        channels_info.append(channel_copy)
    return {"channels" : channels_info}

def get_num_channels():
    """
    Returns the total number of channels
    """
    return len(channels)

def channel_create(new_channel):
    """
    Given a new_channel(dict), adds it to list of existing channels
    """ 
    channels[new_channel["channel_id"]] = new_channel 

def find_channel(message_id):
    """
    Given a message_id, returns channel_id of channel with that message
    """
    for channel in channels:
        if message_id in channels[channel]["messages"]:
            return channel
    raise InputError(description = "Message not in any channel")

def get_message(channel, message_id):
    """
    Given channel containing message and message_id,
    returns dictionary containing message info
    """
    return channels[channel]["messages"][message_id]

def add_message(message, channel_id):
    """
    Adds given message to channel with given channel_id
    """
    channel = channels[channel_id]
    message_id = message["message_id"]
    channel["messages"][message_id] = message

def remove_message(message_id, channel_id):
    """
    Removes message with given message_id from 
    channel with given channel_id.
    """
    channel = channels[channel_id]
    del channel["messages"][message_id]

def edit_message(channel_id, message_id, message):
    """
    Edits the target message and changes
    target_message["message"] to message
    """
    channels[channel_id]["messages"][message_id]["message"] = message

def user_list():
    """
    Returns a list of every user in the system
    """
    list_users = []
    for user in users.values():
        user_info = {
            "u_id" : user["u_id"],
            "email" : user["email"],
            "name_last" : user["name_last"],
            "name_first" : user["name_first"],
            "handle_str" : user["handle_str"]
        }
        list_users.append(user_info)
    return list_users

def change_permission(u_id, permission):
    """
    Changes user's serverwide permissions
    to whatever was specified
    """
    user = get_user_info(u_id)
    user["permission_id"] = permission
