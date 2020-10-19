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
        #     'owner' : ''
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
    'jwt_secret' : 'Mango2Team'
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
