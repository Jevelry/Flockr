data = {
    'users' = [
        {
            'channel_list' = []
            'first' = ''
            'last' = ''
            'u_id' = ''
            'password' = ''
        }
    ]
    'logged_in' = [
        {
            'token' = ''
            'u_id' = ''
        }
    ]
    'channels' = [
        {
            'name' = ''
            'state' = '' # public or private
            'channel_id' = ''
            'owners' = [] # list of u_id's
            'members' = [] # list of u_id's
            'messages' = [
                {
                    'message' = ''
                    'u_id' = ''
                    'date' = ''
                }
            ]
        }
    ]
}


# Clears data
def clear():