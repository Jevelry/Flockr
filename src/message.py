"""
datetime: Gives access to the datetime functions
data(data.py): Gives access to global data variable
error(error.py): Gives access to error classes
"""
#import datetime
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
    #new_message['date'] = datetime.now()
    new_message_id = make_message_id()
    new_message['message_id'] = new_message_id

    for channel in data.data['channels']:
        if channel['channel_id'] == channel_id:
            channel['messages'].append(new_message)

    return {
        'message_id': new_message_id,
    }

def message_remove(token, message_id):
    """
    Removes an existing message from the channel it is in

    Parameters:
        token(string): An authorisation hash
        message_id(string): The id of the message being removed

    Returns:
    """
    user_input_id = token_to_id(token)
    channel = find_message_in_channels(message_id, user_input_id)
    for message in channel['messages']:
        if message['message_id'] == message_id:
            channel['messages'].remove(message)

    return {}

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
def make_message_id():
    """
    Creates a unique string to be a message_id for a new message

    Parameters:

    Returns:
        A String that is the number of strings that have been sent ever
    """
    if data.data['message_num'] == '':
        data.data['message_num'] = 1
    else:
        data.data['message_num'] += 1

    return str(data.data['message_num'])


def find_message_in_channels(message_id, user_id):
    """
    Will go through every channel and if message_in_channel returns a channel it
    will return it otherwise it raises an input error

    Parameters:
        message_id(string): The id of the message being searched for
        user_id(string): The id of the user searching for the message it will return
                         an access error if the user is not an owner of the channel
                         or creator of the message
    Returns:
        channel(channel dictionary): If the channel was found it will return the channel
                                     dictionary
    """
    found_message = False
    for channel in data.data['channels']:
        found_message = message_in_channel(message_id, user_id, channel)
        if found_message:
            return channel
    raise InputError


def message_in_channel(message_id, user_id, channel):
    """
    Will go through a given and if the message_id is in the channel it will return
    true if the user is the creator of the message or an owner of the channel
    otherwise an AccessError will be raised

    Parameters:
        message_id(string): The id of the message being searched for
        user_id(string): The id of the user searching for the message it will return
                         an access error if the user is not an owner of the channel
                         or creator of the message
        channel(channel dictionary): The channel that is being checked
    Returns:
        boolean: If the message_id is found and the user has access true is returned
                 if the message_id is not found false will be returned
    """
    for message in channel['messages']:
        if message['message_id'] == message_id:
            if message['u_id'] == user_id or user_id in channel['owners']:
                return True
            else:
                raise AccessError
    return False
