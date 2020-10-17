import data
import validation
from user import get_uid
from error import InputError
from error import AccessError

def channels_list(token):
    """
    Returns a list of all channels in Flockr that the user is a part of

    Parameters:
        token(string): A user authorisation hash

    Returns:
        channels: A list of channel dictionaries containing channel_id and name
    """

    # Initialise channel_list to return to user
    channels = []

    # Checks if user's token exists
    # Returns AccessError if token does not exist
    validation.check_valid_token(token)

    # Finds u_id associated with user token
    u_id = get_uid(token)

    # Appends all channels that the user is in to channels
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
    Returns a list of all channels in Flockr

    Parameters:
        token(string): A user authorisation hash

    Returns:
        channels: A list of channel dictionaries containing channel_id and name
    """

    # Initialise channels to return to user
    channels = []

    # Checks if user's token exists
    # Returns AccessError if token does not exist
    validation.check_valid_token(token)

    # Appends channel_id and name of all channels into channels
    for channel in data.data['channels']:
        channel_copy = {
            'channel_id' : channel['channel_id'],
            'name' : channel['name'],
        }
        channels.append(channel_copy)
    
    return channels


def channels_create(token, name, is_public):
    """
    Creates a new channel that is set as either public or private

    Parameters:
        token(string): A user authorisation hash
        name(string): Name of channel
        is_public(boolean): True if channel should be public

    Returns:
        channel_id: A dictionary that contains the new channel's channel_id
    """

    # Returns InputError if channel name is more than 20 characters
    if len(name) > 20:
        raise InputError('Name cannot be more than 20 characters long')

    # Checks if user's token exists
    # Returns AccessError if token does not exist
    validation.check_valid_token(token)

    # Finds u_id associated with user token
    u_id = get_uid(token)

    # Creates a new channel and stores to 'channels' in data.py
    new_channel = {
        'channel_id' : (len(data.data['channels']) + 1),
        'name' : name,
        'state' : is_public,
        'owners' : [u_id],
        'members' : [u_id],
        'messages' : [],
    }
    data.data['channels'].append(new_channel)

    # Stores channel as part of the user's channel list
    for user in data.data['users']:
        if user['u_id'] == u_id:
            user['channel_list'].append(new_channel['channel_id'])
    
    return {
        'channel_id': new_channel['channel_id'],
    }