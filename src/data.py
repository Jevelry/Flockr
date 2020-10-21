"""
Global variable containing the state of flockr
"""
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

users = {

}

logged_in = {

}

channels = {
}

data = {
}

# Clears the data variable.
# Removes all users, channels, etc.
def clear_data():
    """
    Restarts the global variable to it's default state (empty)
    """
    global data
    data = {
        'users' : [],
        'logged_in' : [],
        'channels' : [],
        'message_num': '',
        'jwt_secret' : 'Mango2Team'
    }
    
def get_user_with(attributes):
    usr = None
    for user in data["users"]:
        for attr,val in attributes.items():
            if user[attr] != val:
                break
        else:
            usr = user   
    return usr
    
def update_user(user,attributes):
      pass
      
