import data

def channels_list(token):
    channels_list = []

    for user in data.data['logged_in']:
        if user['token'] == token:
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

    for channel in channels_list:
        print(channel)

    return channels_list
 
def channels_listall(token):
    channels_list = []

    for channel in data.data['channels']:
        channel_copy = {
            'channel_id' : channel['channel_id'],
            'name' : channel['name'],
        }
        print(channel)
    
    return channels_list

def channels_create(token, name, is_public):
    for user in data.data['logged_in']:
        if user['token'] == token:
            u_id = user['u_id']
    
        new_channel = {
            'channel_id' : (len(data.data['channels']) + 1),
            'name' : name,
            'state' : is_public,
            'owners' : [u_id],
        }
        channel_copy = new_channel.copy()
        data.data['channels'].append(channel_copy)

        return {
            'channel_id': new_channel['channel_id'],
        }
