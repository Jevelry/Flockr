"""
data(data.py): Gives access to global variable
"""
import data

def clear():
    """
    Clears global data variable
    """
    # Keeping everything related to the
    # global variable in the same file.
    data.clear_data()

def users_all(token):
    """
    Returns a dictionary containing a list of all users in the server.
    """
    result = {
        'users': []
    }

    for user in data.data['users']:
        user_info = {
            'u_id': user['u_id'],
            'email': user['email'],
            'name_first': user['first'],
            'name_last': user['last'],
            'handle_str': user['handle'],
            'ownner': user['owner'],
        }
        result['users'].append(user_info)

    return result

def admin_userpermission_change(token, u_id, permission_id):
    """
    Replace this with your own docstring.
    I just want to pass pylint
    """
    auth_u_id = None
    valid_permission_id = {1, 2}
    # Finds u_id associated with user token
    # Returns AccessError if token does not exist
    for user in data.data['logged_in']:            
        if user['token'] == token:
            auth_u_id = user['u_id']
        
    if auth_u_id == None:
        raise AccessError

    for auth_user in data.data['users']:
        if auth_u_id == auth_user['u_id']:
            if auth_user['owner'] == 1:
                pass
            else:
                raise AccessError
    
    for user in data.data['users']:
        if user['u_id'] == u_id and permission_id in valid_permission_id:
            user['owner'] = permission_id
        else:
            raise InputError

    return {}

def search(token, query_str):
    """
    Replace this with your own docstring.
    I just want to pass pylint
    """
    search_result = {
        'messages': [],
    }
    u_id = None

    # Finds u_id associated with user token
    # Returns AccessError if token does not exist
    for user in data.data['logged_in']:            
        if user['token'] == token:
            u_id = user['u_id']
        
    if u_id == None:
        raise AccessError('Token does not exist!')

    for user in data.data['channels']:
        if member_id['u_id'] == u_id:
            for 

    for channel in data.data['channels']:
        for member_id in channel['members']:
            if member_id == u_id:
                for message in channel['messages']:
                    if query_str in search_message['message']:
                        message_result = {
                            'message_id': search_message['message_id'],
                            'u_id': search_message['u_id'],
                            'message': search_message['message'],
                            'time_created': search_message['date']
                            'token': token,
                            'query_str': query_str,
                        }
                        search_result['messages'].append(message_result)
                        
    return search_result
