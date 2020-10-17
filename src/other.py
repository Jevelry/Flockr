"""
data(data.py): Gives access to global variable
"""
import data
import validation

def clear():
    """
    Clears global data variable
    """
    # Keeping everything related to the
    # global variable in the same file.
    data.clear_data()

def users_all(token):
    """
    Returns a dictionary containing a list of all users in Flockr

    Parameters:
        token(string): A user authorisation hash

    Returns:
        users: A dictionary containing a list of all users in Flockr with their user details
    """
    users = {
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
        users['users'].append(user_info)

    return users

def admin_userpermission_change(token, u_id, permission_id):
    """
    Sets a user's permissions described by permission_id

    Parameters:
        token(string): A user authorisation hash
        u_id(int): Indentifier for User
        permission_id(int): A value describing a user's permissions 

    Returns:
        None
    """

    valid_permission_id = {1, 2}

    # Checks if user's token exists
    # Returns AccessError if token does not exist
    validation.check_valid_token(token)

    # Finds authorised user's u_id associated with user token
    auth_u_id = get_uid(token)

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
    Returns a dictionary containing a list of all users in Flockr

    Parameters:
        token(string): A user authorisation hash

    Returns:
        messages: A dictionary containing a list of all messages that the user has sent 
                  with the corresponding query string
    """
    messages = {
        'messages': [],
    }

    # Checks if user's token exists
    # Returns AccessError if token does not exist
    validation.check_valid_token(token)

    # Finds u_id associated with user token
    u_id = get_uid(token)

    for channel in data.data['channels']:
        if u_id in channel['members']:
            for message in channel['messages']:
                if query_str in message['message']:
                    message_result = {
                        'message_id': message['message_id'],
                        'u_id': message['u_id'],
                        'message': message['message'],
                        'time_created': message['date'],
                        'token': token,
                        'query_str': query_str,
                    }
                    messages['messages'].append(message_result)
                        
    return messages
