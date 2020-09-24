data = {
    'users' : [
        # {
        #     'channel_list' : [],
        #     'first' : '',
        #     'last' : '',
        #     'email': '',
        #     'u_id' : '',
        #     'password' : ''
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

def clear_data():
    global data
    print("before data",len(data['users']))
    data = {
        'users' : [],
        'logged_in' : [],
        'channels' : []
    }
    print("after data",len(data['users']))

if __name__ == '__main__':
    data['users'].append("yobbo")
    print(len(data['users']))
    clear_data()
    print(len(data['users']))
# Clears data
