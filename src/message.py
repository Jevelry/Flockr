"""
data(data.py): Gives access to global data variable
error(error.py): Gives access to error classes
"""
from error import AccessError, InputError
import data


def message_send(token, channel_id, message):
    """
    Adds a new message to the message to the messages in a channel

    Parameters:
        token(string): An authorisation hash
        channel_id(string): The channel_id of the channel the message is being added too
        message(string): The message of the message being added

    Returns:
        message_id(string): An identifier for the new message
    """
    if len(message) > 1000:
        raise InputError

    user_input_id = token_to_id(token)

    if not is_channel_member(user_input_id, channel_id):
        raise AccessError

    new_message = {}
    new_message['message'] = message
    new_message['u_id'] = user_input_id
    new_message_id = make_message_id(channel_id)
    new_message['message_id'] = new_message_id

    for channel in data.data['channels']:
        if channel['channel_id'] == channel_id:
            channel['messages'].append(new_message)

    return {
        'message_id': new_message_id,
    }

def message_remove(token, message_id):
    """
    Replace this with your own docstring.
    I just want to pass pylint
    """
    return {
        'token' : token, # Delete this line.
        'message_id' : message_id # Delete this line
    }

def message_edit(token, message_id, message):
    """
    Replace this with your own docstring.
    I just want to pass pylint
    """
    return {
        'token' : token, # Delete this line
        'message_id' : message_id, # Delete this line
        'message' : message # Delete this line
    }


#Will take a token and return the id
def token_to_id(token):
    """
    Converts a valid token to its corresponding id

    Parameters:
        token(string): An authorisation hash

    Returns:
        u_id relating to the supplied token
    """
    for user in data.data["logged_in"]:
        if user["token"] == token:
            return user["u_id"]
    raise AccessError


#Will determine if someone is a member of a given channel
def is_channel_member(user_id, channel_id):
    """
    Determines whether user is a member of a given channel

    Parameters:
        user_id(int): Identifier for users
        channel_id(int): Identifier for channels

    Returns:
        True if user is a member of the channel
        False if user is not a member of the channel
    """

    for channel in data.data["channels"]:
        if channel["channel_id"] == channel_id:
            for member in channel["members"]:
                if member == user_id:
                    return True
    return False

#When given the channel id it will create a unique string for the message_id
def make_message_id(channel_id):
    """
    Creates a unique string to be a message_id for a new message

    Parameters:
        channel_id(string): to find the channel the message is being added to
        find out how many messages are in the chain

    Returns:
        A String that is the channel_id + '_' + the number of the new message
    """
    message_int = 0
    for channel in data.data["channels"]:
        if channel["channel_id"] == channel_id:
            message_int = len(channel['messages']) + 1

    return str(channel_id) + '_' + str(message_int)
