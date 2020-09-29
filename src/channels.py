import data

def channels_list(token):
    channels_list = []

    for user in data.data['logged_in']:
        if user['token'] == token:
            u_id = user['u_id']

        for channel in data.data['channels']:
            for k in range(len(channel['owners'])):
                if channel['owners'][k] == u_id:
                    channel_copy = channel.copy()
                    channels_list.append(channel_copy)
        
            for l in range(len(channel['members'])):
                if channel['members'][l] == u_id:
                    channel_copy = channel.copy()
                    channels_list.append(channel_copy)

    for channel in channels_list:
        print(channel)

    return channels_list
 
def channels_listall(token):
    for channel in data.data['channels']:
        print(channel)
    
    return data.data['channels']

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

    return {'is_success' : True}
