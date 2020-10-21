"""
docstring do later
"""
from error import AccessError, InputError
"""
Global variable containing the state of flockr
"""
'''
data = {
    'users' : [
        # {
        #     'channel_list' : [],
        #     'first' : '',
        #     'last' : '',
        #     'email': '',
        #     'u_id' : '',
        #     'password' : ''
        #     'handle' : ''
        #     'permission_id' : ''
        #     'num_logged_in : ''
        # }
    ],
    'logged_in' : [], # List of u_id's
    'channels' : [
        # {
        #     'name' : '',
        #     'state' : '', # public or private
        #     'channel_id' : '',
        #     'num_channels' : '',
        #     'owners' : [], # list of u_id's
        #     'members' : [], # list of u_id's
        #     'messages' : [
        #         {
        #             'message' : '',
        #             'message_id' : '',
        #             'u_id' : '',
        #             'date' : ''
        #         }
        #     ]
        # }
    ],
    'message_num' : '', #the number of messages that have been sent
    'jwt_secret' : 'Mango2Team' # Secret jwt password (for tokens)
}
'''
users = {
     # u_id = {
        #     'channel_list'  = set()
        #     'name_first' : '',
        #     'name_last' : '',
        #     'email': '',
        #     'u_id' : '',
        #     'password' : ''
        #     'handle' : ''
        #     'permission_id' : ''
        #     'num_logged_in : ''
        # }
}

logged_in = set() # Set of u_ids

channels = {
    # channel_id {
        # channel_id = {
        #     'name' : '',
        #     'is_public' : '', # public or private (True or False)
        #     'channel_id' : ''
        #     'owners' = set(),
        #     'members' : set(),
         #    'messages' = {
        #         message_id = {
            #         {
            #             'message' : '',
            #             'message_id' : '',
            #             'u_id' : '',
            #             'date' : ''
            #         }
            #    }
        #      
    #}
}

message_num = 0 #the number of messages that have been sent

jwt_secret = "Mango2Team" # Secret jwt password (for tokens)


# Clears the data variable.
# Removes all users, channels, etc.
def clear_data():
    """
    Restarts the global variable to it's default state (empty)
    """
    global users, channels, logged_in, message_num
    users = {}
    channels = {

    }
    logged_in = set()
    message_num = 0
    

def get_user_with(attributes):  
    """
    Given an attribute(dict), finds user(dict) with matching attribute and returns it
    """
    #user = None  
    # user = None  
    # for user in users:
    #     for attr,val in attributes.items():
    #         if user[attr] != val:
    #             break
    #     else:
    #         usr = user   

    #     '''    
    #     if user[attributes.key()] == dict.get(attributes)
    #     return user
    # return None
    # '''
    for user in users:
        if attributes.items() <= users[user].items():
            return users[user]
    return None
     

def get_user_info(u_id):
    """
    Returns user dictionary from u_id
    """
    try:
        return users[u_id]
    except:
        return None
    
def update_user(user,attributes):
    """
    Given a user(dict) and attribute(dict), updates that user with given new attributes
    """
    for item in attributes:
        user[item] = attributes[item]    

def update_user_channel_list(user,channel_id):
    """
    Given a user(dict) and channel_id(int), adds the channel id to the users channel list
    """
    user['channel_list'].add(channel_id)  
          
def register_user(user):
    """
    Given a user(dict), adds it to list of existing users
    """
    users[user["u_id"]] = user

def login_user(u_id):
    """
    Given a u_id(int), adds u_id to list of logged in users
    """
    logged_in.add(u_id) 

def check_logged_in(u_id):
    """
    Given a u_id(int) checks and returns true if user is logged in
    """
    return u_id in logged_in 

def logout_user(u_id):
    """
    Given a u_id(int), removes u_id from logged in list
    """
    logged_in.remove(u_id)

def get_channel_info(channel_id):
    """
    Given a channel_id(int), returns infomation on channel(dict)
    """
    try:
        return channels[channel_id]
    except:
        return None
    
