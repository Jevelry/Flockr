"""
data(data.py): gives access to global data variable
error(error.py): gives access to error classes
"""
import data
from error import InputError, AccessError
import validation
from user import get_uid

def channels_list(token):
    """
    Returns a list of all channels the user is a part of

    Parameters:
        token(string): A user authorisation hash

    Returns:
        List of channel dictionaries containing channel_id and name
    """
    # Initialise channel_list to return to user
    channels = []
    '''
    u_id = None

    # Finds u_id associated with user token
    # Returns AccessError if token does not exist
    for user in data.data['logged_in']:
        if user['token'] == token:
            u_id = user['u_id']

    if u_id is None:
        raise AccessError
    '''
    validation.check_valid_token(token)
    # Appends all channels that the user is in to channel_list
    u_id = get_uid(token)
    for channel in data.data['channels']:
        for member_id in channel['members']:
            if member_id == u_id:
                channel_copy = {
                    'channel_id' : channel['channel_id'],
                    'name' : channel['name'],
                }
                channels.append(channel_copy)

    return channels

def channels_listall(token):
    """
    Returns a list of all channels

    Parameters:
        token(string): A user authorisation hash

    Returns:
        List of channel dictionaries containing channel_id and name
    """
    # Initialise channel_list to return to user
    channels = []

    # Finds u_id associated with user token
    # Returns AccessError if token does not exist
    validation.check_valid_token(token)

    # Appends channel_id and name of all channels into channel_list
    u_id = get_uid(token)
    for channel in data.data['channels']:
        channel_copy = {
            'channel_id' : channel['channel_id'],
            'name' : channel['name'],
        }
        channels.append(channel_copy)

    return channels


def channels_create(token, name, is_public):
    """
    Checks information given is valid, then creates a new channel

    Parameters:
        token(string): A user authorisation hash
        name(string): Name of channel
        is_public(boolean): True if channel should be public

    Returns:
        Dictionary with information about the created channel
    """
    # Returns InputError if channel name is more than 20 characters
    if len(name) > 20:
        raise InputError('Name cannot be more than 20 characters long')

    # Finds u_id associated with user token
    # Returns AccessError if token does not exist
    validation.check_valid_token(token)
    # Creates a new channel and stores to 'channels' in data.py
    u_id = get_uid(token)
    new_channel = {
        'channel_id' : (len(data.data['channels']) + 1),
        'name' : name,
        'state' : is_public,
        'owners' : [u_id],
        'members' : [u_id],
        'messages' : [],
    }
    channel_copy = new_channel.copy()
    data.data['channels'].append(channel_copy)

    # Add channel to user's channel_list
    for user in data.data['users']:
        if user['u_id'] == u_id:
            user['channel_list'].append(new_channel['channel_id'])

    return {
        'channel_id': new_channel['channel_id'],
    }
