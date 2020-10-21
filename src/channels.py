"""
data(data.py): gives access to global data variable
error(error.py): gives access to error classes
"""
import data
from error import InputError, AccessError
import validation

def channels_list(token):
    """
    Returns a list of all channels the user is a part of

    Parameters:
        token(string): A user authorisation hash

    Returns:
        List of channel dictionaries containing channel_id and name
    """
    # Check token is valid
    u_id = validation.check_valid_token(token)
    

    # Appends all channels that the user is in to channel_list
    


    '''
    for channel in data.data['channels']:
        for member_id in channel['members']:
            if member_id == u_id:
                channel_copy = {
                    'channel_id' : channel['channel_id'],
                    'name' : channel['name'],
                }
                channels.append(channel_copy)
    '''
    return data.channels_list_user(u_id)

def channels_listall(token):
    """
    Returns a list of all channels

    Parameters:
        token(string): A user authorisation hash

    Returns:
        List of channel dictionaries containing channel_id and name
    """
    # Check if token is valid
    validation.check_valid_token(token)

    '''
    # Initialise channel_list to return to user
    channels = []

    # Appends channel_id and name of all channels into channel_list
    for channel in data.data['channels']:
        channel_copy = {
            'channel_id' : channel['channel_id'],
            'name' : channel['name'],
        }
        channels.append(channel_copy)
    '''
    return data.channels_list_all


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
    # Check if token is valid
    u_id = validation.check_valid_token(token)

    # Returns InputError if channel name is more than 20 characters
    if len(name) > 20:
        raise InputError(description='Name cannot be more than 20 characters long')
    
    # Creates a new channel and stores to 'channels' in data.py
    
    new_channel = {
        'channel_id' : data.get_num_channels() + 1,
        'name' : name,
        'state' : is_public,
        'owners' : {u_id},
        'members' : {u_id},
        'messages' : {},
    }
    data.channel_create(new_channel)

    # Stores channel as part of the user's channel list
    user = data.get_user_info(u_id)
    data.update_user_channel_list(user, new_channel["channel_id"])    
    
    return {
        'channel_id': new_channel['channel_id'],
    }