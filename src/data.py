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
        #     'first' : '',
        #     'last' : '',
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
        # channel_id = {
        #     'name' : '',
        #     'state' : '', # public or private
        #     'channel_id' : ''
        #     'owners' = set()
        #     'members' : set()
        #     'messages' = {
        #         message_id = {
            #         {
            #             'message' : '',
            #             'message_id' : '',
            #             'u_id' : '',
            #             'date' : ''
            #         }
                # }
        #      
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
    channels = {}
    logged_in = set()
    message_num = 0
    

def get_user_with(attributes):  
    user = None  
    for user in users:
        for attr,val in attributes.items():
            if user[attr] != val:
                break
        else:
            usr = user   

        '''    
        if user[attributes.key()] == dict.get(attributes)
        return user
    return None
    '''
def get_user_info(u_id):     
    return users[u_id]
    
def update_user(user,attributes):
     for item in attributes:
        user[item] = attributes[item]    
        
def register_user(user):
    users[user["u_id"]] = user

def login_user(u_id):
    logged_in.add(u_id) 

def check_logged_in(u_id):
    return u_id in logged_in 

def get_channel_info(channel_id):
    return channels[channel_id]
    
def channel_add_member(channel_id, u_id):
    channel = channels[channel_id]   
    if u_id == 1:
        channel[owners].add(u_id)
    channel[members].add(u_id)
    user = get_user_info(u_id)
    user["channel_list"].add(channel_id)

def check_user_in_channel(channel_id, u_id):
    channel_info = get_channel_info(channel_id)
    return u_id in channel_info['members']
    # if u_id not in channel_info['members']:
    #     raise AccessError(description="User is not in channel")

def check_channel_owner(channel_id, u_id):
    channel_info = get_channel_info(channel_id)
    return u_id in channel_info['owners']

def channel_add_owner(channel_id, u_id):
    channel = channels[channel_id]   
    channel[owners].add(u_id)

def channel_remove_member(channel_id, u_id):
    channel = channels[channel_id]
    if u_id in channel[owners]:
        channel[owners].remove(u_id)
    channel[members].remove(u_id)

def channel_remove_owner(channel_id,u_id):
    channel = channels[channel_id]   
    channel[owners].remove(u_id)

def get_message_num():
    return message_num
    
def make_message_id():
    """
    Creates a unique string to be a message_id for a new message

    Parameters:

    Returns:
        A String that is the number of strings that have been sent ever
    """
    if message_num ==  0:
        data.data['message_num'] = 1
    else:
        data.data['message_num'] += 1

    return str(data.data['message_num'])