def channel_add_member(channel_id, u_id):
    """
    Given a channel_id(int) and u_id(int), add the u_id to channel
    """
    channel = channels[channel_id]   
    if u_id == 1:
        channel['owners'].add(u_id)
    channel['members'].add(u_id)
    user = get_user_info(u_id)
    user["channel_list"].add(channel_id)

def check_user_in_channel(channel_id, u_id):
    """
    Given a channel_id(int) and u_id(int),returns true if user is a member of channel
    """
    channel = get_channel_info(channel_id)
    return u_id in channel['members']
    # if u_id not in channel_info['members']:
    #     raise AccessError(description="User is not in channel")

def check_channel_owner(channel_id, u_id):
    """
    Given a channel_id(int) and u_id(int), returns true if user is an owner of channel
    """
    channel_info = get_channel_info(channel_id)
    return u_id in channel_info['owners']

def channel_add_owner(channel_id, u_id):
    """
    Given a channel_id(int) and u_id(int), adds user to list of owners of channel
    """
    channel = channels[channel_id]   
    channel['owners'].add(u_id)

def channel_remove_member(channel_id, u_id):
    """
    Given a channel_id(int) and u_id(int), removes that member from the channel
    """
    channel = channels[channel_id]
    if u_id in channel['owners']:
        channel['owners'].remove(u_id)
    channel['members'].remove(u_id)

def channel_remove_owner(channel_id,u_id):
    """
    Given a channel_id(int) and u_id(int), removes that member as an owner of the channel
    """
    channel = channels[channel_id]   
    channel['owners'].remove(u_id)

def get_message_num():
    """
    Return the value of message_num
    """
    return message_num

def get_num_users():
    """
    Returns the number of total users
    """
    return len(users)
    
def make_message_id():
    """
    Creates a unique message_id for a new message
    """
    global message_num
    message_num += 1

    return message_num

def channels_list_user(u_id):
    """
    Given a u_id(int), generates a list of all channels user is a part of and returns it
    """
    user = get_user_info(u_id)
    channels_info = []
    for channel in user['channel_list']:
        chan_info = get_channel_info(channel)
        channel_copy = {
            'channel_id' : chan_info['channel_id'],
            'name' : chan_info['name']
        }
        channels_info.append(channel_copy)
    return channels_info        

def channels_list_all():
    """
    Generates a list of all channels and returns it
    """
    channels_info = []
    for channel in channels:
        channel_copy = {
            'channel_id' : channel,
            'name' : channels[channel]['name']
        }
        channels_info.append(channel_copy)
    return channels_info

def get_num_channels():
    """
    Returns the total number of channels
    """
    return len(channels)

def channel_create(new_channel):
    """
    Given a new_channel(dict), adds it to list of existing channels
    """ 
    channels[new_channel['channel_id']] = new_channel 

def find_channel(message_id):
    for channel in channels:
        if message_id in channels[channel]['messages']:
            return channel
    raise InputError(description="Message not in any channel")

def get_message(channel, message_id):
    return channels[channel]['messages'][message_id]

def add_message(message, channel_id):
    channel = channels[channel_id]
    message_id = message['message_id']
    channel['messages'][message_id] = message

def remove_message(message_id, channel_id):
    channel = channels[channel_id]
    del channel['messages'][message_id]

def edit_message(channel_id, message_id, message):
    channels[channel_id]['messages'][message_id]['message'] = message

def user_list():
    list_users = []
    for user in users.values():
        user_info = {
            'u_id' : user['u_id'],
            'email' : user['email'],
            'name_last' : user['name_last'],
            'name_first' : user['name_first'],
            'handle_str' : user['handle_str'],
            'permission_id' : user['permission_id']
        }
        list_users.append(user_info)
    return list_users

def change_permission(u_id, permission):
    user = get_user_info(u_id)
    user['permission_id'] = permission