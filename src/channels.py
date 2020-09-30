import data
from error import InputError

def channels_list(token):
    channels_list = []

    for user in data.data['logged_in']:
        if user['token'] == token:
            global u_id
            u_id = user['u_id']

    for channel in data.data['channels']:
        for owner_id in channel['owners']:
            if owner_id == u_id:
                channel_copy = {
                    'channel_id' : channel['channel_id'],
                    'name' : channel['name'],
                }
                channels_list.append(channel_copy)
        
        for member_id in channel['members']:
            if member_id == u_id:
                channel_copy = {
                    'channel_id' : channel['channel_id'],
                    'name' : channel['name'],
                }
                channels_list.append(channel_copy)

    return channels_list
 
def channels_listall(token):
    channels_list = []

    for channel in data.data['channels']:
        channel_copy = {
            'channel_id' : channel['channel_id'],
            'name' : channel['name'],
        }
        channels_list.append(channel_copy)
    
    return channels_list
import data
from error import InputError

def channels_list(token):
    channels_list = []

    for user in data.data['logged_in']:
        if user['token'] == token:
            global u_id
            u_id = user['u_id']

    for channel in data.data['channels']:
        for owner_id in channel['owners']:
            if owner_id == u_id:
                channel_copy = {
                    'channel_id' : channel['channel_id'],
                    'name' : channel['name'],
                }
                channels_list.append(channel_copy)
        
        for member_id in channel['members']:
            if member_id == u_id:
                channel_copy = {
                    'channel_id' : channel['channel_id'],
                    'name' : channel['name'],
                }
                channels_list.append(channel_copy)

    return channels_list
 
def channels_listall(token):
    channels_list = []

    for channel in data.data['channels']:
        channel_copy = {
            'channel_id' : channel['channel_id'],
            'name' : channel['name'],
        }
        channels_list.append(channel_copy)
    
    return channels_list

"""
NEED TO MAKE SURE TOKEN IS VALID (FROM A USER WHO ALREADY LOGGED IN)
"""
def channels_create(token, name, is_public):
    if len(name) > 20:
        raise InputError('Name cannot be more than 20 characters long')

    for user in data.data['logged_in']:
        if user['token'] == token:
            global u_id
            u_id = user['u_id']
    
    new_channel = {
        'channel_id' : (len(data.data['channels']) + 1),
        'name' : name,
        'state' : is_public,
        'owners' : [u_id],
        'members' : [u_id],
        'num_channels' : [],
        'messages' : [],
    }
    for user in data.data["users"]:
        if user["u_id"] == u_id:
            user["channel_list"].append(new_channel["channel_id"])
            
    channel_copy = new_channel.copy()
    data.data['channels'].append(channel_copy)

    return {
        'channel_id': new_channel['channel_id'],
    }

