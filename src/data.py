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
    global data
    data = {
        'users' : [],
        'logged_in' : [],
        'channels' : []
    }


if __name__ == '__main__':
    data['users'].append("yobbo")
    print(len(data['users']))
    clear_data()
    print(len(data['users']))

