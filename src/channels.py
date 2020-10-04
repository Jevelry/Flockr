import data
import auth
from error import InputError
from error import AccessError


def channels_list(token):
    # Initialise channel_list to return to user
    channels_list = []
    u_id = None
    
    # Finds u_id associated with user token
    # Returns AccessError if token does not exist
    for user in data.data['logged_in']:
        if user['token'] == token:
            u_id = user['u_id']
    
    if u_id == None:
        raise AccessError
        
    # Appends all channels that the user is in to channel_list
    for channel in data.data['channels']:
        for member_id in channel['members']:
            if member_id == u_id:
                channel_copy = {
                    'channel_id' : channel['channel_id'],
                    'name' : channel['name'],
                }
                channels_list.append(channel_copy)

    return channels_list

def channels_listall(token):
    # Initialise channel_list to return to user
    channels_list = []

    # Finds u_id associated with user token
    # Returns AccessError if token does not exist
    u_id = None
    for user in data.data['logged_in']:            
        if user['token'] == token:
            u_id = user['u_id']

    if u_id == None:
        raise AccessError
        
    # Appends channel_id and name of all channels into channel_list    
    for channel in data.data['channels']:
        channel_copy = {
            'channel_id' : channel['channel_id'],
            'name' : channel['name'],
        }
        channels_list.append(channel_copy)
    
    return channels_list


def channels_create(token, name, is_public):
    # Returns InputError if channel name is more than 20 characters
    if len(name) > 20:
        raise InputError('Name cannot be more than 20 characters long')

    # Finds u_id associated with user token
    # Returns AccessError if token does not exist
    u_id = None
    for user in data.data['logged_in']:
        if user['token'] == token:
            u_id = user['u_id']

    if u_id == None:
        raise AccessError

    # Creates a new channel and stores to 'channels' in data.py
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


if __name__ == '__main__':
    pass