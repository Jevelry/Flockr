import data
import auth
from error import InputError
from error import AccessError


def channels_list(token):
    channels_list = []
    u_id = None
    for user in data.data['logged_in']:
        if user['token'] == token:
            u_id = user['u_id']

    if u_id == None:
        raise AccessError
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
    channels_list = []

    u_id = None
    for user in data.data['logged_in']:            
        if user['token'] == token:
            u_id = user['u_id']

    if u_id == None:
        raise AccessError
    for channel in data.data['channels']:
        channel_copy = {
            'channel_id' : channel['channel_id'],
            'name' : channel['name'],
        }
        channels_list.append(channel_copy)
    
    return channels_list


def channels_create(token, name, is_public):
    if len(name) > 20:
        raise InputError('Name cannot be more than 20 characters long')

    u_id = None
    for user in data.data['logged_in']:
        if user['token'] == token:
            u_id = user['u_id']

    if u_id == None:
        raise AccessError

    new_channel = {
        'channel_id' : (len(data.data['channels']) + 1),
        'name' : name,
        'state' : is_public,
        'owners' : [u_id],
        'members' : [u_id],
        'messages' : [],
    }
    # Add channel to user's channel_list
    for user in data.data['users']:
        if user['u_id'] == u_id:
            user['channel_list'].append(new_channel['channel_id'])
    
    channel_copy = new_channel.copy()
    data.data['channels'].append(channel_copy)

    return {
        'channel_id': new_channel['channel_id'],
    }


if __name__ == '__main__':
    pass