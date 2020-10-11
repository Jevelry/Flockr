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
    'logged_in' : [
        # {
        #     'token' : '',
        #     'u_id' : ''
        # }
    ],
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
        #             'u_id' : '',
        #             'date' : ''
        #         }
        #     ]
        # }
    ]
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
        'channels' : []
    }
